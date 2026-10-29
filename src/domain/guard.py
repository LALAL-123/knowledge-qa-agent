"""结束护栏：核对引用与答案是否被原文支持。

- 引用必须对应本轮 read_snippet 读到的片段，quote 必须逐字出现在原文中；否则删除该引用。
- answer 中的数字必须出现在有效引用原文（或其文档 ID、版本日期）中；否则撤回答案。
- 标为 answered 却没有有效引用、或检索全部失败却给出答案，状态会被校正。
冲突是否存在由模型判断（护栏不预知哪些文档冲突），由验收用例检查。
"""
from __future__ import annotations

import re

from ..core.agent import ToolRecord

NUM = re.compile(r"\d+(?:\.\d+)?")


def _squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def read_snippets(records: list[ToolRecord]) -> dict[tuple[str, str], dict]:
    return {(r.result["doc_id"], r.result["snippet_id"]): r.result
            for r in records if r.tool == "read_snippet" and r.ok}


def guard(args: dict, records: list[ToolRecord], payload: dict) -> tuple[dict, list[str]]:
    if not isinstance(args.get("citations"), list):
        raise ValueError("finish.citations 必须是数组")
    fixes: list[str] = []
    read = read_snippets(records)
    valid = []
    for c in args["citations"]:
        if not isinstance(c, dict):
            continue
        src = read.get((c.get("doc_id"), c.get("snippet_id")))
        quote = (c.get("quote") or "").strip()
        if src is None:
            fixes.append(f"引用 {c.get('doc_id')}/{c.get('snippet_id')} 未经 read_snippet 读取，已删除")
        elif not quote or _squash(quote) not in _squash(src["text"]):  # 忽略空白差异（“30 天”与“30天”）
            fixes.append(f"引用 {c.get('snippet_id')} 的 quote 不是原文，已删除")
        else:
            valid.append({"doc_id": src["doc_id"], "snippet_id": src["snippet_id"], "quote": quote,
                          "title": src["title"], "version_date": src["version_date"], "scope": src["scope"]})

    status = args.get("task_status")
    answer = str(args.get("answer") or "")
    searches = [r for r in records if r.tool == "search_docs"]
    allowed = set()
    for v in valid:
        allowed |= set(NUM.findall(v["quote"])) | set(NUM.findall(v["version_date"])) | set(NUM.findall(v["snippet_id"]))
    unsupported = sorted(set(NUM.findall(answer)) - allowed)

    if searches and not any(r.ok for r in searches) and status != "failed":
        fixes.append("检索全部失败，状态校正为 failed")
        status = "failed"
    if status == "answered" and not valid:
        fixes.append("answered 但没有有效引用，校正为 insufficient_evidence")
        status = "insufficient_evidence"
    if unsupported and status in ("answered", "conflict_needs_confirmation"):
        fixes.append(f"答案中的数字 {unsupported} 在引用原文中找不到，撤回答案")
        answer = f"（原答案含无法在引用中核实的数字 {unsupported}，已撤回）"
        status = "insufficient_evidence"
    if status in ("failed", "out_of_scope") and unsupported:
        fixes.append(f"{status} 时答案不应包含无出处的数字 {unsupported}，已改写")
        answer = "无法依据现有资料回答。" if status == "out_of_scope" else "工具失败，暂时无法回答。"
    question = str(args.get("clarifying_question") or "")
    if status in ("conflict_needs_confirmation", "needs_clarification") and not question:
        question = "请说明您适用的制度或补充问题背景。"

    final = {
        "answer": answer,
        "citations": valid,
        "conflicts": args.get("conflicts") or [],
        "gaps": list(args.get("gaps") or []),
        "clarifying_question": question,
        "task_status": status,
        "evidence_check": {"cited_snippets": len(valid), "unsupported_numbers": unsupported,
                           "snippets_read": len(read), "searches": len(searches)},
    }
    if status == "insufficient_evidence" and not final["gaps"]:
        final["gaps"].append("现有引用不足以支撑答案")
    return final, fixes


def on_incomplete(records: list[ToolRecord], payload: dict, reason: str) -> dict:
    read = read_snippets(records)
    return {"answer": "", "citations": [], "snippets_read": [f"{d}/{s}" for d, s in read],
            "gaps": [f"未完成：{reason}，未形成可靠答案"], "clarifying_question": ""}

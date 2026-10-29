"""离线 Mock 策略：确定性规则，读取工具结果后选择下一步。

只用于无模型时验证循环、工具、护栏与 Trace。其中的同义词表、冲突判断（比较不同文档里的“N 天”）
都是为合成数据写的简化规则，不代表真实模型的理解与查证能力。
"""
from __future__ import annotations

import re

from ..core.llm import Observation
from .tools import grams

SYNONYMS = {"歇": "年假", "休息": "年假", "放假": "年假", "多久": "天数", "报账": "报销", "住酒店": "住宿", "电量": "续航"}
FOLLOW_UP = re.compile(r"^(那|那么)|呢[？?]?$")
DAYS = re.compile(r"(\d+)\s*天")


def _ok(o):
    return o is not None and o.result.get("ok")


def _finish(note, status, answer, citations=(), conflicts=(), gaps=(), question=""):
    return "finish", note, {"answer": answer, "citations": list(citations), "conflicts": list(conflicts),
                            "gaps": list(gaps), "clarifying_question": question, "task_status": status}


def mock_policy(payload: dict, obs: list[Observation]):
    q = payload["question"]
    history = payload.get("history") or []
    follow = bool(FOLLOW_UP.search(q)) and len(q) <= 12
    if follow and not history:
        return _finish("问题是追问但没有上下文，无法确定指代", "needs_clarification", "这个问题需要上下文才能回答。",
                       question="请问您指的是哪项制度或产品？")
    base = q
    if follow:
        last_user = [h["content"] for h in history if h["role"] == "user"][-1]
        base = f"{last_user} {q}"

    searches = [o for o in obs if o.tool == "search_docs"]
    if not searches:
        return "search_docs", "先按问题原文检索" + ("（已结合上一轮问题补全指代）" if follow else ""), {"query": base, "top_k": 5}
    if not _ok(searches[-1]):
        if len(searches) < 2:
            return "search_docs", f"检索失败（{searches[-1].result.get('error')}），重试一次", searches[-1].args
        if not any(_ok(s) for s in searches):
            return _finish("检索服务连续失败，不能凭记忆回答", "failed", "检索服务暂时不可用，无法查询制度原文，请稍后再试。",
                           gaps=["检索工具失败"])
    hit_search = next((s for s in reversed(searches) if _ok(s) and s.result["count"] > 0), None)
    if hit_search is None:
        rewritten = " ".join(v for k, v in SYNONYMS.items() if k in base)
        tried = {s.args.get("query") for s in searches}
        if rewritten and rewritten not in tried:
            return "search_docs", f"原问题没有命中，改写为规范用语“{rewritten}”再检索", {"query": rewritten, "top_k": 5}
        return _finish("多次检索均无相关文档", "out_of_scope", "现有制度与产品资料中没有涉及这个问题的内容，无法回答。",
                       gaps=[f"知识库中没有关于“{q}”的文档"], question="如需了解，请联系对应部门或补充相关制度文件。")

    hits = hit_search.result["hits"][:3]
    reads = {}
    for h in hits:
        key = (h["doc_id"], h["snippet_id"])
        tries = [o for o in obs if o.tool == "read_snippet" and (o.args.get("doc_id"), o.args.get("snippet_id")) == key]
        good = next((o for o in tries if _ok(o)), None)
        if good:
            reads[key] = good.result
        elif len(tries) < 2:
            note = f"读取 {h['snippet_id']} 原文以核对" if not tries else f"读取失败（{tries[-1].result.get('error')}），重试一次"
            return "read_snippet", note, {"doc_id": h["doc_id"], "snippet_id": h["snippet_id"]}
    if not reads:
        return _finish("原文读取全部失败，不能只凭预览回答", "failed", "无法读取文档原文，暂时不能回答。", gaps=["片段读取失败"])

    by_doc = {}
    for r in reads.values():
        days = set(DAYS.findall(r["text"]))
        if days:
            by_doc.setdefault(r["doc_id"], (r, days))
    if len(by_doc) >= 2 and len({frozenset(d) for _, d in by_doc.values()}) > 1:
        parts = [f"{r['doc_id']}《{r['title']}》（{r['version_date']} 版，适用范围：{r['scope']}）：{r['text']}" for r, _ in by_doc.values()]
        cites = [{"doc_id": r["doc_id"], "snippet_id": r["snippet_id"], "quote": r["text"]} for r, _ in by_doc.values()]
        return _finish("不同文档给出不同天数，且未说明适用范围与优先级", "conflict_needs_confirmation",
                       "资料存在冲突：" + "；".join(parts) + "。文件均未说明适用范围和优先级，不能确定以哪份为准。",
                       cites, [{"doc_ids": list(by_doc), "description": "同一事项规定的天数不同"}],
                       question="请确认您适用哪份制度，或向制度归口部门确认现行口径。")

    want = grams(q) | grams(base) | grams(" ".join(s.args.get("query", "") for s in searches))
    best = max(reads.values(), key=lambda r: len(want & grams(r["text"])))
    return _finish(f"{best['snippet_id']} 原文直接回答了问题，且读取的片段之间无冲突", "answered",
                   f"依据《{best['title']}》（{best['doc_id']}，{best['version_date']} 版）：{best['text']}",
                   [{"doc_id": best["doc_id"], "snippet_id": best["snippet_id"], "quote": best["text"]}])

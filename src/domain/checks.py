"""验收检查：只看最终答案、引用和工具调用事实，不绑定执行路径；Mock 与真实模型共用。"""
from __future__ import annotations

import re

from .tools import load_docs


def _cited(res) -> set[str]:
    return {c["snippet_id"] for c in res.final.get("citations", [])}


def _quotes_verbatim(res, env=None):
    """每条引用的 quote 都逐字出现在对应文档原文中（以本用例的文档版本为准）。"""
    docs = load_docs(env or {})
    text = {s["snippet_id"]: s["text"] for d in docs.values() for s in d["snippets"]}
    squash = lambda t: re.sub(r"\s+", "", t)  # 与护栏口径一致：忽略空白差异
    bad = [c["snippet_id"] for c in res.final.get("citations", [])
           if squash(c["quote"]) not in squash(text.get(c["snippet_id"], ""))]
    return ("引用均为原文", not bad, str(bad))


def _called(res, tool):
    return [r for r in res.records if r.tool == tool]


def c01(results, store):
    r = results[0]
    return [
        ("状态 answered", r.status == "answered", r.status),
        ("引用 D03-S1", "D03-S1" in _cited(r), str(_cited(r))),
        ("答案包含 5 天", "5" in r.final["answer"], r.final["answer"]),
        ("读取过原文", bool(_called(r, "read_snippet")), ""),
        _quotes_verbatim(r),
    ]


def c02(results, store):
    r = results[0]
    ans = r.final["answer"]
    docs_in_conflict = {d for c in r.final.get("conflicts", []) for d in c.get("doc_ids", [])}
    return [
        ("状态 conflict_needs_confirmation", r.status == "conflict_needs_confirmation", r.status),
        ("同时引用 D01-S1 与 D02-S1", {"D01-S1", "D02-S1"} <= _cited(r), str(_cited(r))),
        ("冲突列出 D01 与 D02", {"D01", "D02"} <= docs_in_conflict, str(docs_in_conflict)),
        ("答案同时给出 30 与 15，不擅自选一个", "30" in ans and "15" in ans, ans),
        ("提出确认问题", bool(r.final["clarifying_question"]), r.final["clarifying_question"]),
        _quotes_verbatim(r),
    ]


def c03(results, store):
    r = results[0]
    return [
        ("状态 answered（冲突消失）", r.status == "answered", r.status),
        ("依据 D01-S1 回答 30 天", "D01-S1" in _cited(r) and "30" in r.final["answer"], r.final["answer"]),
        ("不再出现 15 天", "15" not in r.final["answer"], ""),
        _quotes_verbatim(r, {"doc_overrides": {"D02": None}}),
    ]


def c04(results, store):
    r = results[0]
    return [
        ("状态 out_of_scope", r.status == "out_of_scope", r.status),
        ("没有引用", not r.final["citations"], str(_cited(r))),
        ("写明资料缺口", bool(r.final["gaps"]), str(r.final["gaps"])),
        ("尝试过检索", bool(_called(r, "search_docs")), ""),
    ]


def c05(results, store):
    r = results[0]
    return [
        ("状态 answered", r.status == "answered", r.status),
        ("与 c01 相同依据 D03-S1", "D03-S1" in _cited(r), str(_cited(r))),
        # 第 2 轮起的口径：模型改写了查询即可（先改写再检索、或首检落空后再改写都算）。
        # 第 1 轮按旧口径“必须检索两次”判定，GLM-4-Flash 首次就改写为“入职三年年假天数”并命中，记为未通过。
        ("做了查询改写（检索词不是原问题）", any(x.arguments.get("query") != "入职三年了，每年能歇多久？"
                                       for x in _called(r, "search_docs")), str([x.arguments.get("query") for x in _called(r, "search_docs")])),
        _quotes_verbatim(r),
    ]


def c06(results, store):
    r = results[0]
    return [
        ("状态 answered", r.status == "answered", r.status),
        ("引用 D05-S2（二线城市）", "D05-S2" in _cited(r), str(_cited(r))),
        ("答案为 350 元", "350" in r.final["answer"], r.final["answer"]),
        ("检索时补全了“住宿”指代", any("住宿" in x.arguments.get("query", "") for x in _called(r, "search_docs")), ""),
        _quotes_verbatim(r),
    ]


def c07(results, store):
    r = results[0]
    return [
        ("状态 needs_clarification", r.status == "needs_clarification", r.status),
        ("提出澄清问题", bool(r.final["clarifying_question"]), r.final["clarifying_question"]),
        ("没有给出带数字的答案", not any(ch.isdigit() for ch in r.final["answer"]), r.final["answer"]),
    ]


def c08(results, store):
    r = results[0]
    return [
        ("状态 failed", r.status == "failed", r.status),
        ("没有引用、没有数字答案", not r.final["citations"] and not any(ch.isdigit() for ch in r.final["answer"]), r.final["answer"]),
        ("写明失败原因", bool(r.final["gaps"]) or "不可用" in r.final["answer"], ""),
    ]


def c09(results, store):
    r = results[0]
    reads = _called(r, "read_snippet")
    return [
        ("读取失败后有重试", any(not x.ok for x in reads) and any(x.ok for x in reads), ""),
        ("状态 answered，引用 D04-S3", r.status == "answered" and "D04-S3" in _cited(r), str(_cited(r))),
        ("答案为 10 米", "10" in r.final["answer"], r.final["answer"]),
        _quotes_verbatim(r),
    ]


def c10(results, store):
    r = results[0]
    return [
        ("返回明确未完成状态", r.status == "incomplete" and r.final.get("stop_reason") == "step_limit_reached", r.status),
        ("决策轮数不超过上限", r.steps <= 2, str(r.steps)),
        ("未给出答案", not r.final.get("answer"), ""),
    ]


def c11(results, store):
    r = results[0]
    env = {"doc_overrides": {"D03": {"snippets": {"D03-S1": "员工带薪年休假（以下简称年假）：入职满 1 年后每年享有年假 7 天。"}}}}
    return [
        ("答案随原文改为 7 天", r.status == "answered" and "7" in r.final["answer"], r.final["answer"]),
        ("不再出现旧口径 5 天", "5 天" not in r.final["answer"], ""),
        _quotes_verbatim(r, env),
    ]


CHECKS = {
    "c01_clear_answer": c01, "c02_conflict": c02, "c03_conflict_doc_removed": c03, "c04_out_of_scope": c04,
    "c05_paraphrase": c05, "c06_followup_context": c06, "c07_followup_no_context": c07,
    "c08_tool_failure": c08, "c09_tool_failure_once": c09, "c10_step_limit": c10, "c11_doc_content_changed": c11,
}

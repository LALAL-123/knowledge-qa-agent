"""题 3 业务工具与护栏测试。"""
from pathlib import Path

import pytest

from src import domain
from src.core.agent import ToolRecord
from src.core.llm import ScriptedLLM
from src.core.runner import check_case, load_case, run_case
from src.domain.tools import build_tools

CASES = sorted((Path(__file__).resolve().parent.parent / "examples" / "cases").glob("*.json"))


def tools(tmp_path, env=None):
    return {t.name: t.fn for t in build_tools(request={}, env=env or {}, store_dir=tmp_path)}


def test_search_returns_preview_only_and_both_conflicting_docs(tmp_path):
    r = tools(tmp_path)["search_docs"]("报销期限多久？")
    ids = [h["snippet_id"] for h in r["hits"]]
    assert ids[0] == "D01-S1" and "D02-S1" in ids
    assert all(h["preview"].endswith("…") for h in r["hits"])


def test_colloquial_question_misses_until_rewritten(tmp_path):
    s = tools(tmp_path)["search_docs"]
    assert s("入职三年了，每年能歇多久？")["count"] == 0
    assert s("年假 天数")["hits"][0]["doc_id"] == "D03"


def test_out_of_scope_has_no_hits(tmp_path):
    assert tools(tmp_path)["search_docs"]("公司股票期权怎么行权？")["count"] == 0


def test_doc_overrides_remove_and_replace(tmp_path):
    t = tools(tmp_path, {"doc_overrides": {"D02": None, "D03": {"snippets": {"D03-S1": "年假 7 天"}}}})
    assert all(h["doc_id"] != "D02" for h in t["search_docs"]("报销期限")["hits"])
    assert t["read_snippet"]("D03", "D03-S1")["text"] == "年假 7 天"
    assert t["read_snippet"]("D02", "D02-S1")["ok"] is False


def read(doc, sid, text, date="2025-03-01"):
    return ToolRecord(1, "read_snippet", {}, {"ok": True, "doc_id": doc, "snippet_id": sid, "text": text,
                                              "title": "t", "version_date": date, "scope": "未注明"})


D01 = read("D01", "D01-S1", "报销期限：员工应在费用发生后 30 天内提交报销申请，逾期不予受理。")


def test_guard_drops_unread_or_paraphrased_citations():
    args = {"answer": "30 天", "task_status": "answered", "citations": [
        {"doc_id": "D02", "snippet_id": "D02-S1", "quote": "15 天内"},
        {"doc_id": "D01", "snippet_id": "D01-S1", "quote": "30 天内提交即可"}]}
    final, fixes = domain.guard(args, [D01], {})
    assert final["citations"] == [] and final["task_status"] == "insufficient_evidence" and len(fixes) >= 2


def test_guard_withdraws_answer_with_unsupported_number():
    args = {"answer": "报销期限是 15 天", "task_status": "answered",
            "citations": [{"doc_id": "D01", "snippet_id": "D01-S1", "quote": "费用发生后 30 天内提交报销申请"}]}
    final, fixes = domain.guard(args, [D01], {})
    assert final["task_status"] == "insufficient_evidence" and final["answer"].startswith("（原答案")
    assert final["evidence_check"]["unsupported_numbers"] == ["15"]


def test_guard_accepts_supported_answer():
    args = {"answer": "依据 D01（2025-03-01 版）：30 天内提交", "task_status": "answered",
            "citations": [{"doc_id": "D01", "snippet_id": "D01-S1", "quote": "30 天内提交报销申请"}]}
    final, fixes = domain.guard(args, [D01], {})
    assert final["task_status"] == "answered" and not fixes


def test_guard_marks_failed_when_all_searches_failed():
    rec = ToolRecord(1, "search_docs", {}, {"ok": False, "error": "timeout"})
    final, _ = domain.guard({"answer": "年假 5 天", "task_status": "answered", "citations": []}, [rec], {})
    assert final["task_status"] == "failed" and "5" not in final["answer"]


@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_case_acceptance_with_offline_mock(path, tmp_path):
    case = load_case(path)
    outputs = run_case(case, domain, ScriptedLLM(domain.mock_policy), tmp_path)
    checks = check_case(case, domain, [r for _, r in outputs], tmp_path)
    assert checks and all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]

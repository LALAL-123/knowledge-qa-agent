"""业务工具（本地函数 + 合成文档）：文档检索、片段读取。

检索用字符二元组（bigram）重合度打分，结果只给预览；要引用原文必须用 read_snippet 读取。
这是一个刻意简单的检索器：换一种说法（同义改写）可能检索不到，需要模型自己改写查询再检索。
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from ..core.tools import Tool

DATA = Path(__file__).resolve().parents[2] / "data"
STOP = {"多少", "什么", "怎么", "如何", "可以", "是否", "公司", "员工", "请问", "一下", "我们", "有没"}


def load_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def grams(text: str) -> set[str]:
    t = re.sub(r"[^0-9a-zA-Z一-鿿]", "", text.lower())
    return {t[i:i + 2] for i in range(len(t) - 1)} - STOP


def load_docs(env: dict) -> dict:
    docs = {d["doc_id"]: d for d in copy.deepcopy(load_json("docs.json"))}
    for doc_id, patch in env.get("doc_overrides", {}).items():
        if patch is None:
            docs.pop(doc_id, None)  # 删除整份文档
        elif doc_id in docs:
            snippets = {s["snippet_id"]: s for s in docs[doc_id]["snippets"]}
            for sid, text in patch.pop("snippets", {}).items():
                snippets[sid] = {"snippet_id": sid, "text": text}
            docs[doc_id].update(patch)
            docs[doc_id]["snippets"] = list(snippets.values())
        else:
            docs[doc_id] = patch
    return docs


def build_tools(request: dict, env: dict, store_dir: Path) -> list[Tool]:
    docs = load_docs(env)

    def search_docs(query: str, top_k: int = 5):
        q = grams(query)
        scored = []
        for d in docs.values():
            for s in d["snippets"]:
                score = len(q & (grams(s["text"]) | grams(d["title"])))
                if score:
                    scored.append((score, d, s))
        scored.sort(key=lambda x: -x[0])
        hits = [{"doc_id": d["doc_id"], "snippet_id": s["snippet_id"], "title": d["title"],
                 "version_date": d["version_date"], "score": score, "preview": s["text"][:16] + "…"}
                for score, d, s in scored[: max(1, min(int(top_k), 5))]]
        return {"query": query, "count": len(hits), "hits": hits,
                "note": "预览不可作为引用依据，请用 read_snippet 读取原文" if hits else "没有匹配的文档片段"}

    def read_snippet(doc_id: str, snippet_id: str):
        d = docs.get(doc_id)
        s = next((x for x in (d or {}).get("snippets", []) if x["snippet_id"] == snippet_id), None)
        if s is None:
            return {"ok": False, "error_type": "not_found", "error": f"{doc_id}/{snippet_id} 不存在"}
        return {"doc_id": doc_id, "snippet_id": snippet_id, "title": d["title"], "version_date": d["version_date"],
                "scope": d.get("scope", "未注明"), "text": s["text"]}

    obj = {"type": "object"}
    return [
        Tool("search_docs", "在企业制度与产品 FAQ 中检索，返回文档 ID、片段 ID、版本日期和预览。没有结果时可改写查询再试。",
             {**obj, "properties": {"query": {"type": "string"}, "top_k": {"type": "integer", "description": "1–5，默认 5"}},
              "required": ["query"]}, search_docs),
        Tool("read_snippet", "读取片段原文、版本日期与适用范围。引用必须来自这里返回的原文。",
             {**obj, "properties": {"doc_id": {"type": "string"}, "snippet_id": {"type": "string"}},
              "required": ["doc_id", "snippet_id"]}, read_snippet),
    ]

# c06_followup_context：上下文追问：上一轮问住宿标准，本轮“那二线城市呢？”（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`answered`（model_finished）
- 决策轮数：5；业务工具调用：4

## 输入

```json
{
  "question": "那二线城市呢？",
  "history": [
    {
      "role": "user",
      "content": "出差住宿标准是多少？"
    },
    {
      "role": "assistant",
      "content": "一线城市（北京、上海、广州、深圳）住宿每晚不超过 500 元（D05-S1）。"
    }
  ]
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "出差住宿标准是多少？ 那二线城市呢？", "top_k": 5} | {"query": "出差住宿标准是多少？ 那二线城市呢？", "count": 3, "hits": [{"doc_id": "D05", "snippet_id": "D05-S2", "title": "差旅住宿标准", "version_date": "2026-02-01", "score": 6, "preview": "二线城市住宿每晚不超过 350 …"}, {"doc_id": "D05", "snippet_id": "D05-S1", "title": "差旅住宿标准", "version_date": "2026-02-01", "score": 5, "preview": "一线城市（北京、上海、广州、深圳…"}, {"doc_id": "D02", "snippet_id": "D0… | 先按问题原文检索（已结合上一轮问题补全指代） |
| 2 | `read_snippet` | {"doc_id": "D05", "snippet_id": "D05-S2"} | {"doc_id": "D05", "snippet_id": "D05-S2", "title": "差旅住宿标准", "version_date": "2026-02-01", "scope": "国内出差", "text": "二线城市住宿每晚不超过 350 元；其他城市不超过 250 元。", "ok": true} | 读取 D05-S2 原文以核对 |
| 3 | `read_snippet` | {"doc_id": "D05", "snippet_id": "D05-S1"} | {"doc_id": "D05", "snippet_id": "D05-S1", "title": "差旅住宿标准", "version_date": "2026-02-01", "scope": "国内出差", "text": "一线城市（北京、上海、广州、深圳）住宿每晚不超过 500 元。", "ok": true} | 读取 D05-S1 原文以核对 |
| 4 | `read_snippet` | {"doc_id": "D02", "snippet_id": "D02-S2"} | {"doc_id": "D02", "snippet_id": "D02-S2", "title": "差旅与报销补充说明", "version_date": "2026-01-15", "scope": "未注明", "text": "出差期间的市内交通费按实际发生额凭票报销。", "ok": true} | 读取 D02-S2 原文以核对 |
| 5 | `finish` | status=answered | 护栏校正 0 处 | D05-S2 原文直接回答了问题，且读取的片段之间无冲突 |

## 最终输出

```json
{
  "answer": "依据《差旅住宿标准》（D05，2026-02-01 版）：二线城市住宿每晚不超过 350 元；其他城市不超过 250 元。",
  "citations": [
    {
      "doc_id": "D05",
      "snippet_id": "D05-S2",
      "quote": "二线城市住宿每晚不超过 350 元；其他城市不超过 250 元。",
      "title": "差旅住宿标准",
      "version_date": "2026-02-01",
      "scope": "国内出差"
    }
  ],
  "conflicts": [],
  "gaps": [],
  "clarifying_question": "",
  "task_status": "answered",
  "evidence_check": {
    "cited_snippets": 1,
    "unsupported_numbers": [],
    "snippets_read": 3,
    "searches": 1
  }
}
```

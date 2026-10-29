# c06_followup_context：上下文追问：上一轮问住宿标准，本轮“那二线城市呢？”（运行 1/1）

- 模型：`openai-compat:glm-4-flash`
- 结束状态：`answered`（model_finished）
- 决策轮数：5；业务工具调用：3

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
| 1 | `search_docs` | {"query": "二线城市 出差住宿标准"} | {"query": "二线城市 出差住宿标准", "count": 3, "hits": [{"doc_id": "D05", "snippet_id": "D05-S2", "title": "差旅住宿标准", "version_date": "2026-02-01", "score": 6, "preview": "二线城市住宿每晚不超过 350 …"}, {"doc_id": "D05", "snippet_id": "D05-S1", "title": "差旅住宿标准", "version_date": "2026-02-01", "score": 5, "preview": "一线城市（北京、上海、广州、深圳…"}, {"doc_id": "D02", "snippet_id": "D02-S2", … | 查找二线城市出差住宿标准 |
| 2 | `read_snippet` ✗ | {"doc_id": "D05", "snippet_id": "D05-S2", "version_date": "2026-02-01"} | {"ok": false, "error_type": "invalid_arguments", "error": "build_tools.<locals>.read_snippet() got an unexpected keyword argument 'version_date'"} | 读取二线城市出差住宿标准原文 |
| 3 | `read_snippet` | {"doc_id": "D05", "snippet_id": "D05-S2"} | {"doc_id": "D05", "snippet_id": "D05-S2", "title": "差旅住宿标准", "version_date": "2026-02-01", "scope": "国内出差", "text": "二线城市住宿每晚不超过 350 元；其他城市不超过 250 元。", "ok": true} | 读取二线城市出差住宿标准原文 |
| 4 | no_tool_call | — | 二线城市的出差住宿标准是每晚不超过350元。 | — |
| 5 | `finish` | status=answered | 护栏校正 0 处 | 根据差旅住宿标准文档，二线城市住宿每晚不超过350元。 |

## 最终输出

```json
{
  "answer": "二线城市的出差住宿标准是每晚不超过350元。",
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
    "snippets_read": 1,
    "searches": 1
  }
}
```

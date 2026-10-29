# c04_out_of_scope：资料外问题：知识库中没有股票期权制度（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`out_of_scope`（model_finished）
- 决策轮数：2；业务工具调用：1

## 输入

```json
{
  "question": "公司股票期权怎么行权？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "公司股票期权怎么行权？", "top_k": 5} | {"query": "公司股票期权怎么行权？", "count": 0, "hits": [], "note": "没有匹配的文档片段", "ok": true} | 先按问题原文检索 |
| 2 | `finish` | status=out_of_scope | 护栏校正 0 处 | 多次检索均无相关文档 |

## 最终输出

```json
{
  "answer": "现有制度与产品资料中没有涉及这个问题的内容，无法回答。",
  "citations": [],
  "conflicts": [],
  "gaps": [
    "知识库中没有关于“公司股票期权怎么行权？”的文档"
  ],
  "clarifying_question": "如需了解，请联系对应部门或补充相关制度文件。",
  "task_status": "out_of_scope",
  "evidence_check": {
    "cited_snippets": 0,
    "unsupported_numbers": [],
    "snippets_read": 0,
    "searches": 1
  }
}
```

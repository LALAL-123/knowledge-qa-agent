# c07_followup_no_context：无上下文的追问：无法确定指代，应追问用户（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`needs_clarification`（model_finished）
- 决策轮数：1；业务工具调用：0

## 输入

```json
{
  "question": "那二线城市呢？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `finish` | status=needs_clarification | 护栏校正 0 处 | 问题是追问但没有上下文，无法确定指代 |

## 最终输出

```json
{
  "answer": "这个问题需要上下文才能回答。",
  "citations": [],
  "conflicts": [],
  "gaps": [],
  "clarifying_question": "请问您指的是哪项制度或产品？",
  "task_status": "needs_clarification",
  "evidence_check": {
    "cited_snippets": 0,
    "unsupported_numbers": [],
    "snippets_read": 0,
    "searches": 0
  }
}
```

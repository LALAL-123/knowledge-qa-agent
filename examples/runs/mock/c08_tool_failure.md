# c08_tool_failure：工具失败：检索服务持续不可用，不得凭记忆回答（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`failed`（model_finished）
- 决策轮数：3；业务工具调用：2

## 输入

```json
{
  "question": "年假有几天？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` ✗ | {"query": "年假有几天？", "top_k": 5} | {"ok": false, "error_type": "tool_failure", "error": "检索服务超时（注入故障）"} | 先按问题原文检索 |
| 2 | `search_docs` ✗ | {"query": "年假有几天？", "top_k": 5} | {"ok": false, "error_type": "tool_failure", "error": "检索服务超时（注入故障）"} | 检索失败（检索服务超时（注入故障）），重试一次 |
| 3 | `finish` | status=failed | 护栏校正 0 处 | 检索服务连续失败，不能凭记忆回答 |

## 最终输出

```json
{
  "answer": "检索服务暂时不可用，无法查询制度原文，请稍后再试。",
  "citations": [],
  "conflicts": [],
  "gaps": [
    "检索工具失败"
  ],
  "clarifying_question": "",
  "task_status": "failed",
  "evidence_check": {
    "cited_snippets": 0,
    "unsupported_numbers": [],
    "snippets_read": 0,
    "searches": 2
  }
}
```

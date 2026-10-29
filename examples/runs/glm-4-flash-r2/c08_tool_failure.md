# c08_tool_failure：工具失败：检索服务持续不可用，不得凭记忆回答（运行 1/1）

- 模型：`openai-compat:glm-4-flash`
- 结束状态：`failed`（model_finished）
- 决策轮数：4；业务工具调用：2

## 输入

```json
{
  "question": "年假有几天？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` ✗ | {"query": "年假天数"} | {"ok": false, "error_type": "tool_failure", "error": "检索服务超时（注入故障）"} | 查找关于年假天数的制度或产品信息 |
| 2 | `search_docs` ✗ | {"query": "年假天数"} | {"ok": false, "error_type": "tool_failure", "error": "检索服务超时（注入故障）"} | 尝试重新检索关于年假天数的制度或产品信息 |
| 3 | no_tool_call | — | 很抱歉，目前无法检索到关于年假天数的具体信息。请您稍后再试或联系相关部门获取相关信息。 | — |
| 4 | `finish` | status=failed | 护栏校正 0 处 | 无法检索到关于年假天数的具体信息 |

## 最终输出

```json
{
  "answer": "很抱歉，目前无法检索到关于年假天数的具体信息。请您稍后再试或联系相关部门获取相关信息。",
  "citations": [],
  "conflicts": [],
  "gaps": [],
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

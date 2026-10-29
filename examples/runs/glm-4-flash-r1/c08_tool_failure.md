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
| 1 | `search_docs` ✗ | {"query": "年假天数"} | {"ok": false, "error_type": "tool_failure", "error": "检索服务超时（注入故障）"} | 根据问题，搜索关于年假天数的公司制度规定。 |
| 2 | `search_docs` ✗ | {"query": "员工年假天数"} | {"ok": false, "error_type": "tool_failure", "error": "检索服务超时（注入故障）"} | 由于第一次检索失败，尝试使用同义词进行检索。 |
| 3 | no_tool_call | — | 很抱歉，目前无法从公司制度与产品 FAQ 中找到关于年假天数的具体信息。您可以稍后再试，或者联系人力资源部门获取相关信息。 | — |
| 4 | `finish` | status=failed | 护栏校正 1 处 | 根据检索结果，无法找到关于年假天数的具体信息。 |

## 护栏校正

- 检索全部失败，状态校正为 failed

## 最终输出

```json
{
  "answer": "很抱歉，目前无法从公司制度与产品 FAQ 中找到关于年假天数的具体信息。您可以稍后再试，或者联系人力资源部门获取相关信息。",
  "citations": [],
  "conflicts": [],
  "gaps": [
    "关于年假天数的具体信息"
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

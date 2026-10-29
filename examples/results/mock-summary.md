# 验收结果（mock:scripted-policy）

检查通过 44/44。逐条 Trace 见 `examples/runs/mock/`。

| 用例 | 覆盖验收点 | 结束状态 | 检查通过 |
|---|---|---|---|
| c01_clear_answer | 明确答案 | answered | 5/5 |
| c02_conflict | 文档冲突 | conflict_needs_confirmation | 6/6 |
| c03_conflict_doc_removed | 文档冲突、明确答案 | answered | 4/4 |
| c04_out_of_scope | 资料外问题 | out_of_scope | 4/4 |
| c05_paraphrase | 改写后的相似问题 | answered | 4/4 |
| c06_followup_context | 上下文追问 | answered | 5/5 |
| c07_followup_no_context | 上下文追问 | needs_clarification | 3/3 |
| c08_tool_failure | 工具失败 | failed | 3/3 |
| c09_tool_failure_once | 工具失败、明确答案 | answered | 4/4 |
| c10_step_limit | 步数上限 | incomplete | 3/3 |
| c11_doc_content_changed | 明确答案 | answered | 3/3 |

## 未通过的检查

无

# 验收结果（openai-compat:glm-4-flash）

检查通过 32/44。逐条 Trace 见 `examples/runs/glm-4-flash/`。

| 用例 | 覆盖验收点 | 结束状态 | 检查通过 |
|---|---|---|---|
| c01_clear_answer | 明确答案 | insufficient_evidence | 3/5 |
| c02_conflict | 文档冲突 | answered | 1/6 |
| c03_conflict_doc_removed | 文档冲突、明确答案 | insufficient_evidence | 2/4 |
| c04_out_of_scope | 资料外问题 | out_of_scope | 4/4 |
| c05_paraphrase | 改写后的相似问题 | answered | 3/4 |
| c06_followup_context | 上下文追问 | answered | 5/5 |
| c07_followup_no_context | 上下文追问 | incomplete | 1/3 |
| c08_tool_failure | 工具失败 | failed | 3/3 |
| c09_tool_failure_once | 工具失败、明确答案 | answered | 4/4 |
| c10_step_limit | 步数上限 | incomplete | 3/3 |
| c11_doc_content_changed | 明确答案 | answered | 3/3 |

## 未通过的检查

- c01_clear_answer：状态 answered（insufficient_evidence）
- c01_clear_answer：引用 D03-S1（set()）
- c02_conflict：状态 conflict_needs_confirmation（answered）
- c02_conflict：同时引用 D01-S1 与 D02-S1（{'D01-S1'}）
- c02_conflict：冲突列出 D01 与 D02（set()）
- c02_conflict：答案同时给出 30 与 15，不擅自选一个（员工应在费用发生后 30 天内提交报销申请，逾期不予受理。）
- c02_conflict：提出确认问题（）
- c03_conflict_doc_removed：状态 answered（冲突消失）（insufficient_evidence）
- c03_conflict_doc_removed：依据 D01-S1 回答 30 天（根据《费用报销管理办法》的规定，员工应在费用发生后30天内提交报销申请，逾期不予受理。）
- c05_paraphrase：首次未命中后改写查询再检索（）
- c07_followup_no_context：状态 needs_clarification（incomplete）
- c07_followup_no_context：提出澄清问题（）

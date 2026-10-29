# 验收结果（openai-compat:glm-4-flash）

检查通过 33/44。逐条 Trace 见 `examples/runs/glm-4-flash-r2/`。

| 用例 | 覆盖验收点 | 结束状态 | 检查通过 |
|---|---|---|---|
| c01_clear_answer | 明确答案 | answered | 5/5 |
| c02_conflict | 文档冲突 | answered | 1/6 |
| c03_conflict_doc_removed | 文档冲突、明确答案 | answered | 4/4 |
| c04_out_of_scope | 资料外问题 | incomplete | 3/4 |
| c05_paraphrase | 改写后的相似问题 | answered | 4/4 |
| c06_followup_context | 上下文追问 | answered | 5/5 |
| c07_followup_no_context | 上下文追问 | answered | 0/3 |
| c08_tool_failure | 工具失败 | failed | 2/3 |
| c09_tool_failure_once | 工具失败、明确答案 | answered | 4/4 |
| c10_step_limit | 步数上限 | incomplete | 3/3 |
| c11_doc_content_changed | 明确答案 | answered | 2/3 |

## 未通过的检查

- c02_conflict：状态 conflict_needs_confirmation（answered）
- c02_conflict：同时引用 D01-S1 与 D02-S1（{'D01-S1'}）
- c02_conflict：冲突列出 D01 与 D02（set()）
- c02_conflict：答案同时给出 30 与 15，不擅自选一个（员工应在费用发生后 30 天内提交报销申请，逾期不予受理。）
- c02_conflict：提出确认问题（）
- c04_out_of_scope：状态 out_of_scope（incomplete）
- c07_followup_no_context：状态 needs_clarification（answered）
- c07_followup_no_context：提出澄清问题（）
- c07_followup_no_context：没有给出带数字的答案（关于员工休假制度（年假）的详细信息如下：
- 累计工作已满 1 年不满 10 年的，年假 5 天；
- 已满 10 年不满 20 年的，年假 10 天；
- 已满 20 年的，年假 15 天。

年休假可分段使用，当年未休部分可顺延至次年 3 月 31 日前。）
- c08_tool_failure：写明失败原因（）
- c11_doc_content_changed：引用均为原文（['D03-S1']）

# 03 评估

## 测试结构

| 层次 | 文件 | 内容 |
|---|---|---|
| 内核 | `tests/test_core.py` | 步数/调用上限、finish 同轮拒绝、工具异常转观察、故障注入、模型异常、非法 finish 退回 |
| 业务 | `tests/test_domain.py` | 检索返回冲突双方、口语问题需改写、资料外无命中、文档删除/替换、护栏删除非原文引用、撤回无出处数字、检索失败校正 |
| 验收 | `tests/test_domain.py::test_case_acceptance_with_offline_mock` | 11 个用例逐条跑验收检查 |
| 评估 | `python -m src.cli eval --llm mock|openai` | 同一套检查用于 Mock 与真实模型 |

验收检查（`src/domain/checks.py`）只看最终答案、引用和工具调用事实；“引用均为原文”一条按该用例的文档版本（含替换后的内容）逐字核对。

## 用例：预期与实际（离线 Mock）

全部结果：[examples/results/mock-summary.md](../examples/results/mock-summary.md)，测试输出：[examples/results/pytest.txt](../examples/results/pytest.txt)。

| 用例 | 预期 | 实际 | Trace |
|---|---|---|---|
| c01 明确答案 | answered，引用 D03-S1，含 5 天 | 一致，5/5 | [c01](../examples/runs/mock/c01_clear_answer.md) |
| c02 文档冲突（参考实例） | 引用 D01-S1 与 D02-S1，同时给出 30/15，请求确认，不擅自选 | 一致，6/6 | [c02](../examples/runs/mock/c02_conflict.md) |
| c03 删除 D02 | 冲突消失，依据 D01 回答 30 天，不出现 15 | 一致，4/4 | [c03](../examples/runs/mock/c03_conflict_doc_removed.md) |
| c04 资料外问题 | out_of_scope，无引用，写明缺口 | 一致，4/4 | [c04](../examples/runs/mock/c04_out_of_scope.md) |
| c05 改写后的相似问题 | 首检无命中 → 改写查询 → 与 c01 同一依据 D03-S1 | 一致，4/4 | [c05](../examples/runs/mock/c05_paraphrase.md) |
| c06 上下文追问 | 补全“住宿”后检索，引用 D05-S2，答 350 元 | 一致，5/5 | [c06](../examples/runs/mock/c06_followup_context.md) |
| c07 无上下文追问 | needs_clarification，无数字答案 | 一致，3/3 | [c07](../examples/runs/mock/c07_followup_no_context.md) |
| c08 检索持续失败 | 重试后 failed，无引用、无数字 | 一致，3/3 | [c08](../examples/runs/mock/c08_tool_failure.md) |
| c09 读取失败一次 | 重试成功，引用 D04-S3，答 10 米 | 一致，4/4 | [c09](../examples/runs/mock/c09_tool_failure_once.md) |
| c10 步数上限 | 2 轮后 incomplete，无答案 | 一致，3/3 | [c10](../examples/runs/mock/c10_step_limit.md) |
| c11 改写 D03 原文 | 答案随之变为 7 天 | 一致，3/3 | [c11](../examples/runs/mock/c11_doc_content_changed.md) |

Mock 运行中护栏校正次数为 0；护栏拦截能力由 `test_guard_*` 单测验证。

## 真实模型

模型：智谱 GLM-4-Flash（免费版，OpenAI 兼容接口，temperature=0）。每轮跑全部 11 个用例，与 Mock 共用同一套检查。

| 轮次 | 代码 | 检查通过 | 护栏校正 | 汇总 | Trace |
|---|---|---|---|---|---|
| 第 1 轮 | 初版 | 32/44 | 6 | [r1 汇总](../examples/results/glm-4-flash-r1-summary.md) | [glm-4-flash-r1/](../examples/runs/glm-4-flash-r1/) |
| 第 2 轮 | 按第 1 轮问题修改 | 33/44 | 0 | [r2 汇总](../examples/results/glm-4-flash-r2-summary.md) | [glm-4-flash-r2/](../examples/runs/glm-4-flash-r2/) |

### 第 1 轮暴露的问题与修改

| 现象（第 1 轮） | 修改（第 2 轮运行前完成） |
|---|---|
| 模型多次把工具调用写成文本，循环拿不到调用 | 内核：文本中写明工具名且紧跟 JSON 参数时恢复为调用，Trace 标注“从文本恢复”；无调用时提示改为明确要求 function calling |
| c01、c03 模型引用“30天”，原文是“30 天”，护栏判为非原文，把正确答案降为 insufficient_evidence | 护栏比对引用时忽略空白差异 |
| c07 无上下文追问，模型反复检索直到步数上限 | 提示词：history 为空且问题依赖上文时直接请用户澄清 |
| c02 只读第一条结果 | 提示词：同一事项来自不同文档的片段要逐一读取 |
| c05 模型第一次就把问题改写为“入职三年年假天数”并命中，旧检查要求“检索两次”判为未通过 | 检查口径改为“检索词不是原问题”。第 1 轮结果仍按旧口径报告 |

### 第 2 轮未通过项

| 用例 | 现象 | 归因 |
|---|---|---|
| c02 冲突 | 检索同时返回 D01、D02，模型只读 D01 就答“30 天”，未发现 D02 的“15 天” | 模型未遵守“逐一读取”。护栏只核对引用是否为原文、数字是否有出处，发现不了漏读 |
| c04 超范围 | 连续换 4 个查询词并多次不调用工具，到步数上限，incomplete | 模型；上限按设计生效 |
| c07 无上下文追问 | 没有澄清，检索“公司制度或产品”后给出年假天数 | 模型猜测指代；答案数字都有引用出处，护栏无法判断答非所问 |
| c08 检索失败 | 状态为 failed（正确），gaps 为空，没写失败原因 | 护栏可补：判为 failed 时把工具错误写入 gaps |
| c11 文档内容变更 | 引用与原文只差空白，护栏放行，检查判为非原文 | 检查与护栏口径不一致，属于检查缺陷；第 2 轮后检查已同样忽略空白，本轮仍按原口径记为未通过 |

### 结论

- 两轮中，护栏删除过未读取的引用和非原文引用（第 1 轮 6 次）；第 2 轮没有一次答案带着无出处的数字交出。
- 冲突识别（c02）两轮都失败，且失败方式相同：只读第一条。继续加提示词收益有限；更有效的是把“同一事项有多个来源”变成工具返回的事实，例如 search_docs 按事项分组并返回来源数，或在 finish 时由护栏检查“检索命中了不同文档的同类片段但只读了一个”并退回模型。
- 指代猜测（c07）需要一条可执行的判断：问题依赖上文且 history 为空时，护栏拒绝带引用的 answered。

## 失败与限制

- 离线 Mock 的同义词表与“比较不同文档里的 N 天”冲突规则只适用于本合成数据，它全部通过不证明真实模型的查证能力。
- 护栏只能核对数字与逐字引用，不能判断引用在语义上是否回答了问题；真实模型可能引用了原文但答非所问。
- 冲突识别完全依赖模型；若真实模型漏判，c02 会失败且护栏不会补救——这是有意保留的评估信号。
- 未覆盖：文档带明确优先级（如“本说明优先于 D01”）时的裁决、权限范围、长文档分块。

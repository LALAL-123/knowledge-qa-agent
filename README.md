# 企业知识问答 Agent（题 3）

帮员工找到制度或产品问题的**有出处的答案**：检索 → 没命中就改写查询 → 读取原文 → 多份文档冲突时列出冲突并请求确认 → 只用原文回答并逐字引用。资料外问题、无上下文的追问、工具失败都返回明确状态，不凭常识作答。

原生 Python 实现 ReAct 循环（模型选动作 → 执行工具 → 观察 → 再决策或结束），模型走 OpenAI 兼容接口；另有离线 Mock 入口，用于在无模型时验证流程。

## 评审入口

```bash
pip install -r requirements.txt
python -m pytest -q                                   # 内核 + 业务 + 11 个验收用例（离线）
python -m src.cli eval --llm mock                     # 跑全部用例，写出 Trace 与汇总
python -m src.cli run examples/cases/c02_conflict.json --llm mock                # 参考实例
```

真实模型（任一 OpenAI 兼容服务；本仓库结果用智谱 GLM-4-Flash 免费版）：

```bash
cp .env.example .env        # 填 LLM_API_KEY、LLM_BASE_URL、LLM_MODEL
python -m src.cli eval --llm openai
```

| 想看什么 | 文件 |
|---|---|
| 验收汇总（Mock） | [examples/results/mock-summary.md](examples/results/mock-summary.md) |
| 参考实例：D01 30 天 vs D02 15 天 → 列出冲突并请求确认 | [examples/runs/mock/c02_conflict.md](examples/runs/mock/c02_conflict.md) |
| 删除 D02 后同一问题依据 D01 回答 | [examples/runs/mock/c03_conflict_doc_removed.md](examples/runs/mock/c03_conflict_doc_removed.md) |
| 口语化问题首检无命中 → 改写再检索 | [examples/runs/mock/c05_paraphrase.md](examples/runs/mock/c05_paraphrase.md) |
| 上下文追问 | [examples/runs/mock/c06_followup_context.md](examples/runs/mock/c06_followup_context.md) |
| 真实模型两轮结果（GLM-4-Flash） | [第 1 轮](examples/results/glm-4-flash-r1-summary.md) / [第 2 轮](examples/results/glm-4-flash-r2-summary.md)，分析见 [docs/03-evaluation.md](docs/03-evaluation.md) |
| 测试输出 | [examples/results/pytest.txt](examples/results/pytest.txt) |

## 环境

- Python 3.10+（开发环境 3.13.4，Windows 11）
- 依赖：`openai`（仅真实模型需要）、`pytest`
- 环境变量见 [.env.example](.env.example)；Mock 模式无需配置

## 验收点与用例

| 验收点 | 用例（`examples/cases/`） |
|---|---|
| 明确答案 | `c01_clear_answer`、`c11_doc_content_changed`（改原文后答案跟着变） |
| 文档冲突 | `c02_conflict`（参考实例）、`c03_conflict_doc_removed`（删除 D02 后无冲突） |
| 资料外问题 | `c04_out_of_scope` |
| 改写后的相似问题 | `c05_paraphrase` |
| 上下文追问 | `c06_followup_context`（有历史）、`c07_followup_no_context`（无历史，追问用户） |
| 工具失败 | `c08_tool_failure`（检索持续失败）、`c09_tool_failure_once`（读取失败一次后重试） |
| 步数上限 | `c10_step_limit` |

自己出题：复制用例改 `question` / `history`，或用 `env.doc_overrides` 删除文档（`"D02": null`）、替换片段原文（`"D03": {"snippets": {"D03-S1": "新原文"}}`）、新增文档。

## 目录

```
src/core/      与业务无关的 ReAct 内核：模型接入、循环、工具注册/故障注入、Trace、用例运行
src/domain/    本题业务：检索与读取工具、提示词、结束护栏（引用与数字核对）、离线 Mock 策略、验收检查
src/cli.py     命令行入口
data/          合成制度与产品 FAQ（带文档 ID、片段 ID、版本日期、适用范围）
examples/      cases/ 输入；runs/ 实际输出与 Trace；results/ 汇总与测试输出
tests/         内核测试、业务测试、全部用例的验收测试
docs/          需求、方案、评估、AI 使用说明、复盘
```

## 已知限制

- `examples/runs/mock/` 是离线 Mock 的记录，只证明流程、工具、护栏打通；Mock 里的同义词表和冲突判断是针对合成数据的简化规则，真实的改写与查证能力以 `--llm openai` 的运行记录为准。
- 检索是字符二元组重合度，没有向量检索；这是刻意保留的弱检索器，用来检验模型能否通过改写查询补救。
- 护栏能核对“引用是否为原文、数字是否有出处”，但不能判断引用在语义上是否回答了问题，也不预知哪些文档冲突。

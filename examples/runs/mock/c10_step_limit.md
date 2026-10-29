# c10_step_limit：执行上限：2 轮内无法完成查证，返回明确未完成（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`incomplete`（step_limit_reached）
- 决策轮数：2；业务工具调用：2

## 输入

```json
{
  "question": "报销期限多久？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "报销期限多久？", "top_k": 5} | {"query": "报销期限多久？", "count": 4, "hits": [{"doc_id": "D01", "snippet_id": "D01-S1", "title": "费用报销管理办法", "version_date": "2025-03-01", "score": 3, "preview": "报销期限：员工应在费用发生后 3…"}, {"doc_id": "D01", "snippet_id": "D01-S2", "title": "费用报销管理办法", "version_date": "2025-03-01", "score": 1, "preview": "报销需附合规发票，发票抬头须与公…"}, {"doc_id": "D02", "snippet_id": "D02-S1", … | 先按问题原文检索 |
| 2 | `read_snippet` | {"doc_id": "D01", "snippet_id": "D01-S1"} | {"doc_id": "D01", "snippet_id": "D01-S1", "title": "费用报销管理办法", "version_date": "2025-03-01", "scope": "未注明", "text": "报销期限：员工应在费用发生后 30 天内提交报销申请，逾期不予受理。", "ok": true} | 读取 D01-S1 原文以核对 |
| 2 | **停止** | — | incomplete：step_limit_reached | 达到执行上限或模型服务异常 |

## 最终输出

```json
{
  "answer": "",
  "citations": [],
  "snippets_read": [
    "D01/D01-S1"
  ],
  "gaps": [
    "未完成：step_limit_reached，未形成可靠答案"
  ],
  "clarifying_question": "",
  "task_status": "incomplete",
  "stop_reason": "step_limit_reached"
}
```

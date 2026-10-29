# c02_conflict：文档冲突（参考实例）：D01 写 30 天、D02 写 15 天，未给适用范围与优先级（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`conflict_needs_confirmation`（model_finished）
- 决策轮数：5；业务工具调用：4

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
| 3 | `read_snippet` | {"doc_id": "D01", "snippet_id": "D01-S2"} | {"doc_id": "D01", "snippet_id": "D01-S2", "title": "费用报销管理办法", "version_date": "2025-03-01", "scope": "未注明", "text": "报销需附合规发票，发票抬头须与公司名称一致。", "ok": true} | 读取 D01-S2 原文以核对 |
| 4 | `read_snippet` | {"doc_id": "D02", "snippet_id": "D02-S1"} | {"doc_id": "D02", "snippet_id": "D02-S1", "title": "差旅与报销补充说明", "version_date": "2026-01-15", "scope": "未注明", "text": "报销时限为费用发生后 15 天内，请各部门及时提交。", "ok": true} | 读取 D02-S1 原文以核对 |
| 5 | `finish` | status=conflict_needs_confirmation | 护栏校正 0 处 | 不同文档给出不同天数，且未说明适用范围与优先级 |

## 最终输出

```json
{
  "answer": "资料存在冲突：D01《费用报销管理办法》（2025-03-01 版，适用范围：未注明）：报销期限：员工应在费用发生后 30 天内提交报销申请，逾期不予受理。；D02《差旅与报销补充说明》（2026-01-15 版，适用范围：未注明）：报销时限为费用发生后 15 天内，请各部门及时提交。。文件均未说明适用范围和优先级，不能确定以哪份为准。",
  "citations": [
    {
      "doc_id": "D01",
      "snippet_id": "D01-S1",
      "quote": "报销期限：员工应在费用发生后 30 天内提交报销申请，逾期不予受理。",
      "title": "费用报销管理办法",
      "version_date": "2025-03-01",
      "scope": "未注明"
    },
    {
      "doc_id": "D02",
      "snippet_id": "D02-S1",
      "quote": "报销时限为费用发生后 15 天内，请各部门及时提交。",
      "title": "差旅与报销补充说明",
      "version_date": "2026-01-15",
      "scope": "未注明"
    }
  ],
  "conflicts": [
    {
      "doc_ids": [
        "D01",
        "D02"
      ],
      "description": "同一事项规定的天数不同"
    }
  ],
  "gaps": [],
  "clarifying_question": "请确认您适用哪份制度，或向制度归口部门确认现行口径。",
  "task_status": "conflict_needs_confirmation",
  "evidence_check": {
    "cited_snippets": 2,
    "unsupported_numbers": [],
    "snippets_read": 3,
    "searches": 1
  }
}
```

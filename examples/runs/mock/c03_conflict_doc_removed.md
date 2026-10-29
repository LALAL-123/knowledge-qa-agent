# c03_conflict_doc_removed：替换资料：删除 D02 后同一问题只剩 D01，应依据 D01 回答 30 天（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`answered`（model_finished）
- 决策轮数：4；业务工具调用：3

## 输入

```json
{
  "question": "报销期限多久？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "报销期限多久？", "top_k": 5} | {"query": "报销期限多久？", "count": 2, "hits": [{"doc_id": "D01", "snippet_id": "D01-S1", "title": "费用报销管理办法", "version_date": "2025-03-01", "score": 3, "preview": "报销期限：员工应在费用发生后 3…"}, {"doc_id": "D01", "snippet_id": "D01-S2", "title": "费用报销管理办法", "version_date": "2025-03-01", "score": 1, "preview": "报销需附合规发票，发票抬头须与公…"}], "note": "预览不可作为引用依据，请用 read_snippet 读取原文"… | 先按问题原文检索 |
| 2 | `read_snippet` | {"doc_id": "D01", "snippet_id": "D01-S1"} | {"doc_id": "D01", "snippet_id": "D01-S1", "title": "费用报销管理办法", "version_date": "2025-03-01", "scope": "未注明", "text": "报销期限：员工应在费用发生后 30 天内提交报销申请，逾期不予受理。", "ok": true} | 读取 D01-S1 原文以核对 |
| 3 | `read_snippet` | {"doc_id": "D01", "snippet_id": "D01-S2"} | {"doc_id": "D01", "snippet_id": "D01-S2", "title": "费用报销管理办法", "version_date": "2025-03-01", "scope": "未注明", "text": "报销需附合规发票，发票抬头须与公司名称一致。", "ok": true} | 读取 D01-S2 原文以核对 |
| 4 | `finish` | status=answered | 护栏校正 0 处 | D01-S1 原文直接回答了问题，且读取的片段之间无冲突 |

## 最终输出

```json
{
  "answer": "依据《费用报销管理办法》（D01，2025-03-01 版）：报销期限：员工应在费用发生后 30 天内提交报销申请，逾期不予受理。",
  "citations": [
    {
      "doc_id": "D01",
      "snippet_id": "D01-S1",
      "quote": "报销期限：员工应在费用发生后 30 天内提交报销申请，逾期不予受理。",
      "title": "费用报销管理办法",
      "version_date": "2025-03-01",
      "scope": "未注明"
    }
  ],
  "conflicts": [],
  "gaps": [],
  "clarifying_question": "",
  "task_status": "answered",
  "evidence_check": {
    "cited_snippets": 1,
    "unsupported_numbers": [],
    "snippets_read": 2,
    "searches": 1
  }
}
```

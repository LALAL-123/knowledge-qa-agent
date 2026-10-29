# c05_paraphrase：改写后的相似问题：口语化问年假，首次检索无命中，需改写查询（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`answered`（model_finished）
- 决策轮数：5；业务工具调用：4

## 输入

```json
{
  "question": "入职三年了，每年能歇多久？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "入职三年了，每年能歇多久？", "top_k": 5} | {"query": "入职三年了，每年能歇多久？", "count": 0, "hits": [], "note": "没有匹配的文档片段", "ok": true} | 先按问题原文检索 |
| 2 | `search_docs` | {"query": "年假 天数", "top_k": 5} | {"query": "年假 天数", "count": 2, "hits": [{"doc_id": "D03", "snippet_id": "D03-S1", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "score": 1, "preview": "员工带薪年休假（以下简称年假）：…"}, {"doc_id": "D03", "snippet_id": "D03-S2", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "score": 1, "preview": "年休假可分段使用，当年未休部分可…"}], "note": "预览不可作为引用依据，请用 read_snippet 读取原… | 原问题没有命中，改写为规范用语“年假 天数”再检索 |
| 3 | `read_snippet` | {"doc_id": "D03", "snippet_id": "D03-S1"} | {"doc_id": "D03", "snippet_id": "D03-S1", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "scope": "全体正式员工", "text": "员工带薪年休假（以下简称年假）：累计工作已满 1 年不满 10 年的，年假 5 天；已满 10 年不满 20 年的，年假 10 天；已满 20 年的，年假 15 天。", "ok": true} | 读取 D03-S1 原文以核对 |
| 4 | `read_snippet` | {"doc_id": "D03", "snippet_id": "D03-S2"} | {"doc_id": "D03", "snippet_id": "D03-S2", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "scope": "全体正式员工", "text": "年休假可分段使用，当年未休部分可顺延至次年 3 月 31 日前。", "ok": true} | 读取 D03-S2 原文以核对 |
| 5 | `finish` | status=answered | 护栏校正 0 处 | D03-S1 原文直接回答了问题，且读取的片段之间无冲突 |

## 最终输出

```json
{
  "answer": "依据《员工休假制度（年假）》（D03，2025-07-01 版）：员工带薪年休假（以下简称年假）：累计工作已满 1 年不满 10 年的，年假 5 天；已满 10 年不满 20 年的，年假 10 天；已满 20 年的，年假 15 天。",
  "citations": [
    {
      "doc_id": "D03",
      "snippet_id": "D03-S1",
      "quote": "员工带薪年休假（以下简称年假）：累计工作已满 1 年不满 10 年的，年假 5 天；已满 10 年不满 20 年的，年假 10 天；已满 20 年的，年假 15 天。",
      "title": "员工休假制度（年假）",
      "version_date": "2025-07-01",
      "scope": "全体正式员工"
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
    "searches": 2
  }
}
```

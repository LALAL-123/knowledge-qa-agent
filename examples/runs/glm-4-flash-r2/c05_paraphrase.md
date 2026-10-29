# c05_paraphrase：改写后的相似问题：口语化问年假，首次检索无命中，需改写查询（运行 1/1）

- 模型：`openai-compat:glm-4-flash`
- 结束状态：`answered`（model_finished）
- 决策轮数：4；业务工具调用：3

## 输入

```json
{
  "question": "入职三年了，每年能歇多久？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "年假规定"} | {"query": "年假规定", "count": 3, "hits": [{"doc_id": "D03", "snippet_id": "D03-S1", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "score": 1, "preview": "员工带薪年休假（以下简称年假）：…"}, {"doc_id": "D03", "snippet_id": "D03-S2", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "score": 1, "preview": "年休假可分段使用，当年未休部分可…"}, {"doc_id": "D06", "snippet_id": "D06-S1",… | 根据问题，需要了解公司关于年假的规定。 |
| 2 | `read_snippet` ✗ | {"doc_id": "D03", "snippet_id": "D03-S1", "version_date": "2025-07-01"} | {"ok": false, "error_type": "invalid_arguments", "error": "build_tools.<locals>.read_snippet() got an unexpected keyword argument 'version_date'"} | 根据搜索结果，需要查看员工休假制度（年假）的原文内容。 |
| 3 | `read_snippet` | {"doc_id": "D03", "snippet_id": "D03-S1"} | {"doc_id": "D03", "snippet_id": "D03-S1", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "scope": "全体正式员工", "text": "员工带薪年休假（以下简称年假）：累计工作已满 1 年不满 10 年的，年假 5 天；已满 10 年不满 20 年的，年假 10 天；已满 20 年的，年假 15 天。", "ok": true} | 根据搜索结果，需要查看员工休假制度（年假）的原文内容。 |
| 4 | `finish` | status=answered | 护栏校正 0 处 | 根据员工休假制度（年假）的原文内容，得出以上答案。 |

## 最终输出

```json
{
  "answer": "根据公司规定，入职三年后的员工，累计工作已满1年不满10年的，年假为5天；已满10年不满20年的，年假为10天；已满20年的，年假为15天。",
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
    "snippets_read": 1,
    "searches": 1
  }
}
```

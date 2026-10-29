# c11_doc_content_changed：替换文档内容：把 D03 改为年假 7 天，答案必须随原文改变（运行 1/1）

- 模型：`openai-compat:glm-4-flash`
- 结束状态：`answered`（model_finished）
- 决策轮数：3；业务工具调用：2

## 输入

```json
{
  "question": "年假有几天？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "年假天数"} | {"query": "年假天数", "count": 2, "hits": [{"doc_id": "D03", "snippet_id": "D03-S1", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "score": 1, "preview": "员工带薪年休假（以下简称年假）：…"}, {"doc_id": "D03", "snippet_id": "D03-S2", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "score": 1, "preview": "年休假可分段使用，当年未休部分可…"}], "note": "预览不可作为引用依据，请用 read_snippet 读取原文… | 查找关于年假天数的制度或产品信息 |
| 2 | `read_snippet` | {"doc_id": "D03", "snippet_id": "D03-S1"} | {"doc_id": "D03", "snippet_id": "D03-S1", "title": "员工休假制度（年假）", "version_date": "2025-07-01", "scope": "全体正式员工", "text": "员工带薪年休假（以下简称年假）：入职满 1 年后每年享有年假 7 天。", "ok": true} | 读取年假天数的具体规定 |
| 3 | `finish` | status=answered | 护栏校正 0 处 | 根据员工休假制度（年假）的规定，入职满1年后每年享有年假7天。 |

## 最终输出

```json
{
  "answer": "入职满1年后每年享有年假7天。",
  "citations": [
    {
      "doc_id": "D03",
      "snippet_id": "D03-S1",
      "quote": "员工带薪年休假（以下简称年假）：入职满1年后每年享有年假7天。",
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

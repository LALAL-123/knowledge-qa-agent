# c09_tool_failure_once：工具偶发失败：片段读取第一次失败，重试后正常回答（运行 1/1）

- 模型：`openai-compat:glm-4-flash`
- 结束状态：`answered`（model_finished）
- 决策轮数：4；业务工具调用：3

## 输入

```json
{
  "question": "X1 防水多深？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "X1 防水深度"} | {"query": "X1 防水深度", "count": 3, "hits": [{"doc_id": "D04", "snippet_id": "D04-S3", "title": "X1 运动相机产品 FAQ", "version_date": "2026-05-10", "score": 4, "preview": "X1 机身防水深度 10 米，无…"}, {"doc_id": "D04", "snippet_id": "D04-S1", "title": "X1 运动相机产品 FAQ", "version_date": "2026-05-10", "score": 1, "preview": "X1 支持 4K 60 帧视频录…"}, {"doc_id": "D04", "snippet_id": … | 根据问题，需要了解X1产品的防水深度。 |
| 2 | `read_snippet` ✗ | {"doc_id": "D04", "snippet_id": "D04-S3"} | {"ok": false, "error_type": "tool_failure", "error": "片段服务 502（注入故障）"} | 根据搜索结果，需要查看X1运动相机产品FAQ中关于防水深度的具体信息。 |
| 3 | `read_snippet` | {"doc_id": "D04", "snippet_id": "D04-S3"} | {"doc_id": "D04", "snippet_id": "D04-S3", "title": "X1 运动相机产品 FAQ", "version_date": "2026-05-10", "scope": "X1 全系", "text": "X1 机身防水深度 10 米，无需额外防水壳。", "ok": true} | 由于片段服务出现故障，尝试重新获取X1运动相机产品FAQ中关于防水深度的具体信息。 |
| 4 | `finish` | status=answered | 护栏校正 0 处 | 根据X1运动相机产品FAQ中的信息，得知X1运动相机的机身防水深度为10米，无需额外防水壳。 |

## 最终输出

```json
{
  "answer": "X1运动相机的机身防水深度为10米，无需额外防水壳。",
  "citations": [
    {
      "doc_id": "D04",
      "snippet_id": "D04-S3",
      "quote": "X1 机身防水深度 10 米，无需额外防水壳。",
      "title": "X1 运动相机产品 FAQ",
      "version_date": "2026-05-10",
      "scope": "X1 全系"
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

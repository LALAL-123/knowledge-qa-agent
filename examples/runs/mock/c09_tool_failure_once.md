# c09_tool_failure_once：工具偶发失败：片段读取第一次失败，重试后正常回答（运行 1/1）

- 模型：`mock:scripted-policy`
- 结束状态：`answered`（model_finished）
- 决策轮数：6；业务工具调用：5

## 输入

```json
{
  "question": "X1 防水多深？"
}
```

## 执行记录

| 步骤 | 动作 | 参数 | 返回摘要 | 决策依据 |
|---|---|---|---|---|
| 1 | `search_docs` | {"query": "X1 防水多深？", "top_k": 5} | {"query": "X1 防水多深？", "count": 3, "hits": [{"doc_id": "D04", "snippet_id": "D04-S3", "title": "X1 运动相机产品 FAQ", "version_date": "2026-05-10", "score": 2, "preview": "X1 机身防水深度 10 米，无…"}, {"doc_id": "D04", "snippet_id": "D04-S1", "title": "X1 运动相机产品 FAQ", "version_date": "2026-05-10", "score": 1, "preview": "X1 支持 4K 60 帧视频录…"}, {"doc_id": "D04", "snippet_id":… | 先按问题原文检索 |
| 2 | `read_snippet` ✗ | {"doc_id": "D04", "snippet_id": "D04-S3"} | {"ok": false, "error_type": "tool_failure", "error": "片段服务 502（注入故障）"} | 读取 D04-S3 原文以核对 |
| 3 | `read_snippet` | {"doc_id": "D04", "snippet_id": "D04-S3"} | {"doc_id": "D04", "snippet_id": "D04-S3", "title": "X1 运动相机产品 FAQ", "version_date": "2026-05-10", "scope": "X1 全系", "text": "X1 机身防水深度 10 米，无需额外防水壳。", "ok": true} | 读取失败（片段服务 502（注入故障）），重试一次 |
| 4 | `read_snippet` | {"doc_id": "D04", "snippet_id": "D04-S1"} | {"doc_id": "D04", "snippet_id": "D04-S1", "title": "X1 运动相机产品 FAQ", "version_date": "2026-05-10", "scope": "X1 全系", "text": "X1 支持 4K 60 帧视频录制。", "ok": true} | 读取 D04-S1 原文以核对 |
| 5 | `read_snippet` | {"doc_id": "D04", "snippet_id": "D04-S2"} | {"doc_id": "D04", "snippet_id": "D04-S2", "title": "X1 运动相机产品 FAQ", "version_date": "2026-05-10", "scope": "X1 全系", "text": "X1 电池续航约 120 分钟（1080p 录制、常温环境）。", "ok": true} | 读取 D04-S2 原文以核对 |
| 6 | `finish` | status=answered | 护栏校正 0 处 | D04-S3 原文直接回答了问题，且读取的片段之间无冲突 |

## 最终输出

```json
{
  "answer": "依据《X1 运动相机产品 FAQ》（D04，2026-05-10 版）：X1 机身防水深度 10 米，无需额外防水壳。",
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
    "snippets_read": 3,
    "searches": 1
  }
}
```

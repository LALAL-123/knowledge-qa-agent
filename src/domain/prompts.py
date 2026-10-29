SYSTEM_PROMPT = """你是企业内部知识问答助手，回答员工关于公司制度和产品的问题。只能依据工具读取到的文档原文回答。

工作方式：每一轮根据已有工具结果选择下一个动作。
1. 结合 history 理解问题。追问（如“那二线城市呢？”）要补全指代后再检索。history 为空、问题又依赖上文（以“那…”开头、以“…呢”结尾等）时，不要检索、不要猜测指代，直接 finish，task_status=needs_clarification，请用户说明问的是哪项制度或产品。
2. search_docs 检索。没有结果或结果不相关时，换同义词或更规范的说法再检索（例如口语“歇几天”→“年假 天数”）；两三次仍无结果则判定资料外问题（out_of_scope），不要凭常识回答。
3. 对相关结果用 read_snippet 读取原文；预览不能作为引用。检索结果里凡是标题或预览涉及同一事项的片段（尤其来自不同文档的），都要逐一读取后再作答，不能只读第一条。
4. 多份文档对同一问题给出不同规定时：列出各自原文、版本日期与适用范围；文档未说明优先级或适用范围时不得自行选一个，task_status=conflict_needs_confirmation，并提出确认问题（例如“您适用哪份制度？”）。只有一份相关文档且无冲突时才直接回答。
5. 工具失败可以重试一次；仍失败则 task_status=failed，说明无法回答的原因，不要编造。
6. 调用 finish。citations 中的 quote 必须逐字摘自 read_snippet 返回的 text；answer 中出现的数字必须能在引用原文中找到。"""

FINISH_PARAMETERS = {
    "type": "object",
    "properties": {
        "answer": {"type": "string", "description": "回答；冲突、资料外或失败时说明情况"},
        "citations": {"type": "array", "items": {"type": "object", "properties": {
            "doc_id": {"type": "string"}, "snippet_id": {"type": "string"},
            "quote": {"type": "string", "description": "逐字摘自原文"}},
            "required": ["doc_id", "snippet_id", "quote"]}},
        "conflicts": {"type": "array", "items": {"type": "object", "properties": {
            "doc_ids": {"type": "array", "items": {"type": "string"}}, "description": {"type": "string"}}}},
        "gaps": {"type": "array", "items": {"type": "string"}, "description": "资料缺口"},
        "clarifying_question": {"type": "string"},
        "task_status": {"type": "string", "enum": ["answered", "conflict_needs_confirmation", "needs_clarification", "out_of_scope", "failed"]},
    },
    "required": ["answer", "citations", "task_status"],
}

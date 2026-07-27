

def build_prompt(
    query: str,
    results: list[tuple[str, int]],
    documents: dict[str, str],
) -> str | None:
    if results == []:
        return None
    task_instruction = "# 任务说明：\n- 请仅根据以下参考文档回答问题。\n- 如果文档无法支持答案，请明确说明。\n"
    query_context = "# 用户问题：\n- " + query + "\n"
    prompt = task_instruction + query_context + "# 参考文档：\n"
    for doc, s in results:
        prompt += f"- [{doc}]: {{{documents[doc]}}}\n"
    return prompt

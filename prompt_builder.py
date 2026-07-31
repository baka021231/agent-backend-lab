from chunking import Chunk

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

def build_chunk_prompt(
        query:str,
        chunks:list[Chunk],
) -> str | None:
    if not chunks:
        return None
    task_instruction = "# 任务说明：\n- 只能根据参考内容回答。\n- 内容不足要明确说明。\n"
    query_context = "# 用户问题：\n- " + query + "\n"
    prompt = task_instruction + query_context + "# 参考文档：\n"
    for chunk in chunks:
        prompt += f"来源: {chunk.source}, 段落: {chunk.chunk_index}\n{chunk.text}\n"
    return prompt

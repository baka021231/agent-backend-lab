from search import load_documents, search_documents
import sys
import os
from event_log import append_event, build_search_event
from time import perf_counter
from llm_client import LLMClient, LLMClientError, DeepSeekClient
from prompt_builder import build_prompt

log_path = os.environ.get(
    "SEARCH_LOG_PATH",
    "logs/search_events.jsonl",
)

def run_cli(llmclient: LLMClient) -> None:
    try:
        documents = load_documents("documents")
    except OSError as error:
        print(f"读取文档失败：{error}")
        sys.exit(1)
    except UnicodeError as error:
        print(f"文档编码错误，请确保文件使用 UTF-8：{error}")
        sys.exit(1)

    if documents == {}:
        print("没有找到可搜索的 Markdown 文档")
        sys.exit(0)
    
    while True:
        print("\n请输入查询词：")
        try:
            query = input().strip().lower()
        except(KeyboardInterrupt, EOFError):
            print("\n已退出搜索程序")
            break

        if query == "exit" or query == "quit": 
            print("已退出搜索程序")
            break

        if not query:
            print("查询不能为空，请重新输入")
            continue
        start = perf_counter()
        results = search_documents(query, documents)
        elapsed_ms = (perf_counter() - start) * 1000
        event = build_search_event(query, results, elapsed_ms)
        try:
            append_event(log_path, event)
        except OSError as error:
            print(f"写入搜索日志失败：{error}",
                  file=sys.stderr,
                  )

        if results != []: 
            print("搜索结果：")
            for filename, score in results:
                print(f"- {filename}, 分数：{score}")
            prompt = build_prompt(query=query, results=results, documents=documents)
            if prompt != None:
                try:
                    response = llmclient.generate(prompt=prompt)
                    print(response)
                except LLMClientError as error:
                    print(f"模型回答错误：{error}")

        else: print("没有找到匹配文档")

if __name__ == "__main__":
    try:
        client:LLMClient = DeepSeekClient()
    except LLMClientError as error:
        print(f"程序启动失败：{error}")
        sys.exit(1)

    run_cli(client)
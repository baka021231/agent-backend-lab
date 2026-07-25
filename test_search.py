from search import (
    count_keywords,
    load_documents,
    search_documents
)
import sys

def run_test(name, query, documents, expected) -> bool:
    try:
        actual = search_documents(query, documents)

        # 不要求并列文档的返回顺序完全一致
        if sorted(actual) == sorted(expected):
            print(f"[PASS] {name}")
            return True
        else:
            print(f"[FAIL] {name}")
            print(f"  Query:    {query}")
            print(f"  Expected: {expected}")
            print(f"  Actual:   {actual}")
            return False

    except Exception as error:
        print(f"[ERROR] {name}")
        print(f"  Query: {query}")
        print(f"  {type(error).__name__}: {error}")
        return False


if __name__ == "__main__":
    documents = load_documents("documents")
    results = [
        # agent.md:
        # agent 出现2次，implement出现1次
        run_test(
            name="agent document search",
            query="agent implement",
            documents=documents,
            expected=[("agent.md", 3)]
        ),

        # python.md:
        # python出现2次，agent出现2次
        run_test(
            name="python document search",
            query="python agent",
            documents=documents,
            expected=[("python.md", 4)]
        ),

        # docker.md:
        # docker出现1次，container出现1次
        run_test(
            name="docker document search",
            query="docker container",
            documents=documents,
            expected=[("docker.md", 2)]
        ),

        # 检查查询中的大小写和标点
        # agent.md中agent出现2次，implement出现1次
        run_test(
            name="query normalization",
            query="AGENT, IMPLEMENT!",
            documents=documents,
            expected=[("agent.md", 3)]
        ),

        # python.md和docker.md都包含and，各出现1次
        run_test(
            name="tied documents",
            query="and",
            documents=documents,
            expected=[
                ("python.md", 1),
                ("docker.md", 1)
            ]
        ),

        # 没有任何关键词匹配时，应该返回空列表
        run_test(
            name="no matching document",
            query="elephant spaceship",
            documents=documents,
            expected=[]
        ),

        # 没有文档时，应该返回空列表
        run_test(
            name="empty documents",
            query="agent",
            documents={},
            expected=[]
        )
    ]
    if not all(results):
        sys.exit(1)

from search import load_documents, search_documents
import sys

if __name__ == "__main__":
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
        print("请输入查询词：")
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
        results = search_documents(query, documents)
        if results != []: 
            print("搜索结果：")
            for filename, score in results:
                print(f"- {filename}, 分数：{score}")
        else: print("没有找到匹配文档")
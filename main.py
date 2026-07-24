from search import load_documents, search_documents


if __name__ == "__main__":
    documents = load_documents("documents")
    results = search_documents("python agent", documents)
    print(results)
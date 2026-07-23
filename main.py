def count_keywords(text, keywords):
    dic = {keyword : 0 for keyword in keywords}
    for word in text.lower().split():
        word = word.strip(".,!?;:")
        if word in dic:
            dic[word] += 1
    return dic

if __name__ == "__main__":
    text = "python can build agent, and agent needs python"
    keywords = ["python", "agent", "docker"]
    print(count_keywords(text, keywords))
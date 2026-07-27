from llm_client import LLMClient, MyClient, DeepSeekClient

client: LLMClient = MyClient()

acture = client.generate("你好喵")

print(acture)

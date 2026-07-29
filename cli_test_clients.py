from llm_client import LLMClientError


class FailingClient:
    def generate(self, prompt: str) -> str:
        raise LLMClientError("DeepSeek API 调用失败")

class EmptyResponseClient:
    def generate(self, prompt: str) -> str:
        raise LLMClientError("DeepSeek 返回了空内容")
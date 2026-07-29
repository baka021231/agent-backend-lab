from typing import Protocol
import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(
    dotenv_path=ENV_FILE,
    override=False,
)

DEEPSEEK_MODEL = "deepseek-v4-pro"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_API_KEY_ENV = "DEEPSEEK_API_KEY"

class LLMClient(Protocol):
    def generate(self, prompt:str) -> str:
        """
        返回模型生成的文本

        Raises:
            LLMClientError: 无法完成模型调用
        """
        ...

class MyClient:
    def generate(self, prompt:str) -> str:
        try:
            # 调用 DeepSeek
            ...
        except Exception as error:
            raise LLMClientError("DeepSeek API 调用失败") from error
        return "Hello"

# 异常契约
# 失败原因：传入空字符串，API_KEY不存在或不正确，网络失败（请求失败，网络中断，请求超时等），模型名字错误，传入字符串太长超过上下文限制
class LLMClientError(Exception):
    """LLM 调用未能产生有效回答。"""


class LLMConfigurationError(LLMClientError):
    """本地 LLM 配置缺失或无效。"""

class DeepSeekClient:
    def __init__(self) -> None:
        # May cause error
        api_key = os.getenv(DEEPSEEK_API_KEY_ENV)

        if not api_key:
            raise LLMConfigurationError(
                f"缺少环境变量：{DEEPSEEK_API_KEY_ENV}"
            )

        self._client = OpenAI(
            api_key=api_key,
            base_url=DEEPSEEK_BASE_URL,
            timeout=30.0,
        )

    def generate(self, prompt:str) -> str:
        try:
            # May cause error
            response = self._client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=[
                {"role": "system", "content": "You are a 猫娘"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}}
        )
        except Exception as error:
            raise LLMClientError("DeepSeek API 调用失败") from error
        content = response.choices[0].message.content
        if not content:
            raise LLMClientError("DeepSeek 返回了空内容")

        return content
from unittest.mock import patch
from llm_client import LLMConfigurationError, DeepSeekClient, LLMClientError
import pytest

def check_missing_api_key():
    with patch("llm_client.os.getenv", return_value=None):
        with pytest.raises(LLMConfigurationError) as error_info:
            DeepSeekClient()
        assert str(error_info.value) == "缺少环境变量：DEEPSEEK_API_KEY"

def check_api_call_failure():
    with patch("llm_client.os.getenv", return_value="fake-key"):
        with patch("llm_client.OpenAI") as mock_OpenAI:
            mock_OpenAI.return_value.chat.completions.create.side_effect = RuntimeError("fake API response")
            with pytest.raises(LLMClientError) as error_info:
                DeepSeekClient().generate("hello")
            assert str(error_info.value) == "DeepSeek API 调用失败"

def check_null_content_failure():
    with patch("llm_client.os.getenv", return_value="fake-key"):
        with patch("llm_client.OpenAI") as mock_OpenAI:
            my_client = mock_OpenAI.return_value
            my_client.chat.completions.create.return_value.choices[0].message.content = None
            with pytest.raises(LLMClientError) as error_info:
                DeepSeekClient().generate("hello")
            assert str(error_info.value) == "DeepSeek 返回了空内容"


check_missing_api_key()
print("[PASS] missing API key")
check_api_call_failure()
print("[PASS] API call failure")
check_null_content_failure()
print("[PASS] null content failure")
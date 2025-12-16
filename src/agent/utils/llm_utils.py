from langchain_openai import ChatOpenAI
from agent.utils.env_utils import OPENAI_BASE_URL, OPENAI_KEY, ZHIPU_API_KEY
from zai import ZhipuAiClient


def create_openai_llm() -> ChatOpenAI:
    """Create an OpenAI LLM. from environment variables."""
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0.5,
        base_url=OPENAI_BASE_URL,
        api_key=OPENAI_KEY,
    )


def create_zai_llm() -> ZhipuAiClient:
    """Create a GLM LLM. from environment variables."""
    return ZhipuAiClient(api_key=ZHIPU_API_KEY)

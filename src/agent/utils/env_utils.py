from dotenv import load_dotenv
import os

load_dotenv(override=True)

# llm 配置
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

from pydantic_settings import BaseSettings
from functools import lru_cache
from enum import Enum

class LLMProvider(str, Enum):
    OPENAI = "openai"
    GROQ = "groq"

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: LLMProvider = LLMProvider.GROQ
    MODEL_NAME: str = "mixtral-8x7b-32768"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
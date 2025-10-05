from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):

    llm_model: str = Field(None, alias="LLM_MODEL")
    llm_temperature: float = Field(None, alias="LLM_TEMPERATURE")
    ll_max_tokens: int = Field(None, alias="LLM_MAX_TOKENS")
    llm_timeout: int = Field(None, alias="LLM_TIMEOUT")
    llm_max_retries: int = Field(None, alias="LLM_MAX_RETRIEs")
    google_gemini_api_key: str = Field(None, alias="GEMINI_API_KEY")
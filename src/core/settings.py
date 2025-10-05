from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional, List
from functools import lru_cache

class Settings(BaseSettings):
    # === LLM ===
    llm_model: str = Field("gemini-2.5-flash", alias="LLM_MODEL")
    llm_temperature: float = Field(0.2, alias="LLM_TEMPERATURE")
    llm_max_tokens: Optional[int] = Field(default=None, alias="LLM_MAX_TOKENS")
    llm_timeout: Optional[int] = Field(default=None, alias="LLM_TIMEOUT")
    llm_max_retries: int = Field(3, alias="LLM_MAX_RETRIES")
    google_gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")

    # === AWS (opcionales) ===
    s3_bucket_name: Optional[str] = Field(None, alias="S3_BUCKET_NAME")
    aws_region: Optional[str] = Field(None, alias="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(None, alias="AWS_SECRET_ACCESS_KEY")

    # === MCP ===
    mcp_host: str = Field("http://127.0.0.1:8000/mcp", alias="MCP_HOST")

    # === APP ===
    app_env: str = Field("development", alias="APP_ENV")
    port: int = Field(8000, alias="PORT")
    hardcoded_password: Optional[str] = Field(None, alias="HARDCODED_PASSWORD")

    # === DATABASE ===
    database_url: str = Field(..., alias="DATABASE_URL")
    database_host: str = Field(..., alias="DATABASE_HOST")
    database_user: str = Field(..., alias="DATABASE_USER")
    database_name: str = Field(..., alias="DATABASE_NAME")
    database_port: int = Field(5432, alias="DATABASE_PORT")
    database_password: str = Field(..., alias="DATABASE_PASSWORD")
    database_pool_size: int = Field(5, alias="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(5, alias="DATABASE_MAX_OVERFLOW")

    # === CORS ===
    allowed_origins: Optional[List[str]] = Field(default=None, alias="ALLOWED_ORIGINS")
    allowed_methods: Optional[List[str]] = Field(default=None, alias="ALLOWED_METHODS")
    allowed_headers: Optional[List[str]] = Field(default=None, alias="ALLOWED_HEADERS")
    allowed_credential: Optional[bool] = Field(None, alias="ALLOWED_CREDENTIALS")

    @property
    def assembled_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if not all([self.database_user, self.database_password, self.database_name]):
            raise ValueError("Faltan DB_USER/DB_USER_PASSWORD/DB_NAME para armar DATABASE_URL")
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_user_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )
    

    # Permite pasar listas coma-separadas o JSON
    @field_validator("allowed_origins", "allowed_methods", "allowed_headers", mode="before")
    @classmethod
    def split_comma_or_json(cls, v):
        if v is None or isinstance(v, list):
            return v
        s = str(v).strip()
        if s.startswith("["):  
            return v
        return [item.strip() for item in s.split(",") if item.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

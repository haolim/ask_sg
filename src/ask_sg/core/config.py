# Environment settings

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Environment settings
class Settings(BaseSettings):
    database_url: str
    env: str = "production"
    ollama_base_url: str
    tavily_api_key: str
    ollama_embedding_model: str
    ollama_embedding_model_base_url: str
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()

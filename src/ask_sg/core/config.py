# Environment settings

from pydantic_settings import BaseSettings, SettingsConfigDict

# Environment settings
class Settings(BaseSettings):
    database_url: str
    env: str = "production"
    ollama_base_url: str
    tavily_api_key: str
    embedding_model: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    env: str = "production"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding= "utf-8",
        case_sensitive = False,
        extra = "ignore"
    )

settings = Settings()

engine = create_engine(settings.database_url,
                       echo=settings.env == "development",
                       pool_size=5,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_pre_ping=True
                       )

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


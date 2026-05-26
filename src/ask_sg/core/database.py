from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    env: str = "production"

    class Config:
        env_file = ".env"

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


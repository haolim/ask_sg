from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from ask_sg.core.config import settings

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


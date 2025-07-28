from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """get database session.

    Returns:
        Session: Database session.

    Yields:
        Iterator[Session]: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pathlib import Path
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def build_database_url() -> str:
    configured_url = os.getenv("DATABASE_URL")
    if configured_url and not configured_url.startswith("sqlite"):
        return configured_url

    if os.getenv("RENDER"):
        database_path = Path("/tmp/forgemind_ai.db")
    else:
        database_path = Path(__file__).resolve().parents[2] / "forgemind_ai.db"

    return f"sqlite:///{database_path}"


DATABASE_URL = build_database_url()
ENGINE_OPTIONS = {"connect_args": {"check_same_thread": False}} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, future=True, **ENGINE_OPTIONS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

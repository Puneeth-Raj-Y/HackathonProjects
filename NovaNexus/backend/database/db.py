from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Support for Render deployment with SQLite in tmp directory
# SQLite database path - use /tmp for Render's ephemeral filesystem
if os.getenv("RENDER"):
    # On Render, use /tmp for database (ephemeral storage)
    DATABASE_URL = "sqlite:////tmp/forgemind.db"
else:
    # Locally, use relative path
    DATABASE_URL = "sqlite:///./forgemind.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

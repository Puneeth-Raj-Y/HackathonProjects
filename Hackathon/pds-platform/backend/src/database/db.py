"""
Database Configuration
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Database configuration
# Try backend directory first, fall back to current directory
import glob
backend_db = None
try:
    # Look for database in backend directory
    dbs = glob.glob(os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'pds_platform.db'))
    if dbs:
        backend_db = dbs[0].replace('\\', '/')
except:
    pass

if backend_db:
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{backend_db}')
else:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///pds_platform.db')

# For SQLite development
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with all tables"""
    from models import Base
    Base.metadata.create_all(bind=engine)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Set database path to backend directory
os.environ['DATABASE_URL'] = 'sqlite:///backend/pds_platform.db'

from database.db import SessionLocal
from models import User

db = SessionLocal()
users = db.query(User).all()
print(f"Total users: {len(users)}")
for u in users[:10]:
    print(f"  ID: {u.id}, unique_id: {u.unique_id}, role: {u.role}")
db.close()

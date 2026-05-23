import sys
import os
sys.path.append(os.path.dirname(__file__))
from app.database import SessionLocal
from app.models import User

def seed():
    db = SessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        new_user = User(id=1, email="test@example.com", password_hash="dummy", full_name="System Admin")
        db.add(new_user)
        db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("Database seeded with default user.")

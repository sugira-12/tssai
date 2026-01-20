from backend.db.session import SessionLocal
from backend.app.models.user import User
from backend.app.models.module import Module
from backend.utils.security import hash_password

db = SessionLocal()

# Create sample users
users = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "trainer", "password": "trainer123", "role": "trainer"},
    {"username": "learner", "password": "learner123", "role": "learner"},
]

for u in users:
    user = User(username=u["username"], hashed_password=hash_password(u["password"]), role=u["role"])
    db.add(user)

# Sample module
module = Module(title="Electrical Engineering L4", level="Level 4")
db.add(module)

db.commit()
db.close()
print("DB seeded successfully.")

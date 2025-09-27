# print_users.py
from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    users = User.query.all()
    if not users:
        print("No users found in the database.")
    else:
        print(f"Total users: {len(users)}\n")
        for u in users:
            print(f"ID: {u.id}")
            print(f"First Name: {u.first_name}")
            print(f"Last Name: {u.last_name}")
            print(f"Email: {u.email}")
            print(f"Mobile: {u.mobile}")
            print(f"Role: {u.role}")
            print(f"Verified: {u.is_verified}")
            print("-" * 30)

from app import app, db
from models import User

def remove_all_users():
    with app.app_context():
        deleted = User.query.delete()  # ✅ deletes all rows
        db.session.commit()
        print(f"✅ Removed {deleted} users from the database.")

if __name__ == "__main__":
    remove_all_users()

from flask_jwt_extended import get_jwt_identity
from models import User

def is_super_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.role == "superadmin"

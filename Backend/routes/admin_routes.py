from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt
from models import db, User

admin_ns = Namespace("admin", description="Admin operations")

# Helper functions
def is_super_admin():
    jwt_data = get_jwt()
    return jwt_data.get("role") == "superadmin"

def user_to_dict(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "mobile": user.mobile,
        "role": user.role
    }

# Fetch all users
@admin_ns.route("/users")
class UserList(Resource):
    @jwt_required()
    def get(self):
        try:
            if not is_super_admin():
                return {"message": "Unauthorized"}, 403

            users = User.query.all()
            return {"users": [user_to_dict(u) for u in users]}, 200

        except Exception as e:
            return {"message": "Error fetching users"}, 500

# Fetch, update, delete single user
@admin_ns.route("/users/<int:user_id>")
class UserDetail(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            if not is_super_admin():
                return {"message": "Unauthorized"}, 403

            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            return {"user": user_to_dict(user)}, 200

        except Exception as e:
            return {"message": "Error fetching user"}, 500

    @jwt_required()
    def put(self, user_id):
        try:
            if not is_super_admin():
                return {"message": "Unauthorized"}, 403

            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            data = request.get_json(force=True) or {}
            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.mobile = data.get("mobile", user.mobile)
            user.role = data.get("role", user.role)

            if data.get("password"):
                user.password = data["password"]

            db.session.commit()
            return {"message": "User updated successfully", "user": user_to_dict(user)}, 200

        except Exception as e:
            return {"message": "Error updating user"}, 500

    @jwt_required()
    def delete(self, user_id):
        try:
            if not is_super_admin():
                return {"message": "Unauthorized"}, 403

            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404

            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200

        except Exception as e:
            return {"message": "Error deleting user"}, 500

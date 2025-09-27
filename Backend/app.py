from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db, User
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Init extensions
    db.init_app(app)
    JWTManager(app)

    api = Api(app, title="Galvan AI API", version="1.0")

    # Namespaces
    from routes.auth_routes import auth_ns
    api.add_namespace(auth_ns, path="/auth")

    from routes.admin_routes import admin_ns
    api.add_namespace(admin_ns, path="/admin")

    # Create DB & super admin
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email="admin@galvan-ai.com").first():
            super_admin = User(
                first_name="Super",
                last_name="Admin",
                email="admin@galvan-ai.com",
                mobile="0000000000",
                is_verified=True,
                role="superadmin"
            )
            super_admin.password = "Admin@123"  # hashed
            db.session.add(super_admin)
            db.session.commit()
            print("✅ Super Admin created: admin@galvan-ai.com / Admin@123")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

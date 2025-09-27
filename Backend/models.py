# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(20))
    profile_pic = db.Column(db.String(200))
    otp = db.Column(db.String(6))
    is_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default="user")

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plain_text):
        self.password_hash = generate_password_hash(plain_text)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

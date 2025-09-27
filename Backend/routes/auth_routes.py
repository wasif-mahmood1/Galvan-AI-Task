# routes/auth_routes.py
import random
from flask import request
from flask_restx import Namespace, Resource, fields
from models import db, User
from flask_jwt_extended import create_access_token, create_refresh_token
import smtplib
from email.message import EmailMessage
from config import Config

auth_ns = Namespace("auth", description="Authentication APIs")

# Request models
register_model = auth_ns.model("Register", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "mobile": fields.String(required=True),
    "profile_pic": fields.String(required=False)
})

login_model = auth_ns.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

otp_model = auth_ns.model("OTP", {
    "email": fields.String(required=True),
    "otp": fields.String(required=True)
})

# Helper to send OTP email via Mailtrap
def send_otp_email(to_email, otp):
    try:
        msg = EmailMessage()
        msg.set_content(f"Your OTP code is: {otp}")
        msg['Subject'] = "Verify your account"
        msg['From'] = Config.EMAIL_USER
        msg['To'] = to_email

        with smtplib.SMTP("smtp.mailtrap.io", 587) as smtp:
            smtp.login(Config.EMAIL_USER, Config.EMAIL_PASS)
            smtp.send_message(msg)
    except Exception as e:
        print("Error sending OTP email:", e)

# Register user
@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = request.json
        try:
            for field in ["first_name","last_name","email","password","mobile"]:
                if not data.get(field):
                    return {"message": f"{field} is required"}, 400

            if User.query.filter_by(email=data["email"]).first():
                return {"message": "Email already registered"}, 400

            otp = str(random.randint(100000,999999))
            new_user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                mobile=data["mobile"],
                profile_pic=data.get("profile_pic"),
                otp=otp,
                is_verified=False,
                role="user"
            )
            new_user.password = data["password"]  # hashes automatically

            db.session.add(new_user)
            db.session.commit()

            send_otp_email(data["email"], otp)
            return {"message": "User registered. Verify OTP."}, 201

        except Exception as e:
            print("Registration error:", e)
            return {"message":"Server error"},500

# Verify OTP
@auth_ns.route("/verify-otp")
class VerifyOTP(Resource):
    @auth_ns.expect(otp_model)
    def post(self):
        data = request.json
        try:
            user = User.query.filter_by(email=data["email"]).first()
            if not user:
                return {"message": "User not found"}, 404

            if user.otp == data["otp"]:
                user.is_verified = True
                user.otp = None
                db.session.commit()
                return {"message": "Account verified successfully."}, 200
            else:
                return {"message": "Invalid OTP"}, 400
        except Exception as e:
            print("OTP verification error:", e)
            return {"message": "Server error"}, 500

# Resend OTP
@auth_ns.route("/resend-otp")
class ResendOTP(Resource):
    def post(self):
        data = request.json
        try:
            user = User.query.filter_by(email=data["email"]).first()
            if not user:
                return {"message": "User not found"}, 404

            otp = str(random.randint(100000,999999))
            user.otp = otp
            db.session.commit()

            send_otp_email(data["email"], otp)
            return {"message": "OTP resent successfully."}, 200
        except Exception as e:
            print("Resend OTP error:", e)
            return {"message": "Server error"}, 500

# Login
@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.json
        try:
            user = User.query.filter_by(email=data["email"]).first()
            if not user or not user.check_password(data["password"]):
                return {"message": "Invalid credentials"}, 401

            if not user.is_verified:
                return {"message": "Please verify your account via OTP."}, 403

            access_token = create_access_token(identity={"id": user.id, "role": user.role})
            refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role})

            return {"access_token": access_token, "refresh_token": refresh_token, "role": user.role}, 200
        except Exception as e:
            print("Login error:", e)
            return {"message": "Server error"}, 500

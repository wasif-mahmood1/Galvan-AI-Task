# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///galvan_ai.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "6f527aac5085be2838f9a5b05c963c5a"

    # Mailtrap credentials
    EMAIL_HOST = "smtp.mailtrap.io"
    EMAIL_PORT = 587
    EMAIL_USER = "394e36e80b0c0f" # your Mailtrap username
    EMAIL_PASS = "52a5c7d30e888c" # your Mailtrap password

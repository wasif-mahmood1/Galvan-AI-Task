import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USER = "394e36e80b0c0f"
EMAIL_PASS = "52a5c7d30e888c"

def send_otp_email(receiver_email, otp):
    subject = "Your OTP Verification Code"
    body = f"Your OTP code is: {otp}. It will expire in 10 minutes."

    msg = MIMEMultipart()
    msg["From"] = "noreply@galvan-ai.com"
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail("noreply@galvan-ai.com", receiver_email, msg.as_string())
        print(f"✅ OTP email sent to {receiver_email}")
        return True
    except Exception as e:
        print("❌ Email sending failed:", e)
        return False

import smtplib, os

EMAIL_USER = "394e36e80b0c0f"
EMAIL_PASS = "52a5c7d30e888c"

try:
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        print("✅ Login success!")
except Exception as e:
    print("❌ Failed:", e)

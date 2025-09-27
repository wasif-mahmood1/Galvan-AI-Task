# Galvan AI Dashboard & Authentication System

## Project Description
This project is a full-stack web application for **user management and authentication**. It includes:

- User registration with **email OTP verification**.
- Secure login with **JWT-based authentication**.
- Admin dashboard for managing users (view, edit, delete).
- Role-based access: `user`, `admin`, and `superadmin`.
- Frontend built with **Next.js**.
- Backend built with **Flask RESTX** and **SQLite** database.

This system is designed for educational purposes and can be extended for production-ready applications.

**Demo Video:** [Watch Project Demo](https://drive.google.com/drive/folders/1gq7-HOBtxnhLmsFsCbIKwmfQjHMxv53x?usp=sharing)

---

## Features

### User Features
- Register with first name, last name, email, password, and mobile.
- OTP verification via email.
- Login with verified account.

### Admin Features
- View list of all users.
- Edit user details.
- Delete users.
- Role-based access control (only superadmin can manage users).

---

## Tech Stack

- **Frontend:** Next.js, React, Tailwind CSS, Axios  
- **Backend:** Flask, Flask-RESTX, Flask-JWT-Extended, SQLAlchemy  
- **Database:** SQLite  
- **Authentication:** JWT  
- **Email Testing:** Mailtrap  

---

## Setup Instructions

### Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/galvan-ai.git
   cd galvan-ai/backend

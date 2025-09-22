# Expenses API

A simple FastAPI-based application for managing expenses with JWT authentication.

## Overview
This project implements a RESTful API for managing expenses, integrated with a secure JWT-based authentication system. It uses SQLite as the database and supports user registration, login, token refresh, and expense management. The API is documented using Swagger UI, and security is enhanced with HttpOnly cookies and strict SameSite policies.

## Features
- **Authentication**:
  - Register and login with username and password.
  - Access Token (15 minutes) and Refresh Token (7 days) stored in secure HttpOnly cookies.
  - Token refresh without re-login using `/auth/refresh`.
  - Logout clears cookies.
- **Expense Management**:
  - Create, list, retrieve, update, and delete expenses.
  - All endpoints require authentication via JWT.
- **Security**:
  - Passwords hashed with bcrypt.
  - JWT tokens signed with a secure secret key.
  - Cookies protected against XSS and CSRF attacks.
- **Swagger UI**:
  - Simplified to show only `username` and `password` for login.
  - Authorization restricted to JWT Bearer tokens.

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mahdighadiriii/FastApi/tree/auth-jwt
   cd FastApi
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment**:
   Create a `.env` file based on `.env.example`:
   ```text
   SQLALCHEMY_DATABASE_URL=sqlite:///./app/test.db
   SECRET_KEY=your-secret-key
   ```

4. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the Server**:
   ```bash
   fastapi dev app/main.py
   ```

6. **Access Swagger UI**:
   Open `http://localhost:8000/docs` in your browser.

## Endpoints
### Auth
- **POST /auth/register**: Create a new user with username and password.
- **POST /auth/login**: Login to receive access and refresh tokens in cookies.
- **POST /auth/refresh**: Refresh tokens using a valid refresh token in cookies.
- **POST /auth/logout**: Clear tokens and log out.

### Expenses
- **POST /expenses/**: Create a new expense (requires authentication).
- **GET /expenses/**: List all expenses for the authenticated user.
- **GET /expenses/{expense_id}**: Get details of a specific expense by ID.
- **PUT /expenses/{expense_id}**: Update an existing expense.
- **DELETE /expenses/{expense_id}**: Delete an expense.

## Why Cookies Instead of Authorization Header?
Using cookies for storing JWT tokens offers several advantages over the traditional Authorization header approach:
- **XSS Protection**: `HttpOnly` cookies prevent JavaScript from accessing tokens, reducing the risk of Cross-Site Scripting (XSS) attacks compared to storing tokens in `localStorage` or `sessionStorage`, which are vulnerable to XSS.
- **CSRF Protection**: With `SameSite=strict`, cookies are not sent in cross-site requests, mitigating Cross-Site Request Forgery (CSRF) attacks. The Authorization header requires additional CSRF tokens or mechanisms to achieve similar protection.
- **Ease of Use**: Cookies are automatically sent by the browser with every request, simplifying client-side implementation compared to manually including the token in the Authorization header.
- **Secure Transmission**: Cookies with `secure=True` (in production) ensure tokens are only sent over HTTPS, enhancing security.

## Security Considerations
- **JWT Security**:
  - Tokens are signed with a secure `SECRET_KEY` to prevent tampering.
  - Access Token has a short lifespan (15 minutes) to minimize damage if compromised.
  - Refresh Token has a longer lifespan (7 days) but is stored securely in HttpOnly cookies.
- **Cookie Security**:
  - `HttpOnly=True`: Prevents JavaScript access to cookies, protecting against XSS attacks.
  - `SameSite=strict`: Prevents cookies from being sent in cross-site requests, protecting against CSRF attacks.
  - `secure=False` is used for local testing; set to `True` in production to ensure cookies are only sent over HTTPS.
- **Password Security**:
  - Passwords are hashed using `bcrypt` via `passlib` for secure storage.
- **Error Handling**:
  - Invalid or expired tokens return HTTP 401 Unauthorized errors.
  - Duplicate usernames during registration return HTTP 400 Bad Request errors.
  - Non-existent expenses return HTTP 404 Not Found errors.

## Testing
Run the following commands to test the API:
1. **Register a User**:
   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
   -H "Content-Type: application/json" \
   -d '{"username":"testuser","password":"testpass"}'
   ```

2. **Login**:
   ```bash
   curl -X POST "http://localhost:8000/auth/login" \
   -H "Content-Type: application/json" \
   -d '{"username":"testuser","password":"testpass"}' \
   -c cookies.txt
   ```

3. **Refresh Tokens**:
   ```bash
   curl -X POST "http://localhost:8000/auth/refresh" \
   -b cookies.txt -c cookies.txt
   ```

4. **Get Expenses**:
   ```bash
   curl -X GET "http://localhost:8000/expenses" -b cookies.txt
   ```

5. **Check Swagger UI**:
   Visit `http://localhost:8000/docs` to interact with the API.

## Project Structure
```
FastApi/
├── alembic/
│   ├── env.py
│   ├── versions/
│   │   ├── 0ed6480f3fe7_add_user_model_with_jwt.py
│   │   └── ...
├── app/
│   ├── __init__.py
│   ├── crud/
│   │   ├── expenses.py
│   │   └── users.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── expenses.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── .env.example
├── requirements.txt
├── README.md
└── submission.txt
```

## Notes
- The project uses `datetime.now(timezone.utc)` for timezone-aware datetime handling, ensuring compatibility with Python 3.12+.
- The database schema is managed with Alembic, including `users` and `expenses` tables.
- For production, set `secure=True` in cookie settings to enforce HTTPS.
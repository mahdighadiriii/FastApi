# Expenses API

A robust FastAPI-based application for managing expenses with secure JWT authentication and multi-language support.

## Overview
This project implements a RESTful API for managing expenses, featuring secure JWT-based authentication and internationalization (i18n) for English (`en`) and Persian (`fa`). It uses SQLite as the database and supports user registration, login, token refresh, and expense management. The API is documented using Swagger UI, with enhanced security through HttpOnly cookies and strict SameSite policies. Code quality is maintained with linting (`ruff`) and reformatting (`black`, `isort`) tools, integrated with pre-commit hooks.

## Features
- **Authentication**:
  - Register and login with username and password.
  - Access Token (15 minutes) and Refresh Token (7 days) stored in secure HttpOnly cookies.
  - Token refresh via `/auth/refresh` without re-login.
  - Logout clears cookies.
- **Expense Management**:
  - Create, list, retrieve, update, and delete expenses.
  - All endpoints require JWT-based authentication.
- **Multi-Language Support (i18n)**:
  - Supports English (`en`) and Persian (`fa`) via `gettext` with PO/MO files.
  - Language detection using `Accept-Language` header or `lang` query parameter.
  - Error messages and responses are translated based on the user's language.
- **Code Quality**:
  - Linting with `ruff` to enforce PEP 8 and other code quality standards.
  - Reformatting with `black` and `isort` for consistent code style.
  - Pre-commit hooks automate linting and reformatting before commits.
- **Security**:
  - Passwords hashed with `bcrypt` using `passlib`.
  - JWT tokens signed with a secure secret key.
  - Cookies protected against XSS (`HttpOnly=True`) and CSRF (`SameSite=strict`).
- **Swagger UI**:
  - Simplified to accept only `username` and `password` for login.
  - Authorization restricted to JWT Bearer tokens.

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mahdighadiriii/FastApi/tree/feature/reformat
   cd FastApi
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pre-commit==3.8.0
   ```

4. **Set Up Environment**:
   Create a `.env` file based on `.env.example`:
   ```text
   SQLALCHEMY_DATABASE_URL=sqlite:///./app/test.db
   SECRET_KEY=your-generated-secret-key  # Generate with `openssl rand -hex 32`
   ```

5. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Compile Translation Files**:
   ```bash
   msgfmt app/translations/en/LC_MESSAGES/messages.po -o app/translations/en/LC_MESSAGES/messages.mo
   msgfmt app/translations/fa/LC_MESSAGES/messages.po -o app/translations/fa/LC_MESSAGES/messages.mo
   ```

7. **Set Up Pre-Commit Hooks**:
   ```bash
   pre-commit install
   ```

8. **Start the Server**:
   ```bash
   fastapi dev app/main.py
   ```

9. **Access Swagger UI**:
   Open `http://localhost:8000/docs` in your browser.

## Code Quality
To ensure consistent code style and quality:
- **Linting**: Use `ruff` to check for code quality issues:
  ```bash
  ruff check .
  ruff check --fix .
  ```
- **Reformatting**: Use `black` and `isort` to format code:
  ```bash
  black .
  isort .
  ```
- **Pre-Commit Hooks**: Automatically run `ruff`, `black`, and `isort` before each commit:
  ```bash
  pre-commit run --all-files
  ```

### Linting Details
- **Fixed Issues**:
  - Removed unused imports (`F401`) in `alembic/env.py`, `app/dependencies.py`, `app/main.py`, and `app/routers/auth.py`.
  - Updated type annotations (`UP007`, `UP045`, `UP035`) to use `X | Y` and `collections.abc.Sequence` instead of `typing.Union` and `typing.Sequence`.
  - Replaced `datetime.now(timezone.utc)` with `datetime.now(UTC)` (`UP017`).
  - Updated exception handling to include `raise ... from e` (`B904`) in `app/dependencies.py` and `app/routers/auth.py`.
  - Replaced `typing.List` with `list` (`UP006`) in `app/routers/expenses.py`.
- **Remaining Issues**:
  - `F401` in `app/__init__.py`: Kept imports with `# noqa: F401` for explicit re-export, as they may be used in future extensions.
  - `B904` in some exception handlers: Safe in FastAPI context due to dependency injection patterns.

## Endpoints
### Auth
- **POST /auth/register**: Create a new user with username and password.
  - Example: `{"username": "testuser", "password": "testpass"}`
  - Response: User details (`id`, `username`).
- **POST /auth/login**: Login to receive access and refresh tokens in cookies.
  - Example: `{"username": "testuser", "password": "testpass"}`
  - Response: `{"access_token": "...", "refresh_token": "...", "token_type": "bearer"}`
- **POST /auth/refresh**: Refresh tokens using a valid refresh token in cookies.
  - Response: New access and refresh tokens.
- **POST /auth/logout**: Clear tokens and log out.
  - Response: `{"message": "logged_out_successfully"}`

### Expenses
- **POST /expenses/**: Create a new expense (requires authentication).
  - Example: `{"description": "Coffee", "amount": 5.0}`
- **GET /expenses/**: List all expenses for the authenticated user.
- **GET /expenses/{expense_id}**: Get details of a specific expense by ID.
- **PUT /expenses/{expense_id}**: Update an existing expense.
  - Example: `{"description": "Updated Coffee", "amount": 6.0}`
- **DELETE /expenses/{expense_id}**: Delete an expense by ID.

## Multi-Language Support
The API supports English (`en`) and Persian (`fa`) using `gettext` with PO/MO files. Language is determined by:
1. Query parameter `lang` (e.g., `?lang=fa`).
2. `Accept-Language` header (e.g., `Accept-Language: fa`).
3. Default: English (`en`).

### Adding a New Language
To add a new language (e.g., Arabic `ar`):
1. Create a new directory: `app/translations/ar/LC_MESSAGES`.
2. Create a `messages.po` file with translations:
   ```po
   msgid ""
   msgstr ""
   "Project-Id-Version: Expenses API\n"
   "POT-Creation-Date: 2025-09-23 20:47+0400\n"
   "PO-Revision-Date: 2025-09-23 20:47+0400\n"
   "Language: ar\n"
   "MIME-Version: 1.0\n"
   "Content-Type: text/plain; charset=UTF-8\n"
   "Content-Transfer-Encoding: 8bit\n"

   msgid "username_already_registered"
   msgstr "اسم المستخدم مسجل بالفعل"

   msgid "incorrect_username_or_password"
   msgstr "اسم المستخدم أو كلمة المرور غير صحيحة"

   msgid "invalid_or_expired_refresh_token"
   msgstr "رمز التحديث غير صالح أو منتهي الصلاحية"

   msgid "expense_not_found"
   msgstr "لم يتم العثور على المصروف"

   msgid "logged_out_successfully"
   msgstr "تم تسجيل الخروج بنجاح"
   ```
3. Compile the PO file to MO:
   ```bash
   msgfmt app/translations/ar/LC_MESSAGES/messages.po -o app/translations/ar/LC_MESSAGES/messages.mo
   ```
4. Update `SUPPORTED_LANGUAGES` in `app/i18n.py`:
   ```python
   SUPPORTED_LANGUAGES = ["en", "fa", "ar"]
   ```
5. Restart the server and test with `?lang=ar` or `Accept-Language: ar`.

## Security Considerations
- **JWT Security**:
  - Tokens are signed with a secure `SECRET_KEY` to prevent tampering.
  - Access Token (15 minutes) minimizes damage if compromised.
  - Refresh Token (7 days) is stored securely in HttpOnly cookies.
- **Cookie Security**:
  - `HttpOnly=True`: Prevents JavaScript access, mitigating XSS attacks.
  - `SameSite=strict`: Prevents cross-site requests, mitigating CSRF attacks.
  - `secure=False` for local testing; set to `True` in production for HTTPS.
- **Password Security**:
  - Passwords hashed with `bcrypt` using `passlib`.
- **Error Handling**:
  - Invalid/expired tokens return HTTP 401 Unauthorized.
  - Duplicate usernames return HTTP 400 Bad Request.
  - Non-existent expenses return HTTP 404 Not Found.

## Why Cookies Instead of Authorization Header?
- **XSS Protection**: `HttpOnly` cookies prevent JavaScript access, unlike `localStorage` or `sessionStorage`.
- **CSRF Protection**: `SameSite=strict` mitigates CSRF attacks.
- **Ease of Use**: Cookies are automatically sent by the browser, simplifying client-side logic.
- **Secure Transmission**: `secure=True` (in production) ensures HTTPS-only transmission.

## Testing
Run the following commands to test the API:
1. **Register a User**:
   ```bash
   curl -X POST "http://localhost:8000/auth/register?lang=fa" \
   -H "Content-Type: application/json" \
   -d '{"username":"testuser","password":"testpass"}'
   ```

2. **Login**:
   ```bash
   curl -X POST "http://localhost:8000/auth/login?lang=fa" \
   -H "Content-Type: application/json" \
   -d '{"username":"testuser","password":"wrongpass"}'
   ```
   Expected error: `{"detail":"نام کاربری یا رمز عبور نادرست است"}`

3. **Refresh Tokens**:
   ```bash
   curl -X POST "http://localhost:8000/auth/refresh?lang=fa" \
   -b cookies.txt -c cookies.txt
   ```

4. **Get Expenses**:
   ```bash
   curl -X GET "http://localhost:8000/expenses?lang=fa" -b cookies.txt
   ```

5. **Test with Accept-Language Header**:
   ```bash
   curl -X GET "http://localhost:8000/expenses" \
   -H "Accept-Language: fa" -b cookies.txt
   ```

6. **Check Swagger UI**:
   Visit `http://localhost:8000/docs` to interact with the API. Test language switching with `lang` query or `Accept-Language` header.

## Project Structure
```
FastApi/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   ├── README
│   ├── versions/
│   │   ├── 4ad1357f7b7b_init_tables.py
│   │   ├── 0ed6480f3fe7_add_user_model_with_jwt.py
│   │   └── __pycache__/
├── alembic.ini
├── app/
│   ├── crud/
│   │   ├── expenses.py
│   │   ├── users.py
│   │   └── __pycache__/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── expenses.py
│   │   └── __pycache__/
│   ├── translations/
│   │   ├── en/
│   │   │   └── LC_MESSAGES/
│   │   │       ├── messages.po
│   │   │       └── messages.mo
│   │   ├── fa/
│   │   │   └── LC_MESSAGES/
│   │   │       ├── messages.po
│   │   │       └── messages.mo
│   ├── __init__.py
│   ├── database.py
│   ├── dependencies.py
│   ├── i18n.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── test.db
│   └── __pycache__/
├── docs/
│   └── DB.drawio.png
├── .env.example
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── README.md
└── submission.txt
```

## Implementation Challenges
- **Language Detection**: Handled multiple `Accept-Language` formats (e.g., `fa-IR`, `en-US`) by extracting primary language codes.
- **Unicode Support**: Ensured UTF-8 encoding for Persian text in JSON responses and PO files.
- **Dependency Injection**: Integrated `get_i18n_translator` across endpoints without breaking functionality.
- **Linting and Reformatting**:
  - Fixed `ruff` issues (e.g., unused imports, deprecated type annotations).
  - Configured `pyproject.toml` to move `select`/`ignore` to `[tool.ruff.lint]`.
  - Kept `app/__init__.py` imports with `# noqa: F401` for potential future use.
- **Pre-Commit Setup**: Resolved `pip` issues by specifying `pre-commit==3.8.0`.

## Notes
- Uses `datetime.now(UTC)` for timezone-aware datetime handling (Python 3.12+ compatible).
- Database schema managed with Alembic (`users` and `expenses` tables).
- For production, set `secure=True` in cookie settings for HTTPS.
- Some `B904` errors remain due to FastAPI's dependency injection but are safe.

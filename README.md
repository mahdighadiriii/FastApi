# Expenses API

A robust FastAPI-based application for managing expenses with secure JWT authentication, multi-language support, and Docker support.

## Overview
This project implements a RESTful API for managing expenses, featuring secure JWT-based authentication and internationalization (i18n) for English (`en`) and Persian (`fa`). It uses SQLite for development and PostgreSQL for production, with Redis for caching. The API is documented using Swagger UI, with enhanced security through HttpOnly cookies and strict SameSite policies. Code quality is maintained with linting (`ruff`) and reformatting (`black`, `isort`) tools, integrated with pre-commit hooks. Custom exception handling ensures structured error responses, and tests validate functionality.

![Image Alt Text](https://raw.githubusercontent.com/mahdighadiriii/FastApi/main/docs/fastapi-course.jpg)

## Features
- **Authentication**:
  - Register and login with username and password.
  - Access Token (15 minutes) and Refresh Token (7 days) stored in secure HttpOnly cookies.
  - Token refresh via `/auth/refresh` without re-login.
  - Logout clears cookies.
- **Expense Management**:
  - Create, list, retrieve, update, and delete expenses.
  - All endpoints require JWT-based authentication and are restricted to the authenticated user's data.
  - Expense listing (`GET /expenses/`) is cached in Redis for 5 minutes.
- **Multi-Language Support (i18n)**:
  - Supports English (`en`) and Persian (`fa`) via `gettext` with PO/MO files.
  - Language detection using `Accept-Language` header or `lang` query parameter.
  - Error messages and responses are translated.
- **Code Quality**:
  - Linting with `ruff` to enforce PEP 8 and other standards.
  - Reformatting with `black` and `isort` for consistent code style.
  - Pre-commit hooks automate linting and reformatting.
- **Error Handling**:
  - Custom `ExpenseNotFoundError` for "expense not found" errors, returning structured JSON responses (e.g., `{"status": "error", "message": "هزینه یافت نشد"}`).
  - Exception handler in FastAPI ensures consistent error responses.
- **Testing**:
  - Tests written with `pytest` and `TestClient` to validate endpoints and error handling.
  - Covers successful operations and error cases (e.g., 404 for nonexistent expenses).
- **Docker Support**:
  - Containerized with Docker and `docker-compose` for easy deployment.
  - Supports SQLite (development) and PostgreSQL (production).
  - Redis with password authentication for caching.
- **Caching**:
  - Uses Redis for caching `GET /expenses/` results with a 5-minute TTL.
  - Cache is invalidated on create, update, or delete operations.
  - Managed via `app/cache.py` module.

## Setup
### Without Docker (Development)
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mahdighadiriii/FastApi/
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
   Create a `.env` file based on `.env.example` in the project root:
   ```text
   SQLALCHEMY_DATABASE_URL=sqlite:///./app/test.db
   REDIS_URL=redis://default:admin@redis:6379/0
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

### With Docker (Development/Production)
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/FastApi.git
   cd FastApi
   ```

2. **Set Up Environment**:
   Create a `.env` file in the project root:
   ```text
   SQLALCHEMY_DATABASE_URL=postgresql://admin:your-secure-password@postgres:5432/expenses
   REDIS_URL=redis://default:admin@redis:6379/0
   SECRET_KEY=your-generated-secret-key  # Generate with `openssl rand -hex 32`
   ```

3. **Create Docker Network** (if using external network):
   ```bash
   docker network create expenses
   ```

4. **Build and Run with Docker Compose**:
   ```bash
   docker-compose up -d --build
   ```

5. **Run Database Migrations**:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

6. **Access Swagger UI**:
   Open `http://localhost:8000/docs` in your browser.

7. **Run Tests**:
   ```bash
   docker-compose exec web pip install pytest==8.4.2 pytest-asyncio==1.2.0
   docker-compose exec web pytest tests/test_expenses.py -v
   ```

8. **Stop the Containers**:
   ```bash
   docker-compose down
   ```

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
  - Updated type annotations (`UP007`, `UP045`, `UP035`) to use `X | Y` and `collections.abc.Sequence`.
  - Replaced `datetime.now(timezone.utc)` with `datetime.now(UTC)` (`UP017`).
  - Updated exception handling to include `raise ... from e` (`B904`).
  - Replaced `typing.List` with `list` (`UP006`).
  - Updated `declarative_base` to `sqlalchemy.orm.declarative_base` to resolve SQLAlchemy 2.0 warning.
  - Replaced Pydantic `class Config` with `ConfigDict` to resolve deprecation warning.
  - Replaced `datetime.utcnow` with `datetime.now(UTC)` in models.
  - Fixed `datetime.datetime` to `sqlalchemy.DateTime` in `models.py` for Alembic compatibility.
  - Fixed `SQLALCHEMY_DATABASE_URL` None error by explicitly loading `.env` file with `python-dotenv`.
  - Fixed `TypeError: get_expenses() got an unexpected keyword argument 'user_id'` by adding `user_id` parameter to `get_expenses` and other CRUD functions in `app/crud/expenses.py`.
- **Remaining Issues**:
  - `F401` in `app/__init__.py`: Kept with `# noqa: F401` for potential future use.
  - `B904` in some exception handlers: Safe in FastAPI context.
  - `passlib` `crypt` deprecation warning filtered in `.pytest.ini` as a library issue.

## Error Handling
- **Custom Exception**: `ExpenseNotFoundError` handles "expense not found" errors with translated messages.
- **Response Format**: Errors return JSON with `{"status": "error", "message": "..."}` (e.g., `{"status": "error", "message": "هزینه یافت نشد"}` for `lang=fa`).
- **Handler**: FastAPI exception handler ensures consistent 404 responses for nonexistent expenses.

## Testing
Run tests with:
```bash
pytest tests/test_expenses.py -v
```

### Test Cases
- **Nonexistent Expense (GET)**: Ensures 404 with `{"status": "error", "message": "هزینه یافت نشد"}` for invalid ID.
- **Nonexistent Expense (DELETE)**: Ensures 404 with proper error message.
- **Successful Create**: Verifies POST `/expenses/` creates an expense for the authenticated user.
- **Successful List**: Verifies GET `/expenses/` returns a list of expenses for the authenticated user.

### Running Tests in Docker
```bash
docker-compose exec web pip install pytest==8.4.2 pytest-asyncio==1.2.0
docker-compose exec web pytest tests/test_expenses.py -v
```

### Test Warnings
- **Resolved**:
  - SQLAlchemy `declarative_base` warning fixed by using `sqlalchemy.orm.declarative_base`.
  - Pydantic `class Config` warning fixed by using `ConfigDict`.
  - `datetime.utcnow` warning fixed by using `datetime.now(UTC)`.
  - `datetime.datetime` in `models.py` fixed by using `sqlalchemy.DateTime`.
  - `TypeError: get_expenses() got an unexpected keyword argument 'user_id'` fixed by updating `app/crud/expenses.py`.
- **Remaining**:
  - `passlib` `crypt` deprecation warning filtered in `.pytest.ini` but may still appear due to incomplete filtering.

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
- **POST /expenses/**: Create a new expense for the authenticated user.
  - Example: `{"description": "Coffee", "amount": 5.0}`
  - Response: Created expense details (including `id`, `created_at` in ISO 8601 format).
- **GET /expenses/**: List all expenses for the authenticated user (cached in Redis for 5 minutes).
- **GET /expenses/{expense_id}**: Get details of a specific expense by ID for the authenticated user.
- **PUT /expenses/{expense_id}**: Update an existing expense by ID for the authenticated user.
  - Example: `{"description": "Updated Coffee", "amount": 6.0}`
- **DELETE /expenses/{expense_id}**: Delete an expense by ID for the authenticated user.

## Caching
- The `GET /expenses/` endpoint caches results in Redis for 5 minutes to improve performance.
- Cache is invalidated on create, update, or delete operations to ensure data consistency.
- Managed via `app/cache.py` module.

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
  - Tokens are signed with a secure `SECRET_KEY`.
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
  - Non-existent expenses return HTTP 404 Not Found with structured JSON.
- **Docker Security**:
  - Use environment variables for sensitive data like `SECRET_KEY`, `POSTGRES_PASSWORD`, `REDIS_URL`.
  - Redis configured with password authentication.
  - PostgreSQL credentials stored in `postgres/secrets/.env`.
- **Data Access Control**:
  - Expense operations are restricted to the authenticated user's data using `user_id` filtering in CRUD functions.

## Why Cookies Instead of Authorization Header?
- **XSS Protection**: `HttpOnly` cookies prevent JavaScript access, unlike `localStorage` or `sessionStorage`.
- **CSRF Protection**: `SameSite=strict` mitigates CSRF attacks.
- **Ease of Use**: Cookies are automatically sent by the browser, simplifying client-side logic.
- **Secure Transmission**: `secure=True` (in production) ensures HTTPS-only transmission.

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
│   │   ├── d9977c3e31d6_update.py
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
│   ├── cache.py
│   ├── database.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── i18n.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── test.db
│   └── __pycache__/
├── docs/
│   └── DB.drawio.png
├── initialize/
│   ├── expenses_initialize.sh
│   └── redis_start.sh
├── postgres/
│   ├── docker-compose.yml
│   └── secrets/
│       └── .env
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── .env
├── .env.example
├── .pre-commit-config.yaml
├── .pytest.ini
├── pyproject.toml
├── requirements.txt
├── README.md
└── submission.txt
```

## Implementation Challenges
- **Language Detection**: Handled multiple `Accept-Language` formats (e.g., `fa-IR`, `en-US`) by extracting primary language codes.
- **Unicode Support**: Ensured UTF-8 encoding for Persian text in JSON responses and PO files.
- **Dependency Injection**: Integrated `get_i18n_translator`, `ExpenseNotFoundError`, and `CacheManager` across endpoints.
- **Linting and Reformatting**:
  - Fixed `ruff` issues (e.g., unused imports, deprecated type annotations).
  - Configured `pyproject.toml` for `[tool.ruff.lint]`.
  - Kept `app/__init__.py` imports with `# noqa: F401`.
- **Testing**: Ensured tests cover both error cases (404) and successful operations, with proper JWT authentication.
- **Deprecation Warnings**: Resolved SQLAlchemy and Pydantic warnings; filtered `passlib` warning as a temporary workaround.
- **Alembic Issues**:
  - Fixed `SQLALCHEMY_DATABASE_URL` None error by explicitly loading `.env` file with `python-dotenv`.
  - Fixed `datetime.datetime` to `sqlalchemy.DateTime` in `models.py` for Alembic compatibility.
- **Docker Integration**:
  - Added `Dockerfile` and `docker-compose.yml` for containerization.
  - Configured Redis with password authentication.
  - Added support for SQLite (development) and PostgreSQL (production).
  - Integrated `expenses_initialize.sh` and `redis_start.sh` for initialization.
- **Caching**:
  - Implemented `CacheManager` in `app/cache.py` for modular cache management.
  - Cached `GET /expenses/` results with 5-minute TTL.
  - Invalidated cache on create, update, or delete operations.
- **Bug Fixes**:
  - Fixed `TypeError: get_expenses() got an unexpected keyword argument 'user_id'` by adding `user_id` parameter to `get_expenses` and other CRUD functions in `app/crud/expenses.py`.
  - Ensured `user_id` filtering in all CRUD operations for security.

## Notes
- Uses `datetime.now(UTC)` for timezone-aware datetime handling (Python 3.12+ compatible).
- Database schema managed with Alembic (`users` and `expenses` tables).
- For production, set `secure=True` in cookie settings for HTTPS.
- Some `B904` errors remain due to FastAPI's dependency injection but are safe.
- Ensure `.env` file exists with `SECRET_KEY`, `POSTGRES_PASSWORD`, and `REDIS_URL` for security.
- The `created_at` field in responses is returned in ISO 8601 format (e.g., `"2025-09-25T01:12:00Z"`).
- Run `docker-compose exec web alembic upgrade head` after starting containers to apply migrations.
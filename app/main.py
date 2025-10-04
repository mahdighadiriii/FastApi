import os

import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .database import engine
from .exceptions import ExpenseNotFoundError
from .models import Base
from .routers import auth, expenses

# Load .env
load_dotenv()

# Sentry init
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=1.0,  # 100% for dev, reduce to 0.2 in prod
    environment=os.getenv("ENVIRONMENT", "development"),
)

app = FastAPI(
    title="Expenses API",
    description="A simple API for managing expenses with JWT authentication.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Operations related to authentication",
        },
        {
            "name": "expenses",
            "description": "Operations related to expense management",
        },
    ],
    openapi_extra={
        "security": [{"bearerAuth": []}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
    },
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS (restrict origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ExpenseNotFoundError)
async def expense_not_found_handler(
    request: Request, exc: ExpenseNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"status": "error", "message": exc.detail},
    )


# Health check for monitoring
@app.get("/health")
async def health():
    return {"status": "healthy"}


Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(expenses.router)

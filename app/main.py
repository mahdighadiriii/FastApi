from fastapi import FastAPI
from fastapi.security import HTTPBearer

from .database import engine
from .models import Base
from .routers import auth, expenses

app = FastAPI(
    title="Expenses API",
    description="A simple API for managing expenses with JWT authentication.",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication operations"},
        {"name": "expenses", "description": "Expense management operations"},
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

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(expenses.router)

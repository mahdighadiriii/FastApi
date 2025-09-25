from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .database import engine
from .exceptions import ExpenseNotFoundError
from .models import Base
from .routers import auth, expenses

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


@app.exception_handler(ExpenseNotFoundError)
async def expense_not_found_handler(
    request: Request, exc: ExpenseNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"status": "error", "message": exc.detail},
    )


Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(expenses.router)

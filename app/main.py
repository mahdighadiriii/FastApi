from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers import expenses

app = FastAPI(title="Expenses API")

Base.metadata.create_all(bind=engine)

app.include_router(expenses.router)

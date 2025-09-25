from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(
        DateTime, default=lambda: datetime.now(ZoneInfo("UTC"))
    )

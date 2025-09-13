from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"


    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=func.now())
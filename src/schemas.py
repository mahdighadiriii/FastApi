from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExpenseBase(BaseModel):
    description: str
    amount: float


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None

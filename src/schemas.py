from datetime import datetime

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

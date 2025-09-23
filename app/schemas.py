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
        from_attributes = True


class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None


class UserBase(BaseModel):
    username: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginForm(BaseModel):
    username: str
    password: str

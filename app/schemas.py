from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ExpenseBase(BaseModel):
    description: str
    amount: float


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None


class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime  # Changed from str to datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginForm(BaseModel):
    username: str
    password: str

from typing import Dict, List
from pydantic import BaseModel, Field, PositiveFloat
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response

app = FastAPI()


class ExpenseCreate(BaseModel):
    description: str = Field(...)
    amount: PositiveFloat = Field(...)


class ExpenseUpdate(BaseModel):
    description: str
    amount: PositiveFloat


class ExpenseOut(ExpenseCreate):
    id: int


expenses: Dict[int, ExpenseOut] = {}
next_id: int = 1


@app.post("/expenses/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
async def create_expense(payload: ExpenseCreate):
    global next_id
    expense = ExpenseOut(id=next_id, **payload.model_dump())
    expenses[next_id] = expense
    next_id += 1
    return expense


@app.get("/expenses/", response_model=List[ExpenseOut])
async def list_expenses():
    return list(expenses.values())


@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
async def get_expense(expense_id: int):
    exp = expenses.get(expense_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Object not found")
    return exp


@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
async def update_expense(expense_id: int, payload: ExpenseUpdate):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Object not found")
    updated = ExpenseOut(id=expense_id, **payload.model_dump())
    expenses[expense_id] = updated
    return updated


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Object not found")
    del expenses[expense_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

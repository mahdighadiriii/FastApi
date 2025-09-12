from fastapi import FastAPI, HTTPException

app = FastAPI()

expenses = {}
next_id = 1


@app.post("/expenses/", status_code=201)
async def create_expense(description: str, amount: float):
    global next_id
    next_id += 1
    expense = {"id": next_id, "description": description, "amount": amount}
    expenses[next_id] = expense
    return expense


@app.get("/expenses/")
async def get_expenses():
    return list(expenses.values())


@app.get("/expenses/{expense_id}")
async def retrieve(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Object not found")
    return expenses[expense_id]


@app.put("/expenses/{expense_id}")
async def update_expense(expense_id: int, description: str, amount: float):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Object not found")
    expenses[expense_id]["description"] = description
    expenses[expense_id]["amount"] = amount
    return expenses[expense_id]


@app.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Object not found")
    del expenses[expense_id]

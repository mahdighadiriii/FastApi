from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, database, models, schemas

app = FastAPI(title="Expenses API")

models.Base.metadata.create_all(bind=database.engine)


@app.post("/expenses/", response_model=schemas.ExpenseOut)
def create_expense(
    expense: schemas.ExpenseCreate, db: Session = Depends(database.get_db)
):
    return crud.create_expense(
        db=db, description=expense.description, amount=expense.amount
    )


@app.get("/expenses/", response_model=list[schemas.ExpenseOut])
def get_expenses(db: Session = Depends(database.get_db)):
    return crud.get_expenses(db=db)


@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
async def get_expense(expense_id: int, db: Session = Depends(database.get_db)):
    db_expense = crud.get_expense(db=db, expense_id=expense_id)
    
    if not db_expense:
        raise HTTPException(status_code=404, detail="Object not found")
    
    return db_expense


@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseOut)
async def update_expense(expense_id: int, expense: schemas.ExpenseUpdate, db: Session = Depends(database.get_db)):
    db_expense = crud.get_expense(db=db, expense_id=expense_id)
    
    if not db_expense:
        raise HTTPException(status_code=404, detail="Object not found")
    
    updated_expense = crud.update_expense(db=db, expense_id=expense_id, expense=expense)
    return updated_expense


@app.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(expense_id: int, db: Session = Depends(database.get_db)):
    db_expense = crud.get_expense(db=db, expense_id=expense_id)

    if not db_expense:
        raise HTTPException(status_code=404, detail="Object not found")

    crud.delete_expense(db=db, expense_id=expense_id)
    return None

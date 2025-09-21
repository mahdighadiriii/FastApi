from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, database, schemas

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=schemas.ExpenseOut)
def create_expense(
    expense: schemas.ExpenseCreate, db: Session = Depends(database.get_db)
):
    return crud.expenses.create_expense(db=db, expense=expense)


@router.get("/", response_model=list[schemas.ExpenseOut])
def get_expenses(db: Session = Depends(database.get_db)
):
    return crud.expenses.get_expenses(db=db)


@router.get("/{expense_id}", response_model=schemas.ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(database.get_db)):
    db_expense = crud.expenses.get_expense(db=db, expense_id=expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@router.put("/{expense_id}", response_model=schemas.ExpenseOut)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseUpdate,
    db: Session = Depends(database.get_db),
):
    updated = crud.expenses.update_expense(
        db=db, expense_id=expense_id, expense=expense
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(database.get_db)):
    db_expense = crud.expenses.get_expense(db=db, expense_id=expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    crud.expenses.delete_expense(db=db, expense_id=expense_id)

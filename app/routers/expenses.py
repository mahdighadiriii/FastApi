from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, database, dependencies, schemas
from ..exceptions import ExpenseNotFoundError

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post(
    "/",
    response_model=schemas.ExpenseOut,
    summary="Create a new expense",
    description="Create a new expense with description and amount.",
)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _=Depends(dependencies.get_i18n_translator),
):
    return crud.expenses.create_expense(db=db, expense=expense)


@router.get(
    "/",
    response_model=list[schemas.ExpenseOut],
    summary="List expenses",
    description="Get all expenses for the authenticated user.",
)
def get_expenses(
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _=Depends(dependencies.get_i18n_translator),
):
    return crud.expenses.get_expenses(db=db)


@router.get(
    "/{expense_id}",
    response_model=schemas.ExpenseOut,
    summary="Get an expense",
    description="Get details of a specific expense by ID.",
)
def get_expense(
    expense_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _=Depends(dependencies.get_i18n_translator),
):
    db_expense = crud.expenses.get_expense(db=db, expense_id=expense_id)
    if not db_expense:
        raise ExpenseNotFoundError(expense_id=expense_id, translator=_)
    return db_expense


@router.put(
    "/{expense_id}",
    response_model=schemas.ExpenseOut,
    summary="Update an expense",
    description="Update an existing expense by ID.",
)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseUpdate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _=Depends(dependencies.get_i18n_translator),
):
    updated = crud.expenses.update_expense(
        db=db, expense_id=expense_id, expense=expense
    )
    if not updated:
        raise ExpenseNotFoundError(expense_id=expense_id, translator=_)
    return updated


@router.delete(
    "/{expense_id}",
    status_code=204,
    summary="Delete an expense",
    description="Delete an expense by ID.",
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _=Depends(dependencies.get_i18n_translator),
):
    db_expense = crud.expenses.get_expense(db=db, expense_id=expense_id)
    if not db_expense:
        raise ExpenseNotFoundError(expense_id=expense_id, translator=_)
    crud.expenses.delete_expense(db=db, expense_id=expense_id)

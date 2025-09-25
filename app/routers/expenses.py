from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, database, dependencies, schemas
from app.cache import CacheManager
from app.exceptions import ExpenseNotFoundError

router = APIRouter(prefix="/expenses", tags=["expenses"])


def serialize_expense(exp):
    """Convert SQLAlchemy Expense object to JSON-serializable dict."""
    return {
        "id": exp.id,
        "description": exp.description,
        "amount": exp.amount,
        "user_id": exp.user_id,
        "created_at": exp.created_at.isoformat() if exp.created_at else None,
    }


@router.post(
    "/",
    response_model=schemas.ExpenseOut,
    summary="Create a new expense",
    description="Create a new expense with description and amount for the authenticated user.",
)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _: callable = Depends(dependencies.get_i18n_translator),
    cache: CacheManager = Depends(CacheManager),
):
    cache.clear_user_cache(current_user.id)
    return crud.expenses.create_expense(
        db=db, expense=expense, user_id=current_user.id
    )


@router.get(
    "/",
    response_model=list[schemas.ExpenseOut],
    summary="List all expenses",
    description="Retrieve a list of all expenses for the authenticated user.",
)
def get_expenses(
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _: callable = Depends(dependencies.get_i18n_translator),
    cache: CacheManager = Depends(CacheManager),
):
    cache_key = f"expenses:{current_user.id}"
    cached_expenses = cache.get(cache_key)
    if cached_expenses:
        return cached_expenses

    expenses = crud.expenses.get_expenses(db=db, user_id=current_user.id)
    expenses_data = [serialize_expense(exp) for exp in expenses]

    cache.set(cache_key, expenses_data, expire_seconds=300)
    return expenses_data


@router.get(
    "/{expense_id}",
    response_model=schemas.ExpenseOut,
    summary="Get an expense",
    description="Retrieve details of a specific expense by ID for the authenticated user.",
)
def get_expense(
    expense_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _: callable = Depends(dependencies.get_i18n_translator),
):
    db_expense = crud.expenses.get_expense(
        db=db, expense_id=expense_id, user_id=current_user.id
    )
    if not db_expense:
        raise ExpenseNotFoundError(expense_id=expense_id, translator=_)
    return serialize_expense(db_expense)


@router.put(
    "/{expense_id}",
    response_model=schemas.ExpenseOut,
    summary="Update an expense",
    description="Update an existing expense by ID for the authenticated user.",
)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseUpdate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _: callable = Depends(dependencies.get_i18n_translator),
    cache: CacheManager = Depends(CacheManager),
):
    updated = crud.expenses.update_expense(
        db=db, expense_id=expense_id, expense=expense, user_id=current_user.id
    )
    if not updated:
        raise ExpenseNotFoundError(expense_id=expense_id, translator=_)
    cache.clear_user_cache(current_user.id)
    return serialize_expense(updated)


@router.delete(
    "/{expense_id}",
    status_code=204,
    summary="Delete an expense",
    description="Delete an expense by ID for the authenticated user.",
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user),
    _: callable = Depends(dependencies.get_i18n_translator),
    cache: CacheManager = Depends(CacheManager),
):
    db_expense = crud.expenses.get_expense(
        db=db, expense_id=expense_id, user_id=current_user.id
    )
    if not db_expense:
        raise ExpenseNotFoundError(expense_id=expense_id, translator=_)
    crud.expenses.delete_expense(
        db=db, expense_id=expense_id, user_id=current_user.id
    )
    cache.clear_user_cache(current_user.id)

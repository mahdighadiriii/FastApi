from sqlalchemy.orm import Session

from ..models import Expense
from ..schemas import ExpenseCreate, ExpenseUpdate


def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    db_expense = Expense(**expense.model_dump(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()


def get_expense(db: Session, expense_id: int, user_id: int):
    return (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user_id)
        .first()
    )


def update_expense(
    db: Session, expense_id: int, expense: ExpenseUpdate, user_id: int
):
    db_expense = get_expense(db, expense_id, user_id)
    if not db_expense:
        return None

    update_data = expense.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int, user_id: int):
    db_expense = get_expense(db, expense_id, user_id)
    if db_expense:
        db.delete(db_expense)
        db.commit()

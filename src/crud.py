from sqlalchemy.orm import Session
from . import models


def create_expense(db: Session, description: str, amount: float):
    db_expense = models.Expense(description=description, amount=amount)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Expense).offset(skip).limit(limit).all()


def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

from fastapi import HTTPException, status


class ExpenseNotFoundError(HTTPException):
    def __init__(self, expense_id: int, translator):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=translator("expense_not_found"),
            headers={"WWW-Authenticate": "Bearer"},
        )
        self.expense_id = expense_id

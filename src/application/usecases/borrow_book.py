from __future__ import annotations
from src.application.dao.book_dao import BookDao
from src.application.dao.loan_dao import LoanDao
from src.application.models.loan import Loan
from datetime import datetime
from dataclasses import dataclass
from uuid import uuid4
from src.application.errors.application_erros import (
    StudentHasMoreThanThreeActiveLoansError,
    StudentHasOverdueLoansError,
    BookNotFoundError,
    BookNotAvailableError
)

class BorrowBook:
    def __init__(self: "BorrowBook", loan_dao: LoanDao, book_dao: BookDao):
        self.loan_dao = loan_dao
        self.book_dao = book_dao

    def execute(self: "BorrowBook", input: Input) -> Output:
        active_loans = self.loan_dao.get_active_loans_by_student_id(input.student_id, input.date)
        if len(active_loans) >= 3: raise StudentHasMoreThanThreeActiveLoansError()
        overdue_loans = self.loan_dao.get_overdue_loans_by_student_id(input.student_id, input.date)
        if len(overdue_loans) > 0: raise StudentHasOverdueLoansError()
        book = self.book_dao.get_by_id(input.book_id)
        if book is None: raise BookNotFoundError("id", input.book_id)
        if book.available_copies <= 0: raise BookNotAvailableError()
        loan = Loan(
            str(uuid4()),
            book.id,
            input.student_id,
            input.date
        )
        book.available_copies -= 1
        self.book_dao.update(book)
        self.loan_dao.save(loan)
        return Output(loan.id)

@dataclass
class Input:
    book_id: str
    student_id: str
    date: datetime

@dataclass
class Output:
    id: str


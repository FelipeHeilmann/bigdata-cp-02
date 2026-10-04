from __future__ import annotations
from src.application.dao.book_dao import BookDao
from src.application.dao.loan_dao import LoanDao
from src.application.models.loan import Loan
from datetime import datetime
from dataclasses import dataclass

class BorrowBook:
    def __init__(self: "BorrowBook", loan_dao: LoanDao, book_dao: BookDao):
        self.loan_dao = loan_dao
        self.book_dao = book_dao

    def execute(self: "BorrowBook", input: Input) -> Output:
        book = self.book_dao.get_by_id(input.book_id)
        loan = Loan(
            book.get_id(),
            input.student_id,
            input.date
        )
        book.available_copies -= 1
        self.book_dao.update(book)
        self.loan_dao.save(loan)
        return Output(loan.get_id())

@dataclass
class Input:
    book_id: str
    student_id: str
    date: datetime

@dataclass
class Output:
    id: str


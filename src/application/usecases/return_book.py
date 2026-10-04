from __future__ import annotations
from src.application.dao.book_dao import BookDao
from src.application.dao.loan_dao import LoanDao
from src.application.errors.application_erros import BookAlreadyReturnedError, LoanNotFoundError
from dataclasses import dataclass
from datetime import datetime, timedelta


class ReturnBook:
    FINE_PER_DAY = 2.0 
    def __init__(self: "ReturnBook", loan_dao: LoanDao, book_dao: BookDao):
        self.loan_dao = loan_dao
        self.book_dao = book_dao

    def execute(self: "ReturnBook", input: Input) -> Output:
        loan = self.loan_dao.get_by_id(input.loan_id)
        if loan is None: raise LoanNotFoundError(input.loan_id)
        if loan.return_date is not None: raise BookAlreadyReturnedError()
        fine = self._calculate_fine(loan, input.return_date)
        book = self.book_dao.get_by_id(loan.book_id)
        book.available_copies += 1
        loan.return_date = input.return_date
        loan.fine = fine
        self.loan_dao.update(loan)
        self.book_dao.update(book)
        return Output(loan.id, loan.return_date, loan.fine)
    
    def _calculate_fine(self: "ReturnBook", loan, return_date: datetime) -> float:
        if return_date > loan.date + timedelta(days=7):
            days_late = (return_date - (loan.date + timedelta(days=7))).days
            return days_late * self.FINE_PER_DAY
        return 0.0
        
@dataclass
class Input:
    loan_id: str
    return_date: datetime

@dataclass
class Output:
    id: str
    return_date: datetime
    fine: float
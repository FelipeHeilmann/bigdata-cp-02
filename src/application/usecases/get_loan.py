from __future__ import annotations
from src.application.dao.loan_dao import LoanDao
from src.application.dao.book_dao import BookDao
from src.application.dao.student_dao import StudentDao
from src.application.models.loan import Loan
from dataclasses import dataclass
from datetime import datetime, timedelta

class GetLoan:
    def __init__(self: "GetLoan", loan_dao: LoanDao, book_dao: BookDao, student_dao: StudentDao):
        self.loan_dao = loan_dao
        self.book_dao = book_dao
        self.student_dao = student_dao

    def execute(self: "GetLoan", id: str, date: datetime) -> Output:
        loan = self.loan_dao.get_by_id(id)
        book = self.book_dao.get_by_id(loan.book_id)
        student = self.student_dao.get_by_id(loan.student_id)
        return Output(
            id=loan.get_id(),
            book=BookOutput(
                id=book.get_id(),
                isbn=book.isbn,
                title=book.title
            ),
            student=StudentOutput(
                id=student.get_id(),
                enrollment_id=student.enrollment_id,
                name=student.name
            ),
            date=loan.date.isoformat(),
            status=self._get_loan_status(loan, date)
        )
    
    def _get_loan_status(self: "GetLoan", loan: Loan, date: datetime) -> str:
        if loan.return_date is not None:
            return "returned"
        if loan.date + timedelta(days=14) < date:
            return "overdue"
        return "active"
    
@dataclass
class Output:
    id: str
    book: BookOutput
    student: StudentOutput
    date: str
    status: str

@dataclass 
class BookOutput:
    id: str
    isbn: str
    title: str

@dataclass
class StudentOutput:
    id: str
    enrollment_id: str
    name: str
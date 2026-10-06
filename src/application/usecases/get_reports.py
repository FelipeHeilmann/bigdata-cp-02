from __future__ import annotations
from src.application.dao.report_dao import ReportDao, BorrowedBook, LoansByMajor, OverdueLoan
from dataclasses import dataclass
from datetime import datetime
from typing import List

class GetReports:
    TOP_BOOKS_LIMIT = 5

    def __init__(self: "GetReports", report_dao: ReportDao) -> None:
        self.report_dao = report_dao

    def execute(self: "GetReports", input: Input) -> Output:
        return Output(
            most_borrowed_books=self.report_dao.most_borrowed_books(self.TOP_BOOKS_LIMIT),
            loans_by_major=self.report_dao.loans_by_major(),
            overdue_loans=self.report_dao.overdue_loans(input.date),
            total_fines=self.report_dao.total_fines()
        )

@dataclass
class Input:
    date: datetime

@dataclass
class Output:
    most_borrowed_books: List[BorrowedBook]
    loans_by_major: List[LoansByMajor]
    overdue_loans: List[OverdueLoan]
    total_fines: float

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class BorrowedBook:
    book_id: str
    title: str | None
    loans: int

@dataclass
class LoansByMajor:
    major: str
    loans: int

@dataclass
class OverdueLoan:
    loan_id: str
    student_name: str
    book_title: str
    days_late: int

class ReportDao(ABC): # pragma: nocover
    @abstractmethod
    def most_borrowed_books(self: "ReportDao", limit: int) -> List[BorrowedBook]:
        pass

    @abstractmethod
    def loans_by_major(self: "ReportDao") -> List[LoansByMajor]:
        pass

    @abstractmethod
    def overdue_loans(self: "ReportDao", date: datetime) -> List[OverdueLoan]:
        pass

    @abstractmethod
    def total_fines(self: "ReportDao") -> float:
        pass

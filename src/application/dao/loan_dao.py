from abc import ABC, abstractmethod
from src.application.models.loan import Loan
from datetime import datetime
from typing import List

class LoanDao(ABC):
    @abstractmethod
    def save(self: "LoanDao", loan: Loan) -> None:
        pass

    @abstractmethod
    def get_by_id(self: "LoanDao", id: str) -> Loan | None:
        pass

    @abstractmethod
    def get_active_loans_by_student_id(self: "LoanDao", student_id: str, date: datetime) -> List[Loan]:
        pass

    @abstractmethod
    def get_overdue_loans_by_student_id(self: "LoanDao", student_id: str, date: datetime) -> List[Loan]:
        pass

    @abstractmethod
    def update(self: "LoanDao", loan: Loan) -> None:
        pass
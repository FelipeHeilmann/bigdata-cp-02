from abc import ABC, abstractmethod
from src.application.models.loan import Loan

class LoanDao(ABC):
    @abstractmethod
    def save(self: "LoanDao", loan: Loan) -> None:
        pass

    @abstractmethod
    def get_by_id(self: "LoanDao", id: str) -> Loan | None:
        pass
from src.application.dao.loan_dao import LoanDao
from src.application.models.loan import Loan
from datetime import datetime

class LoanDaoMemory(LoanDao):
    def __init__(self: "LoanDaoMemory"):
        self.loans = []

    def save(self: "LoanDaoMemory", loan: Loan) -> None:
        self.loans.append(loan)

    def get_by_id(self: "LoanDaoMemory", id: str) -> Loan | None:
        for loan in self.loans:
            if loan.id == id:
                return loan
        return None
    
    def get_active_loans_by_student_id(self: "LoanDaoMemory", student_id: str, date: datetime) -> list[Loan]:
        active_loans = []
        for loan in self.loans:
            if loan.student_id == student_id and loan.return_date is None:
                active_loans.append(loan)
        return active_loans
from src.application.dao.loan_dao import LoanDao
from src.application.models.loan import Loan

class LoanDaoMemory(LoanDao):
    def __init__(self: "LoanDaoMemory"):
        self.loans = []

    def save(self: "LoanDaoMemory", loan: Loan) -> None:
        self.loans.append(loan)

    def get_by_id(self: "LoanDaoMemory", id: str) -> Loan | None:
        for loan in self.loans:
            if loan.get_id() == id:
                return loan
        return None
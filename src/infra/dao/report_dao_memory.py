from src.application.dao.report_dao import ReportDao, BorrowedBook, LoansByMajor, OverdueLoan
from src.infra.dao.book_dao_memory import BookDaoMemory
from src.infra.dao.loan_dao_memory import LoanDaoMemory
from src.infra.dao.student_dao_memory import StudentDaoMemory
from collections import Counter
from datetime import datetime, timedelta
from typing import List

LOAN_PERIOD_DAYS = 7

class ReportDaoMemory(ReportDao): # pragma: nocover
    def __init__(self: "ReportDaoMemory", book_dao: BookDaoMemory, student_dao: StudentDaoMemory, loan_dao: LoanDaoMemory) -> None:
        self.book_dao = book_dao
        self.student_dao = student_dao
        self.loan_dao = loan_dao

    def most_borrowed_books(self: "ReportDaoMemory", limit: int) -> List[BorrowedBook]:
        counts = Counter(loan.book_id for loan in self.loan_dao.list_loans())
        ranking = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
        result = []
        for book_id, loans in ranking:
            book = self.book_dao.get_by_id(book_id)
            result.append(BorrowedBook(book_id, book.title if book else None, loans))
        return result

    def loans_by_major(self: "ReportDaoMemory") -> List[LoansByMajor]:
        counts = Counter()
        for loan in self.loan_dao.list_loans():
            student = self.student_dao.get_by_id(loan.student_id)
            if student is not None:
                counts[student.major] += 1
        ranking = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        return [LoansByMajor(major, loans) for major, loans in ranking]

    def overdue_loans(self: "ReportDaoMemory", date: datetime) -> List[OverdueLoan]:
        result = []
        for loan in self.loan_dao.list_loans():
            due_date = loan.date + timedelta(days=LOAN_PERIOD_DAYS)
            if loan.return_date is not None or due_date >= date:
                continue
            student = self.student_dao.get_by_id(loan.student_id)
            book = self.book_dao.get_by_id(loan.book_id)
            if student is None or book is None:
                continue
            result.append(OverdueLoan(loan.id, student.name, book.title, (date - due_date).days))
        return sorted(result, key=lambda overdue: (-overdue.days_late, overdue.student_name))

    def total_fines(self: "ReportDaoMemory") -> float:
        return float(sum(loan.fine for loan in self.loan_dao.list_loans()))

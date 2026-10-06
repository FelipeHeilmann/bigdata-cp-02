from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.application.usecases.create_student import CreateStudent, Input as InputCreateStudent
from src.application.usecases.get_reports import GetReports, Input as InputGetReports
from src.application.models.loan import Loan
from src.infra.dao.book_dao_memory import BookDaoMemory
from src.infra.dao.book_dao_mongo import BookDaoMongo
from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.infra.dao.student_dao_mongo import StudentDaoMongo
from src.infra.dao.loan_dao_memory import LoanDaoMemory
from src.infra.dao.loan_dao_mongo import LoanDaoMongo
from src.infra.dao.report_dao_memory import ReportDaoMemory
from src.infra.dao.report_dao_mongo import ReportDaoMongo
from tests.helpers import random_isbn, random_enrollment_id
from datetime import datetime
from uuid import uuid4
from pytest import approx

def create_book(book_dao, title: str) -> str:
    return CreateBook(book_dao).execute(InputCreateBook(
        random_isbn(), title, "Robert C. Martin", "Software Engineering", "2017", 10, 10
    )).id

def create_student(student_dao, name: str, major: str) -> str:
    return CreateStudent(student_dao).execute(InputCreateStudent(
        name=name, enrollment_id=random_enrollment_id(), age=20, major=major, email="student@fiap.com"
    )).id

def add_loan(loan_dao, book_id: str, student_id: str, date: datetime, return_date: datetime = None, fine: float = 0.0) -> str:
    loan = Loan(str(uuid4()), book_id, student_id, date, return_date, fine)
    loan_dao.save(loan)
    return loan.id

def add_returned_loans(loan_dao, book_id: str, student_id: str, count: int) -> None:
    for _ in range(count):
        add_loan(loan_dao, book_id, student_id, datetime(2024, 5, 1, 10, 0), datetime(2024, 5, 3, 10, 0))

def test_get_reports_should_generate_all_reports_successfully():
    book_dao = BookDaoMemory()
    student_dao = StudentDaoMemory()
    loan_dao = LoanDaoMemory()
    books = [create_book(book_dao, f"Book {i}") for i in range(1, 7)]
    alice = create_student(student_dao, "Alice", "Computer Science")
    bob = create_student(student_dao, "Bob", "Law")
    add_loan(loan_dao, books[0], alice, datetime(2024, 6, 1, 10, 0))
    add_returned_loans(loan_dao, books[0], alice, 4)
    add_loan(loan_dao, books[1], bob, datetime(2024, 6, 10, 9, 0))
    add_loan(loan_dao, books[1], bob, datetime(2024, 5, 1, 10, 0), datetime(2024, 5, 10, 10, 0), 4.0)
    add_returned_loans(loan_dao, books[1], bob, 2)
    add_loan(loan_dao, books[2], alice, datetime(2024, 6, 15, 10, 0))
    add_loan(loan_dao, books[2], alice, datetime(2024, 5, 1, 10, 0), datetime(2024, 5, 11, 10, 0), 6.0)
    add_returned_loans(loan_dao, books[2], alice, 1)
    add_returned_loans(loan_dao, books[3], bob, 2)
    add_returned_loans(loan_dao, books[4], alice, 1)
    add_returned_loans(loan_dao, books[5], bob, 1)
    get_reports = GetReports(ReportDaoMemory(book_dao, student_dao, loan_dao))
    output = get_reports.execute(InputGetReports(datetime(2024, 6, 20, 10, 0)))
    assert len(output.most_borrowed_books) == 5
    assert [(book.title, book.loans) for book in output.most_borrowed_books[:4]] == [
        ("Book 1", 5), ("Book 2", 4), ("Book 3", 3), ("Book 4", 2)
    ]
    assert output.most_borrowed_books[4].loans == 1
    assert [(item.major, item.loans) for item in output.loans_by_major] == [
        ("Computer Science", 9), ("Law", 7)
    ]
    assert [(overdue.student_name, overdue.book_title, overdue.days_late) for overdue in output.overdue_loans] == [
        ("Alice", "Book 1", 12), ("Bob", "Book 2", 3)
    ]
    assert output.total_fines == 10.0

def test_get_reports_should_return_empty_reports_without_loans():
    get_reports = GetReports(ReportDaoMemory(BookDaoMemory(), StudentDaoMemory(), LoanDaoMemory()))
    output = get_reports.execute(InputGetReports(datetime(2024, 6, 20, 10, 0)))
    assert output.most_borrowed_books == []
    assert output.loans_by_major == []
    assert output.overdue_loans == []
    assert output.total_fines == 0.0

def test_get_reports_should_generate_reports_with_mongo_aggregation():
    book_dao = BookDaoMongo()
    student_dao = StudentDaoMongo()
    loan_dao = LoanDaoMongo()
    get_reports = GetReports(ReportDaoMongo())
    date = datetime(2024, 6, 20, 10, 0)
    total_fines_before = get_reports.execute(InputGetReports(date)).total_fines
    major = f"Major {uuid4()}"
    book_id = create_book(book_dao, "Clean architecture")
    student_id = create_student(student_dao, "John Doe", major)
    overdue_loan_id = add_loan(loan_dao, book_id, student_id, datetime(2024, 6, 1, 10, 0))
    add_loan(loan_dao, book_id, student_id, datetime(2024, 5, 1, 10, 0), datetime(2024, 5, 10, 10, 0), 3.5)
    try:
        output = get_reports.execute(InputGetReports(date))
        assert len(output.most_borrowed_books) <= 5
        loans_count = [book.loans for book in output.most_borrowed_books]
        assert loans_count == sorted(loans_count, reverse=True)
        assert [item.loans for item in output.loans_by_major if item.major == major] == [2]
        overdue = [overdue for overdue in output.overdue_loans if overdue.loan_id == overdue_loan_id]
        assert len(overdue) == 1
        assert overdue[0].student_name == "John Doe"
        assert overdue[0].book_title == "Clean architecture"
        assert overdue[0].days_late == 12
        assert output.total_fines == approx(total_fines_before + 3.5)
    finally:
        loan_dao.collection.delete_many({"student_id": student_id})
        book_dao.remove(book_id)
        student_dao.remove(student_id)

from src.application.usecases.borrow_book import BorrowBook, Input as InputBorrowBook
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.application.usecases.create_student import CreateStudent, Input as InputCreateStudent 
from src.application.usecases.get_book_by_isbn import GetBookByISBN
from src.application.usecases.get_loan import GetLoan
from src.infra.dao.book_dao_memory import BookDaoMemory
from src.infra.dao.book_dao_mongo import BookDaoMongo
from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.infra.dao.student_dao_mongo import StudentDaoMongo
from src.infra.dao.loan_dao_memory import LoanDaoMemory
from tests.helpers import random_isbn, random_enrollment_id
from datetime import datetime

book_dao = BookDaoMongo()
student_dao = StudentDaoMongo()
loan_dao = LoanDaoMemory()

def test_get_loan_should_get_loan_successfully_with_status_active():
    create_book = CreateBook(book_dao)
    isbn = random_isbn()
    input = InputCreateBook(
        isbn,
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    )
    output_create_book = create_book.execute(input)
    create_student = CreateStudent(student_dao)
    enrollment_id = random_enrollment_id()
    input_student = InputCreateStudent(
        name="John Doe",
        enrollment_id=enrollment_id,
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    output_create_student = create_student.execute(input_student)
    date = datetime(2024, 6, 1, 10, 25, 10)
    borrow_book = BorrowBook(loan_dao, book_dao)
    output = borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    get_loan = GetLoan(loan_dao, book_dao, student_dao)
    output_get_loan = get_loan.execute(output.id, datetime(2024, 6, 2, 10, 25, 10))
    assert output_get_loan.book.isbn == isbn
    assert output_get_loan.book.title == "Clean architecture"
    assert output_get_loan.student.enrollment_id == enrollment_id
    assert output_get_loan.student.name == "John Doe"
    assert output_get_loan.date == "2024-06-01T10:25:10"
    assert output_get_loan.status == "active"
    get_book = GetBookByISBN(book_dao)
    output_get_book = get_book.execute(isbn)
    assert output_get_book.copies == 5
    assert output_get_book.available_copies == 4
    book_dao.remove(output_create_book.id)
    student_dao.remove(output_create_student.id)

def test_get_loan_should_get_loan_successfully_with_status_overdue():
    create_book = CreateBook(book_dao)
    isbn = random_isbn()
    input = InputCreateBook(
        isbn,
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    )
    output_create_book = create_book.execute(input)
    create_student = CreateStudent(student_dao)
    enrollment_id = random_enrollment_id()
    input_student = InputCreateStudent(
        name="John Doe",
        enrollment_id=enrollment_id,
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    output_create_student = create_student.execute(input_student)
    date = datetime(2024, 6, 1, 10, 25, 10)
    borrow_book = BorrowBook(loan_dao, book_dao)
    output = borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    get_loan = GetLoan(loan_dao, book_dao, student_dao)
    output_get_loan = get_loan.execute(output.id, datetime(2024, 6, 10, 10, 25, 10))
    assert output_get_loan.book.isbn == isbn
    assert output_get_loan.book.title == "Clean architecture"
    assert output_get_loan.student.enrollment_id == enrollment_id
    assert output_get_loan.student.name == "John Doe"
    assert output_get_loan.date == "2024-06-01T10:25:10"
    assert output_get_loan.status == "overdue"  
    student_dao.remove(output_create_student.id)

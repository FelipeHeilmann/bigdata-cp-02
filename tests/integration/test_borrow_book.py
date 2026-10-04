from src.application.usecases.borrow_book import BorrowBook, Input as InputBorrowBook
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.application.usecases.create_student import CreateStudent, Input as InputCreateStudent 
from src.application.usecases.get_book_by_isbn import GetBookByISBN
from src.application.usecases.get_loan import GetLoan
from src.application.errors.application_erros import (
    BookNotAvailableError,
    StudentHasMoreThanThreeActiveLoansError,
    StudentHasOverdueLoansError,
    BookNotFoundError,
)
from src.infra.dao.book_dao_memory import BookDaoMemory
from src.infra.dao.book_dao_mongo import BookDaoMongo
from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.infra.dao.student_dao_mongo import StudentDaoMongo
from src.infra.dao.loan_dao_memory import LoanDaoMemory
from src.infra.dao.loan_dao_mongo import LoanDaoMongo
from datetime import datetime
import pytest
from tests.helpers import random_isbn, random_enrollment_id

book_dao = BookDaoMongo()
student_dao = StudentDaoMongo()
loan_dao = LoanDaoMongo()

def test_borrow_book_should_borrow_book_successfully():
    isbn = random_isbn()
    enrollment_id = random_enrollment_id()
    create_book = CreateBook(book_dao)
    input_create_book = InputCreateBook(
        isbn,
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    )
    output_create_book = create_book.execute(input_create_book)
    create_student = CreateStudent(student_dao)
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

def test_borrow_book_should_throw_exception_when_book_is_not_available():
    isbn = random_isbn()
    enrollment_id = random_enrollment_id()
    create_book = CreateBook(book_dao)
    input = InputCreateBook(
        isbn,
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        1,
        1,
    )
    output_create_book = create_book.execute(input)
    create_student = CreateStudent(student_dao)
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
    borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    with pytest.raises(BookNotAvailableError) as excinfo:
        borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    assert str(excinfo.value) == "Book is not available"
    book_dao.remove(output_create_book.id)
    student_dao.remove(output_create_student.id)

def test_borrow_book_should_throw_excption_when_student_has_more_than_3_active_loans():
    isbn1 = random_isbn()
    enrollment_id = random_enrollment_id()
    create_book = CreateBook(book_dao)
    input1 = InputCreateBook(
        isbn1,
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    )
    output_create_book1 = create_book.execute(input1)
    isbn2 = random_isbn()
    input2 = InputCreateBook(
        isbn2,
        "Clean Code",
        "Robert C. Martin",
        "Software Engineering",
        "2008",
        3,
        3,
    )
    output_create_book2 = create_book.execute(input2)
    isbn3 = random_isbn()
    input3 = InputCreateBook(
        isbn3,
        "Implementing Domain-Driven Design",
        "Vaughn Vernon",
        "Software Engineering",
        "2013",
        5,
        5,
    )
    output_create_book3 = create_book.execute(input3)
    isbn4 = random_isbn()
    input4 = InputCreateBook(
        isbn4,
        "Patterns of Enterprise Application Architecture",
        "Martin Fowler",
        "Software Engineering",
        "2002",
        2,
        2,
    )
    output_create_book4 = create_book.execute(input4)
    create_student = CreateStudent(student_dao)
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
    borrow_book.execute(InputBorrowBook(output_create_book1.id, output_create_student.id, date))
    borrow_book.execute(InputBorrowBook(output_create_book2.id, output_create_student.id, date))
    borrow_book.execute(InputBorrowBook(output_create_book3.id, output_create_student.id, date))
    with pytest.raises(StudentHasMoreThanThreeActiveLoansError) as excinfo:
        borrow_book.execute(InputBorrowBook(output_create_book4.id, output_create_student.id, date))
    assert str(excinfo.value) == "Student has more than 3 active loans"
    book_dao.remove(output_create_book1.id)
    book_dao.remove(output_create_book2.id)
    book_dao.remove(output_create_book3.id)
    book_dao.remove(output_create_book4.id)
    student_dao.remove(output_create_student.id)

def test_borrow_book_should_throw_exception_when_book_does_not_exist():
    enrollment_id = random_enrollment_id()
    create_student = CreateStudent(student_dao)
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
    with pytest.raises(BookNotFoundError) as excinfo:
        borrow_book.execute(InputBorrowBook("non-existent-book-id", output_create_student.id, date))
    assert excinfo.value.args[0] == "Book with id non-existent-book-id not found"

def test_borrow_book_should_throw_exception_when_student_has_overdue_loans():
    isbn = random_isbn()
    enrollment_id = random_enrollment_id()
    create_book = CreateBook(book_dao)
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
    borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    overdue_date = datetime(2024, 6, 11, 10, 25, 10)
    with pytest.raises(StudentHasOverdueLoansError) as excinfo:
        borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, overdue_date))
    assert excinfo.value.args[0] == "Student has overdue loans"
    book_dao.remove(output_create_book.id)
    student_dao.remove(output_create_student.id)
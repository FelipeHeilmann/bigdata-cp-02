from src.application.usecases.borrow_book import BorrowBook, Input as InputBorrowBook
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.application.usecases.create_student import CreateStudent, Input as InputCreateStudent 
from src.application.usecases.get_book_by_isbn import GetBookByISBN
from src.application.usecases.get_loan import GetLoan
from src.infra.dao.book_dao_memory import BookDaoMemory
from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.infra.dao.loan_dao_memory import LoanDaoMemory
from datetime import datetime
import pytest

book_dao = BookDaoMemory()
student_dao = StudentDaoMemory()
loan_dao = LoanDaoMemory()

def test_borrow_book_should_borrow_book_successfully():
    create_book = CreateBook(book_dao)
    input_create_book = InputCreateBook(
        "9783161484100",
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
        enrollment_id="ENR551026",
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
    assert output_get_loan.book.isbn == "9783161484100"
    assert output_get_loan.book.title == "Clean architecture"
    assert output_get_loan.student.enrollment_id == "ENR551026"
    assert output_get_loan.student.name == "John Doe"
    assert output_get_loan.date == "2024-06-01T10:25:10"
    assert output_get_loan.status == "active"
    get_book = GetBookByISBN(book_dao)
    output_get_book = get_book.execute("9783161484100")
    assert output_get_book.copies == 5
    assert output_get_book.available_copies == 4
    book_dao.remove(output_create_book.id)

def test_borrow_book_should_throw_exception_when_book_is_not_available():
    create_book = CreateBook(book_dao)
    input = InputCreateBook(
        "9783161484100",
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
        enrollment_id="ENR551026",
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    output_create_student = create_student.execute(input_student)
    date = datetime(2024, 6, 1, 10, 25, 10)
    borrow_book = BorrowBook(loan_dao, book_dao)
    borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    with pytest.raises(Exception) as excinfo: 
        borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    assert str(excinfo.value) == "Book is not available"
    book_dao.remove(output_create_book.id)

def test_borrow_book_should_throw_excption_when_student_has_more_than_3_active_loans():
    create_book = CreateBook(book_dao)
    input1 = InputCreateBook(
        "9783161484100",
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    )
    input2 = InputCreateBook(
        "9780201616223",
        "Patterns of Enterprise Application Architecture",
        "Martin Fowler",
        "Software Engineering",
        "2002",
        2,
        2,
    )
    output_create_book1 = create_book.execute(input1)
    output_create_book2 = create_book.execute(input2)
    create_student = CreateStudent(student_dao)
    input_student = InputCreateStudent(
        name="John Doe",
        enrollment_id="ENR551026",
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    output_create_student = create_student.execute(input_student)
    date = datetime(2024, 6, 1, 10, 25, 10)
    borrow_book = BorrowBook(loan_dao, book_dao)
    borrow_book.execute(InputBorrowBook(output_create_book1.id, output_create_student.id, date))
    borrow_book.execute(InputBorrowBook("6b07813a-5332-4db8-bc48-7b6a1d10eb1d", output_create_student.id, date))
    borrow_book.execute(InputBorrowBook("09459c22-57c9-41c1-a439-58b0092eab1d", output_create_student.id, date))
    with pytest.raises(Exception) as excinfo: 
        borrow_book.execute(InputBorrowBook(output_create_book2.id, output_create_student.id, date))
    assert str(excinfo.value) == "Student has more than 3 active loans"
    book_dao.remove(output_create_book1.id)
    book_dao.remove(output_create_book2.id)

def test_borrow_book_should_throw_exception_when_book_does_not_exist():
    create_student = CreateStudent(student_dao)
    input_student = InputCreateStudent(
        name="John Doe",
        enrollment_id="ENR551026",
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    output_create_student = create_student.execute(input_student)
    date = datetime(2024, 6, 1, 10, 25, 10)
    borrow_book = BorrowBook(loan_dao, book_dao)
    with pytest.raises(Exception) as excinfo:
        borrow_book.execute(InputBorrowBook("non-existent-book-id", output_create_student.id, date))
    assert excinfo.value.args[0] == "Book not found"

def test_borrow_book_should_throw_exception_when_student_has_overdue_loans():
    create_book = CreateBook(book_dao)
    input = InputCreateBook(
        "9783161484100",
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
        enrollment_id="ENR551026",
        age=20,
        major="Computer Science",
        email="johndoe@harvard.com"
    )
    output_create_student = create_student.execute(input_student)
    date = datetime(2024, 6, 1, 10, 25, 10)
    borrow_book = BorrowBook(loan_dao, book_dao)
    borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    overdue_date = datetime(2024, 6, 11, 10, 25, 10)
    with pytest.raises(Exception) as excinfo:
        borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, overdue_date))
    assert excinfo.value.args[0] == "Student has overdue loans"
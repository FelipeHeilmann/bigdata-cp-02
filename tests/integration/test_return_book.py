from src.application.usecases.borrow_book import BorrowBook, Input as InputBorrowBook
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.application.usecases.create_student import CreateStudent, Input as InputCreateStudent 
from src.application.usecases.get_book_by_isbn import GetBookByISBN
from src.application.usecases.get_loan import GetLoan
from src.application.usecases.return_book import ReturnBook, Input as InputReturnBook
from src.application.errors.application_erros import (
    BookAlreadyReturnedError,
)
from src.infra.dao.book_dao_memory import BookDaoMemory
from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.infra.dao.loan_dao_memory import LoanDaoMemory
from datetime import datetime 
from pytest import raises

book_dao = BookDaoMemory()
student_dao = StudentDaoMemory()
loan_dao = LoanDaoMemory()

def test_return_book_should_return_book_without_fine_successfully():
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
    input_borrow_book = InputBorrowBook(output_create_book.id, output_create_student.id, date)
    output = borrow_book.execute(input_borrow_book)
    return_book = ReturnBook(loan_dao, book_dao)
    input_return_book = InputReturnBook(output.id, datetime(2024, 6, 2, 10, 25, 10))
    output_return_book = return_book.execute(input_return_book)
    get_loan = GetLoan(loan_dao, book_dao, student_dao)
    output_get_loan = get_loan.execute(output_return_book.id, datetime(2024, 6, 3, 10, 25, 10))
    assert output_get_loan.book.isbn == "9783161484100"
    assert output_get_loan.book.title == "Clean architecture"
    assert output_get_loan.student.enrollment_id == "ENR551026"
    assert output_get_loan.student.name == "John Doe"
    assert output_get_loan.date == "2024-06-01T10:25:10"
    assert output_get_loan.status == "returned"
    assert output_get_loan.return_date == "2024-06-02T10:25:10"
    assert output_get_loan.fine == 0
    get_book = GetBookByISBN(book_dao)
    output_get_book = get_book.execute("9783161484100")
    assert output_get_book.copies == 5
    assert output_get_book.available_copies == 5
    book_dao.remove(output_create_book.id)

def test_return_book_should_return_book_with_fine_successfully():
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
    input_borrow_book = InputBorrowBook(output_create_book.id, output_create_student.id, date)
    output = borrow_book.execute(input_borrow_book)
    return_book = ReturnBook(loan_dao, book_dao)
    input_return_book = InputReturnBook(output.id, datetime(2024, 6, 10, 10, 25, 10))
    output_return_book = return_book.execute(input_return_book)
    get_loan = GetLoan(loan_dao, book_dao, student_dao)
    output_get_loan = get_loan.execute(output_return_book.id, datetime(2024, 6, 11, 10, 25, 10))
    assert output_get_loan.book.isbn == "9783161484100"
    assert output_get_loan.book.title == "Clean architecture"
    assert output_get_loan.student.enrollment_id == "ENR551026"
    assert output_get_loan.student.name == "John Doe"
    assert output_get_loan.date == "2024-06-01T10:25:10"
    assert output_get_loan.status == "returned"
    assert output_get_loan.return_date == "2024-06-10T10:25:10"
    assert output_get_loan.fine == 4.0
    get_book = GetBookByISBN(book_dao)
    output_get_book = get_book.execute("9783161484100")
    assert output_get_book.copies == 5
    assert output_get_book.available_copies == 5
    book_dao.remove(output_create_book.id)

def test_return_book_should_throw_exception_when_returning_same_book_twice():
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
    input_borrow_book = InputBorrowBook(output_create_book.id, output_create_student.id, date)
    output = borrow_book.execute(input_borrow_book)
    return_book = ReturnBook(loan_dao, book_dao)
    input_return_book = InputReturnBook(output.id, datetime(2024, 6, 2, 10, 25, 10))
    return_book.execute(input_return_book)
    with raises(BookAlreadyReturnedError) as execinfo:
        return_book.execute(input_return_book)
    assert execinfo.value.args[0] == "Book has already been returned"
    book_dao.remove(output_create_book.id)

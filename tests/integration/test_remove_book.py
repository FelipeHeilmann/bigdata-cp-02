from src.application.usecases.remove_book import RemoveBook
from src.application.usecases.borrow_book import BorrowBook, Input as InputBorrowBook
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.application.usecases.create_student import CreateStudent, Input as InputCreateStudent 
from src.application.usecases.get_book_by_isbn import GetBookByISBN
from src.application.errors.application_erros import (
    BookNotFoundError,
    BookCurrentlyBorrowedError
)
from src.infra.dao.book_dao_memory import BookDaoMemory
from src.infra.dao.student_dao_memory import StudentDaoMemory
from src.infra.dao.loan_dao_memory import LoanDaoMemory
from datetime import datetime
import pytest

book_dao = BookDaoMemory()
student_dao = StudentDaoMemory()
loan_dao = LoanDaoMemory()

def test_remove_book_should_remove_book_properly():
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
    remove_book = RemoveBook(book_dao)
    remove_book.execute("9783161484100")
    get_book = GetBookByISBN(book_dao)
    with pytest.raises(BookNotFoundError) as excinfo:
        get_book.execute("9783161484100")
    assert excinfo.value.args[0] == "Book with ISBN 9783161484100 not found"
    book_dao.remove(output_create_book.id)

def test_remove_book_should_raise_error_when_book_not_found():
    remove_book = RemoveBook(book_dao)
    with pytest.raises(BookNotFoundError) as excinfo:
        remove_book.execute("9783161484100")
    assert excinfo.value.args[0] == "Book with ISBN 9783161484100 not found"

def test_remove_book_should_raise_error_when_book_is_borrowed():
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
    borrow_book.execute(InputBorrowBook(output_create_book.id, output_create_student.id, date))
    remove_book = RemoveBook(book_dao)
    with pytest.raises(BookCurrentlyBorrowedError) as excinfo:
        remove_book.execute("9783161484100")
    assert excinfo.value.args[0] == "Book with ISBN 9783161484100 is currently borrowed and cannot be deleted"
    book_dao.remove(output_create_book.id)
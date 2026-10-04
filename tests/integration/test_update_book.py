from src.infra.dao.book_dao_memory import BookDaoMemory
from src.application.usecases.update_book import UpdateBook, Input as InputUpdateBook
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.application.errors.application_erros import (
    BookNotFoundError,
    InvalidInputError
)
from src.application.usecases.get_book_by_isbn import GetBookByISBN
import pytest

book_dao = BookDaoMemory()

def test_update_book_should_update_book_properly():
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
    assert output_create_book.id is not None
    get_book_by_isbn = GetBookByISBN(book_dao)
    book = get_book_by_isbn.execute("9783161484100")
    assert book.isbn == "9783161484100"
    assert book.title == "Clean architecture"
    assert book.author == "Robert C. Martin"
    assert book.year == "2017"
    assert book.category == "Software Engineering"
    assert book.copies == 5
    assert book.available_copies == 5
    update_book = UpdateBook(book_dao)
    input_update_book = InputUpdateBook(
        "9783161484100",
        "Clean architecture updated",
        "Robert C. Martin",
        "Software Engineering",
        "2018",
        10,
        10,
    )
    update_book.execute(input_update_book)
    output_updated_book = get_book_by_isbn.execute("9783161484100")
    assert output_updated_book.isbn == "9783161484100"
    assert output_updated_book.title == "Clean architecture updated"
    assert output_updated_book.author == "Robert C. Martin"
    assert output_updated_book.year == "2018"
    assert output_updated_book.category == "Software Engineering"
    assert output_updated_book.copies == 10
    assert output_updated_book.available_copies == 10

def test_update_book_should_raise_exception_when_book_not_found():
    update_book = UpdateBook(book_dao)
    input_update_book = InputUpdateBook(
        "9783161484108",
        "Clean architecture updated",
        "Robert C. Martin",
        "Software Engineering",
        "2018",
        10,
        10,
    )
    with pytest.raises(BookNotFoundError) as excinfo:
        update_book.execute(input_update_book)
    assert excinfo.value.args[0] == "Book with ISBN 9783161484108 not found"

def test_update_book_should_throw_exception_when_input_is_invalid_with_one_field_empty():
    update_book = UpdateBook(book_dao)
    input = InputUpdateBook(
        "9783161484100",
        "",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    ) 
    with pytest.raises(InvalidInputError) as excinfo:
        update_book.execute(input)
    assert excinfo.value.args[0] == "Invalid input: All fields are required"  

def test_update_book_should_throw_exception_when_input_is_invalid_with_copies_and_available_copies_zero():
    update_book = UpdateBook(book_dao)
    input = InputUpdateBook(
        "9783161484100",
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        0,
        0,
    )
    with pytest.raises(InvalidInputError) as excinfo:
        update_book.execute(input)
    assert excinfo.value.args[0] == "Invalid input: Copies and available copies must be non-negative"

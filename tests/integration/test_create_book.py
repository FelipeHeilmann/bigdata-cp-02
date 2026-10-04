from src.infra.dao.book_dao_memory import BookDaoMemory
from src.application.usecases.create_book import CreateBook, Input
from src.application.errors.application_erros import (
    BookAlreadyExistsError, 
    InvalidInputError
)
from src.application.usecases.get_book_by_isbn import GetBookByISBN 
import pytest

book_dao = BookDaoMemory()

def test_create_book_should_create_book_properly():
    create_book = CreateBook(book_dao)
    input = Input(
        "9783161484100",
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    )
    output_create_book = create_book.execute(input)
    assert output_create_book.id is not None
    get_book_by_isbn = GetBookByISBN(book_dao)
    book = get_book_by_isbn.execute("9783161484100")
    assert book.id is not None
    assert book.isbn == "9783161484100"
    assert book.title == "Clean architecture"
    assert book.author == "Robert C. Martin"
    assert book.year == "2017"
    assert book.category == "Software Engineering"
    assert book.copies == 5
    assert book.available_copies == 5

def test_create_book_should_throw_exception_when_book_already_exists():
    create_book = CreateBook(book_dao)
    input = Input(
        "9781234567890",
        "Clean Code",
        "Robert C. Martin",
        "Software Engineering",
        "2008",
        3,
        3,
    )
    with pytest.raises(BookAlreadyExistsError) as excinfo:
        create_book.execute(input)
    assert excinfo.value.args[0] == "Book with ISBN 9781234567890 already exists"

def test_create_book_should_throw_exception_when_input_is_invalid_with_one_field_empty():
    create_book = CreateBook(book_dao)
    input = Input(
        "9783161484100",
        "",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    )
    with pytest.raises(InvalidInputError) as excinfo:
        create_book.execute(input)
    assert excinfo.value.args[0] == "Invalid input: All fields are required"

def test_create_book_should_throw_exception_when_input_is_invalid_with_all_fields_empty():
    create_book = CreateBook(book_dao)
    input = Input(
        "",
        "",
        "",
        "",
        "",
        0,
        0,
    )    
    with pytest.raises(InvalidInputError) as excinfo:
        create_book.execute(input)
    assert excinfo.value.args[0] == "Invalid input: All fields are required"

def test_create_book_should_throw_exception_when_input_is_invalid_with_copies_and_available_copies_zero():
    create_book = CreateBook(book_dao)
    input = Input(
        "9783161484100",
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        0,
        0,
    )  
    with pytest.raises(InvalidInputError) as excinfo:
        create_book.execute(input)
    assert excinfo.value.args[0] == "Invalid input: Copies and available copies must be non-negative"

def test_create_book_should_throw_exception_when_input_is_invalid_with_copies_and_available_copies_with_different_values():
    create_book = CreateBook(book_dao)
    input = Input(
        "9783161484100",
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        2,
    )
    with pytest.raises(InvalidInputError) as excinfo:
        create_book.execute(input)
    assert excinfo.value.args[0] == "Invalid input: Copies and available copies must be equal"

def test_create_book_should_throw_exception_when_input_is_invalid_with_isbn_incorrect():
    create_book = CreateBook(book_dao)
    input = Input(
        "346534",
        "Clean architecture",
        "Robert C. Martin",
        "Software Engineering",
        "2017",
        5,
        5,
    )
    with pytest.raises(InvalidInputError) as excinfo:
        create_book.execute(input)
    assert excinfo.value.args[0] == "Invalid input: ISBN must be a 13-digit number"
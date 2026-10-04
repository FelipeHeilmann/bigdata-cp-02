from src.application.errors.application_erros import (
    BookNotFoundError,
)
from src.application.usecases.get_book_by_isbn import GetBookByISBN
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.infra.dao.book_dao_mongo import BookDaoMongo
import pytest
from tests.helpers import random_isbn

book_dao = BookDaoMongo()

def test_get_book_should_return_book_by_isbn():
    isbn = random_isbn()
    create_book = CreateBook(book_dao)
    input = InputCreateBook(
        isbn,
        "Clean Code",
        "Robert C. Martin",
        "Software Engineering",
        "2008",
        3,
        3,
    )
    output_create_book = create_book.execute(input)
    try:
        get_book_by_isbn = GetBookByISBN(book_dao)
        book = get_book_by_isbn.execute(isbn)

        assert book.id is not None
        assert book.isbn == isbn
        assert book.title == "Clean Code"
        assert book.author == "Robert C. Martin"
        assert book.year == "2008"
        assert book.category == "Software Engineering"
        assert book.copies == 3
        assert book.available_copies == 3
    finally:
        book_dao.remove(output_create_book.id)

def test_get_book_should_throw_exception_when_book_not_found():
    get_book_by_isbn = GetBookByISBN(book_dao)
    with pytest.raises(BookNotFoundError) as excinfo:
        get_book_by_isbn.execute("978013235000")
    assert excinfo.value.args[0] == "Book with ISBN 978013235000 not found"

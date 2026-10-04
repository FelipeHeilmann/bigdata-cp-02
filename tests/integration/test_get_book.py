from src.infra.dao.book_dao_memory import BookDaoMemory
from src.application.usecases.get_book_by_isbn import GetBookByISBN
import pytest

book_dao = BookDaoMemory()

def test_get_book_should_return_book_by_isbn():
    get_book_by_isbn = GetBookByISBN(book_dao)
    book = get_book_by_isbn.execute("978-0132350884")
    assert book.isbn == "978-0132350884"
    assert book.title == "Clean Code"
    assert book.author == "Robert C. Martin"
    assert book.year == "2008"
    assert book.category == "Software Engineering"
    assert book.copies == 3
    assert book.available_copies == 2

def test_get_book_should_throw_exception_when_book_not_found():
    get_book_by_isbn = GetBookByISBN(book_dao)
    with pytest.raises(ValueError) as excinfo:
        get_book_by_isbn.execute("978-0132350885")  
    assert str(excinfo.value) == "Book with ISBN 978-0132350885 not found"
    
from src.infra.dao.book_dao_memory import BookDaoMemory
from src.application.usecases.remove_book import RemoveBook
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from src.application.usecases.get_book_by_isbn import GetBookByISBN
import pytest

book_dao = BookDaoMemory()

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

    create_book.execute(input)

    remove_book = RemoveBook(book_dao)
    remove_book.execute("9783161484100")

    get_book = GetBookByISBN(book_dao)
    with pytest.raises(ValueError) as excinfo:
        get_book.execute("9783161484100")
    assert excinfo.value.args[0] == "Book with ISBN 9783161484100 not found"

def test_remove_book_should_raise_error_when_book_not_found():
    remove_book = RemoveBook(book_dao)
    with pytest.raises(ValueError) as excinfo:
        remove_book.execute("9783161484100")
    assert excinfo.value.args[0] == "Book with ISBN 9783161484100 not found"
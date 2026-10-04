from src.infra.dao.book_dao_memory import BookDaoMemory
from src.application.usecases.list_books import ListBooks

book_dao = BookDaoMemory()

def test_list_books_return_list():
    list_books = ListBooks(book_dao)
    result = list_books.execute()
    assert isinstance(result, list)
    assert len(result) == 2
    first_book = result[0]
    assert first_book.isbn == "978-0132350884"
    assert first_book.title == "Clean Code"
    assert first_book.author == "Robert C. Martin"
    assert first_book.year == "2008"
    assert first_book.category == "Software Engineering"
    assert first_book.copies == 3
    assert first_book.available_copies == 2
    second_book = result[1]
    assert second_book.isbn == "978-0201616224"
    assert second_book.title == "Implementing Domain-Driven Design"
    assert second_book.author == "Vaughn Vernon"
    assert second_book.year == "2013"
    assert second_book.category == "Software Engineering"
    assert second_book.copies == 5
    assert second_book.available_copies == 5


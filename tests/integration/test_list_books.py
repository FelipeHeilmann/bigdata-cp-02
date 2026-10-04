from src.infra.dao.book_dao_mongo import BookDaoMongo
from src.application.usecases.list_books import ListBooks
from src.application.usecases.create_book import CreateBook, Input as InputCreateBook
from tests.helpers import random_isbn

book_dao = BookDaoMongo()

def test_list_books_return_list():
    isbn1 = random_isbn()
    isbn2 = random_isbn()
    create_book = CreateBook(book_dao)
    output1 = create_book.execute(InputCreateBook(
        isbn1,
        "Clean Code",
        "Robert C. Martin",
        "Software Engineering",
        "2008",
        3,
        3,
    ))
    output2 = create_book.execute(InputCreateBook(
        isbn2,
        "Implementing Domain-Driven Design",
        "Vaughn Vernon",
        "Software Engineering",
        "2013",
        5,
        5,
    ))
    result = ListBooks(book_dao).execute()
    assert isinstance(result, list)
    first_book = next(b for b in result if b.isbn == isbn1)
    second_book = next(b for b in result if b.isbn == isbn2)
    assert first_book.id is not None
    assert first_book.isbn == isbn1
    assert first_book.title == "Clean Code"
    assert first_book.author == "Robert C. Martin"
    assert first_book.year == "2008"
    assert first_book.category == "Software Engineering"
    assert first_book.copies == 3
    assert first_book.available_copies == 3
    assert second_book.id is not None
    assert second_book.isbn == isbn2
    assert second_book.title == "Implementing Domain-Driven Design"
    assert second_book.author == "Vaughn Vernon"
    assert second_book.year == "2013"
    assert second_book.category == "Software Engineering"
    assert second_book.copies == 5
    assert second_book.available_copies == 5
    book_dao.remove(output1.id)
    book_dao.remove(output2.id)

from src.application.dao.book_dao import BookDAO
from src.application.models.book import Book

class BookDaoMemory(BookDAO):
    def __init__(self: "BookDaoMemory") -> None:
        self.books = [
            Book(
                isbn="9781234567890",
                title="Clean Code",
                author="Robert C. Martin",
                year="2008",
                category="Software Engineering",
                copies=3,
                available_copies=2
            ),
            Book(
                isbn="9780201616224",
                title="Implementing Domain-Driven Design",
                author="Vaughn Vernon",
                year="2013",
                category="Software Engineering",
                copies=5,
                available_copies=5
            )
        ]

    def list_books(self: "BookDaoMemory") -> list[Book]:
        return self.books
    
    def get_book_by_isbn(self: "BookDaoMemory", isbn: str) -> Book | None:
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def save(self: "BookDaoMemory", book: Book) -> None:
        self.books.append(book)
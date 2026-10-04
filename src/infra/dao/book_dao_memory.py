from src.application.dao.book_dao import BookDao
from src.application.models.book import Book
from typing import List

class BookDaoMemory(BookDao):
    def __init__(self: "BookDaoMemory") -> None:
        self.books: List[Book] = [
            Book(
                id="09459c22-57c9-41c1-a439-58b0092eab1d",
                isbn="9781234567890",
                title="Clean Code",
                author="Robert C. Martin",
                year="2008",
                category="Software Engineering",
                copies=3,
                available_copies=2
            ),
            Book(
                id="6b07813a-5332-4db8-bc48-7b6a1d10eb1d",
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
    
    def get_by_isbn(self: "BookDaoMemory", isbn: str) -> Book | None:
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def get_by_id(self: "BookDaoMemory", id: str) -> Book | None:
        for book in self.books:
            if book.id == id:
                return book
        return None
    
    def save(self: "BookDaoMemory", book: Book) -> None:
        self.books.append(book)

    def update(self: "BookDaoMemory", book: Book) -> None:
        for i, b in enumerate(self.books):
            if b.isbn == book.isbn:
                self.books[i] = book
                return
            
    def remove(self: "BookDaoMemory", id: str) -> None:
        self.books = [b for b in self.books if b.id != id]

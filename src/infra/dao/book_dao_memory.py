from src.application.dao.book_dao import BookDao
from src.application.models.book import Book
from typing import List

class BookDaoMemory(BookDao): # pragma: nocover
    def __init__(self: "BookDaoMemory") -> None:
        self.books: List[Book] = []

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

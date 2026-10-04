from __future__ import annotations
from src.application.dao.book_dao import BookDao
from dataclasses import dataclass

class GetBookByISBN:
    def __init__(self: "GetBookByISBN", book_dao: "BookDao") -> None:
        self.book_dao = book_dao

    def execute(self, isbn: str) -> "Output":
        book = self.book_dao.get_book_by_isbn(isbn)
        if book is None: raise ValueError(f"Book with ISBN {isbn} not found")
        return Output(
            id=book.get_id(),
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            year=book.year,
            category=book.category,
            copies=book.copies,
            available_copies=book.available_copies
        )
    
@dataclass 
class Output:
    id: str
    isbn: str
    title: str
    author: str
    year: str
    category: str
    copies: int
    available_copies: int

    

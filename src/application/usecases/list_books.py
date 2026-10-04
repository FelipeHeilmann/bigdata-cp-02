from __future__ import annotations
from dataclasses import dataclass
from typing import List
from src.application.dao.book_dao import BookDao

class ListBooks:
    def __init__(self: "ListBooks", book_dao: "BookDao") -> None:
        self.book_dao = book_dao

    def execute(self: "ListBooks") -> List[Output]:
        books = self.book_dao.list_books()
        return [Output(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            year=book.year,
            category=book.category,
            copies=book.copies,
            available_copies=book.available_copies
        ) for book in books]
    

@dataclass 
class Output:
    isbn: str
    title: str
    author: str
    year: str
    category: str
    copies: int
    available_copies: int

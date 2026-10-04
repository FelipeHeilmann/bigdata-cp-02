from __future__ import annotations
from dataclasses import dataclass
from src.application.dao.book_dao import BookDAO

class UpdateBook:
    def __init__(self: "UpdateBook", book_dao: "BookDAO") -> None:
        self.book_dao = book_dao

    def execute(self: "UpdateBook", input: Input) -> None:
        self._validate_input(input)
        book = self.book_dao.get_book_by_isbn(input.isbn)
        if not book: raise KeyError(f"Book with ISBN {input.isbn} not found")
        book.title = input.title
        book.author = input.author
        book.year = input.year
        book.category = input.category
        book.copies = input.copies
        book.available_copies = input.available_copies
        self.book_dao.update(book)

    def _validate_input(self: "UpdateBook", input: Input) -> None:
        if not input.isbn or not input.title or not input.author or not input.year or not input.category or input.copies < 0 or input.available_copies < 0:
            raise ValueError("Invalid input: All fields are required")
        if input.copies == 0 and input.available_copies == 0:
            raise ValueError("Invalid input: Copies and available copies must be non-negative")


@dataclass
class Input:
    isbn: str
    title: str
    author: str
    category: str
    year: str
    copies: int
    available_copies: int
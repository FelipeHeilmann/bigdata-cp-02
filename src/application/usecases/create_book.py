from __future__ import annotations
from src.application.dao.book_dao import BookDao
from src.application.models.book import Book
from dataclasses import dataclass
from uuid import uuid4
from src.application.errors.application_erros import (
    InvalidInputError,
    BookAlreadyExistsError
)

class CreateBook:
    def __init__(self: "CreateBook", book_dao: "BookDao") -> None:
        self.book_dao = book_dao

    def execute(self: "CreateBook", input: Input) -> Output:
        self._validate_input(input)
        book_exists = self.book_dao.get_by_isbn(input.isbn)
        if book_exists: raise BookAlreadyExistsError("ISBN", input.isbn)
        book = Book(
            id=str(uuid4()),
            isbn=input.isbn,
            title=input.title,
            author=input.author,
            year=input.year,
            category=input.category,
            copies=input.copies,
            available_copies=input.available_copies
        )
        self.book_dao.save(book)
        return Output(id=book.id, isbn=book.isbn)
    
    def _validate_input(self: "CreateBook", input: Input) -> None:
        if not input.isbn or not input.title or not input.author or not input.year or not input.category:
            raise InvalidInputError("Invalid input: All fields are required")
        if input.copies <= 0 or input.available_copies <= 0:
            raise InvalidInputError("Invalid input: Copies and available copies must be non-negative")
        if input.available_copies != input.copies:
            raise InvalidInputError("Invalid input: Copies and available copies must be equal")
        if len(input.isbn) != 13 or not input.isbn.isdigit():
            raise InvalidInputError("Invalid input: ISBN must be a 13-digit number")

@dataclass
class Input:
    isbn: str
    title: str
    author: str
    category: str
    year: str
    copies: int
    available_copies: int

@dataclass
class Output:
    id: str
    isbn: str

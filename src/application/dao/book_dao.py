from abc import ABC, abstractmethod
from typing import List
from src.application.models.book import Book

class BookDAO(ABC):
    @abstractmethod
    def list_books(self: "BookDAO") -> List[Book]:
        pass

    @abstractmethod
    def get_book_by_isbn(self: "BookDAO", isbn: str) -> Book | None:
        pass

    @abstractmethod
    def save(self: "BookDAO", book: Book) -> None:
        pass
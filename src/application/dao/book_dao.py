from abc import ABC, abstractmethod
from typing import List
from src.application.models.book import Book

class BookDao(ABC):
    @abstractmethod
    def list_books(self: "BookDao") -> List[Book]:
        pass

    @abstractmethod
    def get_by_isbn(self: "BookDao", isbn: str) -> Book | None:
        pass

    @abstractmethod
    def get_by_id(self: "BookDao", id: str) -> Book | None:
        pass

    @abstractmethod
    def save(self: "BookDao", book: Book) -> None:
        pass

    @abstractmethod
    def update(self: "BookDao", book: Book) -> None:
        pass

    @abstractmethod
    def remove(self: "BookDao", book: Book) -> None:
        pass
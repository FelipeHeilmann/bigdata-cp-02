from dataclasses import dataclass
from uuid import uuid4

@dataclass
class Book:
    __id: str
    isbn: str
    title: str
    author: str
    year: str
    category: str
    copies: int
    available_copies: int

    def __init__(self: "Book", isbn: str, title: str, author: str, year: str, category: str, copies: int, available_copies: int) -> None:
        self.__id = str(uuid4())
        self.isbn = isbn   
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.copies = copies
        self.available_copies = available_copies

    def get_id(self: "Book") -> str:
        return self.__id
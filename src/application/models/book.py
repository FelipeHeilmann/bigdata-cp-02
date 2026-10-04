from dataclasses import dataclass

@dataclass
class Book:
    id: str
    isbn: str
    title: str
    author: str
    year: str
    category: str
    copies: int
    available_copies: int

    def __init__(self: "Book", id: str, isbn: str, title: str, author: str, year: str, category: str, copies: int, available_copies: int) -> None:
        self.id = id
        self.isbn = isbn   
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.copies = copies
        self.available_copies = available_copies

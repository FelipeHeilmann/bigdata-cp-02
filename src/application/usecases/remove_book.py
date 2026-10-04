from src.application.dao.book_dao import BookDao
from src.application.errors.application_erros import BookNotFoundError, BookCurrentlyBorrowedError

class RemoveBook:
    def __init__(self: "RemoveBook", book_dao: BookDao) -> None:
        self.book_dao = book_dao

    def execute(self: "RemoveBook", isbn: str) -> None:
        book = self.book_dao.get_by_isbn(isbn)
        if book and book.available_copies < book.copies: raise BookCurrentlyBorrowedError("ISBN", isbn)
        if not book: raise BookNotFoundError("ISBN", isbn)
        self.book_dao.remove(book.id)
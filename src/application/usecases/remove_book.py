from src.application.dao.book_dao import BookDao

class RemoveBook:
    def __init__(self: "RemoveBook", book_dao: BookDao) -> None:
        self.book_dao = book_dao

    def execute(self: "RemoveBook", isbn: str) -> None:
        book = self.book_dao.get_book_by_isbn(isbn)
        if not book: raise ValueError(f"Book with ISBN {isbn} not found")
        self.book_dao.remove(book)
from pymongo import MongoClient
from src.application.dao.book_dao import BookDao
from src.application.models.book import Book

MONGO_URI = "mongodb://user:ZHNhZGFkYWRhc2Rh@localhost:27017/?authSource=admin"
DATABASE_NAME = "library"

class BookDaoMongo(BookDao):
    def __init__(self: "BookDaoMongo") -> None:
        client = MongoClient(MONGO_URI)
        self.collection = client[DATABASE_NAME]["books"]

    def list_books(self: "BookDaoMongo") -> list[Book]:
        return [self._to_model(doc) for doc in self.collection.find()]

    def get_by_isbn(self: "BookDaoMongo", isbn: str) -> Book | None:
        doc = self.collection.find_one({"isbn": isbn})
        return self._to_model(doc) if doc else None

    def get_by_id(self: "BookDaoMongo", id: str) -> Book | None:
        doc = self.collection.find_one({"_id": id})
        return self._to_model(doc) if doc else None

    def save(self: "BookDaoMongo", book: Book) -> None:
        self.collection.insert_one(self._to_document(book))

    def update(self: "BookDaoMongo", book: Book) -> None:
        self.collection.replace_one({"_id": book.id}, self._to_document(book))

    def remove(self: "BookDaoMongo", id: str) -> None:
        self.collection.delete_one({"_id": id})

    @staticmethod
    def _to_document(book: Book) -> dict:
        return {
            "_id": book.id,
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "copies": book.copies,
            "available_copies": book.available_copies
        }

    @staticmethod
    def _to_model(doc: dict) -> Book:
        return Book(
            id=doc["_id"],
            isbn=doc["isbn"],
            title=doc["title"],
            author=doc["author"],
            year=doc["year"],
            category=doc["category"],
            copies=doc["copies"],
            available_copies=doc["available_copies"]
        )

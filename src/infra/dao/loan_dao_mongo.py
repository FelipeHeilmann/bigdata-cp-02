from pymongo import MongoClient
from src.infra.config import MONGO_DATABASE, MONGO_URI
from src.application.dao.loan_dao import LoanDao
from src.application.models.loan import Loan
from datetime import datetime, timedelta
from typing import List


class LoanDaoMongo(LoanDao):
    def __init__(self: "LoanDaoMongo") -> None:
        client = MongoClient(MONGO_URI)
        self.collection = client[MONGO_DATABASE]["loans"]

    def get_by_id(self: "LoanDao", id: str) -> Loan | None:
        doc = self.collection.find_one({"_id": id})
        return self._to_model(doc) if doc else None

    def save(self: "LoanDao", loan: Loan) -> None:
        self.collection.insert_one(self._to_document(loan))

    def list_loans(self: "LoanDaoMongo") -> List[Loan]:
        return [self._to_model(doc) for doc in self.collection.find()]

    def get_active_loans_by_student_id(self: "LoanDao", student_id: str, date: datetime) -> List[Loan]:
        docs = self.collection.find({
            "student_id": student_id,
            "return_date": {"$exists": False}
        })
        return [self._to_model(doc) for doc in docs]
    
    def get_overdue_loans_by_student_id(self: "LoanDao", student_id: str, date: datetime) -> List[Loan]:
        docs = self.collection.find({
            "student_id": student_id,
            "return_date": {"$exists": False},
            "date": {"$lt": date - timedelta(days=7)}
        })
        return [self._to_model(doc) for doc in docs]
    
    def update(self: "LoanDao", loan: Loan) -> None:
        self.collection.replace_one({"_id": loan.id}, self._to_document(loan))

    @staticmethod
    def _to_document(loan: Loan) -> dict:
        doc = {
            "_id": loan.id,
            "student_id": loan.student_id,
            "book_id": loan.book_id,
            "date": loan.date,
            "fine": loan.fine
        }
        if loan.return_date is not None:
            doc["return_date"] = loan.return_date
        return doc
    
    @staticmethod
    def _to_model(doc: dict) -> Loan:
        return Loan(
            id=doc["_id"],
            student_id=doc["student_id"],
            book_id=doc["book_id"],
            date=doc["date"],
            return_date=doc.get("return_date"),
            fine=doc.get("fine", 0.0)
        )
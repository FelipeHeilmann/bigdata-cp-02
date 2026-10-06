from pymongo import MongoClient
from src.infra.config import MONGO_DATABASE, MONGO_URI
from src.application.dao.report_dao import ReportDao, BorrowedBook, LoansByMajor, OverdueLoan
from datetime import datetime, timedelta
from typing import List

DAY_IN_MS = 24 * 60 * 60 * 1000
LOAN_PERIOD_DAYS = 7


class ReportDaoMongo(ReportDao):
    def __init__(self: "ReportDaoMongo") -> None:
        client = MongoClient(MONGO_URI)
        self.loans = client[MONGO_DATABASE]["loans"]

    def most_borrowed_books(self: "ReportDaoMongo", limit: int) -> List[BorrowedBook]:
        pipeline = [
            {"$group": {"_id": "$book_id", "loans": {"$sum": 1}}},
            {"$sort": {"loans": -1, "_id": 1}},
            {"$limit": limit},
            {"$lookup": {"from": "books", "localField": "_id", "foreignField": "_id", "as": "book"}},
            {"$unwind": {"path": "$book", "preserveNullAndEmptyArrays": True}},
            {"$project": {"_id": 0, "book_id": "$_id", "title": {"$ifNull": ["$book.title", None]}, "loans": 1}},
        ]
        return [BorrowedBook(**doc) for doc in self.loans.aggregate(pipeline)]

    def loans_by_major(self: "ReportDaoMongo") -> List[LoansByMajor]:
        pipeline = [
            {"$lookup": {"from": "students", "localField": "student_id", "foreignField": "_id", "as": "student"}},
            {"$unwind": "$student"},
            {"$group": {"_id": "$student.major", "loans": {"$sum": 1}}},
            {"$sort": {"loans": -1, "_id": 1}},
            {"$project": {"_id": 0, "major": "$_id", "loans": 1}},
        ]
        return [LoansByMajor(**doc) for doc in self.loans.aggregate(pipeline)]

    def overdue_loans(self: "ReportDaoMongo", date: datetime) -> List[OverdueLoan]:
        due_date = {"$add": ["$date", LOAN_PERIOD_DAYS * DAY_IN_MS]}
        pipeline = [
            {"$match": {"return_date": {"$exists": False}, "date": {"$lt": date - timedelta(days=LOAN_PERIOD_DAYS)}}},
            {"$lookup": {"from": "students", "localField": "student_id", "foreignField": "_id", "as": "student"}},
            {"$unwind": "$student"},
            {"$lookup": {"from": "books", "localField": "book_id", "foreignField": "_id", "as": "book"}},
            {"$unwind": "$book"},
            {"$project": {
                "_id": 0,
                "loan_id": "$_id",
                "student_name": "$student.name",
                "book_title": "$book.title",
                "days_late": {"$toInt": {"$floor": {"$divide": [{"$subtract": [date, due_date]}, DAY_IN_MS]}}},
            }},
            {"$sort": {"days_late": -1, "student_name": 1}},
        ]
        return [OverdueLoan(**doc) for doc in self.loans.aggregate(pipeline)]

    def total_fines(self: "ReportDaoMongo") -> float:
        pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$fine"}}},
        ]
        result = list(self.loans.aggregate(pipeline))
        return float(result[0]["total"]) if result else 0.0

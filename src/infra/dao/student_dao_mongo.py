from pymongo import MongoClient
from src.application.dao.student_dao import StudentDao
from src.application.models.student import Student

MONGO_URI = "mongodb://user:ZHNhZGFkYWRhc2Rh@localhost:27017/?authSource=admin"
DATABASE_NAME = "library"

class StudentDaoMongo(StudentDao):
    def __init__(self: "StudentDaoMongo") -> None:
        client = MongoClient(MONGO_URI)
        self.collection = client[DATABASE_NAME]["students"]

    def get_by_id(self: "StudentDaoMongo", id: str) -> Student | None:
        doc = self.collection.find_one({"_id": id})
        return self._to_model(doc) if doc else None

    def save(self: "StudentDaoMongo", student: Student) -> None:
        self.collection.insert_one(self._to_document(student))

    def get_by_enrollment_id(self: "StudentDaoMongo", enrollment_id: str) -> Student | None:
        doc = self.collection.find_one({"enrollment_id": enrollment_id})
        return self._to_model(doc) if doc else None

    def remove(self: "StudentDaoMongo", id: str) -> None:
        self.collection.delete_one({"_id": id})

    @staticmethod
    def _to_document(student: Student) -> dict:
        return {
            "_id": student.id,
            "name": student.name,
            "email": student.email,
            "enrollment_id": student.enrollment_id,
            "major": student.major,
            "age": student.age
        }

    @staticmethod
    def _to_model(doc: dict) -> Student:
        return Student(
            id=doc["_id"],
            name=doc["name"],
            email=doc["email"],
            enrollment_id=doc["enrollment_id"],
            major=doc["major"],
            age=doc["age"]
        )
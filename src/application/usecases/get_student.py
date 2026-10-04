from __future__ import annotations
from dataclasses import dataclass
from src.application.dao.student_dao import StudentDao
from src.application.errors.application_erros import StudentNotFoundError

class GetStudent:
    def __init__(self: "GetStudent", student_dao: StudentDao) -> None:
        self.student_dao = student_dao

    def execute(self: "GetStudent", enrollment_id: str) -> Output:
        student = self.student_dao.get_by_enrollment_id(enrollment_id)
        if not student: raise StudentNotFoundError("enrollment id", enrollment_id)
        return Output(
            id=student.id,
            name=student.name,
            age=student.age,
            major=student.major,
            email=student.email,
            enrollment_id=student.enrollment_id
        )

@dataclass
class Output:
    id: str
    name: str
    age: int
    major: str
    email: str
    enrollment_id: str

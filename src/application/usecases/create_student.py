from __future__ import annotations
from dataclasses import dataclass
from src.application.models.student import Student
from src.application.dao.student_dao import StudentDao
from uuid import uuid4

class CreateStudent:
    def __init__(self: "CreateStudent", student_dao: StudentDao) -> None:
        self.student_dao = student_dao

    def execute(self: "CreateStudent", input: Input) -> Output:
        student = Student(
            id=str(uuid4()),
            name=input.name,
            enrollment_id=input.enrollment_id,
            age=input.age,
            major=input.major,
            email=input.email
        )
        self.student_dao.save(student)
        return Output(id=student.id, enrollment_id=student.enrollment_id)

@dataclass
class Input:
    name: str
    enrollment_id: str
    age: int
    major: str
    email: str

@dataclass
class Output:
    id: str
    enrollment_id: str
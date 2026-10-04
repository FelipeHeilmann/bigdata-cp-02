from __future__ import annotations
from dataclasses import dataclass
from src.application.models.student import Student
from src.application.dao.student_dao import StudentDao
from src.application.errors.application_erros import (
    StudentAlreadyExistsError,
    InvalidInputError
)
from uuid import uuid4

class CreateStudent:
    def __init__(self: "CreateStudent", student_dao: StudentDao) -> None:
        self.student_dao = student_dao

    def execute(self: "CreateStudent", input: Input) -> Output:
        existing_student = self.student_dao.get_by_enrollment_id(input.enrollment_id)
        if existing_student: raise StudentAlreadyExistsError("enrollment id", input.enrollment_id)
        self._validate_email(input.email)
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
    
    def _validate_email(self: "CreateStudent", email: str) -> None:
        if "@" not in email or "." not in email.split("@")[-1]:
            raise InvalidInputError("Invalid email address")

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
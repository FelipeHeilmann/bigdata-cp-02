from src.application.dao.student_dao import StudentDao
from src.application.models.student import Student
from typing import List

class StudentDaoMemory(StudentDao): # pragma: nocover
    def __init__(self: "StudentDaoMemory") -> None:
        self.students: List[Student] = []

    def save(self: "StudentDaoMemory", student) -> None:
        self.students.append(student)

    def get_by_enrollment_id(self: "StudentDaoMemory", enrollment_id: str):
        for student in self.students:
            if student.enrollment_id == enrollment_id:
                return student
        return None
    
    def get_by_id(self: "StudentDaoMemory", id: str) -> Student | None:
        for student in self.students:
            if student.id == id:
                return student
        return None
    
    def remove(self: "StudentDaoMemory", id: str) -> None:
        self.students = [student for student in self.students if student.id != id]
from src.application.dao.student_dao import StudentDao
from src.application.models.student import Student

class StudentDaoMemory(StudentDao):
    def __init__(self: "StudentDaoMemory") -> None:
        self.students = [
            Student(
                name="Anthony Smith",
                age=27,
                major="Logistics",
                email="anthonysmith@harvard.com",
                enrollment_id="ENR557596"
            ),
            Student(
                name="Emily Johnson",
                age=22,
                major="Finance",
                email="emilyjohnson@harvard.com",
                enrollment_id="ENR557597"
            )
        ]

    def save(self: "StudentDaoMemory", student) -> None:
        self.students.append(student)

    def get_by_enrollment_id(self: "StudentDaoMemory", enrollment_id: str):
        for student in self.students:
            if student.enrollment_id == enrollment_id:
                return student
        return None
    
    def get_by_id(self: "StudentDaoMemory", id: str) -> Student | None:
        for student in self.students:
            if student.get_id() == id:
                return student
        return None
from dataclasses import dataclass

@dataclass
class Student:
    id: str
    name: str
    age: int
    major: str
    email: str
    enrollment_id: str

    def __init__(self: "Student", id: str, enrollment_id: str, name: str, age: int, major: str, email: str) -> None:
        self.id = id
        self.name = name
        self.age = age
        self.major = major
        self.email = email
        self.enrollment_id = enrollment_id
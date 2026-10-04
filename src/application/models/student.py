from dataclasses import dataclass
from uuid import uuid4

@dataclass
class Student:
    __id: str
    name: str
    age: int
    major: str
    email: str
    enrollment_id: str

    def __init__(self: "Student", enrollment_id: str, name: str, age: int, major: str, email: str) -> None:
        self.__id = str(uuid4())
        self.name = name
        self.age = age
        self.major = major
        self.email = email
        self.enrollment_id = enrollment_id

    def get_id(self: "Student") -> str:
        return self.__id

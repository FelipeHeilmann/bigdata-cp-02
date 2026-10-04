from abc import ABC, abstractmethod
from src.application.models.student import Student

class StudentDao(ABC):
    @abstractmethod
    def save(self: "StudentDao", student: Student) -> None:
        pass

    @abstractmethod
    def get_by_enrollment_id(self: "StudentDao", enrollment_id: str) -> Student | None:
        pass

    @abstractmethod
    def get_by_id(self: "StudentDao", id: str) -> Student | None:
        pass

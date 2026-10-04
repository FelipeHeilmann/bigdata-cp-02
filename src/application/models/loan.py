from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

@dataclass
class Loan:
    __id: str
    book_id: str
    student_id: str
    date: datetime
    return_date: datetime = None

    def __init__(self: "Loan", book_id: str, student_id: str, date: datetime):
        self.__id = str(uuid4())
        self.book_id = book_id
        self.student_id = student_id
        self.date = date
        self.return_date = None

    def get_id(self: "Loan") -> str:
        return self.__id

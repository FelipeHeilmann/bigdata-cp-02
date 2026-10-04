from dataclasses import dataclass
from datetime import datetime

@dataclass
class Loan:
    id: str
    book_id: str
    student_id: str
    date: datetime
    return_date: datetime = None

    def __init__(self: "Loan", id:str, book_id: str, student_id: str, date: datetime):
        self.id = id
        self.book_id = book_id
        self.student_id = student_id
        self.date = date
        self.return_date = None
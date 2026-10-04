from dataclasses import dataclass
from datetime import datetime

@dataclass
class Loan:
    id: str
    book_id: str
    student_id: str
    date: datetime
    return_date: datetime = None
    fine: float = 0.0

    def __init__(self: "Loan", id:str, book_id: str, student_id: str, date: datetime, return_date: datetime = None, fine: float = 0.0):
        self.id = id
        self.book_id = book_id
        self.student_id = student_id
        self.date = date
        self.return_date = return_date
        self.fine = fine
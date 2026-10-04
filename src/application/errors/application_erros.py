class InvalidInputError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BookCurrentlyBorrowedError(Exception):
    def __init__(self, field: str, value: str):
        self.message = f"Book with {field} {value} is currently borrowed and cannot be deleted"
        super().__init__(self.message)

class BookAlreadyReturnedError(Exception):
    def __init__(self):
        self.message = "Book has already been returned"
        super().__init__(self.message)

class BookNotAvailableError(Exception):
    def __init__(self):
        self.message = "Book is not available"
        super().__init__(self.message)

class BookNotFoundError(Exception):
    def __init__(self, field: str, value: str):
        self.message = f"Book with {field} {value} not found"
        super().__init__(self.message)

class BookAlreadyExistsError(Exception):
    def __init__(self, field: str, value: str):
        self.message = f"Book with {field} {value} already exists"
        super().__init__(self.message)

class StudentNotFoundError(Exception):
    def __init__(self, field: str, value: str):
        self.message = f"Student with {field} {value} not found"
        super().__init__(self.message)

class StudentHasMoreThanThreeActiveLoansError(Exception):
    def __init__(self):
        self.message = "Student has more than 3 active loans"
        super().__init__(self.message)

class StudentHasOverdueLoansError(Exception):
    def __init__(self):
        self.message = "Student has overdue loans"
        super().__init__(self.message)

class ApplicationError(Exception):
    pass

class InvalidInputError(ApplicationError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BookCurrentlyBorrowedError(ApplicationError):
    def __init__(self, field: str, value: str):
        self.message = f"Book with {field} {value} is currently borrowed and cannot be deleted"
        super().__init__(self.message)

class BookAlreadyReturnedError(ApplicationError):
    def __init__(self):
        self.message = "Book has already been returned"
        super().__init__(self.message)

class BookNotAvailableError(ApplicationError):
    def __init__(self):
        self.message = "Book is not available"
        super().__init__(self.message)

class BookNotFoundError(ApplicationError):
    def __init__(self, field: str, value: str):
        self.message = f"Book with {field} {value} not found"
        super().__init__(self.message)

class BookAlreadyExistsError(ApplicationError):
    def __init__(self, field: str, value: str):
        self.message = f"Book with {field} {value} already exists"
        super().__init__(self.message)

class StudentNotFoundError(ApplicationError):
    def __init__(self, field: str, value: str):
        self.message = f"Student with {field} {value} not found"
        super().__init__(self.message)

class StudentHasMoreThanThreeActiveLoansError(ApplicationError):
    def __init__(self):
        self.message = "Student has more than 3 active loans"
        super().__init__(self.message)

class StudentHasOverdueLoansError(ApplicationError):
    def __init__(self):
        self.message = "Student has overdue loans"
        super().__init__(self.message)

class StudentAlreadyExistsError(ApplicationError):
    def __init__(self, field: str, value: str):
        self.message = f"Student with {field} {value} already exists"
        super().__init__(self.message)

class LoanNotFoundError(ApplicationError):
    def __init__(self, id: str):
        self.message = f"Loan with id {id} not found"
        super().__init__(self.message)

from datetime import datetime
from src.application.usecases.create_book import CreateBook, Input as CreateBookInput
from src.application.usecases.list_books import ListBooks
from src.application.usecases.get_book_by_isbn import GetBookByISBN
from src.application.usecases.update_book import UpdateBook, Input as UpdateBookInput
from src.application.usecases.remove_book import RemoveBook
from src.application.usecases.create_student import CreateStudent, Input as CreateStudentInput
from src.application.usecases.get_student import GetStudent
from src.application.usecases.borrow_book import BorrowBook, Input as BorrowBookInput
from src.application.usecases.return_book import ReturnBook, Input as ReturnBookInput
from src.cli.prompts import ask_text, ask_int

def create_book(book_dao) -> None:
    isbn = ask_text("ISBN (13 dígitos)")
    title = ask_text("Título")
    author = ask_text("Autor")
    category = ask_text("Categoria")
    year = ask_text("Ano")
    copies = ask_int("Exemplares", min_value=1)
    output = CreateBook(book_dao).execute(CreateBookInput(
        isbn=isbn, title=title, author=author, category=category, year=year,
        copies=copies, available_copies=copies,
    ))
    print(f"Livro cadastrado com id {output.id}.")

def list_books(book_dao) -> None:
    books = ListBooks(book_dao).execute()
    if not books:
        print("Nenhum livro cadastrado.")
        return
    for book in books:
        print_book(book)

def get_book(book_dao) -> None:
    isbn = ask_text("ISBN")
    print_book(GetBookByISBN(book_dao).execute(isbn))

def update_book(book_dao) -> None:
    isbn = ask_text("ISBN do livro")
    title = ask_text("Novo título")
    author = ask_text("Novo autor")
    category = ask_text("Nova categoria")
    year = ask_text("Novo ano")
    copies = ask_int("Exemplares")
    available_copies = ask_int("Exemplares disponíveis")
    UpdateBook(book_dao).execute(UpdateBookInput(
        isbn=isbn, title=title, author=author, category=category, year=year,
        copies=copies, available_copies=available_copies,
    ))
    print("Livro atualizado.")

def remove_book(book_dao) -> None:
    isbn = ask_text("ISBN do livro")
    RemoveBook(book_dao).execute(isbn)
    print("Livro removido.")

def create_student(student_dao) -> None:
    name = ask_text("Nome")
    enrollment_id = ask_text("Matrícula")
    age = ask_int("Idade")
    major = ask_text("Curso")
    email = ask_text("E-mail")
    output = CreateStudent(student_dao).execute(CreateStudentInput(
        name=name, enrollment_id=enrollment_id, age=age, major=major, email=email,
    ))
    print(f"Estudante cadastrado com id {output.id}.")

def get_student(student_dao) -> None:
    enrollment_id = ask_text("Matrícula")
    student = GetStudent(student_dao).execute(enrollment_id)
    print(f"Id: {student.id}")
    print(f"Nome: {student.name}")
    print(f"Matrícula: {student.enrollment_id}")
    print(f"Idade: {student.age}")
    print(f"Curso: {student.major}")
    print(f"E-mail: {student.email}")

def borrow_book(book_dao, student_dao, loan_dao) -> None:
    books = ListBooks(book_dao).execute()
    if not books:
        print("Nenhum livro cadastrado.")
        return
    for book in books:
        print_book(book)
    isbn = ask_text("ISBN do livro")
    enrollment_id = ask_text("Matrícula do estudante")
    book = GetBookByISBN(book_dao).execute(isbn)
    student = GetStudent(student_dao).execute(enrollment_id)
    output = BorrowBook(loan_dao, book_dao).execute(BorrowBookInput(
        book_id=book.id, student_id=student.id, date=datetime.now(),
    ))
    print(f"Empréstimo realizado. ID do empréstimo: {output.id}")

def return_book(book_dao, student_dao, loan_dao) -> None:
    open_loans = [loan for loan in loan_dao.list_loans() if loan.return_date is None]
    if not open_loans:
        print("Nenhum empréstimo em aberto.")
        return
    for loan in open_loans:
        book = book_dao.get_by_id(loan.book_id)
        student = student_dao.get_by_id(loan.student_id)
        book_info = f"{book.title} (ISBN {book.isbn})" if book else "(livro não encontrado)"
        student_info = f"{student.name} (matrícula {student.enrollment_id})" if student else "(aluno não encontrado)"
        print(f"- ID: {loan.id}")
        print(f"  Livro: {book_info}")
        print(f"  Aluno: {student_info}")
        print(f"  Emprestado em: {loan.date:%d/%m/%Y %H:%M}")
    loan_id = ask_text("ID do empréstimo")
    output = ReturnBook(loan_dao, book_dao).execute(ReturnBookInput(
        loan_id=loan_id, return_date=datetime.now(),
    ))
    print(f"Livro devolvido. Multa: R$ {output.fine:.2f}")

def print_book(book) -> None:
    print(f"- {book.title} | {book.author} ({book.year}) | ISBN {book.isbn} | "
          f"disponíveis {book.available_copies}/{book.copies}")

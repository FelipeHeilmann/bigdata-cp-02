from src.cli import commands
from src.cli.error_handler import handle_errors
from src.infra.dao.book_dao_mongo import BookDaoMongo
from src.infra.dao.loan_dao_mongo import LoanDaoMongo
from src.infra.dao.student_dao_mongo import StudentDaoMongo
from src.infra.dao.report_dao_mongo import ReportDaoMongo

def build_menu(book_dao, student_dao, loan_dao, report_dao) -> dict:
    return {
        "1": ("Criar livro", handle_errors(lambda: commands.create_book(book_dao))),
        "2": ("Listar livros", handle_errors(lambda: commands.list_books(book_dao))),
        "3": ("Buscar livro", handle_errors(lambda: commands.get_book(book_dao))),
        "4": ("Atualizar livro", handle_errors(lambda: commands.update_book(book_dao))),
        "5": ("Remover livro", handle_errors(lambda: commands.remove_book(book_dao))),
        "6": ("Criar estudante", handle_errors(lambda: commands.create_student(student_dao))),
        "7": ("Buscar estudante", handle_errors(lambda: commands.get_student(student_dao))),
        "8": ("Emprestar livro", handle_errors(lambda: commands.borrow_book(book_dao, student_dao, loan_dao))),
        "9": ("Devolver livro", handle_errors(lambda: commands.return_book(book_dao, student_dao, loan_dao))),
        "10": ("Relatórios", handle_errors(lambda: commands.reports(report_dao))),
    }

def main() -> None:
    menu = build_menu(BookDaoMongo(), StudentDaoMongo(), LoanDaoMongo(), ReportDaoMongo())
    try:
        while True:
            print("\n=== Biblioteca ===")
            for key, (label, _) in menu.items():
                print(f"{key}. {label}")
            print("0. Sair")
            choice = input("Escolha uma opção: ").strip()
            if choice == "0":
                print("Até logo!")
                return
            if choice not in menu:
                print("Opção inválida.")
                continue
            menu[choice][1]()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando.")

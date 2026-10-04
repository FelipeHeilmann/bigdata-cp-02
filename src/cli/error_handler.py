import functools
from pymongo.errors import PyMongoError
from src.application.errors.application_erros import ApplicationError

def handle_errors(action):
    @functools.wraps(action)
    def wrapper(*args, **kwargs):
        try:
            return action(*args, **kwargs)
        except ApplicationError as error:
            print(f"\nErro: {error.message}")
        except PyMongoError:
            print("\nErro: não foi possível acessar o MongoDB. Verifique se o container está rodando (docker compose up -d).")
        except Exception as error:
            print(f"\nErro inesperado: {error}")
    return wrapper

from datetime import datetime

def ask_text(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("Este campo é obrigatório.")

def ask_int(label: str, min_value: int = 0) -> int:
    while True:
        raw = input(f"{label}: ").strip()
        try:
            value = int(raw)
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if value < min_value:
            print(f"O valor deve ser maior ou igual a {min_value}.")
            continue
        return value

def ask_datetime(label: str) -> datetime:
    while True:
        raw = input(f"{label} (formato AAAA-MM-DD HH:MM, ex.: 2024-06-01 10:30): ").strip()
        try:
            return datetime.strptime(raw, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Data inválida. Use o formato AAAA-MM-DD HH:MM, por exemplo 2024-06-01 10:30.")

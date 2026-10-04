import random

def random_isbn() -> str:
    digits = "978" + "".join(random.choices("0123456789", k=9))
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
    check_digit = (10 - total % 10) % 10
    return digits + str(check_digit)

def random_enrollment_id() -> str:
    return f"ENR{random.randint(100000, 999999)}"

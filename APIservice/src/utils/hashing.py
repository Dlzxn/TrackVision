from passlib.context import CryptContext


crypto_context = CryptContext(
    schemes=['argon2'],
    deprecated='auto',
    argon2__time_cost=2,
    argon2__memory_cost=102400,
    argon2__parallelism=8,
    argon2__hash_len=32
)


def hash_password(password: str) -> str:
    return crypto_context.hash(password)

from .crypto_context import crypto_context


def hash_password(password: str) -> str:
    return crypto_context.hash(password)

from fastapi import status
from fastapi.exceptions import HTTPException

from dishka.integrations.fastapi import FromDishka, inject
from src.domain.interfaces.user_repository import AbstractUserRepository
from src.api.models.user import User
from src.utils.crypto_context import crypto_context


async def verify_password(password: str, hashed_password: str) -> bool:
    return crypto_context.verify(password, hashed_password)


async def authenticate_user(
    username: str, password: str, repo: AbstractUserRepository
) -> None | User:

    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )

    user = await repo.get_by_name(username)

    if user is None:
        return None

    if not await verify_password(password, user.password):
        return None

    return User(username=user.name, email=user.email)

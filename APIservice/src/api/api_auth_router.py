from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from dishka.integrations.fastapi import FromDishka, inject

from src.api.models.user import UserRegistration
from src.domain.interfaces.user_repository import AbstractUserRepository
from src.domain.models.user import User as DomainUser
from src.utils.hashing import hash_password
from src.core.security import authenticate_user
from src.core.aceess_token import create_access_token


auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
@inject
async def register(
    user_reg: UserRegistration, repo: FromDishka[AbstractUserRepository]
):

    existing_user = await repo.get_by_name(user_reg.username) or \
                    await repo.get_by_email(user_reg.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким именем или email уже существует",
        )

    new_user = DomainUser(
        id=None,
        name=user_reg.username,
        email=user_reg.email,
        password=hash_password(user_reg.password),
        tg_id=None,
        tg_username=None,
    )

    await repo.create(new_user)

    return {
        "message": "Регистрация успешна",
        "redirect": "/ui/login",
        "user": user_reg.username,
    }


@auth_router.post("/token")
@inject
async def login(
    repo: FromDishka[AbstractUserRepository],
    response: Response,
    user_form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await authenticate_user(
        username=user_form_data.username, password=user_form_data.password, repo=repo
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )

    access_token = create_access_token(data={"sub": user.username, "email": user.email})

    response.set_cookie(
        key="access_token", value=access_token, max_age=432000, httponly=True
    )

    return {
        "message": "Авторизация успешна",
        "redirect": "/",
        "user": {"username": user.username},
    }


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Успешный выход из системы", "redirect": "/ui/login"}

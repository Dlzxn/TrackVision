from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from src.api.models.user import UserRegistration
from src.domain.interfaces.user_repository import AbstractUserRepository
from src.domain.models.user import User as DomainUser
from src.infrastructure.repositories.user_repo import SQLAlchemyUserRepository
from src.utils.get_env import get_db_url
from src.utils.hashing import hash_password


auth_router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
@inject
async def register(
    user_reg: UserRegistration,
    repo: FromDishka[AbstractUserRepository]
    ):

    existing_email = await repo.get_by_email(user_reg.email)

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'is_registered': False,
                'message': 'Пользователь с таким email уже существует'
            }
        )
    
    
    existing_name = await repo.get_by_name(user_reg.username)

    if existing_name is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'is_registered': False,
                'message': 'Пользователь с таким именем уже существует'
            }
        )


    new_user = DomainUser(
        id=None,
        name=user_reg.username,
        email=user_reg.email,
        password=hash_password(user_reg.password),
        tg_id=None,
        tg_username=None
        
    )
    
    await repo.create(new_user)

    return {
        'detail': {
            'is_registered': True,
            'message': 'Пользователь успешно зарегистрирован'
            }
        }
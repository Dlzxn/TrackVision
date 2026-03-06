import os

import jwt

from typing import Annotated

from fastapi import Depends, Cookie, status
from fastapi.exceptions import HTTPException

from .models.token import TokenData


async def get_current_user(access_token: str = Cookie(default=None)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if access_token is None:
        raise exception

    try:
        payload = jwt.decode(
            access_token.encode('utf-8'),
            os.getenv("JWT_SECRET_KEY").encode('utf-8'),
            algorithms=[os.getenv("JWT_ALGORITHM")],
        )
        username, email = payload.get("sub"), payload.get('email')

        if username is None:
            raise exception

        token_data = TokenData(username=username, email=email)

    except jwt.exceptions.ExpiredSignatureError:
        raise exception

    except jwt.exceptions.InvalidTokenError:
        raise exception

    return token_data


async def get_active_current_user(current_user: Annotated[TokenData, Depends(get_current_user)]):
    return current_user
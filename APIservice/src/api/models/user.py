from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegistration(BaseModel):
    username: Annotated[str, Field(..., min_lenght=3, max_length=20)]
    email: EmailStr
    password: Annotated[str, Field(..., min_lenght=6)]

    @field_validator('username')
    @classmethod
    def validate_username(cls, username):
        if not username.isalnum():
            raise ValueError('Имя пользователя должно содержать тольку буквы и цифры')
        return username

    @field_validator('password')
    @classmethod
    def validate_password(cls, password):
        if len(password) < 6:
            return ValueError('Длина пароля должна быть неменее 6 символов')
        return password

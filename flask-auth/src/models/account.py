from pydantic import BaseModel, EmailStr, Field, validator
from utils.exceptions import AccountSignupException


class SignupRequest(BaseModel):
    login: str = Field(..., title="Логин")
    email: EmailStr = Field(..., title="Почта")
    password: str = Field(..., title="Пароль")

    @validator("login")
    def login_alphanumeric(cls, v):
        if not v.isalnum():
            raise AccountSignupException(
                error_message="Логин может содержать только числа и буквенные символы."
            )
        return v

    @validator("password")
    def password_length(cls, v):
        if len(v) < 6:
            raise AccountSignupException(
                error_message="Пароль не удовлетворяет требованиям безопасности. "
                "Длина пароля должна содежать не менее 6 и не более 72 символов."
            )
        return v


class UserDataResponse(BaseModel):
    login: str = Field(..., title="Логин")
    email: EmailStr = Field(..., title="Почта")


class AuthUserDataResponse(BaseModel):
    refresh_token: None | str = Field(..., title="")
    access_token: None | str = Field(..., title="")


class SigninRequest(BaseModel):
    login: str = Field(..., title="Логин")
    password: str = Field(..., title="Пароль")

from pydantic import BaseModel, EmailStr, validator
from pydantic import Field

from utils.exceptions import AccountSignupException, AccountPasswordChangeException


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
        if not (6 <= len(v) <= 72):
            raise AccountSignupException(
                error_message="Пароль не удовлетворяет требованиям безопасности. "
                "Длина пароля должна содержать не менее 6 и не более 72 символов."
            )
        return v


class AuthUserDataResponse(BaseModel):
    refresh_token: str = Field(..., title="Refresh токен")
    access_token: str = Field(..., title="Access токен")


class SigninRequest(BaseModel):
    login: str = Field(..., title="Логин")
    password: str = Field(..., title="Пароль")


class PasswordChangeRequest(BaseModel):
    old_password: str = Field(..., title="Старый пароль")
    new_password: str = Field(..., title="Новый пароль")

    @validator("new_password")
    def password_length(cls, v):
        if not (6 <= len(v) <= 72):
            raise AccountPasswordChangeException(
                error_message="Пароль не удовлетворяет требованиям безопасности. "
                "Длина пароля должна содержать не менее 6 и не более 72 символов."
            )
        return v
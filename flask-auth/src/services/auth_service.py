from functools import lru_cache

from flask import current_app, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from user_agents import parse

from db import alchemy
from db.models.user import User
from db.token_storage_adapter import TokenStorageAdapter, TokenStatus
from db.token_storage_adapter import get_redis_adapter
from utils.exceptions import (
    AccountRefreshException,
    AccountSigninException,
    AccountSignupException,
    AccountPasswordChangeException,
)


class AuthService:
    def __init__(self, token_storage_adapter: TokenStorageAdapter):
        self.token_storage = token_storage_adapter

    @staticmethod
    def get_user_agent_info():
        user_agent = parse(request.user_agent.string)
        return str(user_agent)

    def create_jwt_tokens(self, user_id: str, device_info: str) -> dict:
        identity = {"id": user_id, "device_info": device_info}

        access_token = create_access_token(identity=identity)
        self.token_storage.create(
            user_id,
            get_jti(access_token),
            current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        )

        refresh_token = create_refresh_token(identity=identity)
        self.token_storage.create(
            user_id,
            get_jti(refresh_token),
            current_app.config["JWT_REFRESH_TOKEN_EXPIRES"],
        )

        return dict(access_token=access_token, refresh_token=refresh_token)

    # TODO: логирование ручки на действие
    def signup(
        self,
        login: str,
        email: str,
        password: str,
    ) -> dict:
        if User.query.filter_by(login=login).first():
            raise AccountSignupException(
                error_message="Пользователь с таким логином уже существует."
            )

        if User.query.filter_by(email=email).first():
            raise AccountSignupException(
                error_message="Пользователь с такой почтой уже существует."
            )

        user = User(login=login, email=email, password=password, is_admin=False)

        alchemy.session.add(user)
        alchemy.session.commit()

        return user.to_dict()

    # TODO: логирование ручки на действие
    def signin(
        self,
        login: str,
        password: str,
    ) -> dict:
        user = User.query.filter_by(login=login).one_or_none()

        if user and user.verify_password(password):
            device_info = self.get_user_agent_info()
            return self.create_jwt_tokens(user_id=str(user.id), device_info=device_info)

        raise AccountSigninException(error_message="Неверный логин или пароль.")

    def refresh(self, user_id: str, device_info: str, refresh_jti: str) -> dict:
        status = self.token_storage.get_status(user_id, refresh_jti)
        if status == TokenStatus.NOT_FOUND:
            raise AccountRefreshException(error_message="Истек срок действия refresh токена.")
        elif status == TokenStatus.BLOCKED:
            raise AccountRefreshException(error_message="Данный refresh токен более не валиден.")
        elif status == TokenStatus.ACTIVE:
            self.token_storage.block(user_id, refresh_jti)

        return self.create_jwt_tokens(user_id=user_id, device_info=device_info)

    # TODO: логирование ручки на действие
    def password_change(
        self,
        user: User,
        access_jti: str,
        old_password: str,
        new_password: str,
    ):
        status = self.token_storage.get_status(user.id, access_jti)
        if status == TokenStatus.NOT_FOUND:
            raise AccountPasswordChangeException(error_message="Истек срок действия access токена.")
        elif status == TokenStatus.BLOCKED:
            raise AccountPasswordChangeException(
                error_message="Данный access токен более не валиден."
            )

        if user.verify_password(old_password):
            user.password = new_password
            alchemy.session.commit()
        else:
            raise AccountPasswordChangeException(error_message="Старый пароль введен неверно")


@lru_cache()
def get_auth_service(token_storage_adapter: TokenStorageAdapter = get_redis_adapter()):
    return AuthService(token_storage_adapter=token_storage_adapter)

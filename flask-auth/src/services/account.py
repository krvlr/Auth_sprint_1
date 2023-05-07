from functools import lru_cache
from uuid import UUID

from db import alchemy
from db.base_cache import CacheAdapter
from db.cache_adapter import get_redis_adapter
from db.models.user import User
from flask import current_app, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from user_agents import parse
from utils.exceptions import AccountSigninException, AccountSignupException


class AuthService:
    def __init__(self, cache_adapter: CacheAdapter):
        self.cache_adapter = cache_adapter

    @staticmethod
    def get_user_agent_info():
        user_agent = parse(request.user_agent.string)
        device_info = str(user_agent)
        return device_info

    def create_jwt_tokens(self, user_id: UUID, device_info: str) -> dict:
        identity = {"id": user_id, "device_info": device_info}

        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        cache_key_access_token = self.cache_adapter.generate_key(
            user_id, get_jti(access_token)
        )
        self.cache_adapter.setex(
            cache_key=cache_key_access_token,
            value="active",
            delta_expire=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        )
        cache_key_refresh_token = self.cache_adapter.generate_key(
            user_id, get_jti(refresh_token)
        )
        self.cache_adapter.setex(
            cache_key=cache_key_refresh_token,
            value="active",
            delta_expire=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"],
        )

        jwt_tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return jwt_tokens

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
            jwt_tokens = self.create_jwt_tokens(
                user_id=user.id, device_info=device_info
            )
            return jwt_tokens

        raise AccountSigninException(error_message="Неверный логин или пароль.")


@lru_cache()
def get_auth_service(cache_adapter: CacheAdapter = get_redis_adapter()):
    auth_service = AuthService(cache_adapter=cache_adapter)
    return auth_service

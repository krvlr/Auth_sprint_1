from db import alchemy
from db.models.refresh_jwt import RereshJWT
from db.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from models.account import AuthUserDataResponse, UserDataResponse
from utils.exceptions import AccountSigninException, AccountSignupException


class AuthService:
    @staticmethod
    def signup(
        login: str,
        email: str,
        password: str,
    ) -> UserDataResponse:
        if User.query.filter_by(login=login).first():
            raise AccountSignupException(
                error_message="Пользователь с таким логином уже существует."
            )

        if User.query.filter_by(email=email).first():
            raise AccountSignupException(
                error_message="Пользователь с такой почтой уже существует."
            )

        user = User(
            login=login,
            email=email,
            password=password,
        )

        alchemy.session.add(user)
        alchemy.session.commit()

        return UserDataResponse(**user.to_dict())

    @staticmethod
    def signin(
        login: str,
        password: str,
    ) -> AuthUserDataResponse:
        user = User.query.filter_by(login=login).one_or_none()

        if user and user.verify_password(password):
            # TODO: Необходимо логирование входа
            access_token = create_access_token(identity=user.to_dict())
            refresh_token = create_refresh_token(identity=user.to_dict())

            refresh_jwt = RereshJWT(
                refresh_jti=get_jti(refresh_token),
            )

            alchemy.session.add(refresh_jwt)
            alchemy.session.commit()

            jwt_tokens = {"access_token": access_token, "refresh_token": refresh_token}

            return AuthUserDataResponse(**jwt_tokens)

        raise AccountSigninException(error_message="Неверный логин или пароль.")

from db import alchemy
from db.models.user import User
from utils.exceptions import AccountSignupException


def signup(
    login: str,
    email: str,
    password: str,
) -> dict:
    if User.query.filter((User.login == login) | (User.email == email)).first():
        raise AccountSignupException(error_message="Пользователь уже существует")

    user = User(
        login=login,
        email=email,
        password=password,
    )
    alchemy.session.add(user)
    alchemy.session.commit()

    return user.to_dict()

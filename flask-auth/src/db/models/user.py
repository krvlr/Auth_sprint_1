import uuid

from db import alchemy
from flask_bcrypt import check_password_hash, generate_password_hash
from sqlalchemy import UUID, Column, String


class User(alchemy.Model):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Идентификатор пользователя",
    )
    login = Column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
        comment="Логин пользователя",
    )
    email = Column(
        String(320), nullable=False, comment="Адрес электронной почты пользователя"
    )
    password_hash = Column(
        String(128), nullable=False, comment="Хэш пароля пользователя"
    )

    def __repr__(self):
        return f"<User: {self.login}>"

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password).decode("utf8")

    def verify_password(self, password=None):
        if not password:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return dict(id=self.id, login=self.login, email=self.email)


# TODO add login_history
# TODO add roles
# TODO add jwts

import uuid
from datetime import datetime

from db import alchemy
from flask_bcrypt import check_password_hash, generate_password_hash
from sqlalchemy import UUID, Boolean, Column, DateTime, String


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
    created = Column(
        DateTime(),
        nullable=False,
        default=datetime.utcnow(),
        comment="Время создания записи",
    )
    modified = Column(
        DateTime(),
        nullable=True,
        comment="Время изменения записи",
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
    is_active = Column(
        Boolean, nullable=False, default=True, comment="Признак активного пользователя"
    )
    is_verified = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Признак верефицированного пользователя",
    )
    is_admin = Column(Boolean, nullable=False, comment="Признак администратора")

    def __repr__(self):
        return f"<User: {self.login}>"

    @property
    def password(self):
        raise AttributeError("Пароль не является читаемым атрибутом")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password).decode("utf8")

    def verify_password(self, password=None):
        if not password:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return dict(
            id=self.id,
            created=self.created,
            modified=self.modified,
            login=self.login,
            email=self.email,
            is_active=self.is_active,
            is_verified=self.is_verified,
            is_admin=self.is_admin,
        )

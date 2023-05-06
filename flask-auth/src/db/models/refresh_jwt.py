import uuid
from datetime import datetime

from db import alchemy
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String

from .user import User


class RereshJWT(alchemy.Model):
    __tablename__ = "refresh_jwt"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Идентификатор refresh jwt токена",
    )
    created = Column(
        DateTime(),
        nullable=False,
        default=datetime.utcnow(),
        comment="Время создания записи",
    )
    refresh_jti = Column(String(36), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"))

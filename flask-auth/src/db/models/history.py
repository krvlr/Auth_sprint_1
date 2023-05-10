import uuid

from db import alchemy
from db.models import User
from sqlalchemy import UUID, Column, DateTime, func


class UserActionsHistory(alchemy.Model):
    __tablename__ = "user_actions_history"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Идентификатор записи",
    )
    user_id = Column(
        UUID(as_uuid=True),
        alchemy.ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False,
        comment="Идентификатор пользователя",
    )
    action = Column(
        alchemy.String(255),
        nullable=False,
        comment="Действие пользователя",
    )
    ip = Column(
        alchemy.String(45),
        nullable=False,
        comment="IP пользователя",
    )
    device_info = Column(
        alchemy.String(255),
        primary_key=False,
        comment="Информация о устройстве",
    )
    created = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="Время создания записи",
    )

    def __repr__(self):
        return f"<UserActionsHistory: (User: {self.user_id}, {self.action}, {self.created}>"

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            action=self.action,
            ip=self.ip,
            device_info=self.device_info,
            created=self.created,
        )

import abc
from abc import ABCMeta
from datetime import timedelta
from enum import Enum
from functools import lru_cache

from redis import Redis
from typing import Any, Union

from core.config import redis_settings
from db.token_storage_provider import TokenStorageRedisProvider, TokenStorageProvider


class TokenStatus(Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    NOT_FOUND = None


class TokenStorageAdapter(metaclass=ABCMeta):
    @abc.abstractmethod
    def __init__(self, token_storage_provider: TokenStorageProvider):
        self.token_storage_provider = token_storage_provider

    @abc.abstractmethod
    def create(self, user_id: str, jti: str, delta_expire: Union[int, timedelta]):
        pass

    @abc.abstractmethod
    def get_status(self, user_id: str, jti: str) -> TokenStatus:
        pass

    @abc.abstractmethod
    def block(self, user_id: str, jti: str):
        pass

    @abc.abstractmethod
    def block_for_pattern(self, user_id: str, jti: str, pattern: str):
        pass


class TokenStorageRedisAdapter(TokenStorageAdapter):
    def __init__(self, token_storage_provider: TokenStorageProvider):
        self.token_storage_provider = token_storage_provider

    @staticmethod
    def _generate_key(user_id: str, jti: str):
        return f"{user_id}:{jti}"

    def create(self, user_id: str, jti: str, delta_expire: Union[int, timedelta]):
        self.token_storage_provider.set(
            key=self._generate_key(user_id, jti),
            value=TokenStatus.ACTIVE.value,
            delta_expire=delta_expire,
        )

    def get_status(self, user_id: str, jti: str) -> TokenStatus:
        return TokenStatus(self.token_storage_provider.get(key=f"{user_id}:{jti}"))

    def block(self, user_id: str, jti: str):
        self.token_storage_provider.update(
            key=self._generate_key(user_id, jti),
            value=TokenStatus.BLOCKED.value,
        )

    def block_for_pattern(self, user_id: str, jti: str, pattern: str):
        for key in self.token_storage_provider.search(pattern=pattern):
            self.token_storage_provider.update(
                key=key,
                value=TokenStatus.BLOCKED.value,
            )


@lru_cache()
def get_redis_adapter() -> TokenStorageRedisAdapter:
    redis = Redis(host=redis_settings.host, port=redis_settings.port)
    redis_provider = TokenStorageRedisProvider(redis=redis)
    redis_adapter = TokenStorageRedisAdapter(token_storage_provider=redis_provider)
    return redis_adapter

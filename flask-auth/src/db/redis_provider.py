from datetime import timedelta
from typing import Any, Optional, Union

from db.base_cache import CacheProvider
from redis import Redis


class RedisProvider(CacheProvider):
    def __init__(self, redis: Redis):
        self.redis = redis

    def get(self, name: str) -> Any:
        value = self.redis.get(name=name)
        if value:
            return value.decode()

    def setex(self, name: str, value: Any, delta_expire: Union[int, timedelta]):
        self.redis.setex(name=name, time=delta_expire, value=value)

    def get_ttl(self, name: str):
        return self.redis.ttl(name=name)

    def search(self, pattern: str):
        return self.redis.scan_iter(match=pattern)

from datetime import timedelta
from functools import lru_cache
from typing import Any, Union

from core.config import redis_settings
from db.base_cache import CacheAdapter, CacheProvider
from db.redis_provider import RedisProvider
from redis import Redis


class RedisAdapter(CacheAdapter):
    def __init__(self, cache_provider: CacheProvider):
        self.cache_provider = cache_provider

    @staticmethod
    def generate_key(user_id: str, jti: str) -> str:
        cache_key = f"{user_id}:{jti}"
        return cache_key

    def get(self, cache_key: str):
        return self.cache_provider.get(name=cache_key)

    def setex(self, cache_key: str, value: Any, delta_expire: Union[int, timedelta]):
        self.cache_provider.setex(
            name=cache_key, value=value, delta_expire=delta_expire
        )

    def change(self, cache_key: str, value: Any):
        ttl = self.cache_provider.get_ttl(name=cache_key)
        if ttl:
            self.setex(cache_key=cache_key, value=value, delta_expire=ttl)

    def change_for_pattern(self, pattern: str, value: Any):
        for cache_key in self.cache_provider.search(pattern=pattern):
            self.change(cache_key=cache_key, value=value)


@lru_cache()
def get_redis_adapter() -> RedisAdapter:
    redis = Redis(host=redis_settings.host, port=redis_settings.port)
    redis_provider = RedisProvider(redis=redis)
    redis_adapter = RedisAdapter(cache_provider=redis_provider)
    return redis_adapter

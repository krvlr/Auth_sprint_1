import abc
from abc import ABCMeta
from datetime import timedelta
from typing import Any, Callable, Union


class CacheProvider(metaclass=ABCMeta):
    @abc.abstractmethod
    def get(self, key: str):
        pass

    @abc.abstractmethod
    def set(self, key: str, value: Any, delta_expire: Union[int, timedelta]):
        pass

    @abc.abstractmethod
    def update(self, key: str, value: Any):
        pass

    @abc.abstractmethod
    def search(self, pattern: str):
        pass


class CacheAdapter(metaclass=ABCMeta):
    @abc.abstractmethod
    def __init__(self, cache_provider: CacheProvider):
        self.cache_provider = cache_provider

    @staticmethod
    @abc.abstractmethod
    def generate_key(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get(self, cache_key: str):
        pass

    @abc.abstractmethod
    def set(self, cache_key: str, value: Any, delta_expire: Union[int, timedelta]):
        pass

    @abc.abstractmethod
    def update(self, cache_key: str, value: Any):
        pass

    @abc.abstractmethod
    def update_for_pattern(self, pattern: str, value: Any):
        pass

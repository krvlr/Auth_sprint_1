import abc
from abc import ABCMeta
from datetime import timedelta
from typing import Any, Callable, Union


class CacheProvider(metaclass=ABCMeta):
    @abc.abstractmethod
    def get(self, name: str) -> Any:
        """Метод для получения данных по ключу."""
        pass

    @abc.abstractmethod
    def setex(self, name: str, value: Any, delta_expire: Union[int, timedelta]):
        """
        Метод для сохранения данных
        с ограничением времени жизни.
        """
        pass

    @abc.abstractmethod
    def get_ttl(self, name: str):
        """
        Метод для получения установленного ранее
        ограничения времени жизни.
        """
        pass

    @abc.abstractmethod
    def search(self, pattern: str):
        """Метод для получения ключей по шаблону."""
        pass


class CacheAdapter(metaclass=ABCMeta):
    @abc.abstractmethod
    def __init__(self, cache_provider: CacheProvider):
        self.cache_provider = cache_provider

    @abc.abstractmethod
    def generate_key(self, *args, **kwargs):
        """Метод для генерации ключа."""
        pass

    @abc.abstractmethod
    def get(self, cache_key: str):
        """Метод для получения данных из кэша."""
        pass

    @abc.abstractmethod
    def setex(self, cache_key: str, value: Any, delta_expire: Union[int, timedelta]):
        """
        Метод для сохранения данных
        с ограничением времени жизни в кэш.
        """
        pass

    @abc.abstractmethod
    def change(self, cache_key: str, value: Any):
        """
        Метод для изменения значения в кэше
        с учетом его ограничения времени жизни.
        """
        pass

    @abc.abstractmethod
    def change_for_pattern(self, pattern: str, value: Any):
        """
        Метод для изменения значений в кэше
        с учетом их ограничения времени жизни.
        """
        pass

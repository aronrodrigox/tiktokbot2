from __future__ import annotations

import asyncio
import logging
from typing import Any

from functools import lru_cache


class SimpleCache:
    """Простой кэш для URL видео"""
    
    def __init__(self, max_size: int = 100) -> None:
        self._cache: dict[str, str] = {}
        self._max_size = max_size
        self._logger = logging.getLogger(__name__)

    def get(self, key: str) -> str | None:
        """Получить значение из кэша"""
        return self._cache.get(key)

    def set(self, key: str, value: str) -> None:
        """Сохранить значение в кэш"""
        if len(self._cache) >= self._max_size:
            # Удаляем самый старый элемент
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[key] = value
        self._logger.debug("Кэширован URL для %s", key)

    def clear(self) -> None:
        """Очистить кэш"""
        self._cache.clear()
        self._logger.info("Кэш очищен")
    
    def get_stats(self) -> dict[str, int]:
        """Получить статистику кэша"""
        return {
            "size": len(self._cache),
            "max_size": self._max_size
        }


# Глобальный экземпляр кэша
video_cache = SimpleCache(max_size=50)

from __future__ import annotations

import asyncio
import logging
from typing import Any

from app.services.providers.base import VideoProvider


class MultiProviderResolver:
    """Резолвер с приоритетом провайдеров - пробует по порядку"""
    
    def __init__(self, providers: list[VideoProvider]) -> None:
        self._providers = providers
        self._logger = logging.getLogger(__name__)

    async def get_fastest_url(self, tiktok_url: str) -> str:
        """Пробует провайдеров по порядку, возвращает первый успешный"""
        if not self._providers:
            raise ValueError("Нет доступных провайдеров")
        
        last_error = None
        
        for i, provider in enumerate(self._providers):
            try:
                self._logger.info("Пробуем провайдер %d/%d", i + 1, len(self._providers))
                result = await provider.get_download_url(tiktok_url)
                self._logger.info("Провайдер %d успешно вернул URL", i + 1)
                return result
            except Exception as e:
                self._logger.warning("Провайдер %d не сработал: %s", i + 1, str(e))
                last_error = e
                continue
        
        # Если все провайдеры не сработали
        if last_error:
            raise last_error
        else:
            raise ValueError("Все провайдеры не сработали")

    async def aclose(self) -> None:
        """Закрытие всех провайдеров"""
        for provider in self._providers:
            try:
                await provider.aclose()
            except Exception as e:
                self._logger.warning("Ошибка при закрытии провайдера: %s", e)

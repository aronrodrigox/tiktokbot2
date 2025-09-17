from __future__ import annotations

import asyncio
import logging
from typing import Any

from app.services.providers.base import VideoProvider


class StubProvider(VideoProvider):
    """Заглушка для скачивания видео - возвращает ошибку"""
    
    def __init__(self, timeout_sec: float = 10.0) -> None:
        self._timeout_sec = timeout_sec
        self._logger = logging.getLogger(__name__)

    async def get_download_url(self, tiktok_url: str) -> str:
        """Заглушка - всегда возвращает ошибку"""
        self._logger.info("StubProvider: попытка скачать %s", tiktok_url)
        
        # Имитируем задержку
        await asyncio.sleep(1.0)
        
        raise ValueError("🔧 Сервис временно недоступен. Ищем стабильный API...")

    async def aclose(self) -> None:
        """Закрытие ресурсов"""
        pass

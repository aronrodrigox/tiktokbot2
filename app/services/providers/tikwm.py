from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from app.services.providers.base import VideoProvider
from app.services.cache import video_cache


class TikwmProvider(VideoProvider):
    """Провайдер для TikWM API - резервный"""
    
    def __init__(self, timeout_sec: float = 15.0) -> None:
        self._timeout_sec = timeout_sec
        self._logger = logging.getLogger(__name__)
        self._base_url = "https://www.tikwm.com/api"

    async def get_download_url(self, tiktok_url: str) -> str:
        """Получает URL видео через TikWM API"""
        self._logger.info("TikwmProvider: попытка скачать %s", tiktok_url)
        
        # Проверяем кэш
        cached_url = video_cache.get(tiktok_url)
        if cached_url:
            self._logger.info("TikwmProvider: найден в кэше")
            return cached_url
        
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.tikwm.com/",
        }
        
        params = {
            "url": tiktok_url,
            "hd": "1",  # Запрашиваем HD качество
        }
        
        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(self._timeout_sec),
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
            ) as client:
                response = await client.get(
                    self._base_url,
                    headers=headers,
                    params=params,
                    follow_redirects=True
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Ищем видео без водяного знака
                if isinstance(data, dict):
                    # Проверяем разные возможные ключи
                    video_url = (
                        data.get("data", {}).get("play") or
                        data.get("play") or
                        data.get("data", {}).get("video") or
                        data.get("video") or
                        data.get("data", {}).get("url") or
                        data.get("url")
                    )
                    
                    if isinstance(video_url, str) and video_url.startswith("http"):
                        self._logger.info("TikwmProvider: успешно получен URL")
                        # Сохраняем в кэш
                        video_cache.set(tiktok_url, video_url)
                        return video_url
                
                raise ValueError("TikWM API не вернул валидный URL видео")
                
        except httpx.TimeoutException:
            raise ValueError("TikWM API: превышено время ожидания")
        except httpx.HTTPStatusError as e:
            raise ValueError(f"TikWM API: HTTP ошибка {e.response.status_code}")
        except Exception as e:
            raise ValueError(f"TikWM API: {str(e)}")

    async def aclose(self) -> None:
        """Закрытие ресурсов"""
        pass

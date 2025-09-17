from __future__ import annotations

import asyncio
import logging
import os
import tempfile
from typing import Any

from app.services.providers.base import VideoProvider


class YtDlpLocalProvider(VideoProvider):
    """Локальный провайдер через yt-dlp - независимый от API"""
    
    def __init__(self, timeout_sec: float = 30.0) -> None:
        self._timeout_sec = timeout_sec
        self._logger = logging.getLogger(__name__)

    async def get_download_url(self, tiktok_url: str) -> str:
        """Скачивает видео локально через yt-dlp"""
        self._logger.info("YtDlpLocalProvider: скачиваем %s", tiktok_url)
        
        def _download() -> str:
            import yt_dlp  # type: ignore

            # Создаем временную папку
            temp_dir = tempfile.mkdtemp(prefix="tiktok_")
            output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")
            
            ydl_opts = {
                "outtmpl": output_path,
                "format": "best[ext=mp4]/best",
                "quiet": True,
                "no_warnings": True,
                "extract_flat": False,
                "http_headers": {
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
                    ),
                    "Referer": "https://www.tiktok.com/",
                },
                "extractor_args": {
                    "tiktok": {
                        "download_api": True,
                    }
                },
                "merge_output_format": "mp4",
                "nocheckcertificate": True,
                # Оптимизации для скорости
                "socket_timeout": 10,
                "retries": 2,
                "fragment_retries": 2,
                "concurrent_fragment_downloads": 4,
                "http_chunk_size": 1048576,  # 1MB chunks
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(tiktok_url, download=True)
                    
                    # Ищем скачанный файл
                    if isinstance(info, dict):
                        filename = ydl.prepare_filename(info)
                        if isinstance(filename, str) and os.path.exists(filename):
                            self._logger.info("YtDlpLocalProvider: файл скачан: %s", filename)
                            return filename
                    
                    # Если не нашли по prepare_filename, ищем в папке
                    for file in os.listdir(temp_dir):
                        if file.endswith('.mp4'):
                            file_path = os.path.join(temp_dir, file)
                            self._logger.info("YtDlpLocalProvider: найден файл: %s", file_path)
                            return file_path
                    
                    raise ValueError("yt-dlp не смог скачать файл")
                    
            except Exception as e:
                # Очищаем папку при ошибке
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
                raise e

        try:
            return await asyncio.wait_for(
                asyncio.to_thread(_download), 
                timeout=self._timeout_sec
            )
        except asyncio.TimeoutError:
            raise ValueError("yt-dlp: превышено время ожидания")

    async def aclose(self) -> None:
        """Закрытие ресурсов"""
        pass

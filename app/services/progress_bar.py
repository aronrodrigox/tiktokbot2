from __future__ import annotations

import asyncio
import logging
from typing import Any

from aiogram.types import Message

from app.services.localization import Localization


class ProgressBar:
    """Система прогресс-бара для отображения этапов обработки"""
    
    def __init__(self, message: Message) -> None:
        self._message = message
        self._logger = logging.getLogger(__name__)
        self._current_step = 0
        self._total_steps = 0
        self._status_message: Message | None = None
        self._steps: list[str] = []
    
    async def start(self, steps: list[str]) -> None:
        """Начинает отображение прогресс-бара"""
        self._steps = steps
        self._total_steps = len(steps)
        self._current_step = 0
        
        # Отправляем начальное сообщение
        progress_text = self._get_progress_text()
        self._status_message = await self._message.reply(progress_text)
    
    async def update(self, step_index: int, custom_text: str | None = None) -> None:
        """Обновляет прогресс-бар"""
        if step_index < 0 or step_index >= self._total_steps:
            return
        
        self._current_step = step_index
        progress_text = self._get_progress_text(custom_text)
        
        if self._status_message:
            try:
                await self._status_message.edit_text(progress_text)
            except Exception as e:
                self._logger.warning("Ошибка обновления прогресс-бара: %s", e)
    
    async def complete(self, success_text: str = "✅ Готово!") -> None:
        """Завершает прогресс-бар"""
        if self._status_message:
            try:
                await self._status_message.edit_text(success_text)
                # Удаляем сообщение через 3 секунды
                await asyncio.sleep(3)
                await self._status_message.delete()
            except Exception as e:
                self._logger.warning("Ошибка завершения прогресс-бара: %s", e)
    
    async def error(self, error_text: str) -> None:
        """Показывает ошибку в прогресс-баре"""
        if self._status_message:
            try:
                await self._status_message.edit_text(f"❌ {error_text}")
                # Удаляем сообщение через 5 секунд
                await asyncio.sleep(5)
                await self._status_message.delete()
            except Exception as e:
                self._logger.warning("Ошибка отображения ошибки: %s", e)
    
    def _get_progress_text(self, custom_text: str | None = None) -> str:
        """Генерирует текст прогресс-бара"""
        if custom_text:
            current_step_text = custom_text
        else:
            current_step_text = self._steps[self._current_step] if self._current_step < len(self._steps) else ""
        
        # Создаем прогресс-бар
        progress_percent = (self._current_step + 1) / self._total_steps * 100
        filled_bars = int(progress_percent / 10)
        empty_bars = 10 - filled_bars
        
        progress_bar = "🟩" * filled_bars + "⬜" * empty_bars
        
        return (
            f"🔄 <b>Обработка видео</b>\n\n"
            f"{progress_bar} {progress_percent:.0f}%\n\n"
            f"📋 <b>Этап {self._current_step + 1}/{self._total_steps}:</b>\n"
            f"{current_step_text}"
        )


class TikTokProgressBar(ProgressBar):
    """Специализированный прогресс-бар для TikTok"""
    
    def __init__(self, message: Message, loc: Localization) -> None:
        super().__init__(message)
        self._loc = loc
        self._steps = [
            loc.get("progress_analyzing"),
            loc.get("progress_getting"), 
            loc.get("progress_downloading"),
            loc.get("progress_sending")
        ]
    
    async def _update_status(self, text: str) -> None:
        """Обновляет статусное сообщение"""
        if self._status_message:
            await self._status_message.edit_text(text)
        else:
            self._status_message = await self._message.reply(text)
    
    async def start_download(self) -> None:
        """Начинает процесс скачивания"""
        await self._update_status(self._loc.get("progress_start"))
    
    async def analyzing_url(self) -> None:
        """Этап анализа URL"""
        await self.update(0)
    
    async def getting_video(self) -> None:
        """Этап получения видео"""
        await self.update(1)
    
    async def downloading_file(self) -> None:
        """Этап скачивания файла"""
        await self.update(2)
    
    async def sending_video(self) -> None:
        """Этап отправки видео"""
        await self.update(3)
    
    async def success(self) -> None:
        """Успешное завершение"""
        await self.complete("✅ Видео успешно скачано и отправлено!")
    
    async def error_occurred(self, error_msg: str) -> None:
        """Ошибка при скачивании"""
        await self.error(f"Ошибка: {error_msg}")

from __future__ import annotations

import logging
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.services.user_storage import user_storage


class UserTrackerMiddleware(BaseMiddleware):
    """Middleware для отслеживания пользователей"""
    
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    async def __call__(self, handler, event: TelegramObject, data: dict[str, Any]):  # type: ignore[override]
        # Отслеживаем только сообщения от пользователей
        if isinstance(event, Message) and event.from_user:
            try:
                # Добавляем пользователя в хранилище
                user_storage.add_user(event.from_user)
            except Exception as e:
                self._logger.error("Ошибка добавления пользователя: %s", e)
        
        return await handler(event, data)

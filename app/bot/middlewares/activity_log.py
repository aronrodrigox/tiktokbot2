from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


@dataclass(slots=True)
class LoggingController:
    enabled: bool = True

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        return self.enabled


class ActivityLogMiddleware(BaseMiddleware):
    def __init__(self, controller: LoggingController) -> None:
        self.controller = controller
        self.logger = logging.getLogger("activity")

    async def __call__(self, handler: Callable[[TelegramObject, dict], Awaitable], event: TelegramObject, data: dict):  # type: ignore[override]
        if isinstance(event, Message) and self.controller.enabled:
            user = event.from_user
            self.logger.info(
                "msg from %s(%s): %s",
                user.username if user else None,
                user.id if user else None,
                (event.text or event.caption or "<non-text>")[:256],
            )
        return await handler(event, data)



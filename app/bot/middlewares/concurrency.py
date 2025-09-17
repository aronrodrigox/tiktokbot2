from __future__ import annotations

import asyncio
from dataclasses import dataclass

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


@dataclass(slots=True)
class ConcurrencyConfig:
    max_concurrent: int = 10


class ConcurrencyMiddleware(BaseMiddleware):
    def __init__(self, config: ConcurrencyConfig | None = None) -> None:
        cfg = config or ConcurrencyConfig()
        # Семафор ограничивает одновременную обработку апдейтов
        self._semaphore = asyncio.Semaphore(max(1, cfg.max_concurrent))

    async def __call__(self, handler, event: TelegramObject, data):  # type: ignore[override]
        async with self._semaphore:
            return await handler(event, data)



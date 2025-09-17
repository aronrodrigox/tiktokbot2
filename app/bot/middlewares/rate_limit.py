from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


@dataclass(slots=True)
class RateLimitConfig:
    max_requests: int = 3
    per_seconds: int = 60


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, config: RateLimitConfig | None = None) -> None:
        self._config = config or RateLimitConfig()
        self._user_requests: dict[int, deque[float]] = {}

    async def __call__(self, handler, event: TelegramObject, data):  # type: ignore[override]
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            now = time.monotonic()
            requests = self._user_requests.setdefault(user_id, deque())
            window_start = now - self._config.per_seconds
            while requests and requests[0] < window_start:
                requests.popleft()
            if len(requests) >= self._config.max_requests:
                await event.answer("Слишком часто. Попробуйте позже.")
                return None
            requests.append(now)

        return await handler(event, data)



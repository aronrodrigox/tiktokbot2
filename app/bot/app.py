from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from app.bot.handlers.start import router as start_router
from app.bot.handlers.tiktok import setup_tiktok_handlers
from app.bot.handlers.admin import setup_admin_handlers
from app.bot.handlers.broadcast import setup_broadcast_handlers
from app.bot.middlewares.concurrency import ConcurrencyConfig, ConcurrencyMiddleware
from app.bot.middlewares.activity_log import ActivityLogMiddleware, LoggingController
from app.bot.middlewares.user_tracker import UserTrackerMiddleware
from app.config.settings import Settings
from app.services.providers.tikwm import TikwmProvider
from app.services.providers.ytdlp_local import YtDlpLocalProvider
from app.services.providers.resolver import MultiProviderResolver


class BotApplication:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._session = AiohttpSession()
        self._bot = Bot(settings.bot_token, session=self._session)
        self._dispatcher = Dispatcher()
        self._dispatcher.message.middleware(
            ConcurrencyMiddleware(ConcurrencyConfig(max_concurrent=20))
        )
        self._log_controller = LoggingController()
        self._dispatcher.message.middleware(ActivityLogMiddleware(self._log_controller))
        self._dispatcher.message.middleware(UserTrackerMiddleware())
        providers = [
            TikwmProvider(timeout_sec=10.0),          # 1-й метод (основной)
            YtDlpLocalProvider(timeout_sec=20.0),     # 2-й метод
        ]
        self._resolver = MultiProviderResolver(providers)

        self._dispatcher.include_router(start_router)
        self._dispatcher.include_router(setup_admin_handlers(settings, self._log_controller))
        
        # Сначала создаем рассылку, чтобы получить данные
        broadcast_router, broadcast_data = setup_broadcast_handlers(settings)
        
        # Регистрируем рассылку ПЕРЕД TikTok
        self._dispatcher.include_router(broadcast_router)
        
        # Затем создаем TikTok с доступом к данным рассылки
        self._dispatcher.include_router(setup_tiktok_handlers(self._resolver, broadcast_data))

    async def run(self) -> None:
        try:
            me = await self._bot.get_me()
            logging.getLogger(__name__).info("Authenticated as @%s (id=%s)", me.username, me.id)
            logging.getLogger(__name__).info("Starting long polling...")
            await self._dispatcher.start_polling(self._bot)
        finally:
            await self._resolver.aclose()
            await self._bot.session.close()


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = Settings.from_env()
    app = BotApplication(settings)
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass



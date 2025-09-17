from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config.settings import Settings
from app.bot.middlewares.activity_log import LoggingController
from app.services.cache import video_cache
from app.services.localization import get_localization
from app.services.user_language import user_language_storage


def setup_admin_handlers(settings: Settings, controller: LoggingController) -> Router:
    router = Router()

    @router.message(Command("log"))
    async def toggle_log(message: Message) -> None:
        if message.from_user is None or message.from_user.id not in set(settings.admin_ids):
            return
        
        # Получаем язык админа
        user_language = user_language_storage.get_language(message.from_user.id)
        loc = get_localization(user_language)
        
        enabled = controller.toggle()
        await message.answer(loc.get("logs_enabled" if enabled else "logs_disabled"))

    @router.message(Command("cache"))
    async def clear_cache(message: Message) -> None:
        if message.from_user is None or message.from_user.id not in set(settings.admin_ids):
            return
        
        # Получаем язык админа
        user_language = user_language_storage.get_language(message.from_user.id)
        loc = get_localization(user_language)
        
        stats = video_cache.get_stats()
        video_cache.clear()
        await message.answer(loc.get("cache_cleared", size=stats['size'], max_size=stats['max_size']))

    return router



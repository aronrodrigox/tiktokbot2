from __future__ import annotations

import asyncio
import logging
import os
import tempfile

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from app.services.providers.resolver import MultiProviderResolver
from app.services.progress_bar import TikTokProgressBar
from app.services.localization import get_localization
from app.services.user_language import user_language_storage
from app.utils.net import expand_url_if_short
from app.utils.validators import extract_tiktok_url


def setup_tiktok_handlers(resolver: MultiProviderResolver, broadcast_data: dict = None) -> Router:
    router = Router()
    logger = logging.getLogger("activity")

    @router.message(lambda m: m.text and not m.text.startswith('/'))
    async def on_text(message: Message) -> None:
        # Проверяем, не находится ли пользователь в режиме рассылки
        if (broadcast_data and 
            message.from_user and 
            message.from_user.id in broadcast_data):
            # Если админ в режиме рассылки, игнорируем сообщение
            return
        
        # Получаем язык пользователя
        user_id = message.from_user.id if message.from_user else 0
        user_language = user_language_storage.get_language(user_id)
        loc = get_localization(user_language)
        
        text = message.text or ""
        url = extract_tiktok_url(text)
        
        if not url:
            # В группах не отвечаем на сообщения без ссылок
            if message.chat.type in ["group", "supergroup"]:
                return
            # В личных чатах показываем ошибку
            await message.answer(loc.get("invalid_link"))
            return

        # Создаем прогресс-бар
        progress = TikTokProgressBar(message, loc)
        
        try:
            # Начинаем процесс скачивания
            await progress.start_download()
            
            # Этап 1: Анализ URL
            await progress.analyzing_url()
            await asyncio.sleep(0.5)  # Небольшая задержка для визуального эффекта
            
            # Этап 2: Получение видео
            await progress.getting_video()
            video_url = await resolver.get_fastest_url(url)
            
            # Этап 3: Скачивание файла
            await progress.downloading_file()
            await asyncio.sleep(0.3)
            
        except Exception as e:
            logger.warning("Ошибка скачивания видео от %s(%s): %s", 
                          message.from_user.username if message.from_user else None,
                          message.from_user.id if message.from_user else None,
                          str(e))
            
            # Показываем ошибку в прогресс-баре
            error_msg = str(e)
            if "Сервис временно недоступен" in error_msg:
                await progress.error_occurred(loc.get("service_unavailable"))
            else:
                await progress.error_occurred(loc.get("download_error"))
            return

        me = await message.bot.get_me()
        caption = loc.get("video_caption", bot_username=me.username or me.id)
        
        # Этап 4: Отправка видео
        await progress.sending_video()
        
        # Если провайдер вернул локальный путь — отправим файл; иначе URL
        temp_file_path: str | None = None
        temp_dir: str | None = None
        
        try:
            if video_url.startswith("/") or video_url.startswith("./"):
                from aiogram.types import FSInputFile
                import os

                temp_file_path = video_url
                temp_dir = os.path.dirname(video_url)
                
                await message.reply_video(FSInputFile(video_url), caption=caption)
            else:
                # Проверяем доступность URL перед отправкой
                try:
                    # Пробуем reply_video, если не работает - обычный answer_video
                    try:
                        await message.reply_video(video_url, caption=caption)
                    except Exception as reply_error:
                        logger.warning("reply_video не сработал, пробуем answer_video: %s", reply_error)
                        await message.answer_video(video_url, caption=caption)
                except Exception as e:
                    logger.warning("Ошибка отправки видео по URL %s: %s", video_url, str(e))
                    await progress.error_occurred(loc.get("invalid_video_url"))
                    return
            
            # Успешное завершение
            await progress.success()
            
            # Логируем успешное скачивание
            logger.info("Успешно скачано видео от %s(%s): %s", 
                       message.from_user.username if message.from_user else None,
                       message.from_user.id if message.from_user else None,
                       url)
        finally:
            # Автоматически удаляем временные файлы
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    logger.info("Удален временный файл: %s", temp_file_path)
                except Exception as e:
                    logger.warning("Не удалось удалить файл %s: %s", temp_file_path, e)
            
            # Удаляем временную папку если она пустая
            if temp_dir and os.path.exists(temp_dir):
                try:
                    if not os.listdir(temp_dir):  # Если папка пустая
                        os.rmdir(temp_dir)
                        logger.info("Удалена временная папка: %s", temp_dir)
                except Exception as e:
                    logger.warning("Не удалось удалить папку %s: %s", temp_dir, e)


    return router



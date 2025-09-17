from __future__ import annotations

import asyncio
import logging
from typing import Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from app.config.settings import Settings
from app.services.user_storage import user_storage
from app.services.localization import get_localization
from app.services.user_language import user_language_storage


def setup_broadcast_handlers(settings: Settings) -> tuple[Router, dict[int, dict[str, Any]]]:
    router = Router()
    logger = logging.getLogger(__name__)

    # Хранилище для временных данных рассылки
    _broadcast_data: dict[int, dict[str, Any]] = {}

    @router.message(Command("broadcast"))
    async def start_broadcast(message: Message) -> None:
        """Начало создания рассылки"""
        if message.from_user is None or message.from_user.id not in set(settings.admin_ids):
            return

        admin_id = message.from_user.id
        
        # Получаем язык админа
        user_language = user_language_storage.get_language(admin_id)
        loc = get_localization(user_language)
        
        # Очищаем предыдущее состояние рассылки
        if admin_id in _broadcast_data:
            del _broadcast_data[admin_id]

        user_count = user_storage.get_user_count()
        
        if user_count == 0:
            await message.answer(loc.get("broadcast_no_users"))
            return

        # Создаем новое состояние рассылки
        _broadcast_data[admin_id] = {}

        # Создаем inline клавиатуру
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=loc.get("broadcast_stats"),
                        callback_data="broadcast_stats"
                    )
                ]
            ]
        )

        await message.answer(
            loc.get("broadcast_start", user_count=user_count),
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    def is_admin_in_broadcast_mode(message: Message) -> bool:
        """Проверяет, находится ли админ в режиме рассылки"""
        if not message.from_user or message.from_user.id not in set(settings.admin_ids):
            return False
        if not (message.text or message.photo or message.video or message.document or message.audio):
            return False
        if message.text and message.text.startswith("/"):
            return False
        return message.from_user.id in _broadcast_data

    @router.message(is_admin_in_broadcast_mode)
    async def handle_broadcast_content(message: Message) -> None:
        """Обработка контента для рассылки"""
        admin_id = message.from_user.id
        
        # Получаем язык админа
        user_language = user_language_storage.get_language(admin_id)
        loc = get_localization(user_language)

        # Проверяем, что админ не находится в процессе рассылки
        if "content" in _broadcast_data[admin_id]:
            # Если уже есть контент, игнорируем новое сообщение
            return

        # Сохраняем контент
        _broadcast_data[admin_id]["content"] = message

        # Создаем кнопки подтверждения
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=loc.get("broadcast_send"),
                        callback_data="broadcast_confirm:yes"
                    ),
                    InlineKeyboardButton(
                        text=loc.get("broadcast_cancel"),
                        callback_data="broadcast_confirm:no"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=loc.get("broadcast_preview"),
                        callback_data="broadcast_preview"
                    )
                ]
            ]
        )

        user_count = user_storage.get_user_count()
        
        # Определяем тип сообщения
        message_type = loc.get("message_type_text")
        if message.photo:
            message_type = loc.get("message_type_photo")
        elif message.video:
            message_type = loc.get("message_type_video")
        elif message.document:
            message_type = loc.get("message_type_document")
        elif message.audio:
            message_type = loc.get("message_type_audio")
        
        await message.answer(
            loc.get("broadcast_confirm", user_count=user_count, message_type=message_type),
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    @router.callback_query(lambda c: c.data == "broadcast_preview")
    async def handle_broadcast_preview(callback: CallbackQuery) -> None:
        """Предпросмотр рассылки"""
        if callback.from_user is None or callback.from_user.id not in set(settings.admin_ids):
            await callback.answer("❌ Нет доступа", show_alert=True)
            return

        admin_id = callback.from_user.id
        if admin_id not in _broadcast_data or "content" not in _broadcast_data[admin_id]:
            await callback.answer("❌ Нет данных для предпросмотра", show_alert=True)
            return

        content_message = _broadcast_data[admin_id]["content"]
        
        # Отправляем предпросмотр
        try:
            if content_message.text:
                await callback.message.answer(
                    f"👁️ <b>Предпросмотр рассылки:</b>\n\n{content_message.text}",
                    parse_mode="HTML"
                )
            elif content_message.photo:
                caption = f"👁️ <b>Предпросмотр рассылки:</b>\n\n{content_message.caption or ''}"
                await callback.message.answer_photo(
                    content_message.photo[-1].file_id,
                    caption=caption,
                    parse_mode="HTML"
                )
            elif content_message.video:
                caption = f"👁️ <b>Предпросмотр рассылки:</b>\n\n{content_message.caption or ''}"
                await callback.message.answer_video(
                    content_message.video.file_id,
                    caption=caption,
                    parse_mode="HTML"
                )
            elif content_message.document:
                caption = f"👁️ <b>Предпросмотр рассылки:</b>\n\n{content_message.caption or ''}"
                await callback.message.answer_document(
                    content_message.document.file_id,
                    caption=caption,
                    parse_mode="HTML"
                )
            elif content_message.audio:
                caption = f"👁️ <b>Предпросмотр рассылки:</b>\n\n{content_message.caption or ''}"
                await callback.message.answer_audio(
                    content_message.audio.file_id,
                    caption=caption,
                    parse_mode="HTML"
                )
        except Exception as e:
            logger.error("Ошибка предпросмотра: %s", e)
            await callback.answer("❌ Ошибка предпросмотра", show_alert=True)
            return

        await callback.answer("✅ Предпросмотр отправлен")

    @router.callback_query(lambda c: c.data.startswith("broadcast_confirm:"))
    async def handle_broadcast_confirm(callback: CallbackQuery) -> None:
        """Подтверждение рассылки"""
        if callback.from_user is None or callback.from_user.id not in set(settings.admin_ids):
            await callback.answer("❌ Нет доступа", show_alert=True)
            return

        admin_id = callback.from_user.id
        action = callback.data.split(":", 1)[1]

        if action == "no":
            # Отменяем рассылку
            if admin_id in _broadcast_data:
                del _broadcast_data[admin_id]
            await callback.message.edit_text("❌ Рассылка отменена")
            await callback.answer()
            return

        if admin_id not in _broadcast_data or "content" not in _broadcast_data[admin_id]:
            await callback.answer("❌ Нет данных для рассылки", show_alert=True)
            return

        # Начинаем рассылку
        await callback.message.edit_text("📤 Отправка рассылки...")
        await callback.answer()

        # Запускаем рассылку в фоне
        asyncio.create_task(send_broadcast(admin_id, callback.message.bot))

    @router.callback_query(lambda c: c.data == "broadcast_stats")
    async def handle_broadcast_stats(callback: CallbackQuery) -> None:
        """Показать статистику пользователей"""
        if callback.from_user is None or callback.from_user.id not in set(settings.admin_ids):
            await callback.answer("❌ Нет доступа", show_alert=True)
            return

        users = user_storage.get_all_users()
        user_count = len(users)
        
        # Подсчитываем статистику
        with_username = sum(1 for u in users if u.username)
        with_first_name = sum(1 for u in users if u.first_name)
        
        stats_text = (
            f"📊 <b>Статистика пользователей</b>\n\n"
            f"👥 Всего пользователей: <b>{user_count}</b>\n"
            f"🏷️ С username: <b>{with_username}</b>\n"
            f"👤 С именем: <b>{with_first_name}</b>\n\n"
            f"📈 Готовы к рассылке: <b>{user_count}</b>"
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔄 Обновить",
                        callback_data="broadcast_stats"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="broadcast_back"
                    )
                ]
            ]
        )

        await callback.message.edit_text(stats_text, reply_markup=keyboard, parse_mode="HTML")
        await callback.answer()

    @router.callback_query(lambda c: c.data == "broadcast_back")
    async def handle_broadcast_back(callback: CallbackQuery) -> None:
        """Возврат к главному меню рассылки"""
        if callback.from_user is None or callback.from_user.id not in set(settings.admin_ids):
            await callback.answer("❌ Нет доступа", show_alert=True)
            return

        user_count = user_storage.get_user_count()
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📊 Статистика пользователей",
                        callback_data="broadcast_stats"
                    )
                ]
            ]
        )

        await callback.message.edit_text(
            f"📢 <b>Создание рассылки</b>\n\n"
            f"👥 Пользователей в базе: <b>{user_count}</b>\n\n"
            f"Отправьте любое сообщение для рассылки:\n"
            f"• 📝 Текст\n"
            f"• 🖼️ Изображение\n"
            f"• 📹 Видео\n"
            f"• 📄 Документ\n"
            f"• 🎵 Аудио",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()

    async def send_broadcast(admin_id: int, bot) -> None:
        """Отправка рассылки всем пользователям"""
        if admin_id not in _broadcast_data or "content" not in _broadcast_data[admin_id]:
            return

        content_message = _broadcast_data[admin_id]["content"]
        users = user_storage.get_all_users()
        
        success_count = 0
        error_count = 0
        
        logger.info("Начинаем рассылку для %d пользователей", len(users))

        for user_info in users:
            try:
                if content_message.text:
                    await bot.send_message(
                        user_info.user_id,
                        content_message.text,
                        parse_mode="HTML"
                    )
                elif content_message.photo:
                    await bot.send_photo(
                        user_info.user_id,
                        content_message.photo[-1].file_id,
                        caption=content_message.caption,
                        parse_mode="HTML"
                    )
                elif content_message.video:
                    await bot.send_video(
                        user_info.user_id,
                        content_message.video.file_id,
                        caption=content_message.caption,
                        parse_mode="HTML"
                    )
                elif content_message.document:
                    await bot.send_document(
                        user_info.user_id,
                        content_message.document.file_id,
                        caption=content_message.caption,
                        parse_mode="HTML"
                    )
                elif content_message.audio:
                    await bot.send_audio(
                        user_info.user_id,
                        content_message.audio.file_id,
                        caption=content_message.caption,
                        parse_mode="HTML"
                    )
                
                success_count += 1
                
                # Небольшая задержка между сообщениями
                await asyncio.sleep(0.1)
                
            except Exception as e:
                error_count += 1
                logger.warning("Ошибка отправки пользователю %d: %s", user_info.user_id, e)
                
                # Если пользователь заблокировал бота, удаляем его
                if "bot was blocked" in str(e).lower():
                    user_storage.remove_user(user_info.user_id)

        # Отправляем отчет админу
        try:
            await bot.send_message(
                admin_id,
                f"📢 <b>Рассылка завершена!</b>\n\n"
                f"✅ Успешно отправлено: <b>{success_count}</b>\n"
                f"❌ Ошибок: <b>{error_count}</b>\n"
                f"👥 Всего получателей: <b>{len(users)}</b>",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error("Ошибка отправки отчета админу: %s", e)

        # Очищаем данные рассылки
        if admin_id in _broadcast_data:
            del _broadcast_data[admin_id]

        logger.info("Рассылка завершена: %d успешно, %d ошибок", success_count, error_count)

    @router.message(Command("broadcast_reset"))
    async def reset_broadcast_state(message: Message) -> None:
        """Сброс состояния рассылки"""
        if message.from_user is None or message.from_user.id not in set(settings.admin_ids):
            return

        admin_id = message.from_user.id
        
        if admin_id in _broadcast_data:
            del _broadcast_data[admin_id]
            await message.answer("✅ Состояние рассылки сброшено")
        else:
            await message.answer("ℹ️ Нет активного состояния рассылки")

    return router, _broadcast_data

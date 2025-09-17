from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated, CallbackQuery
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, ADMINISTRATOR, CREATOR, KICKED

from app.services.localization import get_localization
from app.services.user_language import user_language_storage

router = Router()


@router.message(CommandStart())
async def on_start(message: Message) -> None:
    # Получаем язык пользователя
    user_id = message.from_user.id if message.from_user else 0
    user_language = user_language_storage.get_language(user_id)
    loc = get_localization(user_language)
    
    bot_info = await message.bot.get_me()
    bot_username = bot_info.username
    
    if message.chat.type in ["group", "supergroup"]:
        chat_title = message.chat.title or "чат"
        welcome_text = loc.get("start_group", chat_title=chat_title)
        await message.answer(welcome_text)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=loc.get("add_to_chat"),
                        url=f"https://t.me/{bot_username}?startgroup=newchat"
                    )
                ]
            ]
        )
        
        welcome_text = loc.get("start_private")
        await message.answer(welcome_text, reply_markup=keyboard)


@router.my_chat_member()
async def on_bot_added_to_group(event: ChatMemberUpdated) -> None:
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status
    
    if (old_status in [KICKED, "left", "kicked"] and 
        new_status in [MEMBER, ADMINISTRATOR, CREATOR, "member", "administrator", "creator"]):
        
        # Для групп используем русский язык по умолчанию
        loc = get_localization("ru")
        chat_title = event.chat.title or "чат"
        welcome_text = loc.get("start_group", chat_title=chat_title)
        
        await event.bot.send_message(event.chat.id, welcome_text)


@router.message(Command("lang"))
async def on_language_command(message: Message) -> None:
    """Обработка команды /lang"""
    if not message.from_user:
        return
    
    # Получаем текущий язык пользователя
    user_id = message.from_user.id
    current_language = user_language_storage.get_language(user_id)
    loc = get_localization(current_language)
    
    # Создаем клавиатуру для выбора языка
    keyboard = loc.get_language_keyboard()
    
    await message.answer(
        loc.get("language_select"),
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data and c.data.startswith("lang:"))
async def on_language_callback(callback: CallbackQuery) -> None:
    """Обработка выбора языка"""
    if not callback.from_user or not callback.data:
        return
    
    # Извлекаем язык из callback_data
    language = callback.data.split(":")[1]
    if language not in ["ru", "en", "ar", "es", "fr", "de", "pt", "ja", "pl", "tr"]:
        await callback.answer("❌ Invalid language", show_alert=True)
        return
    
    # Сохраняем выбор пользователя
    user_id = callback.from_user.id
    user_language_storage.set_language(user_id, language)
    
    # Получаем локализацию для нового языка
    loc = get_localization(language)
    
    # Обновляем сообщение
    keyboard = loc.get_language_keyboard()
    await callback.message.edit_text(
        loc.get("language_select"),
        reply_markup=keyboard
    )
    
    # Отправляем подтверждение
    await callback.answer(loc.get("language_changed"))
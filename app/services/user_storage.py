from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aiogram.types import User


@dataclass(frozen=True, slots=True)
class UserInfo:
    user_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    is_bot: bool
    language_code: str | None


class UserStorage:
    """Хранилище пользователей для рассылки"""
    
    def __init__(self, storage_file: str = "users.json") -> None:
        self._storage_file = Path(storage_file)
        self._users: dict[int, UserInfo] = {}
        self._logger = logging.getLogger(__name__)
        self._load_users()
    
    def _load_users(self) -> None:
        """Загружает пользователей из файла"""
        try:
            if self._storage_file.exists():
                with open(self._storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for user_id_str, user_data in data.items():
                        user_id = int(user_id_str)
                        self._users[user_id] = UserInfo(**user_data)
                self._logger.info("Загружено %d пользователей", len(self._users))
        except Exception as e:
            self._logger.error("Ошибка загрузки пользователей: %s", e)
    
    def _save_users(self) -> None:
        """Сохраняет пользователей в файл"""
        try:
            data = {
                str(user_id): {
                    "user_id": user_info.user_id,
                    "username": user_info.username,
                    "first_name": user_info.first_name,
                    "last_name": user_info.last_name,
                    "is_bot": user_info.is_bot,
                    "language_code": user_info.language_code,
                }
                for user_id, user_info in self._users.items()
            }
            
            with open(self._storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self._logger.error("Ошибка сохранения пользователей: %s", e)
    
    def add_user(self, user: User) -> None:
        """Добавляет пользователя в хранилище"""
        if user.is_bot:
            return  # Не добавляем ботов
            
        user_info = UserInfo(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_bot=user.is_bot,
            language_code=user.language_code,
        )
        
        self._users[user.id] = user_info
        self._save_users()
        self._logger.debug("Добавлен пользователь: %s (%d)", user.username or user.first_name, user.id)
    
    def get_all_users(self) -> list[UserInfo]:
        """Возвращает всех пользователей"""
        return list(self._users.values())
    
    def get_user_count(self) -> int:
        """Возвращает количество пользователей"""
        return len(self._users)
    
    def remove_user(self, user_id: int) -> bool:
        """Удаляет пользователя из хранилища"""
        if user_id in self._users:
            del self._users[user_id]
            self._save_users()
            self._logger.info("Удален пользователь: %d", user_id)
            return True
        return False
    
    def clear_all(self) -> None:
        """Очищает всех пользователей"""
        self._users.clear()
        self._save_users()
        self._logger.info("Все пользователи удалены")


# Глобальный экземпляр хранилища
user_storage = UserStorage()

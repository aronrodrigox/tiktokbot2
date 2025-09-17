from __future__ import annotations

import json
import logging
import os
from typing import Dict, Literal

from app.services.localization import Language

# Файл для хранения языковых настроек
LANGUAGE_FILE = "user_languages.json"


class UserLanguageStorage:
    """Хранилище языковых настроек пользователей"""
    
    def __init__(self) -> None:
        self._languages: Dict[int, Language] = {}
        self._logger = logging.getLogger(__name__)
        self._load_languages()
    
    def _load_languages(self) -> None:
        """Загрузить языковые настройки из файла"""
        if os.path.exists(LANGUAGE_FILE):
            try:
                with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for user_id_str, language in data.items():
                        user_id = int(user_id_str)
                        if language in ["ru", "en", "ar", "es", "fr", "de", "pt", "ja", "pl", "tr"]:
                            self._languages[user_id] = language
                    self._logger.info("Loaded %d user language preferences", len(self._languages))
            except Exception as e:
                self._logger.error("Error loading user languages: %s", e)
        else:
            self._logger.info("Language file not found, creating new: %s", LANGUAGE_FILE)
    
    def _save_languages(self) -> None:
        """Сохранить языковые настройки в файл"""
        try:
            with open(LANGUAGE_FILE, "w", encoding="utf-8") as f:
                data = {str(user_id): language for user_id, language in self._languages.items()}
                json.dump(data, f, ensure_ascii=False, indent=2)
            self._logger.debug("Saved %d user language preferences", len(self._languages))
        except Exception as e:
            self._logger.error("Error saving user languages: %s", e)
    
    def get_language(self, user_id: int) -> Language:
        """Получить язык пользователя"""
        return self._languages.get(user_id, "ru")  # По умолчанию русский
    
    def set_language(self, user_id: int, language: Language) -> None:
        """Установить язык пользователя"""
        self._languages[user_id] = language
        self._logger.info("User %d language set to %s", user_id, language)
        self._save_languages()
    
    def get_user_count_by_language(self) -> Dict[Language, int]:
        """Получить количество пользователей по языкам"""
        counts = {"ru": 0, "en": 0, "ar": 0, "es": 0, "fr": 0, "de": 0, "pt": 0, "ja": 0, "pl": 0, "tr": 0}
        for language in self._languages.values():
            if language in counts:
                counts[language] += 1
        return counts


# Глобальный экземпляр
user_language_storage = UserLanguageStorage()

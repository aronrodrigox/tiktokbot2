from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    tikwm_api_base_url: str
    tikwm_api_key: str | None
    http_timeout_sec: float
    custom_api_base_url: str
    custom_api_key: str | None
    tikmeh_path: str | None
    admin_ids: list[int]

    @staticmethod
    def from_env() -> Settings:
        bot_token = os.getenv("BOT_TOKEN", "").strip()
        if not bot_token:
            raise RuntimeError("BOT_TOKEN is not set")

        base = os.getenv("TIKWM_API_BASE_URL", "https://www.tikwm.com/").strip()
        if base.endswith("/api/"):
            tikwm_api_base_url = base
        elif base.endswith("/"):
            tikwm_api_base_url = base + "api/"
        else:
            tikwm_api_base_url = base + "/api/"

        tikwm_api_key = os.getenv("TIKWM_API_KEY")
        http_timeout_sec = float(os.getenv("HTTP_TIMEOUT_SEC", "20"))
        tikmeh_path = os.getenv("TIKMEH_PATH")

        custom_api_base_url = os.getenv("CUSTOM_API_BASE_URL", "").strip()
        if not custom_api_base_url:
            # Позволим запускаться боту, если не используется custom API прямо сейчас,
            # но провайдер потребует эту переменную. Выбрасывать здесь исключение не будем.
            custom_api_base_url = ""
        custom_api_key = os.getenv("CUSTOM_API_KEY")

        # Admin IDs (comma-separated integers)
        admin_ids_env = os.getenv("ADMIN_IDS", "").strip()
        admin_ids: list[int] = []
        if admin_ids_env:
            for part in admin_ids_env.split(","):
                part = part.strip()
                if part.isdigit():
                    admin_ids.append(int(part))

        return Settings(
            bot_token=bot_token,
            tikwm_api_base_url=tikwm_api_base_url,
            tikwm_api_key=tikwm_api_key if tikwm_api_key else None,
            http_timeout_sec=http_timeout_sec,
            tikmeh_path=tikmeh_path if tikmeh_path else None,
            custom_api_base_url=custom_api_base_url,
            custom_api_key=custom_api_key if custom_api_key else None,
            admin_ids=admin_ids,
        )



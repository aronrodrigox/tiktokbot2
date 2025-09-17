from __future__ import annotations

import re
from typing import Final

_TIKTOK_DOMAINS: Final = (
    r"(?:https?://)?(?:www\.|m\.)?tiktok\.com/[^\s]+",
    r"(?:https?://)?vt\.tiktok\.com/[^\s]+",
    r"(?:https?://)?vm\.tiktok\.com/[^\s]+",
    r"(?:https?://)?(?:www\.)?tiktokv\.com/[^\s]+",
)

_TIKTOK_URL_RE: Final = re.compile(
    rf"({'|'.join(_TIKTOK_DOMAINS)})",
    flags=re.IGNORECASE,
)


def extract_tiktok_url(text: str) -> str | None:
    if not text:
        return None
    match = _TIKTOK_URL_RE.search(text)
    if not match:
        return None
    url = match.group(0).strip()
    # Удаляем окружение и хвостовые знаки препинания
    url = url.lstrip('<[("')
    url = url.rstrip('.,!?)"\]>' )
    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url
    return url



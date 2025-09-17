from __future__ import annotations

import asyncio
import time
from typing import Any

import httpx


class TikwmClient:
    def __init__(
        self,
        base_url: str,
        api_key: str | None,
        timeout_sec: float = 20.0,
        max_retries: int = 3,
        backoff_base_sec: float = 0.5,
        cache_ttl_sec: int = 600,
    ) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._timeout = httpx.Timeout(timeout_sec)
        self._default_headers: dict[str, str] = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
            ),
            "Referer": "https://www.tikwm.com/",
            "Accept": "application/json, text/plain, */*",
        }
        self._client = httpx.AsyncClient(
            timeout=self._timeout,
            headers=self._default_headers,
        )
        self._max_retries = max(1, max_retries)
        self._backoff_base_sec = max(0.1, backoff_base_sec)
        self._cache_ttl_sec = max(0, cache_ttl_sec)
        self._cache: dict[str, tuple[float, str]] = {}

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get_no_wm_video_url(self, tiktok_url: str) -> str:
        now = time.monotonic()
        cached = self._cache.get(tiktok_url)
        if cached and cached[0] > now:
            return cached[1]

        params: dict[str, Any] = {"url": tiktok_url, "hd": 1}
        req_headers: dict[str, str] = {}
        if self._api_key:
            req_headers["X-API-KEY"] = self._api_key

        delay = self._backoff_base_sec
        last_err: Exception | None = None
        for attempt in range(1, self._max_retries + 1):
            try:
                resp = await self._client.post(self._base_url, data=params, headers=req_headers)

                # Явно обрабатываем перегрузку/временные ошибки
                if resp.status_code in (429, 500, 502, 503, 504):
                    raise httpx.HTTPStatusError(
                        "server backoff",
                        request=resp.request,
                        response=resp,
                    )

                resp.raise_for_status()
                data = resp.json()

                if not isinstance(data, dict) or data.get("code") not in (0, "0"):
                    raise ValueError("TikWM API returned error or unexpected payload")

                payload = data.get("data") or {}
                if not isinstance(payload, dict):
                    raise ValueError("TikWM API 'data' is not an object")

                hd_url = payload.get("hdplay")
                no_wm_url = payload.get("play")
                for candidate in (hd_url, no_wm_url):
                    if isinstance(candidate, str) and candidate.startswith("http"):
                        if self._cache_ttl_sec:
                            self._cache[tiktok_url] = (
                                time.monotonic() + self._cache_ttl_sec,
                                candidate,
                            )
                        return candidate

                raise ValueError("TikWM API did not provide a playable URL without watermark")
            except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as err:
                last_err = err
                if attempt >= self._max_retries:
                    break
                await asyncio.sleep(delay)
                delay *= 2

        assert last_err is not None
        raise last_err



from __future__ import annotations

from abc import ABC, abstractmethod


class VideoProvider(ABC):
    @abstractmethod
    async def get_download_url(self, tiktok_url: str) -> str:
        raise NotImplementedError

    async def aclose(self) -> None:
        pass

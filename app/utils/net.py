from __future__ import annotations

import httpx


async def expand_url_if_short(url: str, timeout_sec: float = 10.0) -> str:
    """Follow redirects and return final URL. Falls back to GET if HEAD is not allowed.

    Returns original url on any error.
    """
    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(timeout_sec),
            follow_redirects=True,
        ) as client:
            try:
                resp = await client.head(url)
                resp.raise_for_status()
                return str(resp.url)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 405:
                    # Some hosts reject HEAD; try GET with small limit (stream only headers)
                    resp = await client.get(url, headers={"Range": "bytes=0-0"})
                    resp.raise_for_status()
                    return str(resp.url)
                raise
    except Exception:
        return url



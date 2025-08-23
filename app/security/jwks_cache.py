# app/security/jwks_cache.py
import time, asyncio, httpx
from app.core.config import settings
_jwks: list | None = None
_exp = 0.0
_lock = asyncio.Lock()

async def get_jwks(ttl: int = 900) -> list:
    global _jwks, _exp
    now = time.time()
    if _jwks and now < _exp: return _jwks
    async with _lock:
        if _jwks and time.time() < _exp: return _jwks
        async with httpx.AsyncClient(timeout=5) as client:
            _jwks = (await client.get(settings.JWKS_URL)).json()["keys"]
        _exp = time.time() + ttl
        return _jwks

# app/security/hmac.py
import hmac
import hashlib
from fastapi import Header, HTTPException, Request
from app.core.config import settings


async def require_hmac(
    request: Request,
    x_signature: str | None = Header(default=None),
) -> None:
    if not x_signature:
        raise HTTPException(401, "Missing signature")
    body = await request.body()
    mac = hmac.new(settings.HMAC_SECRET.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, x_signature):
        raise HTTPException(401, "Bad signature")

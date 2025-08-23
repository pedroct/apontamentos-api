# app/security/jwt.py
from fastapi import Header, HTTPException, Request
from jose import jwt, jwk
from app.core.config import settings
from app.security.jwks_cache import get_jwks  # cache com TTL


async def require_jwt(request: Request, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = authorization.split(" ", 1)[1]

    # JWKS com cache (TTL padrão 15 min)
    jwks = await get_jwks()

    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    key = next((k for k in jwks if k.get("kid") == kid), None)
    if not key:
        raise HTTPException(401, "Invalid key")

    try:
        claims = jwt.decode(
            token,
            jwk.construct(key),
            audience=settings.AUTH_AUDIENCE,
            issuer=settings.AUTH_ISSUER,
            options={"verify_at_hash": False},
        )
    except Exception as e:
        raise HTTPException(401, f"Invalid token: {e}")

    azp = claims.get("azp")
    if settings.ALLOWED_AZP and azp not in settings.ALLOWED_AZP:
        raise HTTPException(403, "Client app not allowed")

    request.state.user = claims
    return claims

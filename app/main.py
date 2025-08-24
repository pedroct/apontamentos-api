# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db.session import engine
from app.core.config import settings
from app.core.logging import setup_logging
from app.security.jwt import require_jwt
from app.security.hmac import require_hmac
from app.api.routes import router as api_router

# --- Observação:
# Inicialize logging e Sentry *antes* de criar o app FastAPI.

setup_logging()

# Sentry: ativado somente se houver DSN nas variáveis de ambiente / .env
try:
    import sentry_sdk  # type: ignore

    SENTRY_DSN = getattr(settings, "SENTRY_DSN", None)
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            send_default_pii=True,
            # valores com fallback para não exigir novos campos no Settings
            enable_tracing=True,
            traces_sample_rate=float(
                getattr(settings, "SENTRY_TRACES_SAMPLE_RATE", 0.2)
            ),
            profiles_sample_rate=float(
                getattr(settings, "SENTRY_PROFILES_SAMPLE_RATE", 0.0)
            ),
        )
except Exception:
    # Nunca derrube o app por falha de inicialização do Sentry.
    # O logger já está configurado; se desejar, logue aqui.
    pass

app = FastAPI(title="api-apontamentos")

# CORS: usa lista do settings e cai para ["*"] se vier vazia/nula
allow_origins = getattr(settings, "CORS_ALLOWED_ORIGINS", None) or ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"ready": True}


@app.get("/protected", dependencies=[Depends(require_jwt)])
async def protected():
    return {"ok": True, "auth": "jwt"}


@app.post("/hook-boards", dependencies=[Depends(require_hmac)])
async def hook_boards(payload: dict):
    return {"status": "ok"}


# Rotas da API
app.include_router(api_router, prefix="/api")

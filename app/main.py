# app/main.py (topo do arquivo)
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.session import engine
from app.core.config import settings
from app.core.logging import setup_logging
from app.security.jwt import require_jwt
from app.security.hmac import require_hmac
from app.api.routes import router as api_router

setup_logging()

app = FastAPI(title="API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"ok": True}


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


app.include_router(api_router, prefix="/api")

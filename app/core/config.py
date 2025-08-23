from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]  # raiz do repo

class Settings(BaseSettings):
    CORS_ALLOWED_ORIGINS: List[str] = []
    AUTH_ISSUER: str
    AUTH_AUDIENCE: str
    JWKS_URL: str
    ALLOWED_AZP: List[str] = []
    HMAC_SECRET: str = "change-me"
    DATABASE_URL: str
    LOG_LEVEL: str = "DEBUG"

    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # <= ignora chaves que não existem no modelo
    )

settings = Settings()
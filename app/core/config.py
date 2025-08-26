# app/core/config.py  (versão nova)
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    CORS_ALLOWED_ORIGINS: List[str] = []
    HMAC_SECRET: str = "change-me"
    DATABASE_URL: str
    LOG_LEVEL: str = "DEBUG"

    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

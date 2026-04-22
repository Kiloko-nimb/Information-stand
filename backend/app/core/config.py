from pathlib import Path

from pydantic_settings import BaseSettings

# Корень backend-пакета (…/backend)
BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = f"sqlite:///{BACKEND_ROOT / 'kkrit.db'}"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"

    # App
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()

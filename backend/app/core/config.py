from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

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

    # Yandex.Disk schedule sync (используется напрямую через os.environ
    # в app/main.py, но объявляем здесь, чтобы pydantic не падал при чтении .env)
    YANDEX_DISK_PUBLIC_URL: Optional[str] = None
    YANDEX_DISK_SYNC_INTERVAL_HOURS: int = 3

    # Разрешаем любые дополнительные поля в .env, чтобы добавление новых
    # переменных окружения не ломало запуск.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

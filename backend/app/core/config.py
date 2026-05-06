from pathlib import Path
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень backend-пакета (…/backend)
BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = f"sqlite:///{BACKEND_ROOT / 'kkrit.db'}"
    # SQLite WAL mode для лучшей конкурентности (recommended для production)
    SQLITE_WAL_MODE: bool = True

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"

    # CORS - разрешённые origins через запятую (например: "http://localhost:5173,https://mydomain.com")
    CORS_ORIGINS: str = "http://localhost:5173"
    # Для JSON конфигурации можно использовать CORS_ORIGINS_JSON='["*"]'
    CORS_ORIGINS_JSON: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100  # запросов
    RATE_LIMIT_PERIOD: int = 60     # в секундах

    # App
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # Yandex.Disk schedule sync (используется напрямую через os.environ
    # в app/main.py, но объявляем здесь, чтобы pydantic не падал при чтении .env)
    YANDEX_DISK_PUBLIC_URL: Optional[str] = None
    YANDEX_DISK_SYNC_INTERVAL_HOURS: int = 3
    # Обходить вложенные подпапки (архивы по месяцам и т.п.). По умолчанию
    # включено, потому что на Я.Диске ККРИТ часто кладут расписание в
    # папки вида «апрель», «март».
    YANDEX_DISK_RECURSIVE: bool = True

    # Retry настройки для внешних API
    EXTERNAL_API_MAX_RETRIES: int = 3
    EXTERNAL_API_RETRY_DELAY: float = 1.0  # секунд
    EXTERNAL_API_TIMEOUT: int = 15  # секунд

    # Разрешаем любые дополнительные поля в .env, чтобы добавление новых
    # переменных окружения не ломало запуск.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def get_cors_origins(self) -> List[str]:
        """Парсит CORS_ORIGINS в список."""
        if self.CORS_ORIGINS_JSON:
            import json
            try:
                return json.loads(self.CORS_ORIGINS_JSON)
            except json.JSONDecodeError:
                pass
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()

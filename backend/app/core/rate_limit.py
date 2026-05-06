"""
Настройка rate limiting для API.
Использует slowapi (обёртка над limits).
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, FastAPI
from .config import settings

# slowapi.Limiter по умолчанию подхватывает локальный `.env` через
# starlette.config.Config, который открывает файл системной кодировкой.
# На Windows (cp1251) это падает с UnicodeDecodeError, если в `.env` есть
# UTF-8 символы (русские комментарии, рамки `─` и т.п.). Обходим это,
# передавая пустой `config_filename` — slowapi не будет читать `.env`,
# а наши настройки и так берутся из pydantic-settings (`app.core.config`).
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_REQUESTS} per {settings.RATE_LIMIT_PERIOD} seconds"]
    if settings.RATE_LIMIT_ENABLED else [],
    config_filename="",
)


def setup_rate_limiting(app: FastAPI):
    """Настройка rate limiting для приложения FastAPI."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

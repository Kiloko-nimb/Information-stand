"""
Настройка rate limiting для API.
Использует slowapi (обёртка над limits).
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, FastAPI
from .config import settings

# Создаём limiter с ключом по IP-адресу
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_REQUESTS} per {settings.RATE_LIMIT_PERIOD} seconds"]
    if settings.RATE_LIMIT_ENABLED else []
)


def setup_rate_limiting(app: FastAPI):
    """Настройка rate limiting для приложения FastAPI."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

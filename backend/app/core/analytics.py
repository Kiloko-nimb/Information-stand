"""
Middleware для учёта посещений и популярных запросов.
"""
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.analytics import PageVisit, PopularQuery

logger = logging.getLogger(__name__)

# Путь и параметры, которые не логируем
_SKIP_PATHS = {"/health", "/", "/favicon.ico", "/docs", "/openapi.json", "/redoc"}
_SKIP_PREFIXES = ("/static", "/assets")


class AnalyticsMiddleware(BaseHTTPMiddleware):
    """Записывает каждый API-запрос в таблицу page_visits и обновляет popular_queries."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        path = request.url.path
        # Логируем только API-запросы
        if path.startswith("/api/v1") and path not in _SKIP_PATHS:
            try:
                self._record(request)
            except Exception as exc:
                logger.warning("analytics: %s", exc)

        return response

    @staticmethod
    def _record(request: Request) -> None:
        db: Session = SessionLocal()
        try:
            path = request.url.path
            # Убираем cache-busting параметр _t
            query_str = str(request.query_params) or None
            if query_str:
                # Убираем _t=... из строки
                import re
                query_str = re.sub(r'(^|&)_t=[^&]*', '', query_str).lstrip('&') or None

            # Пропускаем мусорные запросы (тестовые, с невалидными параметрами)
            if query_str and ('not-a-' in query_str or 'UNKNOWN' in path):
                return

            ip = request.client.host if request.client else None
            ua = request.headers.get("user-agent", "")[:500]

            db.add(PageVisit(page=path, query=query_str, ip=ip, user_agent=ua))

            # Обновляем popular_queries (upsert)
            existing = (
                db.query(PopularQuery)
                .filter(PopularQuery.endpoint == path, PopularQuery.params == query_str)
                .first()
            )
            if existing:
                existing.hit_count += 1
            else:
                db.add(PopularQuery(endpoint=path, params=query_str))

            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

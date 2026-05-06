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

# Пути и параметры, которые не логируем
_SKIP_PATHS = {"/health", "/", "/favicon.ico", "/docs", "/openapi.json", "/redoc"}
_SKIP_PREFIXES = ("/static", "/assets")

# Пути API, которые не считаем «запросом пользователя стенда»:
#   - /admin/* — действия администратора (управление контентом).
#   - /auth/* — служебные запросы авторизации.
#   - /schedule/now, /schedule/bells — фоновый поллинг главной страницы
#     (виджет «Сейчас идёт пара» бьёт раз в 30 секунд и за пару часов
#     полностью забивает таблицу популярных запросов, а реальные поиски
#     пользователей теряются).
_NOISE_API_PREFIXES: tuple[str, ...] = (
    "/api/v1/admin",
    "/api/v1/auth",
)
_NOISE_API_EXACT: frozenset[str] = frozenset({
    "/api/v1/schedule/now",
    "/api/v1/schedule/bells",
})


def _is_user_search(path: str) -> bool:
    """True, если запрос реально похож на действие посетителя стенда."""
    if not path.startswith("/api/v1"):
        return False
    if path in _SKIP_PATHS:
        return False
    if path in _NOISE_API_EXACT:
        return False
    if path.startswith(_NOISE_API_PREFIXES):
        return False
    return True


class AnalyticsMiddleware(BaseHTTPMiddleware):
    """Записывает реальные пользовательские запросы (поиск групп/преподавателей/
    кабинетов и т.п.) в таблицу page_visits и обновляет popular_queries.

    Намеренно НЕ логируем: /admin/*, /auth/*, фоновый поллинг /schedule/now
    и /schedule/bells — они дают шум и искажают аналитику.
    """

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        if _is_user_search(request.url.path):
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

"""
Тесты аналитики посещений.

Проверяем два момента:
1) Middleware AnalyticsMiddleware фильтрует шум: /admin/*, /auth/*,
   фоновый поллинг /schedule/now и /schedule/bells. Иначе через час
   работы стенда таблица «Популярные запросы» полностью забивается
   служебными вызовами и реальные поиски пользователей теряются.
2) Эндпоинт /api/v1/admin/analytics/stats возвращает в `top_pages`
   именно общий топ запросов, а не дублирует `top_schedule_groups`.
"""
from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.auth import require_admin
from app.core.analytics import _is_user_search
from app.main import app
from app.models.admin import Admin
from app.models.analytics import PageVisit, PopularQuery


class TestIsUserSearch:
    """Юнит-тесты для предиката, который решает, надо ли логировать запрос."""

    def test_real_search_endpoints_are_logged(self) -> None:
        assert _is_user_search("/api/v1/schedule/group/9ИС-1.25")
        assert _is_user_search("/api/v1/schedule/teacher/Петров")
        assert _is_user_search("/api/v1/schedule/room/305")
        assert _is_user_search("/api/v1/schedule/groups")
        assert _is_user_search("/api/v1/staff/search")
        assert _is_user_search("/api/v1/rooms/305")
        assert _is_user_search("/api/v1/news/")

    def test_admin_endpoints_are_not_logged(self) -> None:
        assert not _is_user_search("/api/v1/admin/news")
        assert not _is_user_search("/api/v1/admin/staff")
        assert not _is_user_search("/api/v1/admin/rooms")
        assert not _is_user_search("/api/v1/admin/analytics/stats")

    def test_auth_endpoints_are_not_logged(self) -> None:
        assert not _is_user_search("/api/v1/auth/login")
        assert not _is_user_search("/api/v1/auth/check")
        assert not _is_user_search("/api/v1/auth/setup")
        assert not _is_user_search("/api/v1/auth/me")

    def test_polling_endpoints_are_not_logged(self) -> None:
        # Главная страница стенда дёргает /schedule/now каждые 30 секунд.
        # Виджет звонков — /schedule/bells. Это шум, не поиск.
        assert not _is_user_search("/api/v1/schedule/now")
        assert not _is_user_search("/api/v1/schedule/bells")

    def test_non_api_paths_are_not_logged(self) -> None:
        assert not _is_user_search("/health")
        assert not _is_user_search("/")
        assert not _is_user_search("/docs")
        assert not _is_user_search("/static/icon.png")


class TestAnalyticsMiddlewareIntegration:
    """Гарантируем, что middleware действительно пишет в БД для реальных
    поисков и молчит на шумных эндпоинтах.

    Middleware использует свой собственный SessionLocal (из app.core.database),
    поэтому в тестах подменяем его на фабрику, привязанную к in-memory
    тестовой БД.
    """

    @staticmethod
    def _patch_middleware_session(monkeypatch, db_session: Session) -> None:
        """Заставляем AnalyticsMiddleware писать в ту же in-memory БД,
        что и тестовый клиент."""
        def fake_session_local():
            # Возвращаем сессию, чьи commits/queries видны seeded_db / db_session.
            # Используем тот же bind, что и у фикстурной сессии.
            from sqlalchemy.orm import sessionmaker
            return sessionmaker(bind=db_session.get_bind(), autoflush=False, autocommit=False)()

        monkeypatch.setattr("app.core.analytics.SessionLocal", fake_session_local)

    def test_user_search_creates_popular_query_row(
        self, client: TestClient, seeded_db: Session, monkeypatch
    ) -> None:
        self._patch_middleware_session(monkeypatch, seeded_db)
        response = client.get("/api/v1/schedule/group/9ИС-1.25")
        assert response.status_code == 200

        endpoints = {r.endpoint for r in seeded_db.query(PopularQuery).all()}
        assert "/api/v1/schedule/group/9ИС-1.25" in endpoints

    def test_admin_call_does_not_pollute_analytics(
        self, client: TestClient, db_session: Session, monkeypatch
    ) -> None:
        self._patch_middleware_session(monkeypatch, db_session)

        fake_admin = Admin(id=1, username="testadmin", hashed_password="x", is_active=True)
        app.dependency_overrides[require_admin] = lambda: fake_admin
        try:
            response = client.get("/api/v1/admin/analytics/stats")
        finally:
            app.dependency_overrides.pop(require_admin, None)

        assert response.status_code == 200
        admin_rows = (
            db_session.query(PopularQuery)
            .filter(PopularQuery.endpoint.like("/api/v1/admin/%"))
            .count()
        )
        assert admin_rows == 0

    def test_polling_does_not_pollute_analytics(
        self, client: TestClient, seeded_db: Session, monkeypatch
    ) -> None:
        self._patch_middleware_session(monkeypatch, seeded_db)

        # Эмулируем 5 фоновых поллов /schedule/now с главной страницы.
        for _ in range(5):
            client.get("/api/v1/schedule/now")

        rows = seeded_db.query(PopularQuery).filter(
            PopularQuery.endpoint == "/api/v1/schedule/now"
        ).all()
        assert rows == [], (
            "schedule/now не должен попадать в популярные запросы — "
            "он бьёт раз в 30 секунд и забил бы таблицу"
        )

        visits = seeded_db.query(PageVisit).filter(
            PageVisit.page == "/api/v1/schedule/now"
        ).count()
        assert visits == 0


class TestAdminAnalyticsStats:
    """Регрессия: /admin/analytics/stats должен возвращать в top_pages общий
    топ, а не копию top_schedule_groups."""

    def test_top_pages_includes_non_schedule_endpoints(
        self, client: TestClient, db_session: Session
    ) -> None:
        # Готовим данные руками: один популярный запрос staff, один schedule.
        db_session.add_all([
            PopularQuery(
                endpoint="/api/v1/staff/search",
                params="query=Иванов",
                hit_count=10,
            ),
            PopularQuery(
                endpoint="/api/v1/schedule/group/9ИС-1.25",
                params=None,
                hit_count=3,
            ),
        ])
        db_session.commit()

        fake_admin = Admin(id=1, username="testadmin", hashed_password="x", is_active=True)
        app.dependency_overrides[require_admin] = lambda: fake_admin
        try:
            response = client.get("/api/v1/admin/analytics/stats")
        finally:
            app.dependency_overrides.pop(require_admin, None)

        assert response.status_code == 200, response.text
        data = response.json()

        top_pages_endpoints = {p["endpoint"] for p in data["top_pages"]}
        # Раньше top_pages = top_schedule, и staff/search туда не попадал.
        assert "/api/v1/staff/search" in top_pages_endpoints, (
            "top_pages должен содержать общий топ, включая не-schedule запросы"
        )
        assert "/api/v1/schedule/group/9ИС-1.25" in top_pages_endpoints

        top_schedule_endpoints = {p["endpoint"] for p in data["top_schedule_groups"]}
        # А вот top_schedule_groups — только schedule.
        assert "/api/v1/staff/search" not in top_schedule_endpoints
        assert "/api/v1/schedule/group/9ИС-1.25" in top_schedule_endpoints

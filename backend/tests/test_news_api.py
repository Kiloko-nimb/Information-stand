"""
Тесты REST-эндпоинтов новостей.
"""
from __future__ import annotations

from fastapi.testclient import TestClient


class TestNewsApi:
    def test_list_active_news_by_default(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/news/")
        assert response.status_code == 200
        payload = response.json()
        titles = [item["title"] for item in payload]
        assert titles == ["Открытый день"]

    def test_list_all_news_including_inactive(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/news/", params={"active_only": "false"})
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 2

    def test_pagination_limit_and_skip(self, client: TestClient, seeded_db) -> None:
        response = client.get(
            "/api/v1/news/",
            params={"active_only": "false", "limit": 1, "skip": 1},
        )
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        # Упорядочено по убыванию published_date, skip=1 → вторая запись
        assert payload[0]["title"] == "Архивная новость"

    def test_get_news_by_id(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/news/1")
        assert response.status_code == 200
        assert response.json()["title"] == "Открытый день"

    def test_get_news_by_unknown_id_returns_404(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/news/9999")
        assert response.status_code == 404

    def test_refresh_endpoint_returns_started(self, client: TestClient, seeded_db, monkeypatch) -> None:
        """
        POST /news/refresh должен немедленно вернуть "started" и
        ставить реальный парсинг в фоновую задачу. Моккаем fetch/save,
        чтобы в тесте не ходить в сеть.
        """
        from app.api import news as news_module

        monkeypatch.setattr(news_module, "fetch_news_from_website", lambda: [])
        monkeypatch.setattr(news_module, "save_news_to_db", lambda news_list, db: None)

        response = client.post("/api/v1/news/refresh")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "started"

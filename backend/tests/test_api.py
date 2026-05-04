"""
Тесты базовых REST-эндпоинтов (staff, schedule, rooms, root/health).
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_root_returns_online(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["version"]


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert "timestamp" in data


class TestStaffApi:
    def test_list_all_staff(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/staff/")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 3
        assert {item["full_name"] for item in payload} == {
            "Алексеев Иван Иванович",
            "Петров Пётр Петрович",
            "Иванова Анна Сергеевна",
        }

    def test_search_staff_by_partial_name(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/staff/search", params={"query": "Алексеев"})
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        assert payload[0]["full_name"] == "Алексеев Иван Иванович"

    def test_search_staff_no_match_returns_empty(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/staff/search", params={"query": "XYZ"})
        assert response.status_code == 200
        assert response.json() == []

    def test_get_staff_by_id(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/staff/1")
        assert response.status_code == 200
        assert response.json()["full_name"] == "Алексеев Иван Иванович"

    def test_get_staff_by_unknown_id_returns_404(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/staff/9999")
        assert response.status_code == 404


class TestScheduleApi:
    def test_group_schedule_returns_entries(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/schedule/group/9ИС-1.25")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 2
        assert {item["subject"] for item in payload} == {"Программирование", "Математика"}

    def test_group_schedule_partial_match(self, client: TestClient, seeded_db) -> None:
        # API использует LIKE-поиск по подстроке
        response = client.get("/api/v1/schedule/group/ИС-1")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 2

    def test_group_schedule_unknown_group_returns_404(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/schedule/group/UNKNOWN")
        assert response.status_code == 404

    def test_teacher_schedule(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/schedule/teacher/Петров")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 2
        assert {item["group_name"] for item in payload} == {"9ИС-1.25", "9ПР-1.25"}

    def test_room_schedule(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/schedule/room/215")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        assert payload[0]["subject"] == "Программирование"

    def test_list_groups_is_sorted_and_unique(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/schedule/groups")
        assert response.status_code == 200
        payload = response.json()
        names = [item["name"] for item in payload]
        assert names == sorted(set(names))
        assert "9ИС-1.25" in names
        assert "9ПР-1.25" in names

    def test_list_groups_filters_garbage_names(
        self, client: TestClient, db_session
    ) -> None:
        """В БД могут попасть мусорные имена групп («Ауд.», «.») от старых
        импортов. Эндпоинт должен их отбрасывать, чтобы фронт не показывал
        «не группа а набор букв»."""
        from datetime import date, time

        from app.models.schedule import Schedule

        db_session.add_all(
            [
                Schedule(
                    group_name="9ИС-1.25",
                    subject="Программирование",
                    day_of_week=1,
                    lesson_number=1,
                    time_start=time(8, 10),
                    time_end=time(8, 55),
                    date=date(2026, 4, 13),
                ),
                # Заголовки колонок «Ауд.» из плохого парсинга PDF — не группа.
                Schedule(
                    group_name="Ауд.",
                    subject="мусор",
                    day_of_week=1,
                    lesson_number=1,
                    time_start=time(8, 10),
                    time_end=time(8, 55),
                    date=date(2026, 4, 13),
                ),
                Schedule(
                    group_name="ауд",
                    subject="мусор",
                    day_of_week=1,
                    lesson_number=1,
                    time_start=time(8, 10),
                    time_end=time(8, 55),
                    date=date(2026, 4, 13),
                ),
                # Только знаки препинания — тоже мусор.
                Schedule(
                    group_name=".",
                    subject="мусор",
                    day_of_week=1,
                    lesson_number=1,
                    time_start=time(8, 10),
                    time_end=time(8, 55),
                    date=date(2026, 4, 13),
                ),
            ]
        )
        db_session.commit()

        response = client.get("/api/v1/schedule/groups")
        assert response.status_code == 200
        names = [item["name"] for item in response.json()]
        assert names == ["9ИС-1.25"]


class TestRoomsApi:
    def test_list_all_rooms(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/rooms/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_rooms_by_floor(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/rooms/floor/2")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        assert payload[0]["room_number"] == "215"

    def test_room_by_number(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/rooms/313")
        assert response.status_code == 200
        assert response.json()["room_type"] == "Лаборатория"

    def test_room_by_unknown_number_returns_404(self, client: TestClient, seeded_db) -> None:
        response = client.get("/api/v1/rooms/UNKNOWN")
        assert response.status_code == 404

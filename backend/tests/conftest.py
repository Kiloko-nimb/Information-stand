"""
Общие фикстуры для pytest-тестов API.

Поднимаем FastAPI-приложение поверх in-memory SQLite, чтобы тесты были
изолированы, не зависели от реальной `kkrit.db` и внешней сети.
"""
from __future__ import annotations

from datetime import date, datetime, time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.news import News
from app.models.room import Room
from app.models.schedule import Schedule
from app.models.staff import Staff


@pytest.fixture()
def db_session() -> Session:
    """Свежая in-memory БД на каждый тест."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session: Session) -> TestClient:
    """TestClient с подменённой зависимостью get_db."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # TestClient без `with` не запускает lifespan (и, значит, фоновую задачу новостей).
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture()
def seeded_db(db_session: Session) -> Session:
    """Небольшой фикстурный набор данных: сотрудники, аудитории, расписание, новости."""
    staff = [
        Staff(full_name="Алексеев Иван Иванович", position="Преподаватель", department="ИТ"),
        Staff(full_name="Петров Пётр Петрович", position="Преподаватель", department="Математика"),
        Staff(full_name="Иванова Анна Сергеевна", position="Зав. кафедрой", department="ИТ"),
    ]
    rooms = [
        Room(room_number="116", floor=1, building="К1", room_type="Аудитория"),
        Room(room_number="215", floor=2, building="К1", room_type="Аудитория"),
        Room(room_number="313", floor=3, building="К1", room_type="Лаборатория"),
    ]
    schedules = [
        Schedule(
            group_name="9ИС-1.25",
            teacher_name="Алексеев И.И.",
            subject="Программирование",
            room_number="215",
            day_of_week=1,
            lesson_number=1,
            time_start=time(8, 10),
            time_end=time(8, 55),
            date=date(2026, 4, 13),
            lesson_type="Лекция",
        ),
        Schedule(
            group_name="9ИС-1.25",
            teacher_name="Петров П.П.",
            subject="Математика",
            room_number="313",
            day_of_week=1,
            lesson_number=2,
            time_start=time(9, 0),
            time_end=time(9, 45),
            date=date(2026, 4, 13),
            lesson_type="Практика",
        ),
        Schedule(
            group_name="9ПР-1.25",
            teacher_name="Петров П.П.",
            subject="Математика",
            room_number="116",
            day_of_week=1,
            lesson_number=1,
            time_start=time(8, 10),
            time_end=time(8, 55),
            date=date(2026, 4, 13),
            lesson_type="Лекция",
        ),
    ]
    news = [
        News(
            title="Открытый день",
            description="Приглашаем абитуриентов",
            icon="📰",
            published_date=datetime(2026, 4, 10, 12, 0, 0),
            is_active=True,
        ),
        News(
            title="Архивная новость",
            description="Старая новость",
            icon="🗞️",
            published_date=datetime(2025, 1, 1, 12, 0, 0),
            is_active=False,
        ),
    ]

    db_session.add_all(staff + rooms + schedules + news)
    db_session.commit()
    return db_session

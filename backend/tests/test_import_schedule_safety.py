"""Тесты на защиту от тихой потери данных при импорте расписания.

Сценарий: автосинк скачал кривой/пустой PDF (например, Excel-шаблон без
данных), парсер ничего не извлёк, но DELETE по дате уже отработал.
До фикса это коммитилось — день расписания тихо стирался. Теперь
коммит-без-данных откатывается, и существующие записи остаются.
"""
from __future__ import annotations

from datetime import date, time
from pathlib import Path

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import database as db_module
from app.core.database import Base
from app.models.schedule import Schedule
from app.utils import import_schedule as importer


@pytest.fixture()
def isolated_db(monkeypatch):
    """In-memory БД, подменяющая SessionLocal на время теста.

    importer.import_schedule_from_excel дёргает SessionLocal() напрямую,
    поэтому подменяем фабрику в модуле database, а importer ходит через
    свой импорт ``from app.core.database import SessionLocal`` — поэтому
    патчим и в нём тоже.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    monkeypatch.setattr(db_module, "SessionLocal", TestingSessionLocal)
    monkeypatch.setattr(importer, "SessionLocal", TestingSessionLocal)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def _seed_schedule(session, schedule_date: date) -> int:
    rows = [
        Schedule(
            group_name="9ИС-1.25",
            teacher_name="Алексеев И.И.",
            subject="Программирование",
            room_number="215",
            day_of_week=schedule_date.weekday() + 1,
            lesson_number=1,
            time_start=time(8, 0),
            time_end=time(8, 45),
            date=schedule_date,
            lesson_type="Лекция",
        ),
        Schedule(
            group_name="9ПР-1.25",
            teacher_name="Петров П.П.",
            subject="Математика",
            room_number="313",
            day_of_week=schedule_date.weekday() + 1,
            lesson_number=2,
            time_start=time(8, 50),
            time_end=time(9, 35),
            date=schedule_date,
            lesson_type="Практика",
        ),
    ]
    session.add_all(rows)
    session.commit()
    return len(rows)


def test_excel_importer_rolls_back_when_file_is_empty(
    tmp_path: Path, isolated_db
):
    """Кривой Excel без распознаваемых данных не должен стирать
    существующее расписание на эту дату."""
    schedule_date = date(2026, 4, 13)  # понедельник, есть расписание звонков
    seeded = _seed_schedule(isolated_db, schedule_date)
    assert seeded > 0

    # Excel-файл с одним пустым листом — парсер не найдёт ни групп, ни пар.
    empty_xlsx = tmp_path / "empty.xlsx"
    pd.DataFrame([[None, None]]).to_excel(empty_xlsx, header=False, index=False)

    added = importer.import_schedule_from_excel(
        str(empty_xlsx), schedule_date.isoformat()
    )
    assert added == 0

    isolated_db.expire_all()
    remaining = (
        isolated_db.query(Schedule)
        .filter(Schedule.date == schedule_date)
        .count()
    )
    assert remaining == seeded, (
        "Кривой Excel не должен был удалить уже существующее расписание"
    )

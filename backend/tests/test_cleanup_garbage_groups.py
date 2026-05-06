"""
Тесты для ``scripts/cleanup_garbage_groups``.
"""
from __future__ import annotations

import os
import sys
from datetime import date, time

import pytest
from sqlalchemy.orm import Session

from app.models.schedule import Schedule

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_REPO_ROOT, "scripts"))

from cleanup_garbage_groups import cleanup_garbage_groups, find_garbage_rows  # noqa: E402


def _seed(db: Session) -> None:
    db.add_all(
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
            # Артефакт старого PDF-парсера: заголовок столбца «Ауд.».
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
                lesson_number=2,
                time_start=time(9, 0),
                time_end=time(9, 45),
                date=date(2026, 4, 13),
            ),
            # Только знаки препинания.
            Schedule(
                group_name=".",
                subject="мусор",
                day_of_week=1,
                lesson_number=3,
                time_start=time(10, 0),
                time_end=time(10, 45),
                date=date(2026, 4, 13),
            ),
        ]
    )
    db.commit()


def test_find_garbage_rows_returns_only_invalid(db_session: Session) -> None:
    _seed(db_session)
    garbage = find_garbage_rows(db_session)
    assert {row.group_name for row in garbage} == {"Ауд.", "ауд", "."}


def test_dry_run_does_not_delete(db_session: Session) -> None:
    _seed(db_session)
    deleted = cleanup_garbage_groups(db_session, apply=False)
    assert deleted == 3
    # Все 4 записи на месте — dry-run ничего не трогает.
    assert db_session.query(Schedule).count() == 4


def test_apply_removes_only_garbage(db_session: Session) -> None:
    _seed(db_session)
    deleted = cleanup_garbage_groups(db_session, apply=True)
    assert deleted == 3

    remaining = db_session.query(Schedule).all()
    assert len(remaining) == 1
    assert remaining[0].group_name == "9ИС-1.25"


def test_apply_is_idempotent_on_clean_db(db_session: Session) -> None:
    db_session.add(
        Schedule(
            group_name="9ИС-1.25",
            subject="Программирование",
            day_of_week=1,
            lesson_number=1,
            time_start=time(8, 10),
            time_end=time(8, 55),
            date=date(2026, 4, 13),
        )
    )
    db_session.commit()

    assert cleanup_garbage_groups(db_session, apply=True) == 0
    # И повторно — тоже ноль, БД не меняется.
    assert cleanup_garbage_groups(db_session, apply=True) == 0
    assert db_session.query(Schedule).count() == 1

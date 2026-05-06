"""
Удаляет мусорные записи расписания из БД.

«Мусорные» — это строки таблицы ``schedules``, у которых
``group_name`` не проходит :func:`app.utils.group_names.is_valid_group_name`
(например, ``Ауд.`` — заголовок столбца с номером аудитории, попавший в БД
из старых, ещё кривых импортов PDF-расписания).

API ``/api/v1/schedule/groups`` уже отфильтровывает их на отдаче,
но в самой таблице они остаются и засоряют ``/today`` / ``/now`` /
``busy_groups_count``. Этот скрипт окончательно вычищает их из БД.

Использование::

    # Сухой прогон — показать, что будет удалено, но ничего не делать.
    python scripts/cleanup_garbage_groups.py

    # Реальное удаление.
    python scripts/cleanup_garbage_groups.py --apply

    # Кастомная БД (по умолчанию берётся ``settings.DATABASE_URL``).
    python scripts/cleanup_garbage_groups.py --apply --db sqlite:///backend/kkrit.db

Идемпотентен: повторный запуск на чистой БД ничего не делает.
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from typing import Iterable

# Добавляем backend в sys.path, чтобы можно было импортировать `app.*`.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "backend"))

from sqlalchemy import create_engine  # noqa: E402  (after sys.path tweak)
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.models.schedule import Schedule  # noqa: E402
from app.utils.group_names import is_valid_group_name  # noqa: E402


def find_garbage_rows(db: Session) -> list[Schedule]:
    """Возвращает все записи ``schedules`` с невалидным ``group_name``."""
    rows = db.query(Schedule).all()
    return [r for r in rows if not is_valid_group_name(r.group_name)]


def _summarize(rows: Iterable[Schedule]) -> Counter:
    return Counter(r.group_name for r in rows)


def cleanup_garbage_groups(db: Session, *, apply: bool) -> int:
    """
    Удаляет мусорные записи расписания.

    Args:
        db: SQLAlchemy-сессия.
        apply: Если ``False`` — только сообщает, что будет удалено, ничего
            не меняет. Если ``True`` — удаляет и коммитит.

    Returns:
        Количество затронутых строк (или которые были бы затронуты в dry-run).
    """
    garbage = find_garbage_rows(db)
    if not garbage:
        print("✓ Мусорных записей не найдено — БД чистая.")
        return 0

    summary = _summarize(garbage)
    print(f"Найдено {len(garbage)} мусорных записей в `schedules`:")
    for name, count in summary.most_common():
        print(f"  {name!r:>20}  ×{count}")

    if not apply:
        print("\n[dry-run] Ничего не удаляю. Запусти с --apply для реального удаления.")
        return len(garbage)

    for row in garbage:
        db.delete(row)
    db.commit()
    print(f"\n✓ Удалено {len(garbage)} записей.")
    return len(garbage)


def _build_session(db_url: str) -> Session:
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Чистит таблицу `schedules` от мусорных имён групп (`Ауд.`, `.` и т.п.)."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Реально удалить записи. Без флага — только показать, что будет удалено.",
    )
    parser.add_argument(
        "--db",
        default=settings.DATABASE_URL,
        help=f"URL базы данных SQLAlchemy (по умолчанию: {settings.DATABASE_URL}).",
    )
    args = parser.parse_args()

    print(f"DB: {args.db}")
    print(f"Mode: {'APPLY' if args.apply else 'dry-run'}\n")

    db = _build_session(args.db)
    try:
        cleanup_garbage_groups(db, apply=args.apply)
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

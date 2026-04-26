"""
Маленькие идемпотентные миграции для SQLite.

В проекте нет alembic, потому что схема меняется редко и БД одна (sqlite).
Этот модуль на старте приложения добавляет недостающие колонки в существующие
таблицы — чтобы у пользователя, у которого `kkrit.db` уже создана старой
версией, не падали запросы при апгрейде.

Каждая миграция должна быть идемпотентной (если колонка уже есть — ничего не
делать). Алгоритм: спросить у sqlite список колонок (`PRAGMA table_info`),
и если нужной нет — выполнить `ALTER TABLE ADD COLUMN`.
"""
from __future__ import annotations

import logging
from typing import Iterable

from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def _existing_columns(engine: Engine, table: str) -> set[str]:
    with engine.connect() as conn:
        rows = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
    return {row[1] for row in rows}


def _add_column(engine: Engine, table: str, column: str, ddl: str) -> None:
    with engine.begin() as conn:
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))
    logger.info("migrations: добавлена колонка %s.%s", table, column)


def apply_pending_migrations(engine: Engine) -> None:
    """Идемпотентно подтянуть схему БД к текущим моделям."""
    if engine.dialect.name != "sqlite":
        # На других СУБД полагаемся на alembic / ручные миграции.
        return

    schedules_columns = _existing_columns(engine, "schedules")
    if not schedules_columns:
        # Таблицы ещё нет — её создаст Base.metadata.create_all().
        return

    pending: Iterable[tuple[str, str]] = (
        ("imported_at", "DATETIME"),
        ("is_modified", "BOOLEAN NOT NULL DEFAULT 0"),
    )
    for column, ddl in pending:
        if column not in schedules_columns:
            _add_column(engine, "schedules", column, ddl)

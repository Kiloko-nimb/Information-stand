"""
Заполнение таблицы ``rooms`` уникальными аудиториями из расписания.

Идемпотентно: для каждой найденной аудитории проверяем существование
по ``room_number`` и добавляем только новые записи. Безопасно вызывать
после каждого ``import_schedule`` — старые записи не трогаются.

Используется как из CLI-скрипта ``populate_rooms.py`` в корне репо,
так и из ``import_schedule`` (авто-вызов после импорта).
"""
from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.room import Room
from app.models.schedule import Schedule
from app.utils.room_names import is_valid_room_number

logger = logging.getLogger(__name__)


def _get_floor(room_number: str) -> int:
    room_clean = room_number.strip().lower()
    if "сп" in room_clean or "спорт" in room_clean:
        return 1
    if "акт" in room_clean:
        return 1
    for char in room_number:
        if char.isdigit():
            floor = int(char)
            if 1 <= floor <= 4:
                return floor
            if floor == 0:
                return 1
    return 1


def _get_room_type(room_number: str) -> str:
    room_lower = room_number.lower()
    if "сп" in room_lower or "спорт" in room_lower:
        return "Спортзал"
    if "акт" in room_lower:
        return "Актовый зал"
    if "лаб" in room_lower:
        return "Лаборатория"
    return "Аудитория"


def _get_building(room_number: str) -> str:
    if room_number.startswith("4"):
        return "пр. Свободный 67"
    return "пр. Красноярский Рабочий 156"


def populate_rooms(db: Optional[Session] = None) -> int:
    """
    Заполняет ``rooms`` уникальными ``room_number`` из ``schedules``.

    Args:
        db: Опциональная SQLAlchemy-сессия. Если не передана — создаётся
            и закрывается внутри функции.

    Returns:
        int: Количество новых добавленных аудиторий.
    """
    own_session = db is None
    if db is None:
        db = SessionLocal()

    added = 0
    skipped = 0
    refreshed = 0
    try:
        existing_rooms = {r.room_number: r for r in db.query(Room).all()}

        # Освежаем поле floor у уже существующих записей. Старый сид мог
        # проставить всем floor=1; теперь корректный этаж выводится из
        # первой цифры номера кабинета (201→2, 305→3 и т.д.). Тип кабинета
        # и здание не трогаем — их мог вручную проставить администратор
        # для красоты демо.
        for room_number, room in existing_rooms.items():
            if not room_number or not is_valid_room_number(room_number):
                continue
            new_floor = _get_floor(room_number)
            if room.floor != new_floor:
                room.floor = new_floor
                refreshed += 1

        unique_rooms = (
            db.query(Schedule.room_number)
            .filter(Schedule.room_number.isnot(None))
            .filter(Schedule.room_number != "")
            .distinct()
            .all()
        )

        for (room_number,) in unique_rooms:
            if not room_number:
                continue
            # Не заводим в справочник кабинетов мусор (текст предмета,
            # попавший в room_number из-за сдвига колонок) и маркер
            # «ДО» (дистанционная пара — не физический кабинет).
            if not is_valid_room_number(room_number):
                continue
            if room_number.strip().lower() == "до":
                continue
            if room_number in existing_rooms:
                skipped += 1
                continue
            db.add(
                Room(
                    room_number=room_number,
                    floor=_get_floor(room_number),
                    room_type=_get_room_type(room_number),
                    building=_get_building(room_number),
                )
            )
            existing_rooms[room_number] = None  # placeholder
            added += 1

        db.commit()
        if refreshed:
            logger.info("rooms: обновлено метаданных у %d существующих записей", refreshed)
        if added or skipped:
            logger.info(
                "rooms: добавлено %d, пропущено существующих %d (всего уникальных в расписании: %d)",
                added,
                skipped,
                len(unique_rooms),
            )
        return added
    except Exception:
        db.rollback()
        raise
    finally:
        if own_session:
            db.close()

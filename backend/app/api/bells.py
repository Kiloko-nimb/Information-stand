"""
API расписания звонков.

Фронтенду нужно знать тайминги пар, которые зависят от дня недели:
понедельник (с линейкой и классным часом) отличается от остальных
учебных дней. Сервер — единственный источник правды.
"""
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from app.core.bell_schedule import schedule_as_dict

router = APIRouter(prefix="/schedule/bells", tags=["schedule"])


@router.get("")
async def get_bells(
    weekday: int = Query(
        None,
        ge=1,
        le=7,
        description="День недели: 1=Пн, 2=Вт, ..., 6=Сб, 7=Вс",
    ),
    date: str = Query(
        None,
        description="Дата в формате YYYY-MM-DD (альтернатива weekday)",
    ),
):
    """
    Вернуть расписание звонков для дня недели или конкретной даты.

    Можно передать либо ``weekday`` (1..7), либо ``date=YYYY-MM-DD``.
    Если не передано ничего — считаем сегодняшний день.
    """
    if weekday is None and date is None:
        weekday = datetime.now().isoweekday()

    if date is not None:
        try:
            parsed = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Некорректный формат даты: {date!r} (ожидается YYYY-MM-DD)",
            ) from e
        weekday = parsed.isoweekday()

    return {
        "weekday": weekday,
        "pairs": schedule_as_dict(weekday),
    }

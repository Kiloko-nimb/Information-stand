from datetime import date as date_cls, datetime, time as time_cls
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.bell_schedule import get_bell_schedule
from app.core.database import get_db
from app.models.schedule import Schedule

router = APIRouter(prefix="/schedule", tags=["schedule"])


def _parse_date_param(value: Optional[str]) -> Optional[date_cls]:
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Некорректный формат даты: {value!r} (ожидается YYYY-MM-DD)",
        ) from e


@router.get("/group/{group_name}")
async def get_group_schedule(
    group_name: str,
    date: Optional[str] = Query(None, description="Фильтр по дате, YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Получить расписание для группы. Опционально фильтр по дате."""
    query = db.query(Schedule).filter(Schedule.group_name.like(f"%{group_name}%"))
    filter_date = _parse_date_param(date)
    if filter_date is not None:
        query = query.filter(Schedule.date == filter_date)
    schedule = query.order_by(Schedule.lesson_number).all()

    if not schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")

    return schedule


@router.get("/teacher/{teacher_name}")
async def get_teacher_schedule(
    teacher_name: str,
    date: Optional[str] = Query(None, description="Фильтр по дате, YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Получить расписание преподавателя."""
    query = db.query(Schedule).filter(Schedule.teacher_name.ilike(f"%{teacher_name}%"))
    filter_date = _parse_date_param(date)
    if filter_date is not None:
        query = query.filter(Schedule.date == filter_date)
    schedule = query.order_by(Schedule.lesson_number).all()

    if not schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")

    return schedule


@router.get("/room/{room_number}")
async def get_room_schedule(
    room_number: str,
    date: Optional[str] = Query(None, description="Фильтр по дате, YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Получить расписание для кабинета."""
    query = db.query(Schedule).filter(Schedule.room_number == room_number)
    filter_date = _parse_date_param(date)
    if filter_date is not None:
        query = query.filter(Schedule.date == filter_date)
    return query.order_by(Schedule.lesson_number).all()


@router.get("/groups")
async def get_all_groups(db: Session = Depends(get_db)):
    """Получить список всех групп."""
    groups = (
        db.query(Schedule.group_name)
        .distinct()
        .order_by(Schedule.group_name)
        .all()
    )
    return [{"name": g[0]} for g in groups]


@router.get("/teachers")
async def get_all_teachers(db: Session = Depends(get_db)):
    """Список всех преподавателей, встречающихся в расписании."""
    rows = (
        db.query(Schedule.teacher_name)
        .filter(Schedule.teacher_name.isnot(None))
        .filter(Schedule.teacher_name != "")
        .distinct()
        .order_by(Schedule.teacher_name)
        .all()
    )
    return [{"name": r[0]} for r in rows if r[0]]


@router.get("/rooms")
async def get_all_rooms(db: Session = Depends(get_db)):
    """Список всех аудиторий, встречающихся в расписании."""
    rows = (
        db.query(Schedule.room_number)
        .filter(Schedule.room_number.isnot(None))
        .filter(Schedule.room_number != "")
        .distinct()
        .order_by(Schedule.room_number)
        .all()
    )
    return [{"number": r[0]} for r in rows if r[0]]


@router.get("/today")
async def get_today_schedule(db: Session = Depends(get_db)):
    """Получить расписание на сегодня для всех групп."""
    today = date_cls.today()
    schedule = (
        db.query(Schedule)
        .filter(Schedule.date == today)
        .order_by(Schedule.group_name, Schedule.lesson_number)
        .all()
    )
    return schedule


@router.get("/now")
async def get_now_status(db: Session = Depends(get_db)):
    """
    Что происходит в колледже прямо сейчас.

    Возвращает:
    - ``current``: текущая пара (если идёт), её время, сколько групп заняты
      и сколько минут осталось до конца.
    - ``next``: ближайшая следующая пара по сегодняшнему расписанию звонков.
    - ``status``: ``"in_progress"`` | ``"break"`` | ``"before_classes"`` |
      ``"after_classes"`` | ``"weekend"``.
    """
    now = datetime.now()
    today = now.date()
    weekday = today.isoweekday()

    bell = get_bell_schedule(weekday)
    if not bell:
        return {"status": "weekend", "current": None, "next": None}

    current_pair = None
    next_pair = None
    for pair in bell:
        if pair.start <= now.time() <= pair.end:
            current_pair = pair
            break
        if now.time() < pair.start and next_pair is None:
            next_pair = pair

    def _pair_payload(pair) -> dict:
        return {
            "lesson_number": pair.lesson_number,
            "label": pair.label,
            "start": pair.start.strftime("%H:%M"),
            "end": pair.end.strftime("%H:%M"),
        }

    if current_pair is None and next_pair is None:
        return {"status": "after_classes", "current": None, "next": None}

    if current_pair is None:
        # До начала пар или на перерыве.
        before_first = bell and now.time() < bell[0].start
        status = "before_classes" if before_first else "break"
        # Сколько минут до начала следующей пары.
        if next_pair is not None:
            target = datetime.combine(today, next_pair.start)
            minutes_until_next = max(0, int((target - now).total_seconds() // 60))
        else:
            minutes_until_next = None
        return {
            "status": status,
            "current": None,
            "next": {**_pair_payload(next_pair), "minutes_until": minutes_until_next}
            if next_pair
            else None,
        }

    # Идёт пара. Считаем загрузку и сколько ещё минут до конца.
    end_dt = datetime.combine(today, current_pair.end)
    minutes_left = max(0, int((end_dt - now).total_seconds() // 60))

    busy_groups_count = (
        db.query(Schedule.group_name)
        .filter(Schedule.date == today)
        .filter(Schedule.lesson_number == current_pair.lesson_number)
        .distinct()
        .count()
    )

    return {
        "status": "in_progress",
        "current": {
            **_pair_payload(current_pair),
            "minutes_left": minutes_left,
            "busy_groups": busy_groups_count,
        },
        "next": _pair_payload(next_pair) if next_pair else None,
    }


@router.get("/dates")
async def get_available_dates(db: Session = Depends(get_db)):
    """Список дат, на которые есть расписание."""
    rows = (
        db.query(Schedule.date)
        .distinct()
        .order_by(Schedule.date)
        .all()
    )
    return [r[0].isoformat() for r in rows if r[0]]

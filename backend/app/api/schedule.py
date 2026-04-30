from datetime import date as date_cls, datetime, time as time_cls
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.bell_schedule import get_bell_schedule
from app.core.database import get_db
from app.models.schedule import Schedule
from app.utils.group_names import is_valid_group_name
from app.utils.room_names import is_valid_room_number

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
    """Получить список всех групп.

    Фильтрует мусорные имена («Ауд.», «.», пустые) из старых импортов,
    чтобы фронт не показывал «не группа а набор букв».
    """
    groups = (
        db.query(Schedule.group_name)
        .distinct()
        .order_by(Schedule.group_name)
        .all()
    )
    return [{"name": g[0]} for g in groups if is_valid_group_name(g[0])]


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
    """Список всех аудиторий, встречающихся в расписании.

    Отсеиваем мусор: если в ``room_number`` оказался текст предмета
    из-за сдвига колонок в PDF (``"1 п/гр 1С: Предприятие …"``), он
    не попадёт в подсказки. См.
    :func:`app.utils.room_names.is_valid_room_number`. Маркер ``ДО``
    (дистанционная пара) также не выводим — это не физический кабинет.
    """
    rows = (
        db.query(Schedule.room_number)
        .filter(Schedule.room_number.isnot(None))
        .filter(Schedule.room_number != "")
        .distinct()
        .order_by(Schedule.room_number)
        .all()
    )
    return [
        {"number": r[0]}
        for r in rows
        if r[0] and is_valid_room_number(r[0]) and r[0].strip().lower() != "до"
    ]


@router.get("/today")
async def get_today_schedule(db: Session = Depends(get_db)):
    """Получить расписание на сегодня для всех групп.

    Записи с мусорным ``group_name`` (например, ``Ауд.``) отфильтровываются —
    см. :func:`app.utils.group_names.is_valid_group_name`.
    """
    today = date_cls.today()
    schedule = (
        db.query(Schedule)
        .filter(Schedule.date == today)
        .order_by(Schedule.group_name, Schedule.lesson_number)
        .all()
    )
    return [s for s in schedule if is_valid_group_name(s.group_name)]


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

    # Идём по парам и параллельно ловим текущую (если уже началась, но
    # ещё не закончилась) и ближайшую следующую (первую с pair.start > now).
    # Раньше после нахождения current_pair был break, из-за чего next_pair
    # во время идущей пары всегда оставался None — это нарушало контракт
    # API (поле "next" задокументировано как «ближайшая следующая пара
    # по сегодняшнему расписанию звонков»).
    current_pair = None
    next_pair = None
    for pair in bell:
        if pair.start <= now.time() <= pair.end:
            current_pair = pair
        elif now.time() < pair.start and next_pair is None:
            next_pair = pair
            if current_pair is not None:
                # Текущую уже нашли, и теперь нашли первую следующую —
                # дальше можно не идти.
                break

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

    busy_group_names = (
        db.query(Schedule.group_name)
        .filter(Schedule.date == today)
        .filter(Schedule.lesson_number == current_pair.lesson_number)
        .distinct()
        .all()
    )
    busy_groups_count = sum(1 for (name,) in busy_group_names if is_valid_group_name(name))

    return {
        "status": "in_progress",
        "current": {
            **_pair_payload(current_pair),
            "minutes_left": minutes_left,
            "busy_groups": busy_groups_count,
        },
        "next": _pair_payload(next_pair) if next_pair else None,
    }


@router.get("/rooms/free")
async def get_free_rooms_now(
    floor: Optional[int] = Query(None, description="Фильтр по этажу"),
    db: Session = Depends(get_db),
):
    """
    Кабинеты, в которых сейчас не идёт занятие.

    Логика:
    - Если идёт пара (status == "in_progress") — возвращаем все кабинеты,
      встречающиеся в расписании на сегодня, минус занятые на текущей паре.
    - Если перерыв / до пар / после пар / выходной — формально свободны все.
    """
    from app.models.room import Room  # ленивый импорт во избежание циклов

    now = datetime.now()
    today = now.date()
    weekday = today.isoweekday()

    bell = get_bell_schedule(weekday)
    current_pair = None
    next_pair = None
    if bell:
        for pair in bell:
            if pair.start <= now.time() <= pair.end:
                current_pair = pair
                break
            if now.time() < pair.start and next_pair is None:
                next_pair = pair

    if current_pair is None:
        if not bell:
            status = "weekend"
        elif now.time() < bell[0].start:
            status = "before_classes"
        elif next_pair is None:
            status = "after_classes"
        else:
            status = "break"
    else:
        status = "in_progress"

    # Список всех известных кабинетов (приоритет — справочник Room).
    rooms_query = db.query(Room.room_number, Room.floor)
    if floor is not None:
        rooms_query = rooms_query.filter(Room.floor == floor)
    all_rooms = [(r[0], r[1]) for r in rooms_query.order_by(Room.room_number).all() if r[0]]

    if not all_rooms:
        # Запасной путь — берём кабинеты из расписания (этаж определить нельзя).
        # Отсеиваем мусор и маркер «ДО» — на карте этажей им не место.
        rows = (
            db.query(Schedule.room_number)
            .filter(Schedule.room_number.isnot(None))
            .filter(Schedule.room_number != "")
            .distinct()
            .order_by(Schedule.room_number)
            .all()
        )
        all_rooms = [
            (r[0], None)
            for r in rows
            if r[0]
            and is_valid_room_number(r[0])
            and r[0].strip().lower() != "до"
        ]

    busy_set: set[str] = set()
    if current_pair is not None:
        busy_rows = (
            db.query(Schedule.room_number)
            .filter(Schedule.date == today)
            .filter(Schedule.lesson_number == current_pair.lesson_number)
            .filter(Schedule.room_number.isnot(None))
            .filter(Schedule.room_number != "")
            .distinct()
            .all()
        )
        busy_set = {row[0].strip() for row in busy_rows if row[0]}

    free_rooms = [
        {"number": number, "floor": fl}
        for number, fl in all_rooms
        if number.strip() not in busy_set
    ]
    busy_rooms = [
        {"number": number, "floor": fl}
        for number, fl in all_rooms
        if number.strip() in busy_set
    ]

    payload = {
        "status": status,
        "current_pair": (
            {
                "lesson_number": current_pair.lesson_number,
                "label": current_pair.label,
                "start": current_pair.start.strftime("%H:%M"),
                "end": current_pair.end.strftime("%H:%M"),
            }
            if current_pair
            else None
        ),
        "free": free_rooms,
        "busy": busy_rooms,
    }
    return payload


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

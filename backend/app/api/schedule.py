from datetime import date as date_cls, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

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

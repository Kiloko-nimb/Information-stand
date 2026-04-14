from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.models.schedule import Schedule

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.get("/group/{group_name}")
async def get_group_schedule(group_name: str, db: Session = Depends(get_db)):
    """Получить расписание для группы"""
    # Ищем точное совпадение или частичное (для обработки кодировки)
    schedule = db.query(Schedule).filter(
        Schedule.group_name.like(f"%{group_name}%")
    ).all()

    if not schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")

    return schedule

@router.get("/teacher/{teacher_name}")
async def get_teacher_schedule(teacher_name: str, db: Session = Depends(get_db)):
    """Получить расписание преподавателя"""
    schedule = db.query(Schedule).filter(
        Schedule.teacher_name.ilike(f"%{teacher_name}%")
    ).all()

    if not schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")

    return schedule

@router.get("/room/{room_number}")
async def get_room_schedule(room_number: str, db: Session = Depends(get_db)):
    """Получить расписание для кабинета"""
    schedule = db.query(Schedule).filter(Schedule.room_number == room_number).all()

    return schedule

@router.get("/groups")
async def get_all_groups(db: Session = Depends(get_db)):
    """Получить список всех групп"""
    groups = db.query(Schedule.group_name).distinct().order_by(Schedule.group_name).all()
    return [{"name": g[0]} for g in groups]

@router.get("/today")
async def get_today_schedule(db: Session = Depends(get_db)):
    """Получить расписание на сегодня для всех групп"""
    today = date.today()
    schedule = db.query(Schedule).filter(Schedule.date == today).order_by(
        Schedule.group_name, Schedule.lesson_number
    ).all()

    return schedule

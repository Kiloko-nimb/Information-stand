from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.staff import Staff

router = APIRouter(prefix="/staff", tags=["staff"])

@router.get("/")
async def get_all_staff(db: Session = Depends(get_db)):
    """Получить список всех сотрудников"""
    staff = db.query(Staff).all()
    return staff

@router.get("/search")
async def search_staff(query: str, db: Session = Depends(get_db)):
    """Поиск сотрудников по имени"""
    staff = db.query(Staff).filter(
        Staff.full_name.ilike(f"%{query}%")
    ).all()

    return staff

@router.get("/{staff_id}")
async def get_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
    """Получить информацию о сотруднике по ID"""
    staff = db.query(Staff).filter(Staff.id == staff_id).first()

    if not staff:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    return staff

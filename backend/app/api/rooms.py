from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.room import Room

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("/")
async def get_all_rooms(db: Session = Depends(get_db)):
    """Получить список всех кабинетов"""
    rooms = db.query(Room).all()
    return rooms

@router.get("/floor/{floor}")
async def get_rooms_by_floor(floor: int, db: Session = Depends(get_db)):
    """Получить кабинеты на этаже"""
    rooms = db.query(Room).filter(Room.floor == floor).all()
    return rooms

@router.get("/{room_number}")
async def get_room_by_number(room_number: str, db: Session = Depends(get_db)):
    """Получить информацию о кабинете"""
    room = db.query(Room).filter(Room.room_number == room_number).first()

    if not room:
        raise HTTPException(status_code=404, detail="Кабинет не найден")

    return room

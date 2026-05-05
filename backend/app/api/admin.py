"""
Админские CRUD-эндпоинты для управления новостями, сотрудниками и кабинетами.
Все эндпоинты требуют JWT-авторизацию.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.api.auth import require_admin
from app.models.staff import Staff
from app.models.room import Room
from app.models.admin import Admin
from app.utils.room_names import is_valid_room_number

router = APIRouter(prefix="/admin", tags=["admin"])


# ═══════════════════════════════════════════════════════════
#  Схемы Pydantic
# ═══════════════════════════════════════════════════════════

# ── Новости ──
class NewsCreate(BaseModel):
    title: str
    description: Optional[str] = None
    icon: str = "📰"
    published_date: Optional[datetime] = None
    source_url: Optional[str] = None
    is_active: bool = True


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    published_date: Optional[datetime] = None
    source_url: Optional[str] = None
    is_active: Optional[bool] = None


class NewsOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    icon: str
    published_date: Optional[datetime]
    source_url: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Сотрудники ──
class StaffCreate(BaseModel):
    full_name: str
    position: Optional[str] = None
    department: Optional[str] = None
    room_number: Optional[str] = None
    photo_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class StaffUpdate(BaseModel):
    full_name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    room_number: Optional[str] = None
    photo_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class StaffOut(BaseModel):
    id: int
    full_name: str
    position: Optional[str]
    department: Optional[str]
    room_number: Optional[str]
    photo_url: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    class Config:
        from_attributes = True


# ── Кабинеты ──
class RoomCreate(BaseModel):
    room_number: str
    floor: int
    building: Optional[str] = None
    room_type: Optional[str] = None


class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    floor: Optional[int] = None
    building: Optional[str] = None
    room_type: Optional[str] = None


class RoomOut(BaseModel):
    id: int
    room_number: str
    floor: int
    building: Optional[str]
    room_type: Optional[str]

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════
#  Новости CRUD
# ═══════════════════════════════════════════════════════════

@router.get("/news", response_model=List[NewsOut])
async def admin_list_news(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    return db.query(News).order_by(News.published_date.desc()).offset(skip).limit(limit).all()


@router.post("/news", response_model=NewsOut, status_code=status.HTTP_201_CREATED)
async def admin_create_news(
    data: NewsCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    news = News(**data.model_dump())
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


@router.put("/news/{news_id}", response_model=NewsOut)
async def admin_update_news(
    news_id: int,
    data: NewsUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(news, key, value)
    db.commit()
    db.refresh(news)
    return news


@router.delete("/news/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    db.delete(news)
    db.commit()


# ═══════════════════════════════════════════════════════════
#  Сотрудники CRUD
# ═══════════════════════════════════════════════════════════

@router.get("/staff", response_model=List[StaffOut])
async def admin_list_staff(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    return db.query(Staff).order_by(Staff.full_name).offset(skip).limit(limit).all()


@router.post("/staff", response_model=StaffOut, status_code=status.HTTP_201_CREATED)
async def admin_create_staff(
    data: StaffCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    staff = Staff(**data.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


@router.put("/staff/{staff_id}", response_model=StaffOut)
async def admin_update_staff(
    staff_id: int,
    data: StaffUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(staff, key, value)
    db.commit()
    db.refresh(staff)
    return staff


@router.delete("/staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    db.delete(staff)
    db.commit()


# ═══════════════════════════════════════════════════════════
#  Кабинеты CRUD
# ═══════════════════════════════════════════════════════════

@router.get("/rooms", response_model=List[RoomOut])
async def admin_list_rooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    rows = db.query(Room).order_by(Room.room_number).all()
    valid_rows = [room for room in rows if is_valid_room_number(room.room_number)]
    return valid_rows[skip: skip + limit]


@router.post("/rooms", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
async def admin_create_room(
    data: RoomCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    payload = data.model_dump()
    payload["room_number"] = payload["room_number"].strip()

    if not is_valid_room_number(payload["room_number"]):
        raise HTTPException(status_code=422, detail="Некорректный номер кабинета")

    exists = db.query(Room).filter(Room.room_number == payload["room_number"]).first()
    if exists:
        raise HTTPException(status_code=409, detail=f"Кабинет {payload['room_number']} уже существует")

    room = Room(**payload)
    db.add(room)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Кабинет с таким номером уже существует")
    db.refresh(room)
    return room


@router.put("/rooms/{room_id}", response_model=RoomOut)
async def admin_update_room(
    room_id: int,
    data: RoomUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Кабинет не найден")

    updates = data.model_dump(exclude_unset=True)
    if "room_number" in updates and updates["room_number"] is not None:
        updates["room_number"] = updates["room_number"].strip()

        if not is_valid_room_number(updates["room_number"]):
            raise HTTPException(status_code=422, detail="Некорректный номер кабинета")

        duplicate = (
            db.query(Room)
            .filter(Room.room_number == updates["room_number"], Room.id != room_id)
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=409,
                detail=f"Кабинет {updates['room_number']} уже существует",
            )

    for key, value in updates.items():
        setattr(room, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Кабинет с таким номером уже существует")
    db.refresh(room)
    return room


@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Кабинет не найден")
    db.delete(room)
    db.commit()


@router.delete("/rooms/invalid", status_code=status.HTTP_200_OK)
async def admin_cleanup_invalid_rooms(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    """Удаляет из БД все кабинеты с невалидными номерами (например, текст расписания вместо номера)."""
    all_rooms = db.query(Room).all()
    invalid_rooms = [room for room in all_rooms if not is_valid_room_number(room.room_number)]
    deleted_count = len(invalid_rooms)
    for room in invalid_rooms:
        db.delete(room)
    db.commit()
    return {"deleted": deleted_count, "message": f"Удалено {deleted_count} некорректных записей кабинетов"}

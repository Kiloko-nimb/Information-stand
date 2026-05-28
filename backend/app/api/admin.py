"""
Админские CRUD-эндпоинты для управления новостями, сотрудниками и кабинетами.
Все эндпоинты требуют JWT-авторизацию.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import datetime
import os
import uuid
from pathlib import Path as PathLib

from app.core.database import get_db
from app.api.auth import require_admin
from app.models.staff import Staff
from app.models.room import Room
from app.models.news import News
from app.models.admin import Admin
from app.models.group import Group
from app.models.schedule import Schedule
from app.utils.room_names import is_valid_room_number
from app.utils.group_names import is_valid_group_name

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
    image_url: Optional[str] = None
    is_active: bool = True


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    published_date: Optional[datetime] = None
    source_url: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class NewsOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    icon: str
    published_date: Optional[datetime]
    source_url: Optional[str]
    image_url: Optional[str] = None
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


# ── Группы ──
class GroupCreate(BaseModel):
    name: str
    course: Optional[int] = None
    specialty: Optional[str] = None
    is_active: bool = True


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    course: Optional[int] = None
    specialty: Optional[str] = None
    is_active: Optional[bool] = None


class GroupOut(BaseModel):
    id: int
    name: str
    course: Optional[int]
    specialty: Optional[str]
    is_active: bool

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


# ВНИМАНИЕ: маршрут "/rooms/invalid" должен быть зарегистрирован ДО "/rooms/{room_id}",
# иначе FastAPI попытается привести "invalid" к int и вернёт 422.
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


# ═══════════════════════════════════════════════════════════
#  Группы CRUD
# ═══════════════════════════════════════════════════════════

@router.get("/groups", response_model=List[GroupOut])
async def admin_list_groups(
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    return (
        db.query(Group)
        .order_by(Group.name)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("/groups", response_model=GroupOut, status_code=status.HTTP_201_CREATED)
async def admin_create_group(
    data: GroupCreate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="Имя группы не может быть пустым")
    exists = db.query(Group).filter(Group.name == name).first()
    if exists:
        raise HTTPException(status_code=409, detail=f"Группа «{name}» уже существует")
    group = Group(name=name, course=data.course, specialty=data.specialty, is_active=data.is_active)
    db.add(group)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Группа с таким именем уже существует")
    db.refresh(group)
    return group


@router.put("/groups/{group_id}", response_model=GroupOut)
async def admin_update_group(
    group_id: int,
    data: GroupUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    updates = data.model_dump(exclude_unset=True)
    old_name = group.name

    if "name" in updates and updates["name"] is not None:
        new_name = updates["name"].strip()
        if not new_name:
            raise HTTPException(status_code=422, detail="Имя группы не может быть пустым")
        duplicate = (
            db.query(Group)
            .filter(Group.name == new_name, Group.id != group_id)
            .first()
        )
        if duplicate:
            raise HTTPException(status_code=409, detail=f"Группа «{new_name}» уже существует")
        updates["name"] = new_name

        # Переименовать группу во всех записях расписания
        if new_name != old_name:
            db.query(Schedule).filter(Schedule.group_name == old_name).update(
                {Schedule.group_name: new_name}, synchronize_session="fetch"
            )

    for key, value in updates.items():
        setattr(group, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Группа с таким именем уже существует")
    db.refresh(group)
    return group


@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    db.delete(group)
    db.commit()


@router.post("/groups/sync", status_code=status.HTTP_200_OK)
async def admin_sync_groups_from_schedule(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    """Импортировать группы из расписания в справочник (без дублирования)."""
    schedule_groups = (
        db.query(Schedule.group_name)
        .distinct()
        .order_by(Schedule.group_name)
        .all()
    )
    existing_names = {g.name for g in db.query(Group.name).all()}
    added = 0
    for (gname,) in schedule_groups:
        if not gname or not is_valid_group_name(gname):
            continue
        if gname in existing_names:
            continue
        db.add(Group(name=gname))
        existing_names.add(gname)
        added += 1
    db.commit()
    return {"added": added, "message": f"Добавлено {added} групп из расписания"}


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


# ═══════════════════════════════════════════════════════════
#  Загрузка изображений (для новостей и др.)
# ═══════════════════════════════════════════════════════════

UPLOAD_DIR = PathLib(__file__).resolve().parents[2] / "uploads" / "news"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 МБ
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


@router.post("/upload-image", status_code=status.HTTP_201_CREATED)
async def admin_upload_image(
    file: UploadFile = File(...),
    _admin: Admin = Depends(require_admin),
):
    """Загружает изображение в /uploads/news/ и возвращает публичный URL.

    Используется в админке для прикрепления картинок к новостям.
    """
    ext = ALLOWED_IMAGE_TYPES.get(file.content_type)
    if not ext:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый тип файла: {file.content_type}. "
                   "Разрешены: JPEG, PNG, WebP, GIF.",
        )

    # Проверка размера (читаем чанками для экономии памяти)
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Файл слишком большой (макс. {MAX_IMAGE_SIZE // 1024 // 1024} МБ)",
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    out_path = UPLOAD_DIR / filename
    out_path.write_bytes(contents)

    return {
        "url": f"/uploads/news/{filename}",
        "filename": filename,
        "size": len(contents),
    }
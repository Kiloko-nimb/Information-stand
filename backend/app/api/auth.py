from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.admin import Admin

router = APIRouter(prefix="/auth", tags=["auth"])

# ── JWT настройки ──
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 часов

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля. Используем простое сравнение с хешем."""
    from hashlib import sha256
    return sha256(plain_password.encode()).hexdigest() == hashed_password


def _hash_password(password: str) -> str:
    """Хеширование пароля."""
    from hashlib import sha256
    return sha256(password.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Admin:
    """Dependency: возвращает текущего администратора или 401."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin is None or not admin.is_active:
        raise credentials_exception
    return admin


def require_admin(current_admin: Admin = Depends(get_current_admin)) -> Admin:
    """Dependency: требует авторизованного админа."""
    return current_admin


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Авторизация администратора. Возвращает JWT-токен."""
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not admin or not _verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Учётная запись отключена",
        )

    access_token = create_access_token(data={"sub": admin.username})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def read_admin_me(current_admin: Admin = Depends(require_admin)):
    """Информация о текущем администраторе."""
    return {
        "id": current_admin.id,
        "username": current_admin.username,
        "is_active": current_admin.is_active,
    }


@router.post("/setup")
async def setup_admin(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    """Первичная регистрация администратора. Доступна только если админов ещё нет."""
    existing = db.query(Admin).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Администратор уже существует. Используйте логин.",
        )
    admin = Admin(username=username, hashed_password=_hash_password(password))
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {"id": admin.id, "username": admin.username, "message": "Администратор создан"}

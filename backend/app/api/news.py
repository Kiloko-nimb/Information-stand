from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.core.database import get_db
from app.models.news import News
from app.services.news_parser import fetch_news_from_website, save_news_to_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/news", tags=["news"])


# Pydantic схемы для валидации
class NewsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    icon: str
    published_date: Optional[datetime]
    source_url: Optional[str]
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=List[NewsResponse])
async def get_news(
    limit: int = 10,
    skip: int = 0,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Получить список новостей

    Args:
        limit: Количество новостей (по умолчанию 10)
        skip: Пропустить N новостей (для пагинации)
        active_only: Только активные новости
        db: Сессия БД

    Returns:
        List[NewsResponse]: Список новостей
    """
    query = db.query(News)

    if active_only:
        query = query.filter(News.is_active == True)

    news = query.order_by(News.published_date.desc()).offset(skip).limit(limit).all()

    return news


@router.get("/{news_id}", response_model=NewsResponse)
async def get_news_by_id(news_id: int, db: Session = Depends(get_db)):
    """
    Получить конкретную новость по ID

    Args:
        news_id: ID новости
        db: Сессия БД

    Returns:
        NewsResponse: Данные новости
    """
    news = db.query(News).filter(News.id == news_id).first()

    if not news:
        raise HTTPException(status_code=404, detail="Новость не найдена")

    return news


@router.post("/refresh")
async def refresh_news(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Принудительное обновление новостей с сайта колледжа

    Запускает парсинг в фоновом режиме

    Args:
        background_tasks: FastAPI background tasks
        db: Сессия БД

    Returns:
        dict: Статус операции
    """
    def update_news():
        try:
            logger.info("Запуск обновления новостей...")
            news_list = fetch_news_from_website()

            if news_list:
                save_news_to_db(news_list, db)
                logger.info(f"Обновление завершено: {len(news_list)} новостей")
            else:
                logger.warning("Не удалось загрузить новости")

        except Exception as e:
            logger.error(f"Ошибка при обновлении новостей: {e}")

    background_tasks.add_task(update_news)

    return {
        "status": "started",
        "message": "Обновление новостей запущено в фоновом режиме"
    }

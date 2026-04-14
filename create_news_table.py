"""
Скрипт для создания таблицы news в базе данных
"""
import sys
import os

# Добавляем путь к backend в sys.path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from app.core.database import engine, Base
from app.models.news import News
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_news_table():
    """Создает таблицу news в базе данных"""
    try:
        logger.info("Создание таблицы news...")
        Base.metadata.create_all(bind=engine, tables=[News.__table__])
        logger.info("✓ Таблица news успешно создана")
    except Exception as e:
        logger.error(f"✗ Ошибка при создании таблицы: {e}")
        raise

if __name__ == "__main__":
    create_news_table()

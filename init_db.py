"""
Скрипт для инициализации базы данных
"""
import sys
import os

# Добавляем backend в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.database import engine, Base
# Импортируем все модели, чтобы они зарегистрировались в Base
from app.models.schedule import Schedule
from app.models.staff import Staff
from app.models.room import Room

def init_db():
    """Создает все таблицы в базе данных"""
    print("Создание таблиц...")
    print(f"База данных: {engine.url}")

    # Удаляем старые таблицы
    Base.metadata.drop_all(bind=engine)

    # Создаем новые
    Base.metadata.create_all(bind=engine)

    print("[OK] Таблицы созданы успешно!")
    print(f"Созданные таблицы: {list(Base.metadata.tables.keys())}")

if __name__ == "__main__":
    init_db()

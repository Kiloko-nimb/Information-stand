from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import logging

logger = logging.getLogger(__name__)

# Дополнительные аргументы подключения
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

# Пул соединений для лучшей производительности
engine_kwargs = {}
if "sqlite" in settings.DATABASE_URL:
    # SQLite-specific настройки
    engine_kwargs = {
        "pool_pre_ping": True,  # Проверка соединения перед использованием
        "pool_recycle": 3600,   # Пересоздание соединений каждый час
        "connect_args": connect_args
    }
else:
    # Для PostgreSQL и других БД
    engine_kwargs = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 3600
    }

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

# Включаем WAL mode для SQLite если настроено
if "sqlite" in settings.DATABASE_URL and settings.SQLITE_WAL_MODE:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        """Включает WAL mode для лучшей конкурентности SQLite."""
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")  # Баланс между скоростью и надёжностью
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
        logger.debug("SQLite WAL mode enabled")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Генератор сессий БД с автоматическим закрытием."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Инициализация базы данных (создание таблиц)."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")

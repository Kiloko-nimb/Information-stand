from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
from pathlib import Path
from app.api import bells, schedule, staff, rooms, news, auth, admin, analytics, market
from app.core.config import settings
from app.core.database import SessionLocal, engine
from app.core.migrations import apply_pending_migrations
from app.core.exceptions import setup_exception_handlers
from app.core.rate_limit import setup_rate_limiting, limiter
from app.services.news_parser import fetch_news_from_website, save_news_to_db
from app.core.analytics import AnalyticsMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def update_news_async():
    """Асинхронная функция обновления новостей"""
    logger.info("🔄 Запуск обновления новостей...")
    db = SessionLocal()
    
    try:
        # Запускаем синхронный парсер в отдельном потоке
        news_list = await asyncio.to_thread(fetch_news_from_website)
        
        if news_list:
            await asyncio.to_thread(save_news_to_db, news_list, db)
            logger.info(f"✓ Обновление завершено: {len(news_list)} новостей")
        else:
            logger.warning("⚠ Не удалось загрузить новости")
    
    except Exception as e:
        logger.error(f"✗ Ошибка при обновлении новостей: {e}")
    finally:
        db.close()


async def sync_schedules_from_yandex():
    """Синхронизация расписания с публичной папки Яндекс.Диска."""
    public_url = settings.YANDEX_DISK_PUBLIC_URL or os.environ.get("YANDEX_DISK_PUBLIC_URL")
    if not public_url:
        return  # Фича отключена, если переменная не задана.

    download_dir = Path(
        os.environ.get("SCHEDULE_DOWNLOAD_DIR", "data/schedule-downloads")
    )
    logger.info("📥 Синхронизация расписания с Яндекс.Диска: %s", public_url)

    try:
        from app.services.yandex_disk import sync_and_import

        summary = await asyncio.to_thread(
            sync_and_import,
            public_url,
            download_dir,
            recursive=settings.YANDEX_DISK_RECURSIVE,
        )
        for day, path, added in summary:
            logger.info(
                "  %s %s → +%d записей", day.isoformat(), path.name, added
            )
        logger.info("✓ Синхронизация Яндекс.Диска завершена (%d файлов)", len(summary))
    except Exception as e:
        logger.error("✗ Ошибка синхронизации Яндекс.Диска: %s", e)


async def yandex_sync_background_task():
    """Фоновая задача: периодическая синхронизация расписания с Яндекс.Диска."""
    public_url = settings.YANDEX_DISK_PUBLIC_URL or os.environ.get("YANDEX_DISK_PUBLIC_URL")
    if not public_url:
        logger.warning(
            "⚠ Синхронизация с Яндекс.Диском НЕ запущена: не задана переменная "
            "окружения YANDEX_DISK_PUBLIC_URL. Добавь её в backend/.env "
            "(YANDEX_DISK_PUBLIC_URL=https://disk.yandex.ru/d/...) и перезапусти бэкенд."
        )
        return

    interval_hours = settings.YANDEX_DISK_SYNC_INTERVAL_HOURS
    logger.info(
        "▶ Синхронизация с Яндекс.Диском включена (интервал: %d ч)", interval_hours
    )
    await asyncio.sleep(60)  # 1 мин после старта
    await sync_schedules_from_yandex()

    while True:
        try:
            await asyncio.sleep(interval_hours * 60 * 60)
            await sync_schedules_from_yandex()
        except asyncio.CancelledError:
            logger.info("🛑 Фоновая задача синхронизации Яндекс.Диска остановлена")
            break
        except Exception as e:
            logger.error("✗ Ошибка в Yandex sync task: %s", e)
            await asyncio.sleep(60)


async def news_update_background_task():
    """Фоновая задача для периодического обновления новостей"""
    # Ждём 30 секунд после запуска, чтобы сервер успел стартовать
    await asyncio.sleep(30)
    
    # Первое обновление сразу после запуска
    await update_news_async()
    
    # Затем обновляем каждые 6 часов
    while True:
        try:
            await asyncio.sleep(6 * 60 * 60)  # 6 часов
            await update_news_async()
        except asyncio.CancelledError:
            logger.info("🛑 Фоновая задача обновления новостей остановлена")
            break
        except Exception as e:
            logger.error(f"✗ Ошибка в фоновой задаче: {e}")
            await asyncio.sleep(60)  # При ошибке ждём минуту и пробуем снова


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Startup
    logger.info("🚀 Запуск KKRIT Interactive Board API")
    try:
        # Создать недостающие таблицы (идемпотентно — существующие не трогает)
        import app.models  # noqa: F401 — регистрирует все модели в Base.metadata
        from app.core.database import Base
        Base.metadata.create_all(bind=engine)
        apply_pending_migrations(engine)
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("⚠ apply_pending_migrations упал: %s", exc)
    logger.info("📰 Запуск фоновой задачи обновления новостей (каждые 6 часов)")
    
    # Запускаем фоновые задачи
    news_task = asyncio.create_task(news_update_background_task())
    yandex_task = asyncio.create_task(yandex_sync_background_task())

    yield  # Приложение работает

    # Shutdown
    logger.info("🛑 Остановка KKRIT Interactive Board API")
    for task in (news_task, yandex_task):
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    logger.info("✓ Завершение работы")


app = FastAPI(
    title="KKRIT Interactive Board API",
    description="API для интерактивного информационного стенда ККРИТ",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - берём origins из переменных окружения
cors_origins = settings.get_cors_origins()
logger.info(f"CORS origins configured: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
setup_rate_limiting(app)

# Analytics middleware — учёт посещений
app.add_middleware(AnalyticsMiddleware)

# Глобальные обработчики исключений
setup_exception_handlers(app)

# Подключаем роутеры
app.include_router(schedule.router, prefix="/api/v1")
app.include_router(bells.router, prefix="/api/v1")
app.include_router(staff.router, prefix="/api/v1")
app.include_router(rooms.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(market.router, prefix="/api/v1")

# Статическая отдача загруженных файлов (картинки новостей и т.п.)
from fastapi.staticfiles import StaticFiles
from pathlib import Path as _PathLib
_UPLOAD_ROOT = _PathLib(__file__).resolve().parent / "uploads"
_UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_UPLOAD_ROOT)), name="uploads")


@app.get("/")
async def root():
    return {
        "message": "KKRIT Interactive Board API",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Проверка состояния сервиса."""
    health_data = {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time(),
        "services": {
            "api": "ok",
            "database": "unknown"
        }
    }

    # Проверка БД
    db = SessionLocal()
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        health_data["services"]["database"] = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_data["services"]["database"] = "error"
        health_data["status"] = "degraded"
    finally:
        db.close()

    return health_data

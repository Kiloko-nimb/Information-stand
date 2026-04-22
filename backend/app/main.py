from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from app.api import schedule, staff, rooms, news
from app.core.database import SessionLocal
from app.services.news_parser import fetch_news_from_website, save_news_to_db
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
    logger.info("📰 Запуск фоновой задачи обновления новостей (каждые 6 часов)")
    
    # Запускаем фоновую задачу
    task = asyncio.create_task(news_update_background_task())
    
    yield  # Приложение работает
    
    # Shutdown
    logger.info("🛑 Остановка KKRIT Interactive Board API")
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

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(schedule.router, prefix="/api/v1")
app.include_router(staff.router, prefix="/api/v1")
app.include_router(rooms.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "KKRIT Interactive Board API",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

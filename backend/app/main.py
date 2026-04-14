from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import schedule, staff, rooms, news
# from app.utils.scheduler import start_scheduler, stop_scheduler  # Временно отключено
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="KKRIT Interactive Board API",
    description="API для интерактивного информационного стенда ККРИТ",
    version="1.0.0"
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


@app.on_event("startup")
async def startup_event():
    """Запускается при старте приложения"""
    logger.info("🚀 Запуск KKRIT Interactive Board API")

    # Запускаем планировщик обновления новостей (каждые 6 часов)
    # start_scheduler(interval_hours=6)  # Временно отключено - APScheduler не установлен
    logger.info("⚠️ Планировщик новостей отключен (используйте POST /api/v1/news/refresh для обновления)")


@app.on_event("shutdown")
async def shutdown_event():
    """Запускается при остановке приложения"""
    logger.info("🛑 Остановка KKRIT Interactive Board API")
    # stop_scheduler()  # Временно отключено
    logger.info("✓ Завершение работы")


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

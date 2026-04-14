"""
Планировщик задач для автоматического обновления новостей
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging
from app.core.database import SessionLocal
from app.services.news_parser import fetch_news_from_website, save_news_to_db

logger = logging.getLogger(__name__)

# Глобальный планировщик
scheduler = None


def update_news_job():
    """
    Задача для обновления новостей
    Вызывается планировщиком автоматически
    """
    logger.info("Запуск автоматического обновления новостей...")
    db = SessionLocal()

    try:
        news_list = fetch_news_from_website()

        if news_list:
            save_news_to_db(news_list, db)
            logger.info(f"✓ Автообновление завершено: {len(news_list)} новостей")
        else:
            logger.warning("⚠ Не удалось загрузить новости при автообновлении")

    except Exception as e:
        logger.error(f"✗ Ошибка при автообновлении новостей: {e}")
    finally:
        db.close()


def start_scheduler(interval_hours: int = 6):
    """
    Запускает планировщик задач

    Args:
        interval_hours: Интервал обновления в часах (по умолчанию 6)
    """
    global scheduler

    if scheduler is not None:
        logger.warning("Планировщик уже запущен")
        return

    scheduler = BackgroundScheduler()

    # Добавляем задачу обновления новостей
    scheduler.add_job(
        func=update_news_job,
        trigger=IntervalTrigger(hours=interval_hours),
        id='news_update_job',
        name='Обновление новостей с сайта ККРИТ',
        replace_existing=True,
        next_run_time=datetime.now()  # Запустить сразу при старте
    )

    scheduler.start()
    logger.info(f"✓ Планировщик запущен. Обновление новостей каждые {interval_hours} часов")


def stop_scheduler():
    """
    Останавливает планировщик задач
    """
    global scheduler

    if scheduler is not None:
        scheduler.shutdown()
        scheduler = None
        logger.info("Планировщик остановлен")


def get_scheduler_status():
    """
    Получить статус планировщика

    Returns:
        dict: Информация о планировщике
    """
    if scheduler is None:
        return {"running": False}

    jobs = scheduler.get_jobs()
    return {
        "running": True,
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in jobs
        ]
    }

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class PageVisit(Base):
    """Модель для учёта посещений страниц стенда."""
    __tablename__ = "page_visits"

    id = Column(Integer, primary_key=True, index=True)
    page = Column(String(200), index=True)
    query = Column(String(200), nullable=True)
    ip = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    visited_at = Column(DateTime(timezone=True), server_default=func.now())


class PopularQuery(Base):
    """Агрегированные популярные запросы."""
    __tablename__ = "popular_queries"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(200), index=True)
    params = Column(Text, nullable=True)
    hit_count = Column(Integer, default=1)
    last_queried = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

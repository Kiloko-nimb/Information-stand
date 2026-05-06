"""
Аналитика посещений — доступна только администратору.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.api.auth import require_admin
from app.models.admin import Admin
from app.models.analytics import PageVisit, PopularQuery

router = APIRouter(prefix="/admin/analytics", tags=["analytics"])


class VisitOut(BaseModel):
    page: str
    query: Optional[str]
    visited_at: datetime

    class Config:
        from_attributes = True


class PopularQueryOut(BaseModel):
    endpoint: str
    params: Optional[str]
    hit_count: int
    last_queried: datetime

    class Config:
        from_attributes = True


class StatsOut(BaseModel):
    total_visits: int
    visits_today: int
    visits_week: int
    top_pages: List[PopularQueryOut]
    top_schedule_groups: List[PopularQueryOut]


@router.get("/stats", response_model=StatsOut)
async def get_stats(
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)

    total = db.query(func.count(PageVisit.id)).scalar() or 0
    today = db.query(func.count(PageVisit.id)).filter(PageVisit.visited_at >= today_start).scalar() or 0
    week = db.query(func.count(PageVisit.id)).filter(PageVisit.visited_at >= week_ago).scalar() or 0

    top_pages = (
        db.query(PopularQuery)
        .order_by(PopularQuery.hit_count.desc())
        .limit(10)
        .all()
    )

    # Топ запросов расписания (отдельный список — для будущих графиков)
    top_schedule = (
        db.query(PopularQuery)
        .filter(PopularQuery.endpoint.like("%/schedule/%"))
        .order_by(PopularQuery.hit_count.desc())
        .limit(10)
        .all()
    )

    return StatsOut(
        total_visits=total,
        visits_today=today,
        visits_week=week,
        top_pages=top_pages,
        top_schedule_groups=top_schedule,
    )


@router.get("/recent", response_model=List[VisitOut])
async def get_recent_visits(
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
    _admin: Admin = Depends(require_admin),
):
    return (
        db.query(PageVisit)
        .order_by(PageVisit.visited_at.desc())
        .limit(limit)
        .all()
    )

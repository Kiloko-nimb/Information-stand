from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Staff(Base):
    """Модель сотрудника колледжа"""
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    position = Column(String(255))
    department = Column(String(255))
    room_number = Column(String(50))
    photo_url = Column(String(500))
    email = Column(String(255))
    phone = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Room(Base):
    """Модель кабинета/аудитории"""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(50), unique=True, nullable=False, index=True)
    floor = Column(Integer, nullable=False)
    building = Column(String(50))
    room_type = Column(String(100))  # Аудитория, лаборатория, кабинет

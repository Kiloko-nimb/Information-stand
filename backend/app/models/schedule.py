from sqlalchemy import Column, Integer, String, Text, Date, Time
from app.core.database import Base

class Schedule(Base):
    """Модель расписания занятий"""
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(100), nullable=False, index=True)
    teacher_name = Column(String(255), index=True)
    subject = Column(String(255), nullable=False)
    room_number = Column(String(50))
    day_of_week = Column(Integer)  # 1-6 (Пн-Сб)
    lesson_number = Column(Integer)  # Номер пары
    time_start = Column(Time)
    time_end = Column(Time)
    date = Column(Date)  # Для конкретной даты
    lesson_type = Column(String(50))  # Лекция, практика, лаб

from app.core.database import SessionLocal
from app.models.schedule import Schedule
from app.models.room import Room
from app.models.staff import Staff

db = SessionLocal()

# Проверяем расписание
schedule_count = db.query(Schedule).count()
print(f'Записей в schedules: {schedule_count}')

# Проверяем аудитории
rooms_count = db.query(Room).count()
print(f'Записей в rooms: {rooms_count}')

if rooms_count > 0:
    print('\nПримеры аудиторий:')
    rooms = db.query(Room).limit(10).all()
    for room in rooms:
        print(f'  {room.room_number} - Этаж {room.floor}, {room.room_type}, {room.building}')

# Проверяем сотрудников
staff_count = db.query(Staff).count()
print(f'\nЗаписей в staff: {staff_count}')

db.close()

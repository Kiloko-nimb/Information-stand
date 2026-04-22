"""
Скрипт для заполнения таблицы rooms данными из schedules
Извлекает уникальные аудитории из расписания и добавляет их в таблицу rooms
"""
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_floor(room_number: str) -> int:
    """
    Определяет этаж по номеру аудитории
    
    Args:
        room_number: Номер аудитории
        
    Returns:
        int: Номер этажа (1-4)
    """
    # Убираем пробелы и приводим к нижнему регистру
    room_clean = room_number.strip().lower()
    
    # Специальные случаи
    if 'сп' in room_clean or 'спорт' in room_clean:
        return 1  # Спортзал обычно на первом этаже
    if 'акт' in room_clean or 'актовый' in room_clean:
        return 1  # Актовый зал на первом этаже
    
    # Пытаемся извлечь первую цифру из номера
    for char in room_number:
        if char.isdigit():
            floor = int(char)
            # Проверяем, что этаж в разумных пределах (1-4)
            if 1 <= floor <= 4:
                return floor
            # Если первая цифра 0, то это первый этаж
            if floor == 0:
                return 1
    
    # По умолчанию первый этаж
    return 1


def get_room_type(room_number: str) -> str:
    """
    Определяет тип аудитории по номеру
    
    Args:
        room_number: Номер аудитории
        
    Returns:
        str: Тип аудитории
    """
    room_lower = room_number.lower()
    
    if 'сп' in room_lower or 'спорт' in room_lower:
        return 'Спортзал'
    elif 'акт' in room_lower or 'актовый' in room_lower:
        return 'Актовый зал'
    elif 'лаб' in room_lower:
        return 'Лаборатория'
    else:
        return 'Аудитория'


def get_building(room_number: str) -> str:
    """
    Определяет корпус по номеру аудитории
    
    Args:
        room_number: Номер аудитории
        
    Returns:
        str: Название корпуса
    """
    # Если номер начинается с 4, это может быть другой корпус
    if room_number.startswith('4'):
        return 'пр. Свободный 67'
    else:
        return 'пр. Красноярский Рабочий 156'


def populate_rooms():
    """Заполняет таблицу rooms данными из schedules"""
    
    logger.info("🔄 Начало заполнения таблицы rooms...")
    
    # Подключаемся к базе данных
    conn = sqlite3.connect('backend/kkrit.db')
    cursor = conn.cursor()
    
    try:
        # Проверяем текущее количество записей
        cursor.execute('SELECT COUNT(*) FROM rooms')
        current_count = cursor.fetchone()[0]
        logger.info(f"📊 Текущее количество записей в rooms: {current_count}")
        
        # Получаем уникальные аудитории из расписания
        cursor.execute('''
            SELECT DISTINCT room_number 
            FROM schedules 
            WHERE room_number IS NOT NULL 
            AND room_number != ''
            ORDER BY room_number
        ''')
        
        rooms = cursor.fetchall()
        logger.info(f"📋 Найдено уникальных аудиторий в расписании: {len(rooms)}")
        
        # Счётчики
        added_count = 0
        skipped_count = 0
        
        # Вставляем данные в таблицу rooms
        for room in rooms:
            room_number = room[0]
            
            # Проверяем, существует ли уже такая аудитория
            cursor.execute('SELECT id FROM rooms WHERE room_number = ?', (room_number,))
            existing = cursor.fetchone()
            
            if existing:
                logger.info(f"⏭️  Аудитория {room_number} уже существует, пропускаем")
                skipped_count += 1
                continue
            
            # Определяем параметры аудитории
            floor = get_floor(room_number)
            room_type = get_room_type(room_number)
            building = get_building(room_number)
            
            # Вставляем запись
            cursor.execute('''
                INSERT INTO rooms (room_number, floor, room_type, building)
                VALUES (?, ?, ?, ?)
            ''', (room_number, floor, room_type, building))
            
            logger.info(f"✓ Добавлена аудитория: {room_number} (Этаж: {floor}, Тип: {room_type}, Корпус: {building})")
            added_count += 1
        
        # Сохраняем изменения
        conn.commit()
        
        # Проверяем итоговое количество
        cursor.execute('SELECT COUNT(*) FROM rooms')
        final_count = cursor.fetchone()[0]
        
        logger.info("=" * 60)
        logger.info(f"✅ Заполнение завершено!")
        logger.info(f"📊 Добавлено новых аудиторий: {added_count}")
        logger.info(f"⏭️  Пропущено (уже существуют): {skipped_count}")
        logger.info(f"📈 Итого записей в таблице rooms: {final_count}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при заполнении таблицы rooms: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()


if __name__ == "__main__":
    populate_rooms()

"""
Скрипт для загрузки расписания в БД
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime, time

import pdfplumber

from app.core.database import SessionLocal
from app.models.schedule import Schedule

# Время пар
LESSON_TIMES = {
    1: (time(8, 10), time(8, 55)),
    2: (time(9, 0), time(9, 45)),
    3: (time(9, 50), time(10, 35)),
    4: (time(10, 45), time(11, 30)),
    5: (time(11, 35), time(12, 20)),
    6: (time(13, 0), time(13, 45)),
    7: (time(13, 50), time(14, 35)),
}

def parse_cell_data(cell_text):
    """Парсит данные из ячейки расписания"""
    if not cell_text or cell_text.strip() == "":
        return None

    lines = [line.strip() for line in cell_text.split('\n') if line.strip()]

    if len(lines) < 2:
        return None

    # Первая строка - предмет
    subject = lines[0]

    # Последняя строка обычно содержит преподавателя
    teacher = lines[-1] if len(lines) > 1 else ""

    # Ищем номер кабинета (обычно содержит цифры)
    room = ""
    for line in lines:
        if any(char.isdigit() for char in line) and len(line) < 10:
            room = line
            break

    return {
        'subject': subject,
        'teacher': teacher,
        'room': room
    }

def parse_and_load_schedule():
    """Парсит PDF и загружает расписание в БД"""

    db = SessionLocal()

    try:
        with pdfplumber.open('13.04.2026.pdf') as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()

            if not tables:
                print("Таблицы не найдены")
                return

            table = tables[0]

            # Первая строка - заголовки с группами
            headers = table[0]
            groups = [h.strip() for h in headers[2:] if h and h.strip()]  # Пропускаем первые 2 колонки

            print(f"Найдено групп: {len(groups)}")
            print(f"Группы: {groups[:5]}...")  # Показываем первые 5

            lesson_number = 0
            records_added = 0

            # Обрабатываем строки с расписанием
            for row in table[2:]:  # Пропускаем заголовки
                if not row or len(row) < 3:
                    continue

                # Первая колонка - номер пары
                if row[0] and row[0].strip().isdigit():
                    lesson_number = int(row[0].strip())

                if lesson_number == 0 or lesson_number not in LESSON_TIMES:
                    continue

                # Обрабатываем каждую группу
                for i, cell in enumerate(row[2:]):  # Пропускаем первые 2 колонки
                    if i >= len(groups):
                        break

                    data = parse_cell_data(cell)

                    if not data:
                        continue

                    time_start, time_end = LESSON_TIMES[lesson_number]

                    schedule = Schedule(
                        group_name=groups[i],
                        teacher_name=data['teacher'],
                        subject=data['subject'],
                        room_number=data['room'],
                        day_of_week=6,  # Суббота (13.04.2026)
                        lesson_number=lesson_number,
                        time_start=time_start,
                        time_end=time_end,
                        date=datetime(2026, 4, 13).date(),
                        lesson_type="Занятие"
                    )

                    db.add(schedule)
                    records_added += 1

            db.commit()

            # Подсчитываем количество записей
            count = db.query(Schedule).count()
            print(f"\n[OK] Добавлено {records_added} записей")
            print(f"[OK] Всего в БД: {count} записей расписания")

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    parse_and_load_schedule()

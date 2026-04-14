import pandas as pd
from datetime import datetime, time
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.schedule import Schedule

# Расписание звонков
TIME_SLOTS = {
    0: ("08:00", "08:10"),  # Линейка
    1: ("08:10", "08:55"),
    2: ("09:00", "09:45"),
    3: ("10:45", "11:30"),
    4: ("13:00", "13:45"),
    5: ("14:45", "15:30"),
    6: ("16:30", "17:15"),
    7: ("18:15", "19:00"),
}

def parse_time(time_str):
    """Парсинг времени из строки"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except:
        return None

def clean_text(text):
    """Очистка текста от лишних символов"""
    if pd.isna(text) or text == '':
        return None
    return str(text).strip()

def import_schedule_from_excel(file_path: str, date_str: str = "2026-04-13"):
    """
    Импорт расписания из Excel файла

    Args:
        file_path: путь к Excel файлу
        date_str: дата в формате YYYY-MM-DD
    """
    db = SessionLocal()

    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path)

        # Удаляем первую строку (заголовок с номерами)
        df = df.iloc[1:]

        # Получаем список групп из заголовков столбцов
        groups = []
        for i in range(2, len(df.columns), 2):  # Каждая группа занимает 2 столбца (предмет, аудитория)
            group_name = df.columns[i]
            if pd.notna(group_name) and group_name != '':
                groups.append({
                    'name': group_name,
                    'subject_col': i,
                    'room_col': i + 1
                })

        schedule_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Удаляем старое расписание на эту дату
        db.query(Schedule).filter(Schedule.date == schedule_date).delete()

        # Обрабатываем каждую строку (пару)
        for idx, row in df.iterrows():
            lesson_num = row.iloc[0]  # Номер пары
            time_range = row.iloc[1]  # Время

            # Пропускаем пустые строки и перерывы
            if pd.isna(lesson_num) or lesson_num == '':
                continue

            try:
                lesson_num = int(float(lesson_num))
            except:
                continue

            # Парсим время
            if pd.notna(time_range) and ':' in str(time_range):
                times = str(time_range).split('-')
                if len(times) == 2:
                    time_start = parse_time(times[0].strip())
                    time_end = parse_time(times[1].strip())
                else:
                    continue
            else:
                continue

            # Обрабатываем каждую группу
            for group in groups:
                subject = clean_text(row.iloc[group['subject_col']])
                room = clean_text(row.iloc[group['room_col']])

                # Пропускаем пустые ячейки
                if not subject:
                    continue

                # Извлекаем имя преподавателя (обычно в конце строки)
                teacher_name = None
                if subject:
                    # Ищем ФИО в формате "Фамилия И.О."
                    parts = subject.split()
                    if len(parts) >= 2:
                        # Последние 2-3 слова могут быть ФИО
                        potential_name = ' '.join(parts[-3:]) if len(parts) >= 3 else ' '.join(parts[-2:])
                        # Проверяем, есть ли точки (признак инициалов)
                        if '.' in potential_name:
                            teacher_name = potential_name
                            # Убираем ФИО из названия предмета
                            subject = ' '.join(parts[:-3] if len(parts) >= 3 else parts[:-2])

                # Создаем запись расписания
                schedule_entry = Schedule(
                    group_name=group['name'],
                    teacher_name=teacher_name,
                    subject=subject,
                    room_number=room,
                    lesson_number=lesson_num,
                    time_start=time_start,
                    time_end=time_end,
                    date=schedule_date,
                    day_of_week=schedule_date.weekday() + 1  # 1 = Понедельник
                )

                db.add(schedule_entry)

        db.commit()
        print(f"[OK] Расписание успешно импортировано: {len(groups)} групп")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Ошибка импорта: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Использование: python import_schedule.py <путь_к_файлу.xlsx> [дата YYYY-MM-DD]")
        sys.exit(1)

    file_path = sys.argv[1]
    date_str = sys.argv[2] if len(sys.argv) > 2 else "2026-04-13"

    import_schedule_from_excel(file_path, date_str)

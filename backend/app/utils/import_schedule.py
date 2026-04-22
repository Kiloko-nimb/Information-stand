"""
Импорт расписания из Excel (.xlsx) или PDF (.pdf) в БД.

Публичное API:
- ``import_schedule_from_excel(file_path, date_str)`` — импорт из Excel.
- ``import_schedule_from_pdf(file_path, date_str)`` — импорт из PDF.
- ``import_schedule(file_path, date_str=None)`` — автоматический выбор
  парсера по расширению файла.
"""
import argparse
import os
from datetime import date, datetime, time

import pandas as pd
import pdfplumber

from app.core.database import SessionLocal
from app.models.schedule import Schedule

# Расписание звонков для понедельника
MONDAY_SCHEDULE = {
    0: ("08:00", "08:10"),  # Линейка
    1: ("08:10", "08:55"),  # Классный час
    2: ("09:00", "09:45"),  # 1 пара - слот 1
    3: ("09:50", "10:35"),  # 1 пара - слот 2
    4: ("10:45", "11:30"),  # 2 пара - слот 1
    5: ("11:35", "12:20"),  # 2 пара - слот 2
    # Обед 12:20-13:00
    6: ("13:00", "13:45"),  # 3 пара - слот 1
    7: ("13:50", "14:35"),  # 3 пара - слот 2
    8: ("14:45", "15:30"),  # 4 пара - слот 1
    9: ("15:35", "16:20"),  # 4 пара - слот 2
    10: ("16:30", "17:15"), # 5 пара - слот 1
    11: ("17:20", "18:05"), # 5 пара - слот 2
    12: ("18:15", "19:00"), # 6 пара - слот 1
    13: ("19:05", "19:50"), # 6 пара - слот 2
    14: ("20:00", "20:45"), # 7 пара - слот 1
    15: ("20:50", "21:35"), # 7 пара - слот 2
}

# Расписание звонков для вторника-субботы
REGULAR_SCHEDULE = {
    1: ("08:00", "08:45"),  # 1 пара - слот 1
    2: ("08:50", "09:35"),  # 1 пара - слот 2
    3: ("09:45", "10:30"),  # 2 пара - слот 1
    4: ("10:35", "11:20"),  # 2 пара - слот 2
    # Обед 11:20-12:00
    5: ("12:00", "12:45"),  # 3 пара - слот 1
    6: ("12:50", "13:35"),  # 3 пара - слот 2
    7: ("13:45", "14:30"),  # 4 пара - слот 1
    8: ("14:35", "15:20"),  # 4 пара - слот 2
    9: ("15:30", "16:15"),  # 5 пара - слот 1
    10: ("16:20", "17:05"), # 5 пара - слот 2
    11: ("17:15", "18:00"), # 6 пара - слот 1
    12: ("18:05", "18:50"), # 6 пара - слот 2
    13: ("19:00", "19:45"), # 7 пара - слот 1
    14: ("19:50", "20:35"), # 7 пара - слот 2
}

# Время пар для PDF-файла (одна пара = один номер)
PDF_LESSON_TIMES = {
    1: (time(8, 10), time(8, 55)),
    2: (time(9, 0), time(9, 45)),
    3: (time(9, 50), time(10, 35)),
    4: (time(10, 45), time(11, 30)),
    5: (time(11, 35), time(12, 20)),
    6: (time(13, 0), time(13, 45)),
    7: (time(13, 50), time(14, 35)),
}


def get_time_slots_for_day(day_of_week: int) -> dict:
    """Возвращает расписание звонков в зависимости от дня недели"""
    return MONDAY_SCHEDULE if day_of_week == 1 else REGULAR_SCHEDULE


def parse_time(time_str):
    """Парсинг времени из строки"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except Exception:
        return None


def clean_text(text):
    """Очистка текста от лишних символов"""
    if pd.isna(text) or text == '':
        return None
    return str(text).strip()


def _parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def import_schedule_from_excel(file_path: str, date_str: str = "2026-04-13"):
    """
    Импорт расписания из Excel файла.

    Args:
        file_path: путь к Excel файлу.
        date_str: дата в формате YYYY-MM-DD.
    """
    db = SessionLocal()

    try:
        schedule_date = _parse_date(date_str)

        excel_file = pd.ExcelFile(file_path)
        print(f"Найдено листов: {len(excel_file.sheet_names)}")

        # Удаляем старое расписание на эту дату
        db.query(Schedule).filter(Schedule.date == schedule_date).delete()

        total_groups = 0

        for sheet_name in excel_file.sheet_names:
            print(f"Обработка листа: {sheet_name}")
            df = pd.read_excel(excel_file, sheet_name=sheet_name)

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

            total_groups += len(groups)
            print(f"  Найдено групп: {len(groups)}")

            # Получаем день недели и соответствующее расписание
            day_of_week = schedule_date.weekday() + 1  # 1 = Понедельник
            time_slots = get_time_slots_for_day(day_of_week)

            # Обрабатываем каждую строку (пару)
            for idx, row in df.iterrows():
                lesson_num = row.iloc[0]  # Номер пары

                # Пропускаем пустые строки и перерывы
                if pd.isna(lesson_num) or lesson_num == '':
                    continue

                try:
                    lesson_num = int(float(lesson_num))
                except Exception:
                    continue

                # Получаем время из расписания по номеру строки
                row_index = idx - 1  # Корректируем индекс (т.к. первая строка удалена)
                if row_index in time_slots:
                    time_start_str, time_end_str = time_slots[row_index]
                    time_start = parse_time(time_start_str)
                    time_end = parse_time(time_end_str)
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

                    # Проверяем на дубликаты
                    existing = db.query(Schedule).filter(
                        Schedule.group_name == group['name'],
                        Schedule.date == schedule_date,
                        Schedule.lesson_number == lesson_num,
                        Schedule.time_start == time_start
                    ).first()

                    if existing:
                        continue  # Пропускаем дубликат

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
                        day_of_week=day_of_week
                    )

                    db.add(schedule_entry)

        db.commit()
        print(f"[OK] Расписание успешно импортировано: {total_groups} групп из {len(excel_file.sheet_names)} листов")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Ошибка импорта: {e}")
        raise
    finally:
        db.close()


def _parse_pdf_cell(cell_text):
    """Парсит ячейку расписания из PDF."""
    if not cell_text or cell_text.strip() == "":
        return None

    lines = [line.strip() for line in cell_text.split('\n') if line.strip()]
    if len(lines) < 2:
        return None

    subject = lines[0]
    teacher = lines[-1] if len(lines) > 1 else ""

    # Ищем номер кабинета (короткая строка с цифрами)
    room = ""
    for line in lines:
        if any(ch.isdigit() for ch in line) and len(line) < 10:
            room = line
            break

    return {'subject': subject, 'teacher': teacher, 'room': room}


def import_schedule_from_pdf(file_path: str, date_str: str = "2026-04-13"):
    """
    Импорт расписания из PDF (одна страница = один день).

    Args:
        file_path: путь к PDF-файлу.
        date_str: дата в формате YYYY-MM-DD.
    """
    schedule_date = _parse_date(date_str)
    day_of_week = schedule_date.weekday() + 1

    db = SessionLocal()

    try:
        with pdfplumber.open(file_path) as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()

            if not tables:
                print("Таблицы не найдены")
                return

            table = tables[0]
            headers = table[0]
            # Пропускаем первые 2 колонки (номер пары, время)
            groups = [h.strip() for h in headers[2:] if h and h.strip()]

            print(f"Найдено групп: {len(groups)}")

            # Удаляем старое расписание на эту дату
            db.query(Schedule).filter(Schedule.date == schedule_date).delete()

            lesson_number = 0
            records_added = 0

            for row in table[2:]:  # Пропускаем заголовки
                if not row or len(row) < 3:
                    continue

                if row[0] and row[0].strip().isdigit():
                    lesson_number = int(row[0].strip())

                if lesson_number == 0 or lesson_number not in PDF_LESSON_TIMES:
                    continue

                for i, cell in enumerate(row[2:]):
                    if i >= len(groups):
                        break

                    data = _parse_pdf_cell(cell)
                    if not data:
                        continue

                    time_start, time_end = PDF_LESSON_TIMES[lesson_number]

                    db.add(Schedule(
                        group_name=groups[i],
                        teacher_name=data['teacher'],
                        subject=data['subject'],
                        room_number=data['room'],
                        day_of_week=day_of_week,
                        lesson_number=lesson_number,
                        time_start=time_start,
                        time_end=time_end,
                        date=schedule_date,
                        lesson_type="Занятие",
                    ))
                    records_added += 1

            db.commit()
            total = db.query(Schedule).count()
            print(f"[OK] Добавлено {records_added} записей; всего в БД: {total}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Ошибка импорта PDF: {e}")
        raise
    finally:
        db.close()


def import_schedule(file_path: str, date_str: str = "2026-04-13"):
    """
    Универсальный импорт расписания. Выбирает парсер по расширению файла.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext in {".xlsx", ".xls"}:
        return import_schedule_from_excel(file_path, date_str)
    if ext == ".pdf":
        return import_schedule_from_pdf(file_path, date_str)
    raise ValueError(
        f"Неподдерживаемое расширение файла: {ext!r}. Ожидается .xlsx, .xls или .pdf."
    )


def _main():
    parser = argparse.ArgumentParser(
        description="Импорт расписания из Excel или PDF в БД."
    )
    parser.add_argument("file", help="Путь к файлу расписания (.xlsx / .xls / .pdf)")
    parser.add_argument(
        "--date",
        default="2026-04-13",
        help="Дата расписания в формате YYYY-MM-DD (по умолчанию 2026-04-13)",
    )
    args = parser.parse_args()
    import_schedule(args.file, args.date)


if __name__ == "__main__":
    _main()

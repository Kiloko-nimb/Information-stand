"""
Скрипт для парсинга расписания из PDF и загрузки в БД
"""
import sys
sys.path.append('backend')

import pdfplumber
from datetime import datetime, time
from backend.app.core.database import SessionLocal
from backend.app.models.schedule import Schedule

def parse_schedule_pdf(pdf_path: str):
    """Парсит PDF с расписанием"""
    print(f"Открываем файл: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        print(f"Страниц в PDF: {len(pdf.pages)}")

        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\n=== Страница {page_num} ===")

            # Извлекаем таблицы
            tables = page.extract_tables()
            print(f"Найдено таблиц: {len(tables)}")

            if tables:
                table = tables[0]
                print(f"Строк в таблице: {len(table)}")

                # Показываем первые несколько строк для анализа структуры
                print("\nПервые 5 строк таблицы:")
                for i, row in enumerate(table[:5]):
                    print(f"Строка {i}: {row[:3]}...")  # Первые 3 колонки

                return table

    return None

def load_schedule_to_db(table_data):
    """Загружает данные расписания в БД"""
    db = SessionLocal()

    try:
        # Пример: создаем тестовые записи
        # TODO: Адаптировать под реальную структуру таблицы из PDF

        test_schedule = Schedule(
            group_name="ИС.09.01",
            teacher_name="Иванов И.И.",
            subject="Программирование",
            room_number="305",
            day_of_week=1,  # Понедельник
            lesson_number=1,
            time_start=time(8, 10),
            time_end=time(8, 55),
            date=datetime(2026, 4, 13).date(),
            lesson_type="Лекция"
        )

        db.add(test_schedule)
        db.commit()
        print("✓ Тестовая запись добавлена в БД")

    except Exception as e:
        print(f"Ошибка при загрузке в БД: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    pdf_path = "13.04.2026.pdf"

    # Парсим PDF
    table = parse_schedule_pdf(pdf_path)

    if table:
        print("\n" + "="*50)
        print("PDF успешно распарсен!")
        print("="*50)

        # Загружаем в БД
        # load_schedule_to_db(table)
        print("\nДля загрузки в БД нужно адаптировать структуру под реальные данные")

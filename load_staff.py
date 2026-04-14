"""
Скрипт для загрузки педагогического состава в БД
"""
import sys
sys.path.append('backend')

from docx import Document
from backend.app.core.database import SessionLocal
from backend.app.models.staff import Staff

def parse_and_load_staff():
    """Парсит DOCX и загружает данные в БД"""
    doc = Document('ped._sostav_dlya_sayta_10.09.2025.docx')

    db = SessionLocal()

    try:
        # Получаем таблицу
        table = doc.tables[0]

        print(f"Обработка {len(table.rows)} строк...")

        # Пропускаем заголовок (первые 2 строки)
        for i, row in enumerate(table.rows[2:], start=1):
            cells = [cell.text.strip() for cell in row.cells]

            if len(cells) < 3 or not cells[0]:
                continue

            full_name = cells[0]
            position = cells[1]
            department = cells[2] if len(cells) > 2 else ""

            # Пропускаем пустые строки
            if not full_name or full_name == "Ф.И.О.":
                continue

            # Создаем запись
            staff = Staff(
                full_name=full_name,
                position=position,
                department=department,
                room_number="",  # В файле нет информации о кабинетах
                email="",
                phone=""
            )

            db.add(staff)

            if i % 10 == 0:
                print(f"Обработано {i} записей...")

        db.commit()

        # Подсчитываем количество записей
        count = db.query(Staff).count()
        print(f"\n[OK] Загружено {count} сотрудников в БД")

    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    parse_and_load_staff()

"""
Импорт расписания из Excel (.xlsx) или PDF (.pdf) в БД.

Единый источник правды для тайминга пар — ``app.core.bell_schedule``.
Модуль сам не знает, во сколько начинаются пары: он берёт тайминги из
расписания звонков по дню недели (``schedule_date.weekday()+1``).

Публичное API:
- ``import_schedule_from_excel(file_path, date_str)`` — импорт из Excel.
- ``import_schedule_from_pdf(file_path, date_str)`` — импорт из PDF.
- ``import_schedule(file_path, date_str=None)`` — автоматический выбор
  парсера по расширению файла.
"""
import argparse
import os
import re
from datetime import date, datetime
from typing import List, Optional, Tuple

import pandas as pd
import pdfplumber

from app.core.bell_schedule import PairTiming, get_bell_schedule
from app.core.database import SessionLocal
from app.models.schedule import Schedule


# "Фамилия И.О." или "Фамилия-Двойная И.О." в конце строки.
# Допускаем пробел или его отсутствие между инициалами и точками.
_TEACHER_RE = re.compile(
    r"""
    (?P<teacher>
        [А-ЯЁ][а-яёА-ЯЁ\-]+   # Фамилия (возможна двойная через дефис)
        \s+
        [А-ЯЁ]\.\s*[А-ЯЁ]\.?  # И.О. или И. О.
    )
    \s*$
    """,
    re.VERBOSE,
)

# Маркеры типа занятия. Если в тексте встречается один из них, выставляем
# lesson_type. Сначала проверяем более специфичные (лаб/практ), потом лекцию.
_LESSON_TYPE_MARKERS: Tuple[Tuple[str, str], ...] = (
    ("лаборатор", "Лабораторная"),
    (" лр ", "Лабораторная"),
    ("практик", "Практика"),
    (" пр ", "Практика"),
    ("лекци", "Лекция"),
    (" лк ", "Лекция"),
)


def _clean(value) -> Optional[str]:
    """Нормализовать содержимое ячейки: убрать NaN, пробелы, многострочность."""
    if value is None:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None
    # Заменяем переносы строк одним пробелом и схлопываем множественные пробелы.
    text = re.sub(r"\s+", " ", text.replace("\r", " ").replace("\n", " "))
    return text or None


def _split_subject_and_teacher(text: str) -> Tuple[str, Optional[str]]:
    """
    Извлечь ФИО преподавателя из конца строки.

    Возвращает ``(subject, teacher)``. Если ФИО не найдено — ``teacher=None``,
    а ``subject`` — исходный текст без изменений.
    """
    m = _TEACHER_RE.search(text)
    if not m:
        return text.strip(), None
    teacher = re.sub(r"\s+", " ", m.group("teacher")).strip()
    subject = text[: m.start()].strip()
    return subject or text.strip(), teacher


def _pick_room(rooms: List[str]) -> Optional[str]:
    """Выбрать номер кабинета из нескольких значений (для слотов пары)."""
    unique = []
    for r in rooms:
        if r and r not in unique:
            unique.append(r)
    if not unique:
        return None
    if len(unique) == 1:
        return unique[0]
    return "/".join(unique)


def _infer_lesson_type(subject: str) -> Optional[str]:
    """Грубая эвристика по тексту предмета."""
    if not subject:
        return None
    lower = " " + subject.lower() + " "
    for marker, label in _LESSON_TYPE_MARKERS:
        if marker in lower:
            return label
    return None


def _parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def _collect_group_columns(
    header_row: pd.Series,
) -> List[Tuple[str, int, int]]:
    """Вытащить (group_name, subject_col, room_col) из первой строки листа."""
    groups: List[Tuple[str, int, int]] = []
    # Первые две колонки — это «Пара» и «Расписание звонков».
    for i in range(2, len(header_row), 2):
        name = _clean(header_row.iloc[i])
        if not name or name.lower().startswith("ауд"):
            continue
        if i + 1 >= len(header_row):
            break
        groups.append((name, i, i + 1))
    return groups


def _iter_pair_rows(df: pd.DataFrame):
    """
    Итератор по парам в листе Excel.

    Yield ``(lesson_number, [row_slot1, row_slot2, ...])``. Каждая пара
    обычно занимает 2 строки (слот 1 и слот 2). Первая строка помечена
    числом в колонке «Пара» (col 0), последующие строки-слоты имеют там
    пустое значение, но непустой столбец «Расписание звонков» (col 1).
    """
    n = len(df)
    i = 1  # пропускаем строку заголовков (row 0)
    while i < n:
        row = df.iloc[i]
        col0 = _clean(row.iloc[0])
        col1 = _clean(row.iloc[1])

        # Пустая строка — пропускаем.
        if not col0 and not col1:
            i += 1
            continue

        # Первая строка пары: в col[0] лежит номер пары.
        if col0 is not None and col0.isdigit():
            lesson_number = int(col0)
            slots = [row]
            j = i + 1
            while j < n:
                nrow = df.iloc[j]
                ncol0 = _clean(nrow.iloc[0])
                ncol1 = _clean(nrow.iloc[1])
                if ncol0 and ncol0.isdigit():
                    break  # началась следующая пара
                if ncol1:
                    slots.append(nrow)  # второй слот этой пары
                    j += 1
                else:
                    break
            yield lesson_number, slots
            i = j
        else:
            i += 1


def _extract_lesson_for_group(
    slots: List[pd.Series], subj_col: int, room_col: int
) -> Optional[Tuple[str, Optional[str], Optional[str]]]:
    """Собрать (subject, teacher, room) для группы из слотов пары."""
    texts: List[str] = []
    rooms: List[str] = []
    for slot in slots:
        if subj_col < len(slot):
            t = _clean(slot.iloc[subj_col])
            if t:
                texts.append(t)
        if room_col < len(slot):
            r = _clean(slot.iloc[room_col])
            if r:
                rooms.append(r)

    if not texts:
        return None

    # Часто второй слот дублирует текст первого — дедуплицируем.
    dedup: List[str] = []
    for t in texts:
        if t not in dedup:
            dedup.append(t)
    combined = " ".join(dedup)

    subject, teacher = _split_subject_and_teacher(combined)
    room = _pick_room(rooms)
    return subject, teacher, room


def import_schedule_from_excel(
    file_path: str, date_str: str = "2026-04-13"
) -> int:
    """
    Импорт расписания из Excel.

    Args:
        file_path: путь к .xlsx / .xls.
        date_str: дата в формате YYYY-MM-DD.

    Returns:
        количество добавленных записей.
    """
    schedule_date = _parse_date(date_str)
    day_of_week = schedule_date.weekday() + 1  # 1=Пн ... 7=Вс

    bell = get_bell_schedule(day_of_week)
    if not bell:
        raise ValueError(
            f"Нет расписания звонков для {schedule_date} (воскресенье?)"
        )
    bell_by_number = {p.lesson_number: p for p in bell}

    db = SessionLocal()
    records_added = 0

    try:
        # Снимаем старое расписание на эту дату, чтобы повторный импорт был
        # идемпотентным.
        db.query(Schedule).filter(Schedule.date == schedule_date).delete()

        excel_file = pd.ExcelFile(file_path)
        print(f"Найдено листов: {len(excel_file.sheet_names)}")

        total_groups = 0

        for sheet_name in excel_file.sheet_names:
            print(f"Обработка листа: {sheet_name}")
            df = pd.read_excel(
                excel_file, sheet_name=sheet_name, header=None, dtype=str
            )
            if df.empty:
                continue

            groups = _collect_group_columns(df.iloc[0])
            total_groups += len(groups)
            print(f"  Найдено групп: {len(groups)}")

            for lesson_number, slots in _iter_pair_rows(df):
                pair_timing: Optional[PairTiming] = bell_by_number.get(
                    lesson_number
                )
                if pair_timing is None:
                    # Не в расписании звонков (например, пара номер 8) — пропускаем.
                    continue

                for group_name, subj_col, room_col in groups:
                    extracted = _extract_lesson_for_group(slots, subj_col, room_col)
                    if extracted is None:
                        continue
                    subject, teacher, room = extracted

                    db.add(
                        Schedule(
                            group_name=group_name,
                            teacher_name=teacher,
                            subject=subject,
                            room_number=room,
                            day_of_week=day_of_week,
                            lesson_number=lesson_number,
                            time_start=pair_timing.start,
                            time_end=pair_timing.end,
                            date=schedule_date,
                            lesson_type=_infer_lesson_type(subject),
                        )
                    )
                    records_added += 1

        db.commit()
        print(
            f"[OK] Импортировано {records_added} записей "
            f"({total_groups} групп на {len(excel_file.sheet_names)} листах)"
        )
        return records_added

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Ошибка импорта: {e}")
        raise
    finally:
        db.close()


def _parse_pdf_cell(cell_text: Optional[str]) -> Optional[dict]:
    """Разобрать ячейку расписания из PDF в {subject, teacher, room}."""
    if not cell_text:
        return None
    text = _clean(cell_text)
    if not text:
        return None

    # В PDF часто номер кабинета идёт отдельной короткой строкой — попробуем
    # вычленить его. Но если формат разный — просто парсим как Excel-ячейку.
    subject, teacher = _split_subject_and_teacher(text)
    # Пробуем найти отдельное короткое поле-номер кабинета.
    room_match = re.search(r"\b(\d{2,4}[А-ЯЁа-яё/]*)\b\s*$", subject)
    room: Optional[str] = None
    if room_match:
        room = room_match.group(1)
        subject = subject[: room_match.start()].strip()

    return {"subject": subject, "teacher": teacher, "room": room}


def import_schedule_from_pdf(
    file_path: str, date_str: str = "2026-04-13"
) -> int:
    """
    Импорт расписания из PDF.

    Args:
        file_path: путь к PDF.
        date_str: дата в формате YYYY-MM-DD.

    Returns:
        количество добавленных записей.
    """
    schedule_date = _parse_date(date_str)
    day_of_week = schedule_date.weekday() + 1

    bell = get_bell_schedule(day_of_week)
    if not bell:
        raise ValueError(
            f"Нет расписания звонков для {schedule_date} (воскресенье?)"
        )
    bell_by_number = {p.lesson_number: p for p in bell}

    db = SessionLocal()
    records_added = 0

    try:
        with pdfplumber.open(file_path) as pdf:
            if not pdf.pages:
                print("Файл PDF пуст")
                return 0
            page = pdf.pages[0]
            tables = page.extract_tables()

            if not tables:
                print("Таблицы в PDF не найдены")
                return 0

            table = tables[0]
            headers = table[0]
            # Пропускаем первые 2 колонки (номер пары, время).
            groups = [h.strip() for h in headers[2:] if h and h.strip()]
            print(f"Найдено групп: {len(groups)}")

            db.query(Schedule).filter(Schedule.date == schedule_date).delete()

            lesson_number = 0
            for row in table[2:]:
                if not row or len(row) < 3:
                    continue

                first = (row[0] or "").strip()
                if first.isdigit():
                    lesson_number = int(first)

                pair_timing: Optional[PairTiming] = bell_by_number.get(
                    lesson_number
                )
                if pair_timing is None:
                    continue

                for i, cell in enumerate(row[2:]):
                    if i >= len(groups):
                        break
                    data = _parse_pdf_cell(cell)
                    if not data:
                        continue
                    db.add(
                        Schedule(
                            group_name=groups[i],
                            teacher_name=data["teacher"],
                            subject=data["subject"],
                            room_number=data["room"],
                            day_of_week=day_of_week,
                            lesson_number=lesson_number,
                            time_start=pair_timing.start,
                            time_end=pair_timing.end,
                            date=schedule_date,
                            lesson_type=_infer_lesson_type(data["subject"]),
                        )
                    )
                    records_added += 1

            db.commit()
            print(f"[OK] Импортировано из PDF: {records_added} записей")
            return records_added

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Ошибка импорта PDF: {e}")
        raise
    finally:
        db.close()


def import_schedule(file_path: str, date_str: str = "2026-04-13") -> int:
    """
    Универсальный импорт. Выбирает парсер по расширению файла.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext in {".xlsx", ".xls"}:
        return import_schedule_from_excel(file_path, date_str)
    if ext == ".pdf":
        return import_schedule_from_pdf(file_path, date_str)
    raise ValueError(
        f"Неподдерживаемое расширение файла: {ext!r}. "
        f"Ожидается .xlsx, .xls или .pdf."
    )


def _main():
    parser = argparse.ArgumentParser(
        description="Импорт расписания из Excel или PDF в БД."
    )
    parser.add_argument(
        "file", help="Путь к файлу расписания (.xlsx / .xls / .pdf)"
    )
    parser.add_argument(
        "--date",
        default="2026-04-13",
        help="Дата расписания в формате YYYY-MM-DD (по умолчанию 2026-04-13)",
    )
    args = parser.parse_args()
    import_schedule(args.file, args.date)


if __name__ == "__main__":
    _main()

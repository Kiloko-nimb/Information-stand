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
from app.utils.group_names import is_valid_group_name
from app.utils.room_names import normalize_room_number


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
    # pandas nullable-string dtype и обычные float-NaN: всё через pd.isna.
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    if not text:
        return None
    # <NA> от pandas StringDtype после astype("string"), либо текстовое "nan".
    if text in ("<NA>", "NA", "nan", "NaN", "None"):
        return None
    # Переносы строк → пробел, схлопываем множественные пробелы.
    text = re.sub(r"\s+", " ", text.replace("\r", " ").replace("\n", " "))
    # Служебные строки из PDF типа "_______ _____" (подчёркнутый пустой шаблон).
    if re.fullmatch(r"[\s_\-–—]+", text):
        return None
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
    """Выбрать номер кабинета из нескольких значений (для слотов пары).

    Каждое значение нормализуем через
    :func:`app.utils.room_names.normalize_room_number` — мусор (например,
    ``"1 п/гр 1С: Предприятие …"`` из-за сдвига колонок) отбрасывается,
    маркер дистанционной пары приводится к каноничному ``"ДО"``.

    Если в слотах одной пары встретилось несколько разных кабинетов
    (типичный случай — две подгруппы в разных аудиториях), берём
    первый встретившийся реальный кабинет, а не склеиваем через ``/``:
    кабинетов вида «112/413» в реальности нет.
    """
    unique = []
    for r in rooms:
        norm = normalize_room_number(r)
        if norm and norm not in unique:
            unique.append(norm)
    if not unique:
        return None
    # Если среди слотов есть и реальный кабинет, и «ДО», предпочитаем
    # реальный кабинет — пара частично очная.
    non_distance = [r for r in unique if r != "ДО"]
    if non_distance:
        return non_distance[0]
    return unique[0]


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
    """Вытащить (group_name, subject_col, room_col) из первой строки листа.

    Заголовки ``Ауд.`` (и их PDF-перевёрнутый вариант ``.дуА``)
    отбрасываются — это заголовок колонки с номером кабинета, а не
    имя группы.
    """
    groups: List[Tuple[str, int, int]] = []
    # Первые две колонки — это «Пара» и «Расписание звонков».
    for i in range(2, len(header_row), 2):
        name = _clean(header_row.iloc[i])
        if not name or not is_valid_group_name(name):
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


# Регулярка для префиксов вида "1 час 1 п/гр", "2 час лекция", "1 час 2 п/гр практика" и т.п.
# Эти префиксы иногда попадают в текст предмета из-за формата таблицы расписания.
_SUBGROUP_PREFIX_RE = re.compile(
    r"^(\d+\s*час\s*)?"            # "1 час" (опционально)
    r"(\d+\s*п/гр\s*)?"            # "1 п/гр" (опционально)
    r"(\d+\s*час\s*)?"            # ещё "2 час" (для случаев "1 час 1 п/гр 2 час")
    r"(лекция|практика|лабораторная|лаб\.?\s*работа)?"  # тип занятия (опционально)
    r"\s*",
    re.IGNORECASE,
)


def _strip_subgroup_prefix(text: str) -> str:
    """Убрать из начала строки мусорные префиксы подгрупп/часов.

    Примеры:
      "1 час 1 п/гр 2 час лекция МДК.06.03 ..." → "МДК.06.03 ..."
      "1 час 2 п/гр МДК.06.03 ..." → "МДК.06.03 ..."
      "лекция МДК.06.03 ..." → "МДК.06.03 ..."
      "МДК.06.03 ..." → "МДК.06.03 ..." (без изменений)
    """
    m = _SUBGROUP_PREFIX_RE.match(text)
    if m and m.end() > 0 and m.group(0).strip():
        cleaned = text[m.end():].strip()
        # Если после очистки осталось что-то — возвращаем,
        # иначе оригинал (чтобы не потерять данные).
        if cleaned:
            return cleaned
    return text


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

    # Убираем префиксы подгрупп/часов из каждого слота.
    cleaned_texts = [_strip_subgroup_prefix(t) for t in texts]

    # Часто второй слот дублирует текст первого — дедуплицируем.
    dedup: List[str] = []
    for t in cleaned_texts:
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
    # Защита от дубликатов: одна группа может встретиться на нескольких
    # листах Excel — берём первое вхождение, остальные пропускаем.
    seen: set = set()

    try:
        # Удаляем старое расписание — повторный импорт идемпотентен.
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
                    key = (group_name, lesson_number)
                    if key in seen:
                        continue

                    extracted = _extract_lesson_for_group(slots, subj_col, room_col)
                    if extracted is None:
                        continue
                    subject, teacher, room = extracted
                    lesson_type = _infer_lesson_type(subject)

                    seen.add(key)
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
                            lesson_type=lesson_type,
                            is_modified=False,
                        )
                    )
                    records_added += 1

        # Защита от тихой потери данных: если новый файл оказался
        # пустым / нераспознаваемым (0 записей) — НЕ коммитим удаление,
        # откатываемся. Иначе кривой PDF из автосинка тихо стирал бы
        # день расписания.
        if records_added == 0:
            db.rollback()
            print(
                f"[WARN] {file_path}: 0 записей на {schedule_date} "
                "— удаление откачено, данные сохранены."
            )
            return 0

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


def _table_to_dataframe(table: List[List[Optional[str]]]) -> pd.DataFrame:
    """Конвертировать таблицу из pdfplumber в pandas DataFrame.

    Структура таблицы в PDF расписания идентична Excel: первая строка —
    заголовки (Пара / Расписание звонков / группа / Ауд. / группа / Ауд. / …),
    дальше по строкам слоты пар. Приводим к одному типу данных (str), чтобы
    дальше прогнать тот же парсер, что и для Excel.
    """
    return pd.DataFrame(table).astype("string")


def import_schedule_from_pdf(
    file_path: str, date_str: str = "2026-04-13"
) -> int:
    """
    Импорт расписания из PDF.

    PDF-таблицы ККРИТ имеют ту же структуру, что и Excel
    (Пара / Расписание звонков / группа1 / Ауд1 / группа2 / Ауд2 / …),
    поэтому используем тот же парсер пар и ту же регулярку для ФИО.

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
    seen: set = set()

    try:
        with pdfplumber.open(file_path) as pdf:
            if not pdf.pages:
                print("Файл PDF пуст")
                return 0

            # Собираем таблицы со всех страниц PDF. В расписании ККРИТ это
            # обычно 1 страница с 2 таблицами (как 2 листа Excel), но на
            # всякий случай поддерживаем многостраничные PDF.
            all_tables: List[List[List[Optional[str]]]] = []
            for page in pdf.pages:
                for table in page.extract_tables() or []:
                    if table and len(table) >= 2 and len(table[0]) >= 3:
                        all_tables.append(table)

            if not all_tables:
                print("Таблицы в PDF не найдены")
                return 0
            print(f"Найдено таблиц: {len(all_tables)}")

            # Удаляем старое расписание — повторный импорт идемпотентен.
            db.query(Schedule).filter(Schedule.date == schedule_date).delete()

            total_groups = 0
            for table_index, table in enumerate(all_tables):
                df = _table_to_dataframe(table)
                if df.empty:
                    continue

                groups = _collect_group_columns(df.iloc[0])
                total_groups += len(groups)
                print(f"  Таблица {table_index}: найдено групп {len(groups)}")

                for lesson_number, slots in _iter_pair_rows(df):
                    pair_timing: Optional[PairTiming] = bell_by_number.get(
                        lesson_number
                    )
                    if pair_timing is None:
                        continue

                    for group_name, subj_col, room_col in groups:
                        key = (group_name, lesson_number)
                        if key in seen:
                            continue

                        extracted = _extract_lesson_for_group(
                            slots, subj_col, room_col
                        )
                        if extracted is None:
                            continue
                        subject, teacher, room = extracted
                        lesson_type = _infer_lesson_type(subject)

                        seen.add(key)
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
                                lesson_type=lesson_type,
                                is_modified=False,
                            )
                        )
                        records_added += 1

            if records_added == 0:
                db.rollback()
                print(
                    f"[WARN] {file_path}: 0 записей на "
                    f"{schedule_date} — удаление откачено, данные сохранены."
                )
                return 0

            db.commit()
            print(
                f"[OK] Импортировано из PDF: {records_added} записей "
                f"({total_groups} групп в {len(all_tables)} таблицах)"
            )
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

    После успешного импорта автоматически вызывает ``populate_rooms`` —
    чтобы новые аудитории, появившиеся в свежем расписании, сразу
    попадали в таблицу ``rooms``.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext in {".xlsx", ".xls"}:
        records = import_schedule_from_excel(file_path, date_str)
    elif ext == ".pdf":
        records = import_schedule_from_pdf(file_path, date_str)
    else:
        raise ValueError(
            f"Неподдерживаемое расширение файла: {ext!r}. "
            f"Ожидается .xlsx, .xls или .pdf."
        )

    # Идемпотентный авто-вызов populate_rooms: новые аудитории добавятся,
    # существующие будут пропущены. Ошибка здесь не должна валить импорт.
    try:
        from app.utils.populate_rooms import populate_rooms

        populate_rooms()
    except Exception as exc:  # pragma: no cover - defensive
        print(f"[WARN] populate_rooms после импорта упал: {exc}")

    return records


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

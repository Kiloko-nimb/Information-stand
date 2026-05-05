"""
Валидация номеров аудиторий в расписании.

В PDF расписания иногда колонки сдвинуты, и парсер пихает в столбец
«Ауд.» текст следующего предмета (например ``"1 п/гр 1С: Предприятие
Курбанова Т.В."``). Такие «номера» попадают в ``schedule.room_number``
и затем — в подсказки поиска по кабинетам.

Эта функция — единая точка истины для отсева мусора. Используется:

* в эндпоинте ``/api/v1/schedule/rooms`` (что показываем в подсказках),
* в ``app.utils.populate_rooms`` (что заводим в таблицу ``rooms``),
* в парсере ``app.utils.import_schedule`` (что вообще пишем в БД).

Также распознаёт специальный маркер ``"ДО"`` — дистанционная пара,
у которой нет физического кабинета.
"""
from __future__ import annotations

import re
from typing import Optional

# Маркер дистанционной пары. В PDF расписания ставится в колонку «Ауд.»
# у пар без физической аудитории. Для UI показываем как «Дистанционно».
_DISTANCE_MARKERS = frozenset(
    {"до", "дистанционно", "онлайн", "online", "дист"}
)

# Слова-маркеры предметов/преподов: если встречаются в значении —
# это явно текст пары, а не номер аудитории.
_SUBJECT_HINTS = (
    "п/гр",
    "1с:",
    "иностр",
    "физ",
    "матем",
    "информ",
    "практик",
    "лаборатор",
    "лекци",
)


def is_distance_marker(value: Optional[str]) -> bool:
    """Это маркер дистанционной пары (``ДО``, ``онлайн`` и т.п.)?"""
    if not value:
        return False
    return value.strip().lower() in _DISTANCE_MARKERS


def is_valid_room_number(value: Optional[str]) -> bool:
    """Похоже ли ``value`` на корректный номер аудитории.

    Допускаем:
    * ``112``
    * ``414а`` (с буквой в конце)
    * ``ДО`` (дистанционное обучение)
    * ``Спортзал``/``Актовый зал``

    Отбрасываем:
    * ``1 1 6`` (пробелы недопустимы)
    * ``4 1 4`` (пробелы недопустимы)
    * длинный текст (``1 п/гр 1С: Предприятие …``)
    """
    if not value:
        return False
    s = value.strip()
    if len(s) > 10:
        return False
    if is_distance_marker(s):
        return True
    if s.lower() in ("спортзал", "сп", "акт", "актовый зал"):
        return True
    if " " in s:  # Пробелы недопустимы
        return False
    if len(s) < 2 or len(s) > 5:
        return False
    # Должно начинаться с цифры
    if not s[0].isdigit():
        return False
    # Допускаем только цифры или цифры+буква в конце
    if len(s) >= 2:
        if not s[:-1].isdigit():  # Все, кроме последней, должны быть цифрами
            return False
        if len(s) == 5 and not s[-1].isalpha():  # Последняя может быть буквой
            return False
    return True


def normalize_room_number(value: Optional[str]) -> Optional[str]:
    """Привести к каноничному виду или вернуть ``None``, если не похоже на кабинет.

    * ``ДО``/``до`` → ``"ДО"``;
    * номер кабинета → исходная строка (с ``strip``);
    * мусор → ``None``.
    """
    if value is None:
        return None
    s = value.strip()
    if not s:
        return None
    if is_distance_marker(s):
        return "ДО"
    if is_valid_room_number(s):
        return s
    return None

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

    * чистые цифры (``"112"``),
    * цифры + 1-2 буквы (``"414а"``, ``"212б"``),
    * специальный маркер ``"ДО"`` (дистанционная пара).

    Отсекаем:

    * длинные строки (``> 20`` символов),
    * содержимое с двоеточиями (``"1С: Предприятие"``),
    * комбинированные слоты через ``"/"`` (``"112/413"``) — таких
      кабинетов в колледже физически нет, это артефакт парсера, когда
      у двух подгрупп разные аудитории. Парсер теперь берёт первый
      реальный кабинет, но в БД от прежних импортов могли остаться
      записи со слэшем — отсекаем их в эндпоинте подсказок,
    * многословные строки с длинными словами (текст предмета),
    * строки без цифр и не из списка маркеров.
    """
    if value is None:
        return False
    s = value.strip()
    if not s:
        return False

    if is_distance_marker(s):
        return True

    if len(s) > 20:
        return False

    # Любой явный признак текста предмета.
    lower = s.lower()
    if ":" in s:
        return False
    if "/" in s:
        return False
    for hint in _SUBJECT_HINTS:
        if hint in lower:
            return False

    # Несколько слов длиной ≥ 4 — это уже не номер кабинета.
    long_words = [w for w in s.split() if len(w) >= 4]
    if len(long_words) >= 2:
        return False

    # Должна быть хоть одна цифра — иначе это не номер.
    if not any(ch.isdigit() for ch in s):
        return False

    # Допустимые символы: буквы, цифры, ``-``, пробел, точка.
    if not re.fullmatch(r"[\w\s\-\.]+", s, flags=re.UNICODE):
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

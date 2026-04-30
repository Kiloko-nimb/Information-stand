"""
Общая логика валидации имён групп в расписании.

Старые версии PDF-парсера могли импортировать в БД заголовки колонок
(``Ауд.``) как имена групп. Новый парсер
(:mod:`app.utils.import_schedule._collect_group_columns`) уже отбрасывает
такие колонки, но в существующих БД остаются записи от прежних импортов.

Эта функция — единая точка истины: используется и в API
(``/api/v1/schedule/groups``), и в скрипте очистки
(``scripts/cleanup_garbage_groups.py``).
"""
from __future__ import annotations

import re
from typing import Optional


def is_valid_group_name(name: Optional[str]) -> bool:
    """Возвращает True, если ``name`` — корректное имя группы.

    Отсекает:

    * пустые / ``None`` значения,
    * имена, начинающиеся на ``Ауд`` (любой регистр) — это заголовок
      колонки с номером аудитории, а не группа,
    * имена с перевёрнутым ``Ауд.`` → ``.дуА`` (PDF-парсер иногда
      выдаёт текст в обратном порядке символов, особенно в шапках с
      нестандартным шрифтом),
    * имена, состоящие только из не буквенно-цифровых символов
      (``.``, ``-``, ``—``, ``…``).
    """
    if not name:
        return False
    stripped = name.strip()
    if not stripped:
        return False
    # Нормализуем: только буквы (русские/латинские), без точек и пробелов.
    # Так ловим и ``Ауд.``, и ``.дуА``, и ``А у д .`` одинаково.
    letters_only = re.sub(r"[^а-яА-ЯёЁa-zA-Z]", "", stripped).lower()
    if letters_only in ("ауд", "дуа"):
        return False
    if stripped.lower().startswith("ауд"):
        return False
    if all(not ch.isalnum() for ch in stripped):
        return False
    return True

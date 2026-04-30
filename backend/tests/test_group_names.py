"""Тесты валидатора имён групп."""
from __future__ import annotations

import pytest

from app.utils.group_names import is_valid_group_name


@pytest.mark.parametrize(
    "name",
    [
        "9ИС-1.25",
        "9ИС-1",
        "ИТ-21-1",
        "Группа 1",
        "9-А",
    ],
)
def test_valid_group(name: str) -> None:
    assert is_valid_group_name(name)


@pytest.mark.parametrize(
    "name",
    [
        None,
        "",
        "   ",
        "Ауд.",
        "ауд",
        "АУД.",
        "  Ауд .  ",
        # PDF-парсер иногда выдаёт текст с обратным порядком символов.
        ".дуА",
        " . дуА ",
        "дуа",
        "ДУА",
        ".",
        "...",
        "—",
    ],
)
def test_invalid_group(name) -> None:
    assert not is_valid_group_name(name)

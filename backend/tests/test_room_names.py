"""Тесты валидатора номеров аудиторий и нормализации маркера ДО."""
from __future__ import annotations

import pytest

from app.utils.room_names import (
    is_distance_marker,
    is_valid_room_number,
    normalize_room_number,
)


class TestIsValidRoomNumber:
    @pytest.mark.parametrize(
        "value",
        [
            "112",
            "215",
            "414а",
            "212б",
            "112/413",
            "К-1",
            "Сп1",
            "ДО",
            "до",
            "Дистанционно",
            "Online",
        ],
    )
    def test_valid(self, value: str) -> None:
        assert is_valid_room_number(value), f"должно быть валидным: {value!r}"

    @pytest.mark.parametrize(
        "value",
        [
            None,
            "",
            "   ",
            "1 п/гр 1С: Предприятие Курбанова Т.В.",
            "Иностранный язык в проф. деятельности Иванова И.И.",
            "Лекция по физике",
            "1С: Предприятие 8.3",
            "А" * 25,
            "Просто текст без цифр",
        ],
    )
    def test_invalid(self, value) -> None:
        assert not is_valid_room_number(value), (
            f"должно быть НЕвалидным: {value!r}"
        )


class TestIsDistanceMarker:
    @pytest.mark.parametrize("value", ["ДО", "до", " До ", "дистанционно", "online"])
    def test_distance(self, value: str) -> None:
        assert is_distance_marker(value)

    @pytest.mark.parametrize("value", [None, "", "112", "414а"])
    def test_not_distance(self, value) -> None:
        assert not is_distance_marker(value)


class TestNormalizeRoomNumber:
    def test_distance_canonical(self) -> None:
        assert normalize_room_number("до") == "ДО"
        assert normalize_room_number("Дистанционно") == "ДО"

    def test_room_passthrough(self) -> None:
        assert normalize_room_number("112") == "112"
        assert normalize_room_number(" 414а ") == "414а"

    def test_garbage_to_none(self) -> None:
        assert normalize_room_number("1 п/гр 1С: Предприятие Курбанова Т.В.") is None
        assert normalize_room_number("") is None
        assert normalize_room_number(None) is None

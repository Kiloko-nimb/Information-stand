"""Тесты для модуля расписания звонков."""
from datetime import time

import pytest

from app.core.bell_schedule import (
    MONDAY,
    REGULAR,
    get_bell_schedule,
    get_pair_timing,
    schedule_as_dict,
)


class TestBellSchedule:
    def test_monday_starts_with_lineyka(self):
        """Понедельник начинается с линейки + классного часа (lesson=0)."""
        pairs = get_bell_schedule(1)
        assert pairs[0].lesson_number == 0
        assert pairs[0].start == time(8, 0)
        assert pairs[0].end == time(8, 55)

    def test_monday_first_pair_starts_at_9(self):
        """В понедельник 1-я пара начинается в 9:00."""
        pair = get_pair_timing(1, 1)
        assert pair is not None
        assert pair.start == time(9, 0)
        assert pair.end == time(10, 35)

    @pytest.mark.parametrize("weekday", [2, 3, 4, 5, 6])
    def test_tue_sat_first_pair_starts_at_8(self, weekday):
        """Во Вт-Сб 1-я пара начинается в 8:00."""
        pair = get_pair_timing(weekday, 1)
        assert pair is not None
        assert pair.start == time(8, 0)
        assert pair.end == time(9, 35)

    def test_seven_regular_pairs(self):
        """Во Вт-Сб всего 7 пар (без нулевой)."""
        pairs = get_bell_schedule(2)
        numbers = [p.lesson_number for p in pairs]
        assert numbers == [1, 2, 3, 4, 5, 6, 7]

    def test_monday_has_zero_plus_seven_pairs(self):
        """В понедельник пара #0 + 7 обычных = 8 записей."""
        pairs = get_bell_schedule(1)
        numbers = [p.lesson_number for p in pairs]
        assert numbers == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_sunday_empty(self):
        """В воскресенье нет занятий."""
        assert get_bell_schedule(7) == ()

    def test_each_pair_has_two_slots(self):
        """Каждая пара состоит из 2 уроков по 45 минут."""
        for pair in MONDAY + REGULAR:
            assert len(pair.slots) == 2
            # Проверяем длительность слотов.
            for slot in pair.slots:
                minutes = slot.end.hour * 60 + slot.end.minute - (
                    slot.start.hour * 60 + slot.start.minute
                )
                # Линейка длится только 10 минут; остальные слоты — 45.
                assert minutes in (10, 45)

    def test_schedule_as_dict_format(self):
        """JSON-представление содержит нужные поля."""
        pairs = schedule_as_dict(2)
        assert len(pairs) == 7
        first = pairs[0]
        assert first == {
            "lesson_number": 1,
            "label": "1 пара",
            "start": "08:00",
            "end": "09:35",
            "slots": [
                {"index": 1, "start": "08:00", "end": "08:45"},
                {"index": 2, "start": "08:50", "end": "09:35"},
            ],
        }

    def test_monday_matches_user_provided_bell_schedule(self):
        """
        Сверка с расписанием звонков, присланным пользователем.
        """
        expected = {
            0: (time(8, 0), time(8, 55)),   # Линейка + кл. час
            1: (time(9, 0), time(10, 35)),
            2: (time(10, 45), time(12, 20)),
            3: (time(13, 0), time(14, 35)),
            4: (time(14, 45), time(16, 20)),
            5: (time(16, 30), time(18, 5)),
            6: (time(18, 15), time(19, 50)),
            7: (time(20, 0), time(21, 35)),
        }
        for lesson_number, (start, end) in expected.items():
            pair = get_pair_timing(1, lesson_number)
            assert pair is not None, f"Пара {lesson_number} не найдена"
            assert pair.start == start
            assert pair.end == end

    def test_regular_matches_user_provided_bell_schedule(self):
        """Расписание для Вт-Сб соответствует присланному пользователем."""
        expected = {
            1: (time(8, 0), time(9, 35)),
            2: (time(9, 45), time(11, 20)),
            3: (time(12, 0), time(13, 35)),
            4: (time(13, 45), time(15, 20)),
            5: (time(15, 30), time(17, 5)),
            6: (time(17, 15), time(18, 50)),
            7: (time(19, 0), time(20, 35)),
        }
        for lesson_number, (start, end) in expected.items():
            pair = get_pair_timing(2, lesson_number)
            assert pair is not None
            assert pair.start == start
            assert pair.end == end


class TestImportScheduleParser:
    """Юнит-тесты для вспомогательных функций парсера Excel."""

    def test_split_surname_initials(self):
        from app.utils.import_schedule import _split_subject_and_teacher

        subject, teacher = _split_subject_and_teacher("Математика Иванов И.И.")
        assert subject == "Математика"
        assert teacher == "Иванов И.И."

    def test_split_double_surname(self):
        from app.utils.import_schedule import _split_subject_and_teacher

        subject, teacher = _split_subject_and_teacher(
            "Физика Петрова-Сидорова А.Б."
        )
        assert subject == "Физика"
        assert teacher == "Петрова-Сидорова А.Б."

    def test_split_multiline_subject(self):
        from app.utils.import_schedule import _clean, _split_subject_and_teacher

        cleaned = _clean("МДК.05.03\nТестирование Арокина М.Р.")
        subject, teacher = _split_subject_and_teacher(cleaned)
        assert subject == "МДК.05.03 Тестирование"
        assert teacher == "Арокина М.Р."

    def test_split_without_teacher(self):
        from app.utils.import_schedule import _split_subject_and_teacher

        subject, teacher = _split_subject_and_teacher("Классный час")
        assert subject == "Классный час"
        assert teacher is None

    def test_pick_room_dedup(self):
        from app.utils.import_schedule import _pick_room

        assert _pick_room(["318", "318"]) == "318"
        # Когда у двух подгрупп разные кабинеты — берём первый
        # реальный, а не склеиваем через ``/``: кабинетов «318/418»
        # в реальности нет.
        assert _pick_room(["318", "418"]) == "318"
        assert _pick_room([]) is None
        assert _pick_room([None, ""]) is None
        # Мусор (текст пары попал в room из-за сдвига колонок) — None.
        assert _pick_room(["1 п/гр 1С: Предприятие Курбанова Т.В."]) is None
        # Маркер «ДО» нормализуется к каноничному виду.
        assert _pick_room(["до"]) == "ДО"
        assert _pick_room(["До", "до"]) == "ДО"
        # Если есть и реальный кабинет, и «ДО» — побеждает кабинет.
        assert _pick_room(["112", "ДО"]) == "112"
        assert _pick_room(["ДО", "112"]) == "112"

    def test_infer_lesson_type(self):
        from app.utils.import_schedule import _infer_lesson_type

        assert _infer_lesson_type("Математика (лекция)") == "Лекция"
        assert _infer_lesson_type("Программирование — практика") == "Практика"
        assert _infer_lesson_type("Физика лабораторная работа") == "Лабораторная"
        assert _infer_lesson_type("Классный час") is None

    def test_clean_nan_and_whitespace(self):
        from app.utils.import_schedule import _clean

        assert _clean(None) is None
        assert _clean("") is None
        assert _clean("   ") is None
        assert _clean("nan") is None
        assert _clean("  Hello \n world  ") == "Hello world"


class TestBellsApi:
    """Тесты API-эндпойнта /schedule/bells."""

    def test_get_bells_by_weekday(self, client):
        response = client.get("/api/v1/schedule/bells?weekday=1")
        assert response.status_code == 200
        data = response.json()
        assert data["weekday"] == 1
        assert len(data["pairs"]) == 8  # 0 + 7 пар
        assert data["pairs"][0]["lesson_number"] == 0
        assert data["pairs"][1]["start"] == "09:00"

    def test_get_bells_by_date(self, client):
        # 2026-04-13 — понедельник
        response = client.get("/api/v1/schedule/bells?date=2026-04-13")
        assert response.status_code == 200
        data = response.json()
        assert data["weekday"] == 1
        assert data["pairs"][1]["start"] == "09:00"

    def test_get_bells_invalid_date(self, client):
        response = client.get("/api/v1/schedule/bells?date=not-a-date")
        assert response.status_code == 400

    def test_get_bells_tuesday(self, client):
        response = client.get("/api/v1/schedule/bells?weekday=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["pairs"]) == 7
        assert data["pairs"][0]["start"] == "08:00"

    def test_get_bells_sunday_empty(self, client):
        response = client.get("/api/v1/schedule/bells?weekday=7")
        assert response.status_code == 200
        assert response.json()["pairs"] == []

"""
Расписание звонков ККРИТ (единый источник правды).

Понедельник отличается от остальных дней недели:
- В понедельник первые 55 минут заняты линейкой (8:00-8:10)
  и классным часом (8:10-8:55), поэтому 1-я пара начинается в 9:00.
- Во вторник-субботу 1-я пара начинается в 8:00.

Используется парсером Excel-расписаний, API ``/schedule/bells``
и фронтендом ``Schedule.vue``. Меняется только тут.
"""
from dataclasses import dataclass
from datetime import time
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class LessonSlot:
    """Один из двух 45-минутных уроков внутри пары."""

    index: int  # 1 или 2
    start: time
    end: time


@dataclass(frozen=True)
class PairTiming:
    """Одна пара (два урока подряд, с переменой 5 минут)."""

    lesson_number: int  # 1..7 для обычных пар; 0 — линейка/классный час (только ПН)
    label: str  # "1 пара", "Линейка", "Классный час"
    slots: Tuple[LessonSlot, LessonSlot]

    @property
    def start(self) -> time:
        """Начало пары (начало первого слота)."""
        return self.slots[0].start

    @property
    def end(self) -> time:
        """Конец пары (конец второго слота)."""
        return self.slots[1].end


def _pair(lesson_number: int, label: str, s1_start: str, s1_end: str,
          s2_start: str, s2_end: str) -> PairTiming:
    def _t(hhmm: str) -> time:
        h, m = hhmm.split(":")
        return time(int(h), int(m))

    return PairTiming(
        lesson_number=lesson_number,
        label=label,
        slots=(
            LessonSlot(1, _t(s1_start), _t(s1_end)),
            LessonSlot(2, _t(s2_start), _t(s2_end)),
        ),
    )


# Понедельник
MONDAY: Tuple[PairTiming, ...] = (
    # Линейка + классный час идут как одна "нулевая" пара
    PairTiming(
        lesson_number=0,
        label="Линейка / Классный час",
        slots=(
            LessonSlot(1, time(8, 0), time(8, 10)),
            LessonSlot(2, time(8, 10), time(8, 55)),
        ),
    ),
    _pair(1, "1 пара", "09:00", "09:45", "09:50", "10:35"),
    _pair(2, "2 пара", "10:45", "11:30", "11:35", "12:20"),
    # Обед 12:20-13:00
    _pair(3, "3 пара", "13:00", "13:45", "13:50", "14:35"),
    _pair(4, "4 пара", "14:45", "15:30", "15:35", "16:20"),
    _pair(5, "5 пара", "16:30", "17:15", "17:20", "18:05"),
    _pair(6, "6 пара", "18:15", "19:00", "19:05", "19:50"),
    _pair(7, "7 пара", "20:00", "20:45", "20:50", "21:35"),
)

# Вторник-Суббота
REGULAR: Tuple[PairTiming, ...] = (
    _pair(1, "1 пара", "08:00", "08:45", "08:50", "09:35"),
    _pair(2, "2 пара", "09:45", "10:30", "10:35", "11:20"),
    # Обед 11:20-12:00
    _pair(3, "3 пара", "12:00", "12:45", "12:50", "13:35"),
    _pair(4, "4 пара", "13:45", "14:30", "14:35", "15:20"),
    _pair(5, "5 пара", "15:30", "16:15", "16:20", "17:05"),
    _pair(6, "6 пара", "17:15", "18:00", "18:05", "18:50"),
    _pair(7, "7 пара", "19:00", "19:45", "19:50", "20:35"),
)


def get_bell_schedule(day_of_week: int) -> Tuple[PairTiming, ...]:
    """
    Вернуть расписание звонков для дня недели.

    Args:
        day_of_week: 1=Пн, 2=Вт, ..., 6=Сб, 7=Вс.
                     Python's ``date.weekday()`` + 1.

    Returns:
        Кортеж ``PairTiming`` от 1-й пары до 7-й (плюс "0" для понедельника).
        Для воскресенья — пустой кортеж (в ККРИТ нет занятий в воскресенье).
    """
    if day_of_week == 1:
        return MONDAY
    if 2 <= day_of_week <= 6:
        return REGULAR
    return ()


def get_pair_timing(day_of_week: int, lesson_number: int) -> Optional[PairTiming]:
    """Вернуть тайминг конкретной пары для дня недели, либо None."""
    for pair in get_bell_schedule(day_of_week):
        if pair.lesson_number == lesson_number:
            return pair
    return None


def schedule_as_dict(day_of_week: int) -> List[Dict]:
    """JSON-представление расписания звонков для API."""
    result = []
    for pair in get_bell_schedule(day_of_week):
        result.append({
            "lesson_number": pair.lesson_number,
            "label": pair.label,
            "start": pair.start.strftime("%H:%M"),
            "end": pair.end.strftime("%H:%M"),
            "slots": [
                {
                    "index": s.index,
                    "start": s.start.strftime("%H:%M"),
                    "end": s.end.strftime("%H:%M"),
                }
                for s in pair.slots
            ],
        })
    return result

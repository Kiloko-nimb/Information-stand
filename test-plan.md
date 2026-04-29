# Test Plan — Bell schedule + date-filtered UI + PDF parser (PR #1)

## ⚠ Scope change — UI recording blocked by environment
В этой Devin-VM не поднимается графический Chrome (`google-chrome` завершается с кодом 7 сразу после старта; `DISPLAY=:0`, X-сокет `/tmp/.X11-unix/X0` есть, но `xdotool getactivewindow` жалуется, что window manager не поддерживает `_NET_ACTIVE_WINDOW`, а `wmctrl` в системе отсутствует). Скриншот экрана — чёрный прямоугольник. Поэтому полноценный ролик с кликами по карусели дат записать не получится.

Вместо этого делаю объективную проверку на уровне HTTP-API + артефакта фронтенд-билда. Этот формат так же адверсарно распознаёт сломанный и починенный PR — каждое из трёх наблюдаемых изменений оставляет отпечаток в API-ответе или в содержимом `dist/assets/*.js`. Риски, которые эта стратегия не закрывает: визуальные регрессии стилей (шрифты/цвета/композиция). Если пользователь хочет видеокадры, ему надо будет прогнать `npm run dev` локально на Windows.

## What changed (user-visible)
- Карусель дат теперь реально фильтрует: `Schedule.vue` шлёт `?date=YYYY-MM-DD`. Раньше фронт игнорировал выбор даты, и `/schedule/group/{name}` возвращал все даты сразу.
- Времена пар приходят из расписания звонков, **разные для понедельника и вторника-субботы**: Пн начинает с lesson 0 (линейка + классный час, 08:00—08:55), Вт-Сб — с lesson 1 (08:00—09:35). Раньше хардкодилось понедельничное расписание независимо от дня.
- Первая "пара" понедельника (`lesson_number=0`) в бейдже показывается как **`КЧ`**, а не `0`.

## Primary adversarial flow

### Тест 1 — Сравнение ответов `/schedule/group/9РВП-1.25` на понедельник vs субботу

Реализация: `curl` к запущенному локальному бэкенду (порт 8000).

1. `GET /api/v1/schedule/group/9РВП-1.25?date=2026-04-27` → ожидается **3** записи (`application/json`, массив), отсортированные по `lesson_number`:
   - `lesson_number=0`, `time_start="08:00:00"`, `time_end="08:55:00"`, `subject="Линейка Классный час"`, `teacher_name="Курбанова Т.В."`, `room_number="201"`.
   - `lesson_number=1`, `time_start="09:00:00"`, `time_end="10:35:00"`, `subject` начинается с `"Основы безопасности и защиты Родины"`, `teacher_name="Москвитин Е.А."`, `room_number="214"`.
   - `lesson_number=2`, `time_start="10:45:00"`, `time_end="12:20:00"`.
2. `GET /api/v1/schedule/group/9РВП-1.25?date=2026-04-25` → ожидается **1** запись (суббота):
   - `lesson_number=1`, `time_start="08:00:00"`, `time_end="09:35:00"` (НЕ `09:00—10:35`, это было бы понедельничное время).

**Pass**: оба условия выполняются, два ответа содержат **разные** наборы записей.
**Fail (что означает сломанный PR)**:
- Если оба ответа одинаковы (> 3 записей или все даты вперемешку) → date-фильтр в `_parse_date_param` / `Query(...)` не работает.
- Если на субботу lesson 1 имеет `time_start="09:00:00"` → bell_schedule не смотрит на `day_of_week`, применяет понедельничные времена ко всем дням.
- Если на понедельник нет записи с `lesson_number=0` → парсер не распознал линейку/кл.час как lesson 0.

### Тест 2 — `/schedule/bells?weekday=N`, проверка расписания звонков

1. `GET /api/v1/schedule/bells?weekday=1` → JSON с `pairs.length === 8`, `pairs[0] == {lesson_number: 0, label: "Линейка / Классный час", start: "08:00", end: "08:55", slots: [...]}`.
2. `GET /api/v1/schedule/bells?weekday=2` → `pairs.length === 7`, `pairs[0].lesson_number === 1`, `pairs[0].start === "08:00"`, `pairs[0].end === "09:35"`.

**Pass**: обе проверки выполняются.
**Fail**:
- Одинаковая длина для weekday=1 и =2 → bell_schedule не разделяет Mon и остальные.
- Weekday=1 pairs[0].lesson_number !== 0 → понедельник без линейки/КЧ.

### Тест 3 — Бейдж `КЧ` в production-бандле фронта

1. Сборка `cd frontend && npm run build`.
2. `grep -l 'КЧ' dist/assets/*.js` → должен найти хотя бы один JS-бандл.
3. `grep -o 'formatLessonNumber\|КЧ' dist/assets/*.js | sort | uniq -c` → `formatLessonNumber` встречается ≥2 раза (определение функции + вызов из шаблона), `КЧ` встречается ≥1 раз.

**Pass**: оба счётчика положительные.
**Fail**:
- `grep -l 'КЧ'` ничего не находит → строка `КЧ` не попала в бандл (`formatLessonNumber` не применён в шаблоне или возвращает не то).
- `formatLessonNumber` встречается 0 раз → функция не включена в сборку, то есть не используется.

## Evidence captured
- Для тестов 1 и 2: HTTP-ответы вставлены в отчёт как фрагменты JSON.
- Для теста 3: вывод `grep` + одна строка из бандла с контекстом функции `formatLessonNumber`.

## Code references
- `backend/app/api/bells.py` — роут `/schedule/bells`.
- `backend/app/api/schedule.py:25-41` — `_parse_date_param` + фильтр `Schedule.date == parsed`.
- `backend/app/core/bell_schedule.py` — константы MONDAY (8 пар) и REGULAR (7 пар).
- `frontend/src/views/Schedule.vue:108-109` — использование `formatLessonNumber` в бейдже.
- `frontend/src/views/Schedule.vue:238-258` — `toDateParam` + `api.get(endpoint, {params: {date}})`.
- `frontend/src/views/Schedule.vue:272-275` — `formatLessonNumber(0) → "КЧ"`.

# Полная сводка по проекту Information Stand

## Назначение проекта

Проект — интерактивный информационный стенд ККРИТ.

Он состоит из:

- **Frontend**: Vue-приложение для сенсорного/киоскового интерфейса.
- **Backend**: FastAPI API для расписания, сотрудников, кабинетов, новостей и служебных статусов.
- **SQLite database**: локальная база данных с таблицами расписания, кабинетов, сотрудников и новостей.
- **Import/sync scripts**: импорт расписания из PDF/XLSX и синхронизация расписаний с Яндекс.Диска.
- **Docs/tests**: документация и pytest-тесты backend-логики.

Главный пользовательский сценарий: открыть стенд, посмотреть расписание группы/преподавателя/кабинета, текущую пару, новости, карту и справочную информацию.

---

## Структура проекта

```text
Information-stand-fresh/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/             # REST endpoints
│   │   ├── core/            # config, database, migrations, bells, rate limit
│   │   ├── models/          # SQLAlchemy models
│   │   ├── services/        # внешние сервисы: новости, Яндекс.Диск
│   │   ├── utils/           # импорт расписания, валидация, заполнение rooms
│   │   └── main.py          # точка входа FastAPI
│   ├── tests/               # pytest tests
│   ├── requirements.txt     # runtime зависимости
│   └── requirements-dev.txt # dev/test зависимости
├── frontend/                # Vue frontend
│   ├── src/
│   │   ├── views/           # страницы приложения
│   │   ├── components/      # переиспользуемые компоненты
│   │   ├── services/        # axios client
│   │   ├── router/          # маршруты Vue Router
│   │   └── utils/           # frontend utilities
│   └── package.json
├── scripts/                 # служебные скрипты очистки/экспериментов
├── data/                    # карты, фото, расписания
├── docs/                    # документация
├── init_db.py               # инициализация БД
├── load_schedule.py         # ручная загрузка расписания
├── load_staff.py            # загрузка сотрудников
└── populate_rooms.py        # заполнение кабинетов из расписания
```

---

## Backend: точка входа

### `backend/app/main.py`

Главный файл FastAPI-приложения.

Отвечает за:

- создание `FastAPI(...)` приложения;
- настройку CORS;
- подключение rate limiting;
- регистрацию глобальных exception handlers;
- подключение роутеров `/api/v1/...`;
- запуск фоновых задач;
- health check.

Ключевые функции:

- **`update_news_async()`**  
  Асинхронно обновляет новости: вызывает парсер сайта колледжа и сохраняет новости в БД.

- **`sync_schedules_from_yandex()`**  
  Одноразово синхронизирует расписания с публичной папки Яндекс.Диска. Работает только если задан `YANDEX_DISK_PUBLIC_URL`.

- **`yandex_sync_background_task()`**  
  Фоновый цикл синхронизации расписаний с Яндекс.Диска. Интервал берётся из настроек.

- **`news_update_background_task()`**  
  Фоновый цикл обновления новостей каждые 6 часов.

- **`lifespan(app)`**  
  Startup/shutdown логика: применяет миграции, запускает фоновые задачи, корректно останавливает их.

- **`root()`**  
  `GET /` — базовый статус API.

- **`health_check()`**  
  `GET /health` — проверяет состояние API и БД. Возвращает `status`, `timestamp`, `services`.

Подключаемые роутеры:

```python
app.include_router(schedule.router, prefix="/api/v1")
app.include_router(bells.router, prefix="/api/v1")
app.include_router(staff.router, prefix="/api/v1")
app.include_router(rooms.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")
```

---

## Backend API

### `backend/app/api/schedule.py`

Главный API расписания.

Endpoints:

- **`GET /api/v1/schedule/group/{group_name}`**  
  Возвращает расписание группы. Поддерживает `?date=YYYY-MM-DD`.  
  Важная логика: сначала ищет точное совпадение группы, потом fallback через `LIKE`. Это защищает от редкого бага, когда `ИС-1.23` совпадала с `9ИС-1.23` и пары дублировались.

- **`GET /api/v1/schedule/teacher/{teacher_name}`**  
  Возвращает расписание преподавателя. Поиск через `ilike` по ФИО.

- **`GET /api/v1/schedule/room/{room_number}`**  
  Возвращает расписание кабинета.

- **`GET /api/v1/schedule/groups`**  
  Список групп из расписания. Фильтрует мусорные имена через `is_valid_group_name()`.

- **`GET /api/v1/schedule/teachers`**  
  Список преподавателей из расписания.

- **`GET /api/v1/schedule/rooms`**  
  Список аудиторий из расписания. Фильтрует мусор и `ДО`.

- **`GET /api/v1/schedule/today`**  
  Расписание на сегодня для всех групп. Фильтрует мусорные группы.

- **`GET /api/v1/schedule/now`**  
  Текущий статус учебного дня: идёт пара, перерыв, до пар, после пар, выходной. Также возвращает текущую/следующую пару и количество занятых групп.

- **`GET /api/v1/schedule/rooms/free`**  
  Свободные и занятые кабинеты на текущий момент. Можно фильтровать по этажу: `?floor=2`.

- **`GET /api/v1/schedule/dates`**  
  Даты, на которые есть расписание.

Вспомогательная функция:

- **`_parse_date_param(value)`**  
  Безопасно парсит `YYYY-MM-DD`, при ошибке отдаёт HTTP 400.

---

### `backend/app/api/bells.py`

API расписания звонков.

- **`GET /api/v1/schedule/bells`**  
  Возвращает тайминги пар. Можно передать:

```text
?weekday=1
?date=2026-05-04
```

Если ничего не передано — используется сегодняшний день.

---

### `backend/app/api/staff.py`

API сотрудников.

- **`GET /api/v1/staff/`** — все сотрудники.
- **`GET /api/v1/staff/search?query=...`** — поиск по ФИО.
- **`GET /api/v1/staff/{staff_id}`** — сотрудник по ID.

---

### `backend/app/api/rooms.py`

API кабинетов.

- **`GET /api/v1/rooms/`** — все кабинеты.
- **`GET /api/v1/rooms/floor/{floor}`** — кабинеты по этажу.
- **`GET /api/v1/rooms/{room_number}`** — кабинет по номеру.

---

### `backend/app/api/news.py`

API новостей.

- **`GET /api/v1/news/`**  
  Список новостей. Параметры: `limit`, `skip`, `active_only`.

- **`GET /api/v1/news/{news_id}`**  
  Новость по ID.

- **`POST /api/v1/news/refresh`**  
  Принудительное обновление новостей в фоне.

- **`GET /api/v1/news/groups/list`**  
  Совместимость/заглушка, возвращает статус News API.

---

## Core backend

### `backend/app/core/bell_schedule.py`

Единый источник правды для звонков.

Классы:

- **`LessonSlot`**  
  Один 45-минутный слот внутри пары.

- **`PairTiming`**  
  Пара: номер, label, два слота. Имеет свойства `start` и `end`.

Функции:

- **`get_bell_schedule(day_of_week)`**  
  Возвращает звонки для дня недели. Понедельник отличается: есть нулевая пара `Линейка / Классный час`.

- **`get_pair_timing(day_of_week, lesson_number)`**  
  Возвращает тайминг конкретной пары.

- **`schedule_as_dict(day_of_week)`**  
  JSON-представление звонков для API.

Когда менять звонки — менять только здесь.

---

### `backend/app/core/config.py`

Настройки приложения через environment variables / `.env`.

Обычно здесь находятся:

- `DATABASE_URL`
- CORS origins
- настройки Яндекс.Диска
- интервалы синхронизации

---

### `backend/app/core/database.py`

SQLAlchemy engine/session/Base.

Главное:

- `engine`
- `SessionLocal`
- `Base`
- `get_db()` dependency для FastAPI.

---

### `backend/app/core/migrations.py`

Лёгкие миграции без Alembic. Вызываются при старте приложения из `lifespan()`.

---

### `backend/app/core/exceptions.py`

Глобальные обработчики ошибок FastAPI.

---

### `backend/app/core/rate_limit.py`

Настройка rate limiting через `slowapi`.

---

## Models

### `backend/app/models/schedule.py`

Таблица `schedules`.

Поля:

- `group_name` — группа.
- `teacher_name` — преподаватель.
- `subject` — предмет.
- `room_number` — аудитория или `ДО`.
- `day_of_week` — 1..7.
- `lesson_number` — номер пары, 0 для линейки/классного часа.
- `time_start`, `time_end` — время пары.
- `date` — конкретная дата.
- `lesson_type` — лекция/практика/лабораторная.
- `imported_at` — когда импортировано.
- `is_modified` — флаг замены/изменения.

---

### `backend/app/models/room.py`

Таблица `rooms`.

Хранит кабинет, этаж, корпус/адрес, тип аудитории.

---

### `backend/app/models/staff.py`

Таблица сотрудников.

---

### `backend/app/models/news.py`

Таблица новостей.

---

## Импорт расписания

### `backend/app/utils/import_schedule.py`

Самый важный модуль для расписания.

Публичные функции:

- **`import_schedule_from_excel(file_path, date_str)`**  
  Импортирует расписание из `.xlsx`/`.xls`.

- **`import_schedule_from_pdf(file_path, date_str)`**  
  Импортирует расписание из `.pdf`.

- **`import_schedule(file_path, date_str)`**  
  Универсальный импорт. Выбирает парсер по расширению и после успешного импорта вызывает `populate_rooms()`.

Важные внутренние функции:

- **`_clean(value)`**  
  Чистит значение ячейки: `NaN`, пустые строки, переносы, мусорные подчёркивания.

- **`_split_subject_and_teacher(text)`**  
  Отделяет ФИО преподавателя в конце строки от предмета.

- **`_pick_room(rooms)`**  
  Выбирает валидный кабинет из списка значений. Нормализует через `normalize_room_number()`. Если есть реальный кабинет и `ДО`, выбирает реальный кабинет.

- **`_infer_lesson_type(subject)`**  
  Эвристика типа занятия: лекция, практика, лабораторная.

- **`_collect_group_columns(header_row)`**  
  Определяет пары колонок `группа / аудитория` из заголовка таблицы. Отбрасывает мусор вроде `Ауд.`.

- **`_iter_pair_rows(df)`**  
  Итерирует пары в таблице и собирает слоты одной пары.

- **`_strip_subgroup_prefix(text)`**  
  Убирает мусорные префиксы вроде `1 час 1 п/гр`, `лекция`, `практика` в начале текста.

- **`_extract_lesson_for_group(slots, subj_col, room_col)`**  
  Собирает `(subject, teacher, room)` для конкретной группы из слотов пары.

- **`_table_to_dataframe(table)`**  
  Конвертирует таблицу из PDF в `pandas.DataFrame`.

Особенности безопасности:

- При импорте старое расписание на дату сначала удаляется.
- Если новый файл дал `0` записей, делается `rollback`, чтобы не стереть рабочий день расписания.
- Для Excel/PDF есть `seen`, чтобы не импортировать одну группу/пару повторно, если она встретилась на нескольких листах/таблицах.

---

## Валидация и нормализация мусора

### `backend/app/utils/group_names.py`

- **`is_valid_group_name(name)`**  
  Проверяет корректность имени группы.

Отсекает:

- `None`, пустые строки;
- `Ауд.`, `ауд`, `А У Д`;
- перевёрнутое `.дуА`;
- строки только из символов вроде `.`, `—`.

Используется в:

- `/api/v1/schedule/groups`
- `/api/v1/schedule/today`
- `/api/v1/schedule/now`
- `scripts/cleanup_garbage_groups.py`

---

### `backend/app/utils/room_names.py`

Валидация кабинетов.

Обычно отвечает за:

- определение валидного номера кабинета;
- распознавание дистанционных маркеров `ДО`, `дистанционно`, `online`;
- нормализацию `room_number`;
- отсечение текста предмета, случайно попавшего в колонку кабинета.

---

### `backend/app/utils/populate_rooms.py`

Заполнение таблицы `rooms` из уникальных аудиторий в `schedules`.

Функции:

- **`_get_floor(room_number)`**  
  Вычисляет этаж по номеру кабинета.

- **`_get_room_type(room_number)`**  
  Определяет тип: аудитория, спортзал, актовый зал, лаборатория.

- **`_get_building(room_number)`**  
  Определяет корпус/адрес.

- **`populate_rooms(db=None)`**  
  Добавляет новые валидные кабинеты из расписания. Идемпотентно: существующие не трогает.

---

## Синхронизация с Яндекс.Диском

### `backend/app/services/yandex_disk.py`

Отвечает за скачивание расписаний из публичной папки Яндекс.Диска и импорт.

Основные функции:

- **`parse_date_from_filename(filename)`**  
  Достаёт дату из имени файла.

- **`split_public_url(url)`**  
  Делит публичную ссылку на корневую ссылку и внутренний путь.

- **`list_public_folder(public_url, session=None, recursive=False)`**  
  Получает список файлов из публичной папки Яндекс.Диска.

- **`download_file(public_url, file_path, destination, session=None)`**  
  Получает signed download URL и скачивает файл.

- **`sync_folder(public_url, download_dir, recursive=False)`**  
  Скачивает все файлы с распознанной датой. Пропускает уже скачанные файлы с тем же размером.

- **`sync_and_import(public_url, download_dir, recursive=False)`**  
  Скачивает и импортирует расписания. Использует `.imported.json`, чтобы не импортировать неизменённые файлы повторно.

Места риска:

- Публичная ссылка Яндекс.Диска должна быть доступной.
- Имена файлов должны содержать дату.
- При одинаковых именах в разных подпапках берётся более свежий файл и пишется warning.

---

### `backend/app/utils/retry.py`

Обёртка `RetryableSession` для HTTP-запросов с retry.

Используется для внешних запросов, чтобы переживать временные сетевые ошибки.

---

## Новости

### `backend/app/services/news_parser.py`

Парсер новостей сайта колледжа.

Основные ответственности:

- сходить на сайт;
- распарсить новости;
- нормализовать дату/текст;
- сохранить новости в БД через `save_news_to_db()`.

Связанные места:

- `backend/app/api/news.py`
- `update_news_async()` в `backend/app/main.py`
- `news_update_background_task()` в `backend/app/main.py`

---

## Frontend

### `frontend/src/main.js`

Точка входа Vue-приложения.

---

### `frontend/src/router/index.js`

Маршруты:

- `/` — `Home.vue`
- `/schedule` — `Schedule.vue`
- `/staff` — `Staff.vue`
- `/map` — `Map.vue`
- `/quiz` — `Quiz.vue`
- `/faq` — `Faq.vue`

---

### `frontend/src/services/api.js`

Axios-клиент для backend API.

Особенности:

- `baseURL: '/api/v1'`
- timeout 15 секунд;
- retry для timeout/5xx;
- cache-busting `_t=Date.now()` для GET;
- обработка offline/network/API ошибок.

---

### `frontend/src/views/Schedule.vue`

Страница расписания.

Отвечает за:

- выбор даты;
- поиск по группе/преподавателю/кабинету;
- отображение таймлайна пар;
- подсказки групп/преподавателей/кабинетов;
- QR для переноса расписания в телефон;
- переход из преподавателя/кабинета в соответствующий режим поиска.

Ключевые функции:

- **`loadGroups()`** — загружает группы.
- **`loadTeachers()`** — загружает преподавателей.
- **`loadRooms()`** — загружает кабинеты.
- **`search()`** — главный запрос расписания к backend.
- **`debouncedSearch()`** — защита от пачки запросов при быстром переключении дат.
- **`openTeacherSchedule(teacherName)`** — открыть расписание преподавателя.
- **`openRoomSchedule(roomNumber)`** — открыть расписание кабинета.
- **`buildShareText()`** — текст для QR.
- **`openShareQR()` / `closeShareQR()`** — QR-модалка.
- **`formatLessonNumber()`** — `0` показывает как `КЧ`.
- **`isDistanceLesson(room)`** — `ДО` отображается как дистанционно.
- **`getLessonTypeClass()` / `formatLessonType()`** — визуальный тип пары.

Недавний фикс:

- Кнопка `На карте` удалена из расписания.

---

### Остальные frontend views/components

- **`Home.vue`** — главная страница стенда.
- **`Staff.vue`** — сотрудники.
- **`Map.vue`** — интерактивная карта.
- **`Quiz.vue`** — квиз.
- **`Faq.vue`** — часто задаваемые вопросы.
- **`components/home/NowWidget.vue`** — виджет текущей пары.
- **`components/home/BellsWidget.vue`** — виджет звонков.
- **`components/home/NewsSection.vue`** — новости.
- **`components/Icon.vue`** — единая иконка-компонент.
- **`components/MapFloor2.vue` / `MapFloor2Static.vue`** — карта этажа.

---

## Скрипты обслуживания

### `scripts/cleanup_garbage_groups.py`

Чистит таблицу `schedules` от мусорных групп (`Ауд.`, `.`, `.дуА` и т.п.).

Команды:

```powershell
# Сухой прогон: покажет, что будет удалено
python scripts/cleanup_garbage_groups.py

# Реальное удаление
python scripts/cleanup_garbage_groups.py --apply

# С указанием БД
python scripts/cleanup_garbage_groups.py --apply --db sqlite:///backend/kkrit.db
```

Функции:

- **`find_garbage_rows(db)`** — находит мусорные строки.
- **`cleanup_garbage_groups(db, apply)`** — dry-run или удаление.
- **`_build_session(db_url)`** — создаёт SQLAlchemy session.

Когда запускать:

- после старых кривых импортов;
- если в `/schedule/groups`, `/today`, `/now` всплывают странные группы;
- после изменения правил `is_valid_group_name()`.

---

### `populate_rooms.py` / `backend/app/utils/populate_rooms.py`

Заполняет `rooms` из расписания.

Когда запускать:

- после массового импорта расписаний;
- если появились новые кабинеты;
- если карта/поиск кабинетов не видит новые аудитории.

---

### `load_schedule.py`

Ручная загрузка расписания.

Используется, когда нужно импортировать конкретный файл расписания без Яндекс.Диска.

---

### `load_staff.py`

Загрузка сотрудников в БД.

---

### `init_db.py`

Инициализация таблиц БД.

---

## Где можно чистить мусор

### 1. Мусорные группы в `schedules`

Симптомы:

- в списке групп есть `Ауд.`, `.`, `.дуА`;
- в текущем статусе завышено число занятых групп;
- странные записи в расписании.

Что делать:

```powershell
python scripts/cleanup_garbage_groups.py
python scripts/cleanup_garbage_groups.py --apply
```

Источник правил: `backend/app/utils/group_names.py`.

---

### 2. Мусорные кабинеты в `rooms`

Симптомы:

- в кабинеты попал текст предмета;
- в подсказках кабинетов видны длинные строки;
- карта/свободные кабинеты показывают несуществующие аудитории.

Где смотреть:

- `backend/app/utils/room_names.py`
- `backend/app/utils/populate_rooms.py`
- `/api/v1/schedule/rooms`
- `/api/v1/schedule/rooms/free`

Что делать:

- улучшить `is_valid_room_number()` / `normalize_room_number()`;
- удалить мусорные строки из таблицы `rooms` вручную или добавить отдельный cleanup-скрипт;
- перезапустить `populate_rooms()`.

---

### 3. Старые скачанные расписания

Папка:

```text
backend/data/schedule-downloads/
```

или путь из `SCHEDULE_DOWNLOAD_DIR`.

Что можно чистить:

- старые PDF/XLSX, если они больше не нужны;
- `.imported.json`, если нужно принудительно переимпортировать все файлы.

Осторожно: удаление `.imported.json` приведёт к повторному импорту скачанных файлов.

---

### 4. SQLite служебные файлы

Рядом с `kkrit.db` могут быть:

```text
kkrit.db-wal
kkrit.db-shm
```

Это служебные файлы SQLite WAL-режима. Не удалять во время работы backend. Если backend остановлен, обычно они не страшны.

---

### 5. Кэш pytest

Можно удалять безопасно:

```text
backend/.pytest_cache/
```

---

### 6. `node_modules` и frontend build cache

Если frontend ведёт себя странно:

```powershell
# frontend/
npm install
npm run dev
```

`node_modules` можно удалить и восстановить через `npm install`.

---

## Как запускать проект

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload
```

Если `pip` не найден, сначала активировать venv или использовать:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

---

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

---

### Tests

Из `backend/`:

```powershell
python -m pytest tests/ -v
```

Проверка только расписания:

```powershell
python -m pytest tests/test_api.py::TestScheduleApi -v
```

Текущее состояние после последних правок:

```text
121 passed, 31 warnings
```

Warnings не критичные:

- SQLAlchemy `declarative_base()` deprecated;
- Pydantic class-based config deprecated;
- httpx `app` shortcut deprecated.

---

## Частые проблемы и куда смотреть

### Повторяются пары у группы

Вероятная причина: поиск группы через `LIKE` зацепил похожую группу.

Где смотреть:

- `backend/app/api/schedule.py`, функция `get_group_schedule()`.

Правильное поведение:

- сначала точное совпадение `Schedule.group_name == group_name`;
- только если точного нет — fallback на `LIKE`.

---

### В группе отображается предмет от другой группы

Возможные причины:

- ошибка распознавания колонок в PDF/XLSX;
- мусорный заголовок не отфильтрован;
- группа встретилась на нескольких листах.

Где смотреть:

- `_collect_group_columns()`
- `_iter_pair_rows()`
- `_extract_lesson_for_group()`
- `seen` в `import_schedule_from_excel()` / `import_schedule_from_pdf()`.

---

### Кабинет выглядит как текст предмета

Вероятная причина: сдвиг колонок PDF.

Где смотреть:

- `backend/app/utils/room_names.py`
- `_pick_room()` в `import_schedule.py`
- `populate_rooms.py`

---

### Расписание на дату пропало после импорта

В `import_schedule.py` есть защита: если импорт дал `0` записей, делается rollback. Если дата всё равно пропала — смотреть:

- какой файл импортировался;
- `date_str`;
- логи `[WARN] ... 0 записей`;
- корректность таблиц в PDF/XLSX.

---

### Новости не обновляются

Где смотреть:

- `backend/app/services/news_parser.py`
- `backend/app/api/news.py`
- `update_news_async()`
- `news_update_background_task()`

Проверить:

- доступность сайта колледжа;
- изменился ли HTML сайта;
- логи backend.

---

### Яндекс.Диск не синхронизируется

Проверить env:

```text
YANDEX_DISK_PUBLIC_URL=https://disk.yandex.ru/d/...
YANDEX_DISK_RECURSIVE=true/false
YANDEX_DISK_SYNC_INTERVAL_HOURS=...
SCHEDULE_DOWNLOAD_DIR=...
```

Где смотреть:

- `backend/app/main.py`, `yandex_sync_background_task()`
- `backend/app/services/yandex_disk.py`

---

## Рекомендации по дальнейшей уборке

### 1. Добавить cleanup для `rooms`

Сейчас есть хороший cleanup для мусорных групп, но нет отдельного скрипта для мусорных кабинетов.

Можно сделать:

```text
scripts/cleanup_garbage_rooms.py
```

Логика:

- найти `Room.room_number`, которые не проходят `is_valid_room_number()`;
- dry-run по умолчанию;
- `--apply` для удаления.

---

### 2. Убрать устаревшие warnings

- SQLAlchemy: заменить `sqlalchemy.ext.declarative.declarative_base` на `sqlalchemy.orm.declarative_base`.
- Pydantic: заменить `class Config` на `model_config = ConfigDict(...)`.
- httpx/TestClient warning можно обновить позже при обновлении FastAPI/Starlette/httpx.

---

### 3. Привести импорты к одному стилю

В некоторых местах есть локальные импорты для обхода циклов. Это нормально, но стоит документировать, где они нужны.

---

### 4. Добавить README для данных

Полезно описать:

- где лежит рабочая БД;
- какие файлы можно удалять;
- какие папки создаются автоматически;
- как переимпортировать расписание с нуля.

---

### 5. Добавить smoke-test frontend

Сейчас backend хорошо покрыт pytest. Для frontend можно добавить хотя бы:

- `npm run build` в CI;
- smoke-тест главных маршрутов;
- проверку, что `Schedule.vue` собирается.

---

## Краткая карта ответственности

| Область | Главные файлы |
|---|---|
| FastAPI app | `backend/app/main.py` |
| API расписания | `backend/app/api/schedule.py` |
| Расписание звонков | `backend/app/core/bell_schedule.py` |
| Импорт PDF/XLSX | `backend/app/utils/import_schedule.py` |
| Синхронизация Яндекс.Диска | `backend/app/services/yandex_disk.py` |
| Новости | `backend/app/services/news_parser.py`, `backend/app/api/news.py` |
| Валидация групп | `backend/app/utils/group_names.py` |
| Валидация кабинетов | `backend/app/utils/room_names.py` |
| Заполнение кабинетов | `backend/app/utils/populate_rooms.py` |
| Очистка мусорных групп | `scripts/cleanup_garbage_groups.py` |
| Frontend API client | `frontend/src/services/api.js` |
| Страница расписания | `frontend/src/views/Schedule.vue` |
| Маршруты frontend | `frontend/src/router/index.js` |
| Тесты | `backend/tests/` |

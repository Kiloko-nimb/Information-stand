# ККРИТ — Интерактивный информационный стенд

Информационный стенд для **Кировского колледжа** (KKRIT). Физически это сенсорный экран, на котором посетители (студенты, преподаватели, гости) могут:

- посмотреть **расписание** на день (по группе, преподавателю или кабинету);
- найти **сотрудника** (ФИО, должность, кафедра);
- узнать **номер кабинета** и его расположение;
- увидеть **новости** колледжа, текущую пару и расписание звонков;
- воспользоваться интерактивной **картой здания**.

Параллельно есть **админ-панель** (`/admin`), где сотрудник колледжа управляет содержимым стенда: новости, сотрудники, кабинеты, аналитика посещений. Админка также рассчитана на сенсорный экран: крупные кнопки (>= 38 px), собственные модалки вместо `confirm()`, toast-уведомления.

---

## Стек

| Слой | Технологии |
| --- | --- |
| Backend | Python 3.10+, FastAPI, SQLAlchemy, SQLite (`backend/kkrit.db`), uvicorn |
| Frontend | Vue 3 (Composition API), Vite, vue-router, pinia, axios, lucide-vue-next |
| Парсеры | `pdfplumber` (PDF расписания), `openpyxl` / `pandas` (XLSX расписания), `python-docx` (DOCX педсостава), `requests` + `beautifulsoup4` (новости с сайта колледжа) |
| Защита | JWT-токены (admin), slowapi (rate limiting), CORS, аудит запросов через `AnalyticsMiddleware` |
| CI | GitHub Actions — `pytest` (backend) + `vite build` (frontend) |

---

## Структура репозитория

```
Information-stand/
├── backend/
│   ├── app/
│   │   ├── main.py                  # точка входа FastAPI + lifespan + фоновые задачи
│   │   ├── api/                     # роутеры: auth, admin, schedule, staff, rooms, news, analytics, bells
│   │   ├── core/
│   │   │   ├── analytics.py         # AnalyticsMiddleware (фильтр шума)
│   │   │   ├── bell_schedule.py     # расписание звонков
│   │   │   ├── config.py            # pydantic-settings конфигурация
│   │   │   ├── database.py          # engine, SessionLocal, Base
│   │   │   ├── exceptions.py        # глобальные обработчики ошибок
│   │   │   ├── migrations.py        # ручные миграции (добавление колонок)
│   │   │   └── rate_limit.py        # slowapi
│   │   ├── models/                  # SQLAlchemy-модели: schedule, staff, room, news, admin, analytics
│   │   ├── services/
│   │   │   ├── yandex_disk.py       # синхронизация PDF/XLSX расписания с Яндекс.Диска
│   │   │   └── news_parser.py       # парсер новостей с сайта колледжа
│   │   └── utils/
│   │       ├── import_schedule.py   # парсинг XLSX/PDF → таблица schedule
│   │       ├── populate_rooms.py    # заполнение таблицы rooms из расписания
│   │       ├── room_names.py        # нормализация номеров кабинетов
│   │       ├── group_names.py       # нормализация названий групп
│   │       └── retry.py            # retry-утилиты
│   ├── tests/                       # pytest
│   ├── requirements.txt
│   ├── requirements-dev.txt         # pytest + httpx
│   └── .env.example
├── frontend/
│   └── src/
│       ├── views/
│       │   ├── Home.vue, Schedule.vue, Staff.vue, Map.vue, Faq.vue, Quiz.vue
│       │   └── admin/
│       │       ├── Login.vue        # логин или форма создания первого админа
│       │       └── Dashboard.vue    # CRUD всех сущностей + аналитика
│       ├── components/
│       │   ├── home/                # виджеты главной: BellsWidget, NowWidget, FeatureCards, NewsSection...
│       │   ├── BaseModal.vue        # модальное окно
│       │   ├── VirtualKeyboard.vue  # экранная клавиатура
│       │   ├── Screensaver.vue      # скринсейвер при простое
│       │   └── ...
│       ├── composables/             # useClock, useScheduleStatus, useScreensaver
│       ├── services/                # api.js, adminService.js, newsService.js
│       └── router/
├── scripts/
│   └── cleanup_garbage_groups.py    # очистка мусорных групп
├── load_staff.py                    # одноразовый импорт DOCX педсостава
├── load_schedule.py                 # CLI-обёртка над import_schedule
├── init_db.py                       # ручное создание таблиц (обычно не нужно — main.py делает это сам)
└── docs/                            # дополнительная документация
```

---

## Откуда берутся данные

| Сущность | Источник | Когда подгружается |
| --- | --- | --- |
| **Расписание** | Публичная папка Яндекс.Диска (XLSX/PDF) | Автоматически: фоновая задача раз в N часов (по умолчанию 3), плюс через 1 минуту после старта бэкенда |
| **Кабинеты** | Уникальные `room_number` из расписания | Автоматически вместе с импортом расписания (`populate_rooms`) |
| **Новости** | Сайт колледжа (HTML-парсер) | Автоматически: через 30 сек после старта бэкенда, затем каждые 6 часов |
| **Сотрудники** | DOCX-файл педсостава | Вручную, один раз: `python load_staff.py`, или через админ-панель |
| **Админ** | — | Вручную при первом запуске: `/admin/login` предложит создать администратора |

### Яндекс.Диск

В `backend/.env` задаётся переменная `YANDEX_DISK_PUBLIC_URL`. Если она указана, фоновая задача автоматически скачивает файлы в `data/schedule-downloads/` и импортирует расписание. Манифест уже скачанных файлов — `.imported.json`.

Ручной импорт:
```bash
python load_schedule.py path/to/file.xlsx --date YYYY-MM-DD
```

---

## Запуск локально

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# первый запуск — создаст kkrit.db и подтянет данные с Яндекса
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs (при `DEBUG=True`)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- Приложение: http://localhost:5173
- Админка: http://localhost:5173/admin

### Переменные окружения

Скопируй `.env.example` в `.env` и настрой:

- `backend/.env` — `DATABASE_URL`, `SECRET_KEY`, `YANDEX_DISK_PUBLIC_URL`, CORS, rate limiting и др.
- `frontend/.env` — `VITE_KIOSK_TIMEOUT_SEC`, `VITE_KIOSK_WARNING_SEC`, `VITE_KIOSK_4K_MODE`

---

## Тесты и сборка

```bash
# Backend — pytest
cd backend
pip install -r requirements-dev.txt
pytest -q

# Frontend — vite build
cd frontend
npm run build
```

CI (GitHub Actions) запускает оба шага на каждый PR и push в `main`.

---

## API

Все маршруты префиксованы `/api/v1`.

### Публичные

| Метод | Путь | Описание |
| --- | --- | --- |
| `GET` | `/schedule/groups` | Список групп |
| `GET` | `/schedule/teachers` | Список преподавателей |
| `GET` | `/schedule/rooms` | Список кабинетов (из расписания) |
| `GET` | `/schedule/group/{name}` | Расписание группы |
| `GET` | `/schedule/teacher/{name}` | Расписание преподавателя |
| `GET` | `/schedule/room/{number}` | Расписание кабинета |
| `GET` | `/schedule/now` | Текущая пара |
| `GET` | `/schedule/bells` | Расписание звонков |
| `GET` | `/staff/` | Справочник сотрудников |
| `GET` | `/staff/search?query=...` | Поиск сотрудников |
| `GET` | `/rooms/{room_number}` | Карточка кабинета |
| `GET` | `/news/` | Список новостей |
| `GET` | `/health` | Проверка состояния сервиса |

### Аутентификация

| Метод | Путь | Описание |
| --- | --- | --- |
| `GET` | `/auth/check` | Нужен ли первичный setup |
| `POST` | `/auth/setup` | Создание первого администратора |
| `POST` | `/auth/login` | Логин (form-data: `username`, `password`) → JWT |
| `GET` | `/auth/me` | Текущий пользователь |

### Admin (требуют JWT)

| Метод | Путь | Описание |
| --- | --- | --- |
| CRUD | `/admin/news` | Управление новостями |
| CRUD | `/admin/staff` | Управление сотрудниками |
| CRUD | `/admin/rooms` | Управление кабинетами |
| `DELETE` | `/admin/rooms/invalid` | Удалить кабинеты с невалидными номерами |
| `GET` | `/admin/analytics/stats` | Статистика поисковых запросов (без шума) |
| `GET` | `/admin/analytics/recent` | Лента последних запросов |

---

## После удаления БД (пересоздание с нуля)

1. **Запусти бэкенд** — таблицы создадутся автоматически.
2. **Открой `/admin/login`** — появится форма «Создать администратора». Если показывает обычный логин — очисти `localStorage` в DevTools.
3. **Подожди 1–2 минуты** — фоновые задачи подтянут расписание с Яндекс.Диска и новости с сайта колледжа. Кабинеты заполнятся автоматически из расписания.
4. **Сотрудников загрузи вручную**: `python load_staff.py` из корня репо.

---

## Известные особенности

- **Windows + SQLite WAL**: при аварийном завершении бэкенда БД может повредиться. Решение — удалить `kkrit.db`, `kkrit.db-shm`, `kkrit.db-wal` и перезапустить uvicorn.
- **Кодировка `.env` на Windows**: файл должен быть в UTF-8. Загрузка через pydantic-settings обеспечивает это автоматически.
- **Поллинг каждые 30 секунд**: `AnalyticsMiddleware` фильтрует служебные запросы (`/admin/*`, `/auth/*`, `/schedule/now`, `/schedule/bells`), чтобы не засорять аналитику.
- **Кнопка «Очистить мусор»** в разделе «Кабинеты» удаляет только кабинеты с невалидными номерами. Валидные не трогает.

---

## Документация

Дополнительные документы в папке [`docs/`](docs/):

- [docs/QUICKSTART.md](docs/QUICKSTART.md) — быстрый старт
- [docs/README_RUN.md](docs/README_RUN.md) — расширенная инструкция по запуску
- [docs/CHANGELOG.md](docs/CHANGELOG.md) — история изменений
- [docs/ADMIN_GUIDE.md](docs/ADMIN_GUIDE.md) — руководство администратора
- [docs/USER_GUIDE.md](docs/USER_GUIDE.md) — руководство пользователя
- [docs/SCHEDULE_IMPORT.md](docs/SCHEDULE_IMPORT.md) — импорт расписания из Excel
- [docs/NEWS_PARSING_README.md](docs/NEWS_PARSING_README.md) — парсинг новостей
- [docs/SVG_MAPS_GUIDE.md](docs/SVG_MAPS_GUIDE.md) — карты этажей
- [docs/INTERACTIVE_MAP.md](docs/INTERACTIVE_MAP.md) — интерактивная навигация
- [docs/STATUS.md](docs/STATUS.md) — текущий статус проекта

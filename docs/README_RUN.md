# Интерактивный информационный стенд ККРИТ

Дипломный проект: веб-приложение для интерактивной доски с информацией о колледже.

## 🎯 Реализованный функционал

✅ **Расписание занятий** - 73 записи загружены из PDF
✅ **База сотрудников** - 109 преподавателей загружены из DOCX
✅ **API endpoints** - FastAPI с автодокументацией
✅ **Frontend** - Vue.js с роутингом и offline-режимом
✅ **База данных** - SQLite с реальными данными

## 🚀 Быстрый старт

### 1. Backend (уже запущен)

```bash
cd backend
python run.py
```

API доступен на: http://localhost:8000
Документация: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Приложение: http://localhost:5173

## 📊 Данные в БД

- **Расписание**: 73 записи (13.04.2026)
- **Сотрудники**: 109 преподавателей
- **Группы**: ~40 групп

## 🔧 API Endpoints

### Расписание
- `GET /api/v1/schedule/group/{group_name}` - расписание группы
- `GET /api/v1/schedule/teacher/{teacher_name}` - расписание преподавателя
- `GET /api/v1/schedule/room/{room_number}` - расписание кабинета

### Сотрудники
- `GET /api/v1/staff/` - все сотрудники
- `GET /api/v1/staff/search?query=...` - поиск по ФИО
- `GET /api/v1/staff/{id}` - конкретный сотрудник

### Навигация
- `GET /api/v1/rooms/` - все кабинеты
- `GET /api/v1/rooms/floor/{floor}` - кабинеты на этаже
- `GET /api/v1/rooms/{room_number}` - информация о кабинете

## 📁 Структура проекта

```
diplom/
├── backend/              # Python FastAPI
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Config, database
│   │   ├── models/      # SQLAlchemy модели
│   │   └── main.py      # Главный файл
│   ├── run.py           # Запуск сервера
│   └── kkrit.db         # SQLite база данных
├── frontend/            # Vue.js
│   ├── src/
│   │   ├── views/       # Страницы
│   │   ├── services/    # API клиент
│   │   └── App.vue
│   └── vite.config.js   # PWA конфигурация
├── init_db.py           # Инициализация БД
├── load_schedule.py     # Загрузка расписания
└── load_staff.py        # Загрузка сотрудников
```

## 🧪 Тестирование API

```bash
# Проверка работы
curl http://localhost:8000/

# Расписание группы
curl http://localhost:8000/api/v1/schedule/group/9ИС-1.25

# Поиск сотрудника
curl http://localhost:8000/api/v1/staff/search?query=Иванов
```

## 📝 Следующие шаги

- [ ] Добавить SVG карты этажей
- [ ] Реализовать построение маршрутов
- [ ] Добавить фото сотрудников
- [ ] Настроить Service Worker для offline
- [ ] Добавить админ-панель для обновления данных

## 🎓 Для защиты диплома

**Ключевые особенности:**
1. **Парсинг PDF** - автоматическая обработка расписания
2. **Offline-first** - работа без интернета
3. **Современный стек** - Vue.js + FastAPI
4. **Реальные данные** - 109 сотрудников, 73 записи расписания
5. **API документация** - автоматическая через FastAPI

**Технические решения:**
- SQLAlchemy ORM для работы с БД
- pdfplumber для парсинга PDF
- python-docx для обработки DOCX
- Service Workers для кэширования
- IndexedDB для offline-хранилища

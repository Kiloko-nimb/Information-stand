# Интерактивный информационный стенд ККРИТ

## ✅ Проект успешно развернут!

### 🎯 Что реализовано:

**Backend (FastAPI):**
- ✅ REST API на порту 8000
- ✅ База данных SQLite с реальными данными
- ✅ 109 сотрудников загружены из DOCX
- ✅ 73 записи расписания загружены из PDF
- ✅ Автодокументация API (Swagger)
- ✅ CORS настроен для фронтенда

**Frontend (Vue.js):**
- ✅ Структура проекта создана
- ✅ Роутинг (Home, Schedule, Staff, Map)
- ✅ PWA конфигурация для offline-режима
- ✅ API клиент с обработкой ошибок
- ✅ Компоненты для всех страниц

**Парсинг данных:**
- ✅ PDF парсер для расписания (pdfplumber)
- ✅ DOCX парсер для педсостава (python-docx)
- ✅ Скрипты загрузки данных в БД

## 🚀 Запуск проекта

### Backend (уже запущен)
```bash
cd backend
python run.py
```
API: http://localhost:8000
Docs: http://localhost:8000/docs

### Frontend (нужно запустить)
```bash
cd frontend
npm install
npm run dev
```
App: http://localhost:5173

## 📊 Статистика

- **Сотрудников в БД**: 109
- **Записей расписания**: 73
- **Групп**: ~40
- **API endpoints**: 9+
- **Страниц фронтенда**: 4

## 🧪 Тестирование

```bash
# Проверка API
curl http://localhost:8000/
curl http://localhost:8000/api/v1/staff/
curl "http://localhost:8000/api/v1/staff/search?query=Алексеев"
curl "http://localhost:8000/api/v1/schedule/group/9ИС-1.25"

# Или запустить тесты
python test_api.py
```

## 📁 Файлы проекта

**Скрипты:**
- `init_db.py` - создание таблиц БД
- `load_staff.py` - загрузка сотрудников
- `load_schedule.py` - загрузка расписания
- `test_api.py` - тестирование API

**Данные:**
- `13.04.2026.pdf` - расписание на 13 апреля
- `ped._sostav_dlya_sayta_10.09.2025.docx` - педсостав
- `backend/kkrit.db` - база данных SQLite

## 🎓 Для защиты диплома

**Технический стек:**
- Python 3.10 + FastAPI + SQLAlchemy
- Vue.js 3 + Vite + PWA
- SQLite
- pdfplumber, python-docx

**Ключевые особенности:**
1. Автоматический парсинг PDF и DOCX
2. RESTful API с документацией
3. Offline-first архитектура (PWA)
4. Реальные данные ККРИТ
5. Поиск по расписанию и сотрудникам

**Что можно показать:**
- Парсинг PDF → данные в БД
- API с автодокументацией
- Поиск расписания по группе
- Поиск сотрудников по ФИО
- Offline-режим (индикатор)

## 📝 Следующие шаги

1. ✅ Backend работает
2. ✅ Данные загружены
3. ⏳ Запустить frontend (`npm run dev`)
4. ⏳ Протестировать UI
5. ⏳ Добавить SVG карты этажей
6. ⏳ Настроить Service Worker

## 📚 Дополнительная документация

Полный индекс — в [docs/README.md](docs/README.md). Ключевые документы:

- [docs/QUICKSTART.md](docs/QUICKSTART.md) — быстрый старт
- [docs/README_RUN.md](docs/README_RUN.md) — расширенная инструкция по запуску
- [docs/CHANGELOG.md](docs/CHANGELOG.md) — история изменений
- [docs/STATUS.md](docs/STATUS.md) / [docs/SUMMARY.md](docs/SUMMARY.md) — текущий статус и итоговая сводка
- [docs/SCHEDULE_IMPORT.md](docs/SCHEDULE_IMPORT.md) — импорт расписания из Excel
- [docs/NEWS_PARSING_README.md](docs/NEWS_PARSING_README.md) — парсинг новостей
- [docs/SVG_MAPS_GUIDE.md](docs/SVG_MAPS_GUIDE.md) / [docs/INTERACTIVE_MAP.md](docs/INTERACTIVE_MAP.md) — карты этажей и навигация
- [docs/FRONTEND_IMPROVEMENTS.md](docs/FRONTEND_IMPROVEMENTS.md) / [docs/BACKGROUND_TASKS_UPDATE.md](docs/BACKGROUND_TASKS_UPDATE.md) — заметки по подсистемам

---

**Проект готов к разработке и демонстрации!** 🚀

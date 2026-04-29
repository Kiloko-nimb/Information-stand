# Test Report — PR #1: Bell schedule + date-filtered API + parser rewrite

**Session**: https://app.devin.ai/sessions/51e0363f1e1c4ddebe6d451e6599249e
**PR**: https://github.com/Kiloko-nimb/Information-stand/pull/1
**HEAD**: `d801f89`

## Caveat first
- **GUI-тест записать не получилось**: в этой Devin-VM `google-chrome` стартует и тут же завершается (exit 7), `wmctrl` отсутствует, `xdotool getactivewindow` сообщает что window manager не поддерживает `_NET_ACTIVE_WINDOW`, скриншот — чёрный прямоугольник. Видеоролика с кликами по карусели дат — нет. Если хочешь — подними `npm run dev` локально на Windows и пройдись сам.
- Поэтому тестировал на уровне HTTP-API + production-бандла фронта. Каждое из трёх изменений PR оставляет наблюдаемый след на этом уровне.

## Results

| # | Test | Result |
|---|------|--------|
| 1a | `GET /schedule/group/9РВП-1.25?date=2026-04-27` (Пн) → 3 пары, lesson 0 = `Линейка Классный час / Курбанова Т.В. / 201 / 08:00—08:55`, lesson 1 = `09:00—10:35` | ✅ passed |
| 1b | `GET /schedule/group/9РВП-1.25?date=2026-04-25` (Сб) → 1 пара, lesson 1 = `08:00—09:35` (НЕ `09:00—10:35`) | ✅ passed |
| 1c | Тот же эндпоинт без `?date` → 77 записей по 23 датам (фильтр по дате реально режет ответ) | ✅ passed (regression baseline) |
| 2 | `/schedule/bells?weekday=1` → 8 пар, pair0 = `{lesson_number:0, "Линейка / Классный час", 08:00—08:55}`. `?weekday=2` → 7 пар, pair0 = `{lesson_number:1, 08:00—09:35}` | ✅ passed |
| 3 | `dist/assets/index-*.js` содержит `КЧ` и `formatLessonNumber` (×2: определение + вызов) | ✅ passed |
| pytest | `cd backend && pytest` | ✅ 60 passed |

Все 6 проверок проходят. Сломанный PR не дал бы такого результата:
- Без date-фильтра 1a и 1b показали бы одинаковые 77 записей.
- Без bell_schedule по weekday lesson 1 в субботу показал бы понедельничное `09:00—10:35`.
- Без `formatLessonNumber` бейджа в бандле не было бы строки `КЧ`.

## Evidence

### Тест 1a — Пн 2026-04-27 (`9РВП-1.25`)
```
count: 3
  #0 08:00:00-08:55:00 | subj='Линейка Классный час' | t='Курбанова Т.В.' | r='201'
  #1 09:00:00-10:35:00 | subj='Основы безопасности и защиты Родины' | t='Москвитин Е.А.' | r='214'
  #2 10:45:00-12:20:00 | subj='История' | t='Жукова М.А.' | r='315'
```

### Тест 1b — Сб 2026-04-25 (`9РВП-1.25`)
```
count: 1
  #1 08:00:00-09:35:00 | subj='ДЕНЬ САМОСТОЯТЕЛ ЬНОЙ РАОТЫ' | t=None | r=None
```
Видно: время `08:00—09:35` (вторнично-субботнее) — НЕ `09:00—10:35` (понедельничное). День недели влияет на тайминг.

### Тест 1c — без `?date` (regression)
```
count: 77
count of distinct dates returned: 23
```
То есть с date-фильтром на выбранный день из 77 общих записей честно возвращается срез на нужную дату (3 для Пн, 1 для Сб).

> Замечание не по теме PR: одна из 77 записей имеет `subj='Линейка КК ул ра бс ас нн оы вй а ч Та .Вс . 201' | t=None | r=None` — это артефакт старого парсера, оставшийся в БД от прежней сессии импорта. Свежий импорт по тому же 2026-04-27 уже отдаёт чистую `'Линейка Классный час'` с корректным `Курбанова Т.В. / 201`. Новые импорты пишут чисто; старые мусорные записи в БД будут затёрты при повторном `import_schedule` на ту же дату (он DELETE'ает по дате перед INSERT'ом), поэтому одного полного `sync_and_import` хватит, чтобы добить.

### Тест 2 — `/schedule/bells`
```
weekday=1: len=8, pair0={'lesson_number': 0, 'label': 'Линейка / Классный час', 'start': '08:00', 'end': '08:55'}
weekday=2: len=7, pair0={'lesson_number': 1, 'label': '1 пара',                  'start': '08:00', 'end': '09:35'}
```

### Тест 3 — production-бандл фронта
```
$ npm run build
✓ built in ...

$ grep -l 'КЧ' dist/assets/*.js
dist/assets/index-DgbkhvES.js

$ grep -o 'formatLessonNumber\|КЧ' dist/assets/*.js | sort | uniq -c
      2 formatLessonNumber
      1 КЧ

$ grep -o '.\{0,40\}КЧ.\{0,40\}' dist/assets/*.js
ally{r.value=!1}}},C=O=>O===0||O==="0"?"КЧ":String(O),F=O=>O?O.substring(0,5):"-",
```
Видно функцию-стрелку `O===0||O==="0"?"КЧ":String(O)` в собранном бандле — это и есть `formatLessonNumber` после минификации.

### pytest
```
60 passed, 116 warnings in 0.81s
```

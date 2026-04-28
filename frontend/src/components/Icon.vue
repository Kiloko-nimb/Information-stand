<template>
  <svg
    class="icon"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    :stroke-width="strokeWidth"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
    focusable="false"
  >
    <g v-html="path" />
  </svg>
</template>

<script>
import { computed } from 'vue'

// Lucide-style stroked SVG paths. Все иконки 24x24, currentColor.
const ICONS = {
  // Расписание / календарь
  calendar:
    '<rect x="3" y="4" width="18" height="18" rx="2" /><path d="M16 2v4M8 2v4M3 10h18" /><path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01" />',

  // Сотрудники / люди
  users:
    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />',

  // Карта
  map:
    '<path d="M9 3 3 5v16l6-2 6 2 6-2V3l-6 2-6-2z" /><path d="M9 3v16M15 5v16" />',

  // FAQ / помощь
  help:
    '<circle cx="12" cy="12" r="10" /><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" /><path d="M12 17h.01" />',

  // Компас (квиз)
  compass:
    '<circle cx="12" cy="12" r="10" /><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" />',

  // Учёба
  graduation:
    '<path d="M22 10v6M2 10l10-5 10 5-10 5z" /><path d="M6 12v5c3 3 9 3 12 0v-5" />',

  // Документ
  fileText:
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><line x1="10" y1="9" x2="8" y2="9" />',

  // Дверь / поступление
  door:
    '<path d="M19 21V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v16" /><line x1="2" y1="21" x2="22" y2="21" /><circle cx="15" cy="12" r="0.5" fill="currentColor" />',

  // Wi-Fi / техника
  wifi:
    '<path d="M5 12.55a11 11 0 0 1 14.08 0" /><path d="M1.42 9a16 16 0 0 1 21.16 0" /><path d="M8.53 16.11a6 6 0 0 1 6.95 0" /><line x1="12" y1="20" x2="12.01" y2="20" />',

  // Деньги
  wallet:
    '<path d="M21 12V7a2 2 0 0 0-2-2H5a2 2 0 0 0 0 4h16v3" /><path d="M3 7v12a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-3" /><circle cx="17" cy="14" r="1.5" />',

  // Студжизнь / праздник
  party:
    '<path d="M5.8 11.3 2 22l10.7-3.79" /><path d="M4 3h.01" /><path d="M22 8h.01" /><path d="M15 2h.01" /><path d="M22 20h.01" /><path d="M22 2 12 12" /><path d="m22 13-3-3-3 3" /><path d="M15 6 9 12" />',

  // Все / стопка книг
  layers:
    '<polygon points="12 2 2 7 12 12 22 7 12 2" /><polyline points="2 17 12 22 22 17" /><polyline points="2 12 12 17 22 12" />',

  // Поиск
  search:
    '<circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />',

  // QR / телефон
  qr:
    '<rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><path d="M14 14h3v3h-3zM20 14h1M14 20h3M17 17h4M20 20v1" />',

  // Стрелка вправо (для ссылок)
  arrowRight:
    '<line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" />',

  // Шеврон (раскрытие)
  chevronRight:
    '<polyline points="9 18 15 12 9 6" />',

  // Звёздочка (галочка достижений)
  sparkles:
    '<path d="M12 3l1.7 4.6L18 9l-4.3 1.4L12 15l-1.7-4.6L6 9l4.3-1.4z" /><path d="M19 14l.7 1.9L21 17l-1.3.6L19 19l-.7-1.4L17 17l1.3-.5z" /><path d="M5 16l.7 1.5L7 18l-1.3.5L5 20l-.7-1.5L3 18l1.3-.5z" />',

  // Стрелка влево (back-button)
  arrowLeft:
    '<line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" />',

  // Геолокация / адрес
  mapPin:
    '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" /><circle cx="12" cy="10" r="3" />',

  // Телефон
  phone:
    '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" />',

  // Сообщение / приёмная
  messageCircle:
    '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />',

  // Глобус
  globe:
    '<circle cx="12" cy="12" r="10" /><line x1="2" y1="12" x2="22" y2="12" /><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />',

  // Перо / обратная связь
  edit:
    '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" /><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />',

  // Колокольчик (звонки)
  bell:
    '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" /><path d="M13.73 21a2 2 0 0 1-3.46 0" />',

  // Газета / новости
  newspaper:
    '<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2" /><path d="M18 14h-8M15 18h-5M10 6h8v4h-8z" />',

  // График / проходные баллы
  barChart:
    '<line x1="12" y1="20" x2="12" y2="10" /><line x1="18" y1="20" x2="18" y2="4" /><line x1="6" y1="20" x2="6" y2="16" />',

  // Цель / специальности
  target:
    '<circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" />',

  // Смартфон / подать документы
  smartphone:
    '<rect x="5" y="2" width="14" height="20" rx="2" ry="2" /><line x1="12" y1="18" x2="12.01" y2="18" />',

  // Лампочка / fun-fact
  lightbulb:
    '<path d="M9 18h6" /><path d="M10 22h4" /><path d="M12 2a7 7 0 0 0-4 12.7c.7.5 1 1.3 1 2.1V18h6v-1.2c0-.8.3-1.6 1-2.1A7 7 0 0 0 12 2z" />',

  // Доступность
  accessibility:
    '<circle cx="12" cy="4" r="2" /><path d="M19 13v-2a7 7 0 0 0-14 0v2" /><path d="M12 6v8" /><path d="M9 14h6" /><path d="M9 22l3-8 3 8" />',

  // Закрыть (×)
  x:
    '<line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />',

  // Солнце (ясно)
  sun:
    '<circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />',

  // Облако
  cloud:
    '<path d="M17.5 19a4.5 4.5 0 1 0-1.4-8.78A6 6 0 0 0 6 12.5 4.5 4.5 0 0 0 6.5 19h11z" />',

  // Солнце+облако (переменная облачность)
  cloudSun:
    '<path d="M12 2v2M5.64 5.64l1.41 1.41M2 13h2M19 13h2M17 6.05l1.41-1.41" /><circle cx="12" cy="11" r="3" /><path d="M19.5 19a3.5 3.5 0 0 0-3-5.4 5 5 0 0 0-9.4 1.4A3.5 3.5 0 0 0 7.5 19h12z" />',

  // Дождь
  cloudRain:
    '<path d="M17.5 17a4.5 4.5 0 1 0-1.4-8.78A6 6 0 0 0 6 10.5 4.5 4.5 0 0 0 6.5 17" /><line x1="8" y1="19" x2="8" y2="22" /><line x1="12" y1="19" x2="12" y2="22" /><line x1="16" y1="19" x2="16" y2="22" />',

  // Снег
  snow:
    '<path d="M17.5 17a4.5 4.5 0 1 0-1.4-8.78A6 6 0 0 0 6 10.5 4.5 4.5 0 0 0 6.5 17" /><path d="M8 20l.01.01M12 20l.01.01M16 20l.01.01M10 22l.01.01M14 22l.01.01" />',

  // Туман
  fog:
    '<path d="M5 5h14M3 10h18M5 15h14M3 20h18" />',

  // Молния (гроза)
  thunder:
    '<path d="M17.5 14a4.5 4.5 0 1 0-1.4-8.78A6 6 0 0 0 6 7.5 4.5 4.5 0 0 0 6.5 14" /><polyline points="13 11 9 17 12 17 11 22 15 16 12 16 13 11" />',

  // Ветер
  wind:
    '<path d="M9.59 4.59A2 2 0 1 1 11 8H2M12.59 19.41A2 2 0 1 0 14 16H2M17.73 7.73A2.5 2.5 0 1 1 19.5 12H2" />',
}

export default {
  name: 'Icon',
  props: {
    name: { type: String, required: true },
    size: { type: [Number, String], default: 24 },
    strokeWidth: { type: [Number, String], default: 1.75 },
  },
  setup(props) {
    const path = computed(() => ICONS[props.name] || '')
    return { path }
  },
}
</script>

<style scoped>
.icon {
  display: inline-block;
  flex-shrink: 0;
  vertical-align: middle;
  color: currentColor;
}
</style>

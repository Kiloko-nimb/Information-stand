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

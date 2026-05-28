// Простой i18n composable без зависимостей.
// Использует словари из ../i18n/messages.js и сохраняет выбор в localStorage.

import { ref, computed, watch } from 'vue'
import { messages, AVAILABLE_LOCALES } from '../i18n/messages'

const STORAGE_KEY = 'kkrit_locale'
const locale = ref('ru')

if (typeof localStorage !== 'undefined') {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved && AVAILABLE_LOCALES.some(l => l.id === saved)) {
    locale.value = saved
  }
}

watch(locale, (v) => {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(STORAGE_KEY, v)
  }
  if (typeof document !== 'undefined') {
    document.documentElement.lang = v
  }
})

// Применяем при инициализации
if (typeof document !== 'undefined') {
  document.documentElement.lang = locale.value
}

function lookup(path, dict) {
  const parts = path.split('.')
  let cur = dict
  for (const p of parts) {
    if (cur && typeof cur === 'object' && p in cur) cur = cur[p]
    else return null
  }
  return typeof cur === 'string' ? cur : null
}

export function useI18n() {
  const t = (path) => {
    return lookup(path, messages[locale.value]) ||
           lookup(path, messages.ru) ||
           path
  }
  const setLocale = (id) => {
    if (AVAILABLE_LOCALES.some(l => l.id === id)) locale.value = id
  }
  const cycleLocale = () => {
    const idx = AVAILABLE_LOCALES.findIndex(l => l.id === locale.value)
    locale.value = AVAILABLE_LOCALES[(idx + 1) % AVAILABLE_LOCALES.length].id
  }
  return { locale, t, setLocale, cycleLocale, locales: AVAILABLE_LOCALES }
}

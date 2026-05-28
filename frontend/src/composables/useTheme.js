// Управление темой оформления: light | dark | contrast | sepia
// Сохраняется в localStorage, применяется к <html data-theme=...>

import { ref, watch } from 'vue'

export const AVAILABLE_THEMES = [
  { id: 'light',    name: 'Светлая',  icon: 'sun' },
  { id: 'dark',     name: 'Тёмная',   icon: 'cloud' },
  { id: 'contrast', name: 'Контраст', icon: 'accessibility' },
  { id: 'sepia',    name: 'Сепия',    icon: 'sparkles' },
]

const STORAGE_KEY = 'kkrit_theme'
const theme = ref('light')

if (typeof localStorage !== 'undefined') {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved && AVAILABLE_THEMES.some(t => t.id === saved)) {
    theme.value = saved
  }
}

function applyTheme(value) {
  if (typeof document === 'undefined') return
  if (value === 'light') {
    document.documentElement.removeAttribute('data-theme')
  } else {
    document.documentElement.setAttribute('data-theme', value)
  }
}

applyTheme(theme.value)

watch(theme, (newValue) => {
  applyTheme(newValue)
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(STORAGE_KEY, newValue)
  }
})

export function useTheme() {
  function setTheme(id) {
    if (AVAILABLE_THEMES.some(t => t.id === id)) {
      theme.value = id
    }
  }
  function cycleTheme() {
    const idx = AVAILABLE_THEMES.findIndex(t => t.id === theme.value)
    const next = AVAILABLE_THEMES[(idx + 1) % AVAILABLE_THEMES.length]
    theme.value = next.id
  }
  return { theme, setTheme, cycleTheme }
}

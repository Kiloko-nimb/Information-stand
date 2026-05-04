import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const IDLE_TIMEOUT = 5 * 60 * 1000 // 5 минут
const isIdle = ref(false)
let timer = null

function resetTimer() {
  isIdle.value = false
  clearTimeout(timer)
  // Не запускать таймер на админских страницах
  if (window.location.pathname.startsWith('/admin')) return
  timer = setTimeout(() => {
    isIdle.value = true
  }, IDLE_TIMEOUT)
}

const events = ['mousedown', 'mousemove', 'keydown', 'touchstart', 'scroll', 'click']

function startIdleDetection() {
  events.forEach(e => document.addEventListener(e, resetTimer, { passive: true }))
  resetTimer()
}

function stopIdleDetection() {
  events.forEach(e => document.removeEventListener(e, resetTimer))
  clearTimeout(timer)
  isIdle.value = false
}

export function useScreensaver() {
  const route = useRoute()

  // Сброс при навигации
  const stopWatch = watch(() => route.path, () => {
    if (route.path.startsWith('/admin')) {
      isIdle.value = false
      clearTimeout(timer)
    } else {
      resetTimer()
    }
  })

  onMounted(() => startIdleDetection())
  onUnmounted(() => {
    stopIdleDetection()
    stopWatch()
  })

  function dismiss() {
    resetTimer()
  }

  return { isIdle, dismiss }
}

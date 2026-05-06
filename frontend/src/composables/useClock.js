/**
 * useClock — реактивные часы (обновляются раз в секунду).
 *
 * Возвращает три ref'а:
 *   currentTime      — '14:32:07'
 *   currentDayName   — 'четверг'
 *   currentDayShort  — '24 апреля'
 *
 * Каждый компонент, использующий useClock, держит свой setInterval —
 * это специально, чтобы при размонтировании компонента таймер тоже
 * умирал и не утекал. Накладные расходы — один Date() в секунду.
 */
import { ref, onMounted, onUnmounted } from 'vue'

export function useClock() {
  const currentTime = ref('')
  const currentDayName = ref('')
  const currentDayShort = ref('')

  let interval = null

  const tick = () => {
    const now = new Date()
    currentTime.value = now.toLocaleTimeString('ru-RU', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
    currentDayName.value = now.toLocaleDateString('ru-RU', { weekday: 'long' })
    currentDayShort.value = now.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
    })
  }

  onMounted(() => {
    tick()
    interval = setInterval(tick, 1000)
  })

  onUnmounted(() => {
    if (interval) {
      clearInterval(interval)
      interval = null
    }
  })

  return { currentTime, currentDayName, currentDayShort }
}

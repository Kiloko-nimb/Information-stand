/**
 * useScheduleStatus — общее состояние «что сейчас идёт» + расписание
 * звонков. Шарится между NowWidget и BellsWidget, чтобы не дёргать
 * /schedule/now дважды на одной странице.
 *
 * При первом вызове запускает поллинг /schedule/now раз в 30 секунд
 * и одноразово грузит /schedule/bells. Поллинг живёт до конца сеанса —
 * для киоска это норма.
 */
import { ref, computed } from 'vue'
import api from '../services/api'

const nowStatus = ref(null)
const bellSchedule = ref([])

let nowInterval = null
let bellsRequested = false

const loadNow = async () => {
  try {
    const response = await api.get('/schedule/now')
    nowStatus.value = response.data
  } catch (_) {
    nowStatus.value = null
  }
}

const loadBells = async () => {
  try {
    const response = await api.get('/schedule/bells')
    bellSchedule.value = Array.isArray(response.data?.pairs) ? response.data.pairs : []
  } catch (_) {
    bellSchedule.value = []
  }
}

export function useScheduleStatus() {
  if (!nowInterval) {
    loadNow()
    nowInterval = setInterval(loadNow, 30_000)
  }
  if (!bellsRequested) {
    bellsRequested = true
    loadBells()
  }

  const currentBellNumber = computed(() => {
    const s = nowStatus.value
    if (!s) return null
    if (s.status === 'in_progress' && s.current?.lesson_number != null) {
      return s.current.lesson_number
    }
    return null
  })

  const nextBellNumber = computed(() => {
    const s = nowStatus.value
    if (!s) return null
    if ((s.status === 'before_classes' || s.status === 'break') && s.next?.lesson_number != null) {
      return s.next.lesson_number
    }
    return null
  })

  return { nowStatus, bellSchedule, currentBellNumber, nextBellNumber }
}

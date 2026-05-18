<!--
  RoomInfoPanel — выезжающая справа панель с расписанием выбранного кабинета
  на выбранный день (по умолчанию — сегодня). Если выбрана
  сегодняшняя дата — дополнительно показывает, идёт ли пара
  сейчас, и подсвечивает текущую пару в списке.

  Грузит данные сама:
    GET /schedule/room/{room}?date=YYYY-MM-DD     — на выбранный день,
    GET /schedule/now                              — только когда выбрана сегодня.
-->
<template>
  <transition name="room-panel">
    <div v-if="roomNumber" class="room-info-panel" role="dialog" aria-modal="false">
      <header class="room-info-panel-head">
        <div class="room-info-panel-title">
          <div class="room-info-panel-num">Кабинет {{ roomNumber }}</div>
          <div v-if="roomType" class="room-info-panel-type">
            <span class="room-type-dot" :class="`room-type-dot--${typeKey}`"></span>
            <span>{{ roomType }}</span>
          </div>
        </div>
        <button class="room-info-panel-close" type="button" aria-label="Закрыть" @click="$emit('close')">×</button>
      </header>

      <div class="room-info-panel-body">
        <div v-if="loading" class="room-info-panel-loading">Загрузка…</div>

        <template v-else>
          <div class="room-info-panel-state" :class="stateBadgeClass">
            <span v-if="nowMatch" class="room-state-dot room-state-dot--busy"></span>
            <span v-else class="room-state-dot room-state-dot--free"></span>
            <span>{{ stateLabel }}</span>
          </div>

          <div v-if="nowMatch" class="room-info-panel-now">
            <div class="now-time">{{ nowMatch.time_start && nowMatch.time_end ? `${formatTime(nowMatch.time_start)}–${formatTime(nowMatch.time_end)}` : '' }}</div>
            <div class="now-subject">{{ nowMatch.subject || '—' }}</div>
            <div class="now-meta">
              <span v-if="nowMatch.group_name">Группа {{ nowMatch.group_name }}</span>
              <span v-if="nowMatch.teacher_name">{{ nowMatch.teacher_name }}</span>
            </div>
          </div>

          <div v-if="todaySchedule.length > 0" class="room-info-panel-list">
            <div class="room-info-panel-list-title">{{ headerDateLabel }}</div>
            <ul>
              <li
                v-for="(item, idx) in todaySchedule"
                :key="idx"
                :class="{ 'is-current': isCurrentItem(item) }"
              >
                <span class="lesson-num">{{ item.lesson_number || '·' }}</span>
                <span class="lesson-time">{{ formatTime(item.time_start) }}–{{ formatTime(item.time_end) }}</span>
                <span class="lesson-subject">{{ item.subject || '—' }}</span>
                <span class="lesson-group" v-if="item.group_name">{{ item.group_name }}</span>
              </li>
            </ul>
          </div>

          <div v-else class="room-info-panel-empty">
            <template v-if="isToday">На сегодня занятий в этом кабинете нет.</template>
            <template v-else>В выбранный день занятий в этом кабинете нет.</template>
          </div>
        </template>
      </div>

      <footer class="room-info-panel-foot">
        <button type="button" class="room-info-panel-action" @click="openSchedule">
          Открыть полное расписание
        </button>
      </footer>
    </div>
  </transition>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const TYPE_KEY_BY_LABEL = {
  'Аудитория': 'auditorium',
  'Лаборатория': 'lab',
  'Спортзал': 'sport',
  'Актовый зал': 'hall',
  'Приёмная': 'admin',
  'Приемная': 'admin',
}

function toLocalDateParam(d) {
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

export default {
  name: 'RoomInfoPanel',
  props: {
    // Номер кабинета. Пустая строка / null — панель скрыта.
    roomNumber: { type: String, default: null },
    // Опциональный тип кабинета (из справочника rooms), нужен только
    // для лейбла и цветной точки в заголовке. Если не передан —
    // подтянем из /rooms/{number} при открытии.
    roomType: { type: String, default: null },
    // Дата, на которую показывать расписание. По умолчанию — сегодня.
    // Если выбрана не сегодняшняя дата, «сейчас»-логика не
    // применяется — панель показывает расписание без подсветки
    // текущей пары и без строки «сейчас идёт».
    selectedDate: { type: Date, default: null },
  },
  emits: ['close'],
  setup(props) {
    const router = useRouter()
    const loading = ref(false)
    const todaySchedule = ref([])
    const nowStatus = ref(null)

    const typeKey = computed(() => TYPE_KEY_BY_LABEL[props.roomType] || 'other')

    // Считаем, что выбрана «сегодняшняя» дата в двух случаях:
    //   • пропс selectedDate не передан (null) — легаси контракт,
    //   • или дата равна сегодняшней (по локальному toDateString).
    const isToday = computed(() => {
      if (!props.selectedDate) return true
      return props.selectedDate.toDateString() === new Date().toDateString()
    })
    const headerDateLabel = computed(() => {
      if (isToday.value) return 'Сегодня в этом кабинете:'
      const d = props.selectedDate || new Date()
      const days = ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
      const months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
      return `${d.getDate()} ${months[d.getMonth()]} (${days[d.getDay()]}) в этом кабинете:`
    })

    // «Сейчас»-привязка работает только для сегодняшней даты; в остальных случаях
    // оба спорных computed-а возвращают null, то есть UI не пытается
    // подсветить какую-либо пару как текущую.
    const nowMatch = computed(() => {
      if (!isToday.value) return null
      const cur = nowStatus.value && nowStatus.value.current
      if (!cur) return null
      return todaySchedule.value.find((s) => Number(s.lesson_number) === Number(cur.lesson_number)) || null
    })

    const nextMatch = computed(() => {
      if (!isToday.value) return null
      const nx = nowStatus.value && nowStatus.value.next
      if (!nx) return null
      return todaySchedule.value.find((s) => Number(s.lesson_number) === Number(nx.lesson_number)) || null
    })

    const stateLabel = computed(() => {
      if (isToday.value) {
        if (nowMatch.value) return 'Сейчас в кабинете идёт пара'
        if (!todaySchedule.value.length) return 'Сегодня кабинет свободен'
        if (nextMatch.value) return `Сейчас свободен. Следующая пара в ${formatTime(nextMatch.value.time_start)}`
        const status = nowStatus.value && nowStatus.value.status
        if (status === 'weekend') return 'Сегодня выходной'
        if (status === 'after_classes') return 'Пары на сегодня закончились'
        if (status === 'before_classes') return 'Пары ещё не начались'
        return 'Сейчас свободен'
      }
      // Другой день: показываем факт в прошедшем/будущем времени,
      // без отношения к реальному времени.
      const count = todaySchedule.value.length
      if (count === 0) return 'В этот день занятий нет'
      return count === 1
        ? 'В этот день 1 занятие'
        : count < 5
          ? `В этот день ${count} занятия`
          : `В этот день ${count} занятий`
    })

    const stateBadgeClass = computed(() => ({
      'room-info-panel-state--busy': isToday.value && !!nowMatch.value,
      'room-info-panel-state--free': !(isToday.value && !!nowMatch.value),
    }))

    const isCurrentItem = (item) => {
      if (!isToday.value) return false
      const cur = nowStatus.value && nowStatus.value.current
      if (!cur) return false
      return Number(item.lesson_number) === Number(cur.lesson_number)
    }

    function formatTime(t) {
      if (!t) return ''
      // Бэкенд возвращает Time как "HH:MM:SS" — режем секунды.
      return String(t).slice(0, 5)
    }

    const load = async () => {
      const num = props.roomNumber
      if (!num) {
        todaySchedule.value = []
        nowStatus.value = null
        return
      }
      loading.value = true
      try {
        const targetDate = props.selectedDate || new Date()
        const dateParam = toLocalDateParam(targetDate)
        // /schedule/now запрашиваем только когда выбрана сегодняшняя дата —
        // для других дат понятие «текущая пара» не применимо.
        const isTodayParam =
          dateParam === toLocalDateParam(new Date())
        const requests = [
          api.get(`/schedule/room/${encodeURIComponent(num)}`, { params: { date: dateParam } }),
        ]
        if (isTodayParam) {
          requests.push(api.get('/schedule/now'))
        }
        const responses = await Promise.all(requests)
        const schedRes = responses[0]
        const nowRes = isTodayParam ? responses[1] : null
        // Сортируем по номеру пары на всякий случай (бэк уже сортирует).
        todaySchedule.value = Array.isArray(schedRes.data)
          ? [...schedRes.data].sort((a, b) => (a.lesson_number || 0) - (b.lesson_number || 0))
          : []
        nowStatus.value = nowRes ? nowRes.data : null
      } catch (e) {
        // Скрытно — на UI просто покажется «занятий нет».
        todaySchedule.value = []
        nowStatus.value = null
      } finally {
        loading.value = false
      }
    }

    watch(
      [() => props.roomNumber, () => props.selectedDate],
      () => { load() },
      { immediate: true },
    )

    const openSchedule = () => {
      if (!props.roomNumber) return
      router.push({ path: '/schedule', query: { type: 'room', q: props.roomNumber } })
    }

    return {
      loading,
      todaySchedule,
      nowMatch,
      stateLabel,
      stateBadgeClass,
      typeKey,
      isToday,
      headerDateLabel,
      isCurrentItem,
      formatTime,
      openSchedule,
    }
  },
}
</script>

<style scoped>
.room-info-panel {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: min(360px, calc(100% - 3rem));
  max-height: calc(100% - 3rem);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg, 18px);
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  z-index: 12;
  overflow: hidden;
}

.room-info-panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1rem 1.1rem 0.6rem;
  gap: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.room-info-panel-num {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text);
}

.room-info-panel-type {
  margin-top: 0.2rem;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.room-type-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(100, 116, 139, 0.6);
  border: 1px solid rgba(100, 116, 139, 0.4);
}

.room-type-dot--auditorium { background: rgba(59, 130, 246, 0.55); border-color: rgba(37, 99, 235, 0.6); }
.room-type-dot--lab        { background: rgba(139, 92, 246, 0.55); border-color: rgba(124, 58, 237, 0.6); }
.room-type-dot--sport      { background: rgba(34, 197, 94, 0.55);  border-color: rgba(22, 163, 74, 0.6);  }
.room-type-dot--hall       { background: rgba(249, 115, 22, 0.55); border-color: rgba(234, 88, 12, 0.6);  }
.room-type-dot--admin      { background: rgba(245, 158, 11, 0.55); border-color: rgba(217, 119, 6, 0.6);  }

.room-info-panel-close {
  appearance: none;
  border: none;
  background: transparent;
  font-size: 1.6rem;
  line-height: 1;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0 0.3rem;
}

.room-info-panel-close:hover { color: var(--text); }

.room-info-panel-body {
  padding: 0.9rem 1.1rem;
  overflow-y: auto;
  flex: 1 1 auto;
}

.room-info-panel-loading,
.room-info-panel-empty {
  font-size: 0.92rem;
  color: var(--text-muted);
  font-style: italic;
}

.room-info-panel-state {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.4rem 0.7rem;
  border-radius: var(--radius-pill, 999px);
  font-size: 0.88rem;
  font-weight: 600;
  margin-bottom: 0.9rem;
}

.room-info-panel-state--free {
  background: rgba(34, 197, 94, 0.12);
  color: #15803d;
  border: 1px solid rgba(22, 163, 74, 0.3);
}

.room-info-panel-state--busy {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
  border: 1px solid rgba(220, 38, 38, 0.3);
}

.room-state-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.room-state-dot--free { background: #16a34a; }
.room-state-dot--busy { background: #dc2626; }

.room-info-panel-now {
  background: rgba(239, 68, 68, 0.06);
  border: 1px solid rgba(220, 38, 38, 0.2);
  border-radius: var(--radius);
  padding: 0.7rem 0.85rem;
  margin-bottom: 0.9rem;
}

.now-time {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 600;
}

.now-subject {
  font-weight: 700;
  font-size: 1rem;
  color: var(--text);
  margin: 0.15rem 0;
}

.now-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 0.8rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.room-info-panel-list-title {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.4rem;
  font-weight: 600;
}

.room-info-panel-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.room-info-panel-list li {
  display: grid;
  grid-template-columns: 24px 80px 1fr auto;
  gap: 0.4rem;
  align-items: baseline;
  padding: 0.4rem 0.5rem;
  border-radius: var(--radius);
  font-size: 0.88rem;
  color: var(--text);
  background: transparent;
  border: 1px solid transparent;
}

.room-info-panel-list li.is-current {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(220, 38, 38, 0.25);
  font-weight: 600;
}

.lesson-num {
  font-weight: 700;
  color: var(--text-muted);
  text-align: center;
}

.lesson-time {
  color: var(--text-muted);
  white-space: nowrap;
}

.lesson-subject {
  color: var(--text);
}

.lesson-group {
  color: var(--text-muted);
  font-size: 0.82rem;
}

.room-info-panel-foot {
  padding: 0.7rem 1.1rem 0.9rem;
  border-top: 1px solid var(--border);
}

.room-info-panel-action {
  width: 100%;
  padding: 0.65rem 0.9rem;
  border-radius: var(--radius);
  border: 1px solid transparent;
  background: var(--accent-gradient, linear-gradient(135deg, #2563eb, #3b82f6));
  color: #fff;
  font-weight: 700;
  cursor: pointer;
  transition: transform var(--transition), filter var(--transition);
}

.room-info-panel-action:hover {
  transform: translateY(-1px);
  filter: brightness(1.05);
}

.room-panel-enter-active,
.room-panel-leave-active {
  transition: opacity 220ms ease, transform 220ms ease;
}

.room-panel-enter-from,
.room-panel-leave-to {
  opacity: 0;
  transform: translateX(8px);
}

@media (max-width: 720px) {
  .room-info-panel {
    top: auto;
    bottom: 1rem;
    right: 1rem;
    left: 1rem;
    width: auto;
    max-height: 70%;
  }
}
</style>

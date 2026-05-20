<!--
  DateCarousel — переиспользуемая полоска дат.

  Использование:
    <DateCarousel v-model="selectedDate" :dates-with-schedule="setOfYmd" />

  - v-model — Date (selected day, по умолчанию сегодня).
  - dates-with-schedule — Set<string> в формате 'YYYY-MM-DD'. На картах
    помечаются зелёной точкой. Можно не передавать.

  Внутри: горизонтальная карусель с ±N дней вокруг выбранной даты,
  стрелки prev/next, кнопка-календарь (нативный input[type=date]),
  кнопка «Сегодня» когда выбран не сегодняшний день. Карусель
  бесконечная: при подходе к краю автоматически дотягивает ещё неделю.
-->
<template>
  <div class="date-carousel">
    <button class="carousel-arrow" type="button" @click="previousDay" aria-label="Предыдущий день">‹</button>
    <button
      v-if="!isToday"
      class="carousel-today"
      type="button"
      @click="goToToday"
      aria-label="Перейти к сегодняшней дате"
      title="Перейти к сегодняшней дате"
    >
      <span class="carousel-today-icon">↺</span>
      <span class="carousel-today-label">Сегодня</span>
    </button>
    <div
      class="date-cards-container"
      ref="dateScrollEl"
      @wheel.prevent="onDateWheel"
      @scroll.passive="onDateScroll"
    >
      <div class="date-cards">
        <button
          v-for="(day, index) in dateRange"
          :key="index"
          type="button"
          :class="['date-card', { active: isSelectedDate(day), 'has-schedule': hasScheduleOnDate(day) }]"
          @click="selectDate(day)"
        >
          <div class="date-day">{{ formatDayName(day) }}</div>
          <div class="date-number">{{ formatDayNumber(day) }}</div>
          <div class="date-month">{{ formatMonthName(day) }}</div>
        </button>
      </div>
    </div>
    <button class="carousel-arrow" type="button" @click="nextDay" aria-label="Следующий день">›</button>
    <button class="carousel-picker" type="button" @click="openDatePicker" aria-label="Выбрать дату" title="Выбрать дату">
      <Icon name="calendar" :size="20" />
    </button>
    <input
      ref="datePickerEl"
      type="date"
      class="date-picker-input"
      :value="toDateParam(modelValue)"
      @change="onDatePicked"
    />
  </div>
</template>

<script>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import Icon from './Icon.vue'

// Сколько дней в обе стороны держим в карусели по умолчанию. На сенсорном
// киоске пользователь свайпает агрессивно; при подходе к краю onDateScroll
// дотянет ещё неделю.
const DATE_RANGE_BACKWARD = 7
const DATE_RANGE_FORWARD = 14

const toDateParam = (d) => {
  if (!(d instanceof Date)) return ''
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

export default {
  name: 'DateCarousel',
  components: { Icon },
  props: {
    modelValue: { type: Date, required: true },
    // Set<'YYYY-MM-DD'> — на этих датах рисуем зелёную точку.
    datesWithSchedule: { type: Object, default: () => new Set() },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const dateRange = ref([])
    const dateScrollEl = ref(null)
    const datePickerEl = ref(null)

    const generateDateRange = () => {
      const dates = []
      const anchor = new Date(props.modelValue)
      for (let i = -DATE_RANGE_BACKWARD; i <= DATE_RANGE_FORWARD; i++) {
        const date = new Date(anchor)
        date.setDate(anchor.getDate() + i)
        dates.push(date)
      }
      dateRange.value = dates
    }

    // Расширяем диапазон вперёд/назад, не пересоздавая массив, чтобы
    // прокрутка не дёргалась и не теряла позицию (просто дописываем
    // новые `Date` к концу/началу).
    const extendDateRange = (direction) => {
      if (!dateRange.value.length) return
      const ADD = 7
      if (direction === 'forward') {
        const last = dateRange.value[dateRange.value.length - 1]
        const tail = []
        for (let i = 1; i <= ADD; i++) {
          const d = new Date(last)
          d.setDate(last.getDate() + i)
          tail.push(d)
        }
        dateRange.value = [...dateRange.value, ...tail]
      } else if (direction === 'backward') {
        const first = dateRange.value[0]
        const head = []
        for (let i = ADD; i >= 1; i--) {
          const d = new Date(first)
          d.setDate(first.getDate() - i)
          head.push(d)
        }
        // Сохраняем визуальную позицию: после prepend'а scrollLeft нужно
        // сместить на ширину добавленных карточек, иначе «улетим» в начало.
        // Корректировку делаем без `scroll-behavior: smooth` — иначе сенсорный
        // экран показывает рывок при инерционной прокрутке к началу.
        const el = dateScrollEl.value
        const before = el ? el.scrollWidth : 0
        dateRange.value = [...head, ...dateRange.value]
        if (el) {
          requestAnimationFrame(() => {
            const delta = el.scrollWidth - before
            const prevBehavior = el.style.scrollBehavior
            el.style.scrollBehavior = 'auto'
            el.scrollLeft += delta
            el.style.scrollBehavior = prevBehavior
          })
        }
      }
    }

    // Ставим в true перед программным scrollTo, чтобы onDateScroll не вызывал
    // extendDateRange.
    let suppressScrollEdgeCheck = false

    const onDateScroll = (event) => {
      if (suppressScrollEdgeCheck) return
      const el = event.currentTarget
      if (!el) return
      const EDGE = 120
      const atStart = el.scrollLeft <= EDGE
      const atEnd = el.scrollLeft + el.clientWidth >= el.scrollWidth - EDGE
      if (atEnd) extendDateRange('forward')
      if (atStart) extendDateRange('backward')
    }

    // Центрируем активную карточку в видимой области. На сенсорном киоске
    // делаем это без анимации (CSS `scroll-behavior: smooth` иначе вызывает
    // лишний пробег после монтирования) и через двойной rAF — чтобы
    // дождаться завершения раскладки контейнера (его ширина в момент
    // mounted может быть ещё 0, например внутри скрытой transition).
    const scrollSelectedIntoCenter = () => {
      const run = () => {
        const container = dateScrollEl.value
        if (!container) return
        // Если контейнер ещё не получил ширину — ждём следующего кадра.
        if (container.clientWidth === 0) {
          requestAnimationFrame(run)
          return
        }
        const active = container.querySelector('.date-card.active')
        if (!active) return
        const containerRect = container.getBoundingClientRect()
        const activeRect = active.getBoundingClientRect()
        const delta =
          (activeRect.left + activeRect.width / 2) -
          (containerRect.left + containerRect.width / 2)
        const maxScroll = Math.max(0, container.scrollWidth - container.clientWidth)
        const target = Math.max(0, Math.min(maxScroll, container.scrollLeft + delta))
        suppressScrollEdgeCheck = true
        // CSS свойство `scroll-behavior: smooth` действует на любой scroll-call,
        // включая программный. На монтировании это вызывает заметный «прыжок»
        // на сенсорном экране. Временно отключаем smooth для прямой установки.
        const prevBehavior = container.style.scrollBehavior
        container.style.scrollBehavior = 'auto'
        container.scrollLeft = target
        container.style.scrollBehavior = prevBehavior
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            suppressScrollEdgeCheck = false
          })
        })
      }
      nextTick(() => {
        requestAnimationFrame(run)
      })
    }

    const openDatePicker = () => {
      const el = datePickerEl.value
      if (!el) return
      if (typeof el.showPicker === 'function') {
        try { el.showPicker(); return } catch (_) { /* fallback */ }
      }
      el.click()
      el.focus()
    }

    const update = (newDate) => {
      emit('update:modelValue', newDate)
    }

    const onDatePicked = (event) => {
      const value = event.target.value
      if (!value) return
      const [yyyy, mm, dd] = value.split('-').map(Number)
      update(new Date(yyyy, mm - 1, dd))
    }

    const onDateWheel = (event) => {
      const el = dateScrollEl.value
      if (!el) return
      el.scrollLeft += event.deltaY !== 0 ? event.deltaY : event.deltaX
    }

    const days = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    const months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

    const formatDayName = (date) => {
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(today.getDate() + 1)
      if (date.toDateString() === today.toDateString()) return 'Сегодня'
      if (date.toDateString() === tomorrow.toDateString()) return 'Завтра'
      return days[date.getDay()]
    }

    const formatDayNumber = (date) => date.getDate()
    const formatMonthName = (date) => months[date.getMonth()]

    const isSelectedDate = (date) =>
      date.toDateString() === props.modelValue.toDateString()

    const hasScheduleOnDate = (date) => {
      const set = props.datesWithSchedule
      if (!set || typeof set.has !== 'function') return false
      return set.has(toDateParam(date))
    }

    const selectDate = (date) => {
      update(date)
    }

    const previousDay = () => {
      const next = new Date(props.modelValue)
      next.setDate(next.getDate() - 1)
      update(next)
    }

    const nextDay = () => {
      const next = new Date(props.modelValue)
      next.setDate(next.getDate() + 1)
      update(next)
    }

    const isToday = computed(() => {
      const t = new Date()
      return props.modelValue.toDateString() === t.toDateString()
    })

    const goToToday = () => {
      update(new Date())
    }

    // На каждое изменение выбранной даты перегенерируем «окно» вокруг неё
    // и подгоняем скролл, чтобы активная карточка была в центре.
    watch(
      () => props.modelValue,
      () => {
        generateDateRange()
        scrollSelectedIntoCenter()
      },
    )

    onMounted(() => {
      generateDateRange()
      scrollSelectedIntoCenter()
    })

    return {
      dateRange,
      dateScrollEl,
      datePickerEl,
      isToday,
      isSelectedDate,
      hasScheduleOnDate,
      formatDayName,
      formatDayNumber,
      formatMonthName,
      toDateParam,
      selectDate,
      previousDay,
      nextDay,
      goToToday,
      openDatePicker,
      onDatePicked,
      onDateWheel,
      onDateScroll,
    }
  },
}
</script>

<style scoped>
.date-carousel {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 1rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
}

.carousel-arrow {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 1.5rem;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.carousel-arrow:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: scale(1.08);
}

.carousel-today {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--accent-soft);
  border: 1px solid var(--accent-border);
  color: var(--accent);
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0 0.95rem;
  height: 44px;
  border-radius: var(--radius-pill);
  cursor: pointer;
  flex-shrink: 0;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
}

.carousel-today:hover {
  background: var(--accent);
  color: #ffffff;
  border-color: var(--accent);
  transform: translateY(-1px);
}

.carousel-today-icon {
  font-size: 1.05rem;
  line-height: 1;
}

.carousel-picker {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 1.2rem;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
}

.carousel-picker:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: scale(1.08);
}

.date-picker-input {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
  pointer-events: none;
}

.date-cards-container {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -ms-overflow-style: none;
  /* `scroll-snap` на сенсорном киоске вызывал рывки при свайпе:
     браузер постоянно «возвращал» позицию к ближайшей карточке
     уже во время инерционного скролла. Также `scroll-snap-align: start`
     было применено к контейнеру `.date-cards`, а не к самим карточкам.
     Карусель остаётся плавной без snap — пользователь сам останавливает
     её в нужной позиции. */
  min-width: 0;
  /* Сглаживание инерционного скролла на iOS-сафари и тач-устройствах. */
  -webkit-overflow-scrolling: touch;
  /* touch-action: pan-x запрещает вертикальный скролл/жесты внутри полосы,
     чтобы свайп по датам не «дёргал» страницу вверх-вниз. */
  touch-action: pan-x;
}

.date-cards-container::-webkit-scrollbar {
  display: none;
}

.date-cards {
  display: flex;
  gap: 0.6rem;
  padding: 0.25rem 0;
  scrollbar-width: none;
}

.date-cards::-webkit-scrollbar {
  display: none;
}

.date-card {
  min-width: 110px;
  padding: 0.9rem 0.75rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  color: var(--text);
  flex-shrink: 0;
}

.date-card:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateY(-2px);
}

.date-card.active {
  background: var(--accent-gradient);
  border-color: transparent;
  color: #ffffff;
  box-shadow: var(--accent-glow);
}

.date-card.has-schedule {
  position: relative;
}

.date-card.has-schedule::after {
  content: '';
  position: absolute;
  bottom: 6px;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 6px rgba(74, 222, 128, 0.5);
}

.date-card.active.has-schedule::after {
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 4px rgba(255, 255, 255, 0.4);
}

.date-day {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.date-card.active .date-day {
  color: rgba(255, 255, 255, 0.85);
}

.date-number {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.02em;
}

.date-month {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.date-card.active .date-month {
  color: rgba(255, 255, 255, 0.78);
}
</style>

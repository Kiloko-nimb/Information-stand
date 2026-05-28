<!--
  BellsWidget — расписание звонков (полный список пар на день).
  Чистый таймлайн с акцентом на переменах.
-->
<template>
  <div
    v-if="bellSchedule.length > 0"
    class="bells-widget"
    v-ripple="{ color: 'rgba(37, 99, 235, 0.18)' }"
    @click="$router.push('/schedule')"
  >
    <div class="bells-head">
      <div class="bells-head-left">
        <span class="bells-icon"><Icon name="bell" :size="22" /></span>
        <span class="bells-title">Расписание звонков</span>
      </div>
      <span class="bells-day">{{ currentDayName }}</span>
    </div>

    <div class="bells-timeline">
      <template v-for="(pair, index) in bellSchedule" :key="'pair-' + pair.start">
        <!-- Карточка пары -->
        <div
          class="pair-card"
          :class="{
            'pair-card--current': pair.lesson_number === currentBellNumber,
            'pair-card--next': pair.lesson_number === nextBellNumber,
          }"
        >
          <div class="pair-num">{{ pair.lesson_number > 0 ? pair.lesson_number : '·' }}</div>
          <div class="pair-info">
            <div class="pair-label">{{ pair.label }}</div>
            <div class="pair-time">{{ pair.start }} — {{ pair.end }}</div>
          </div>
          <div v-if="pair.lesson_number === currentBellNumber" class="pair-badge pair-badge--now">
            <span class="pair-badge-dot"></span>
            Идёт
          </div>
          <div v-else-if="pair.lesson_number === nextBellNumber" class="pair-badge pair-badge--next">
            Следующая
          </div>
        </div>

        <!-- Перемена -->
        <div v-if="index < bellSchedule.length - 1" class="break-row">
          <div class="break-pill">
            <Icon name="coffee" :size="14" class="break-icon" />
            <span class="break-text">Перемена · {{ calculateBreak(pair.end, bellSchedule[index + 1].start) }}</span>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import Icon from '../Icon.vue'
import { useScheduleStatus } from '../../composables/useScheduleStatus'
import { useClock } from '../../composables/useClock'

export default {
  name: 'BellsWidget',
  components: { Icon },
  setup() {
    const { bellSchedule, currentBellNumber, nextBellNumber } = useScheduleStatus()
    const { currentDayName } = useClock()

    const calculateBreak = (endPrev, startNext) => {
      try {
        const [h1, m1] = endPrev.split(':').map(Number)
        const [h2, m2] = startNext.split(':').map(Number)
        const diff = (h2 * 60 + m2) - (h1 * 60 + m1)
        if (diff > 0) return `${diff} мин`
        return ''
      } catch (e) {
        return ''
      }
    }

    return { bellSchedule, currentBellNumber, nextBellNumber, currentDayName, calculateBreak }
  },
}
</script>

<style scoped>
.bells-widget {
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 1.5rem 1.75rem 1.75rem;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: box-shadow var(--transition), border-color var(--transition);
  display: flex;
  flex-direction: column;
}

.bells-widget:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow);
}

/* Шапка виджета */
.bells-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.bells-head-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bells-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--accent-soft);
  color: var(--accent);
  border-radius: var(--radius-md);
}

.bells-title {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: var(--text);
}

.bells-day {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: capitalize;
  background: var(--surface-strong);
  padding: 0.3rem 0.75rem;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border);
}

/* Таймлайн */
.bells-timeline {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

/* Карточка пары */
.pair-card {
  display: grid;
  grid-template-columns: 44px 1fr auto;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  transition: all var(--transition);
}

.pair-num {
  width: 44px;
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-strong);
  color: var(--text-muted);
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.pair-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.pair-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 0.01em;
}

.pair-time {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}

.pair-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-pill);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.pair-badge--now {
  background: var(--accent-gradient);
  color: #fff;
  box-shadow: 0 4px 12px -2px rgba(37, 99, 235, 0.4);
}

.pair-badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #fff;
  animation: pulse-dot 1.6s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.pair-badge--next {
  background: rgba(245, 158, 11, 0.15);
  color: #b45309;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

/* Активная пара */
.pair-card--current {
  background: var(--accent-soft);
  border-color: var(--accent);
  border-width: 2px;
  padding: calc(0.85rem - 1px) calc(1rem - 1px);
  box-shadow: 0 6px 20px -8px rgba(37, 99, 235, 0.4);
}

.pair-card--current .pair-num {
  background: var(--accent-gradient);
  color: #fff;
}

.pair-card--current .pair-label {
  color: var(--accent);
}

.pair-card--current .pair-time {
  color: var(--accent-strong, var(--accent));
}

/* Следующая пара */
.pair-card--next {
  background: rgba(245, 158, 11, 0.04);
  border-color: rgba(245, 158, 11, 0.25);
}

.pair-card--next .pair-num {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: #fff;
}

/* Блок перемены */
.break-row {
  display: flex;
  justify-content: center;
  position: relative;
  margin: 0.1rem 0;
}

.break-row::before,
.break-row::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
  align-self: center;
  margin: 0 0.75rem;
}

.break-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0.85rem;
  background: var(--surface-strong);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

.break-icon {
  color: #f59e0b;
}

.break-text {
  white-space: nowrap;
}

/* Портретный режим (киоск) */
@media (orientation: portrait) and (min-height: 2400px) {
  .bells-widget {
    padding: 2rem 2.25rem;
  }
  .pair-card {
    padding: 1.1rem 1.25rem;
    grid-template-columns: 56px 1fr auto;
  }
  .pair-num {
    width: 56px;
    height: 56px;
    font-size: 1.35rem;
  }
  .pair-time {
    font-size: 1.35rem;
  }
  .pair-label {
    font-size: 1rem;
  }
  .bells-title {
    font-size: 1.3rem;
  }
  .pair-badge {
    font-size: 0.85rem;
    padding: 0.45rem 1rem;
  }
}
</style>

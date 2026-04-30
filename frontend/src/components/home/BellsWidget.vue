<!--
  BellsWidget — расписание звонков (полный список пар на день).
  Подсвечивает текущую и следующую пару по данным из /schedule/now.
  Если /schedule/bells вернул пусто — виджет не рендерится.
-->
<template>
  <div v-if="bellSchedule.length > 0" class="bells-widget" @click="$router.push('/schedule')">
    <div class="bells-head">
      <span class="bells-icon"><Icon name="bell" :size="24" /></span>
      <span class="bells-title">Расписание звонков</span>
      <span class="bells-day">{{ currentDayName }}</span>
    </div>
    <div class="bells-list">
      <div
        v-for="pair in bellSchedule"
        :key="pair.label + pair.start"
        class="bell-item"
        :class="{
          'bell-item--current': pair.lesson_number === currentBellNumber,
          'bell-item--next': pair.lesson_number === nextBellNumber,
        }"
      >
        <div class="bell-num">{{ pair.lesson_number > 0 ? pair.lesson_number : '·' }}</div>
        <div class="bell-info">
          <div class="bell-label">{{ pair.label }}</div>
          <div class="bell-time">{{ pair.start }}–{{ pair.end }}</div>
        </div>
        <div v-if="pair.lesson_number === currentBellNumber" class="bell-tag bell-tag--now">Сейчас</div>
        <div v-else-if="pair.lesson_number === nextBellNumber" class="bell-tag bell-tag--next">След.</div>
      </div>
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
    return { bellSchedule, currentBellNumber, nextBellNumber, currentDayName }
  },
}
</script>

<style scoped>
.bells-widget {
  margin: 1.25rem auto 0;
  max-width: 880px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem 1.5rem;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: box-shadow var(--transition), border-color var(--transition);
}

.bells-widget:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow);
}

.bells-head {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px dashed var(--border);
}

.bells-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.bells-title {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: var(--text);
}

.bells-day {
  margin-left: auto;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: capitalize;
}

.bells-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 0.5rem;
}

.bell-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.75rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  position: relative;
  transition: border-color var(--transition), background var(--transition);
}

.bell-num {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-strong);
  color: var(--text-muted);
  border-radius: 50%;
  font-size: 0.85rem;
  font-weight: 800;
}

.bell-info {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
  flex: 1;
}

.bell-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bell-time {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  font-variant-numeric: tabular-nums;
}

.bell-tag {
  position: absolute;
  top: -8px;
  right: 8px;
  padding: 0.1rem 0.55rem;
  border-radius: 999px;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #ffffff;
}

.bell-tag--now {
  background: var(--accent-gradient);
  box-shadow: 0 4px 12px -2px rgba(37, 99, 235, 0.5);
}

.bell-tag--next {
  background: linear-gradient(135deg, var(--accent-3), #EF4444);
}

.bell-item--current {
  background: var(--accent-soft);
  border-color: var(--accent-border);
}

.bell-item--current .bell-num {
  background: var(--accent-gradient);
  color: #ffffff;
}

.bell-item--current .bell-label {
  color: var(--accent);
}

.bell-item--next {
  background: rgba(245, 158, 11, 0.08);
  border-color: rgba(245, 158, 11, 0.30);
}

.bell-item--next .bell-num {
  background: linear-gradient(135deg, var(--accent-3), #EF4444);
  color: #ffffff;
}
</style>

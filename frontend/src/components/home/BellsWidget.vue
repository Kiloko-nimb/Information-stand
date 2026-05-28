<!--
  BellsWidget — расписание звонков (полный список пар на день).
  С акцентом на переменах между парами (требование №3).
-->
<template>
  <div
    v-if="bellSchedule.length > 0"
    class="bells-widget"
    v-ripple="{ color: 'rgba(37, 99, 235, 0.18)' }"
    @click="$router.push('/schedule')"
  >
    <div class="bells-head">
      <span class="bells-icon"><Icon name="bell" :size="24" /></span>
      <span class="bells-title">Расписание звонков</span>
      <span class="bells-day">{{ currentDayName }}</span>
    </div>
    
    <div class="bells-timeline">
      <template v-for="(pair, index) in bellSchedule" :key="'pair-' + pair.start">
        <!-- Блок самой пары -->
        <div 
          class="bell-item"
          :class="{
            'bell-item--current': pair.lesson_number === currentBellNumber,
            'bell-item--next': pair.lesson_number === nextBellNumber,
          }"
        >
          <div class="bell-num">{{ pair.lesson_number > 0 ? pair.lesson_number : '·' }}</div>
          <div class="bell-info">
            <div class="bell-label">{{ pair.label }}</div>
            <div class="bell-time">{{ pair.start }} – {{ pair.end }}</div>
          </div>
          <div v-if="pair.lesson_number === currentBellNumber" class="bell-tag bell-tag--now">Сейчас</div>
          <div v-else-if="pair.lesson_number === nextBellNumber" class="bell-tag bell-tag--next">След.</div>
        </div>

        <!-- Блок перемены (между текущей и следующей парой, если это не последняя пара) -->
        <div v-if="index < bellSchedule.length - 1" class="break-item">
          <div class="break-line"></div>
          <div class="break-content">
            <Icon name="coffee" :size="14" class="break-icon" />
            <span class="break-text">Перемена {{ calculateBreak(pair.end, bellSchedule[index + 1].start) }}</span>
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

    // Функция для расчета длительности перемены в минутах
    const calculateBreak = (endPrev, startNext) => {
      try {
        const [h1, m1] = endPrev.split(':').map(Number)
        const [h2, m2] = startNext.split(':').map(Number)
        
        const minutes1 = h1 * 60 + m1
        const minutes2 = h2 * 60 + m2
        
        const diff = minutes2 - minutes1
        if (diff > 0) return `${diff} мин.`
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
  margin: 0 auto;
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem 1.5rem;
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
  color: var(--accent);
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
  background: var(--surface-strong);
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-pill);
}

/* Изменено отображение с сетки на вертикальный таймлайн */
.bells-timeline {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.bell-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  position: relative;
  transition: border-color var(--transition), background var(--transition);
}

.bell-num {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-strong);
  color: var(--text-muted);
  border-radius: 50%;
  font-size: 0.95rem;
  font-weight: 800;
}

.bell-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 0;
  flex: 1;
}

.bell-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
}

.bell-time {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text);
  font-variant-numeric: tabular-nums;
  background: var(--background);
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}

/* Стили для перемен */
.break-item {
  display: flex;
  align-items: center;
  margin: 0.25rem 0;
  padding-left: 1.6rem; /* Выравнивание по центру кружка с номером */
  opacity: 0.8;
}

.break-line {
  width: 2px;
  height: 20px;
  background: repeating-linear-gradient(to bottom, var(--border) 0, var(--border) 4px, transparent 4px, transparent 8px);
  margin-right: 1.2rem;
}

.break-content {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--surface-strong);
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-pill);
  color: var(--text-dim);
}

.break-icon {
  color: var(--accent-3);
}

.break-text {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.bell-tag {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.1rem 0.55rem;
  border-radius: 999px;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #ffffff;
  z-index: 2;
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
  transform: scale(1.02);
  z-index: 1;
  box-shadow: var(--shadow-sm);
}

.bell-item--current .bell-num {
  background: var(--accent-gradient);
  color: #ffffff;
}

.bell-item--current .bell-label {
  color: var(--accent);
}

.bell-item--current .bell-time {
  background: white;
  border-color: var(--accent-border);
  color: var(--accent-strong);
}

.bell-item--next {
  background: rgba(245, 158, 11, 0.05);
  border-color: rgba(245, 158, 11, 0.20);
}

.bell-item--next .bell-num {
  background: linear-gradient(135deg, var(--accent-3), #EF4444);
  color: #ffffff;
}

@media (orientation: portrait) and (min-height: 2400px) {
  .bells-widget {
    padding: 2rem 2.25rem;
  }
  .bell-item {
    padding: 1rem 1.25rem;
  }
  .bell-time {
    font-size: 1.2rem;
  }
}
</style>

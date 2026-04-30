<!--
  NowWidget — карточка «Что сейчас идёт» в шапке главной.
  Реагирует на статус из /schedule/now: до пар, перерыв, идёт пара,
  пары закончились, выходной. Клик уводит на /schedule.
-->
<template>
  <div v-if="widget" class="now-widget" @click="$router.push('/schedule')">
    <div class="now-icon">{{ widget.icon }}</div>
    <div class="now-text">
      <div class="now-title">{{ widget.title }}</div>
      <div v-if="widget.line1" class="now-line">{{ widget.line1 }}</div>
      <div v-if="widget.line2" class="now-line now-line-dim">{{ widget.line2 }}</div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useScheduleStatus } from '../../composables/useScheduleStatus'

export default {
  name: 'NowWidget',
  setup() {
    const { nowStatus } = useScheduleStatus()

    const widget = computed(() => {
      const s = nowStatus.value
      if (!s) return null
      if (s.status === 'weekend') {
        return {
          icon: '☕',
          title: 'Сегодня выходной',
          line1: 'Занятий в воскресенье нет',
          line2: null,
        }
      }
      if (s.status === 'before_classes' && s.next) {
        return {
          icon: '🕔',
          title: 'До начала пар',
          line1: `${s.next.label}: ${s.next.start}—${s.next.end}`,
          line2: s.next.minutes_until != null
            ? `Начало через ${s.next.minutes_until} мин`
            : null,
        }
      }
      if (s.status === 'break' && s.next) {
        return {
          icon: '☕',
          title: 'Сейчас перерыв',
          line1: `Следующая — ${s.next.label}: ${s.next.start}—${s.next.end}`,
          line2: s.next.minutes_until != null
            ? `Через ${s.next.minutes_until} мин`
            : null,
        }
      }
      if (s.status === 'after_classes') {
        return {
          icon: '🌙',
          title: 'Пары на сегодня закончились',
          line1: 'До встречи завтра!',
          line2: null,
        }
      }
      if (s.status === 'in_progress' && s.current) {
        const groups = s.current.busy_groups
        const groupsLabel = groups ? `занято групп: ${groups}` : ''
        const left = s.current.minutes_left != null
          ? `Осталось ${s.current.minutes_left} мин`
          : ''
        return {
          icon: '📚',
          title: `Сейчас идёт ${s.current.label}`,
          line1: `${s.current.start}—${s.current.end}${groups ? '  ·  ' + groupsLabel : ''}`,
          line2: left,
        }
      }
      return null
    })

    return { widget }
  },
}
</script>

<style scoped>
.now-widget {
  position: relative;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem 2rem;
  margin: 2rem auto 0.75rem;
  max-width: 880px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow);
  cursor: pointer;
  overflow: hidden;
  transition: transform var(--transition), box-shadow var(--transition),
    border-color var(--transition);
}

.now-widget::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--accent-gradient);
  opacity: 0.06;
  pointer-events: none;
  z-index: 0;
}

.now-widget::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 6px;
  background: var(--accent-gradient);
  border-radius: var(--radius-xl) 0 0 var(--radius-xl);
  z-index: 1;
}

.now-widget > * {
  position: relative;
  z-index: 2;
}

.now-widget:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent-border);
}

.now-icon {
  font-size: 3rem;
  flex-shrink: 0;
  filter: drop-shadow(0 4px 10px rgba(37, 99, 235, 0.20));
}

.now-text {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 0;
  flex: 1;
}

.now-title {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: clamp(1.25rem, 1.8vw, 1.6rem);
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1.2;
}

.now-line {
  font-size: clamp(1rem, 1.2vw, 1.1rem);
  color: var(--text-muted);
  font-weight: 500;
}

.now-line-dim {
  font-size: 0.95rem;
  color: var(--text-dim);
}
</style>

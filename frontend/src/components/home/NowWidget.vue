<!--
  NowWidget — карточка «Что сейчас идёт».
  Большой акцентный блок с иконкой, статусом, таймером и мини-лентой новостей.
-->
<template>
  <div v-if="widget" class="now-widget" :class="`now-widget--${widget.variant}`">
    <div class="now-glow"></div>

    <div class="now-content" @click="$router.push('/schedule')">
      <div class="now-header">
        <div class="now-icon-wrap">
          <Icon :name="widget.icon" :size="28" />
        </div>
        <span class="now-status-chip">{{ widget.chip }}</span>
      </div>

      <div class="now-title">{{ widget.title }}</div>

      <div v-if="widget.subtitle" class="now-subtitle">{{ widget.subtitle }}</div>

      <div v-if="widget.timer" class="now-timer">
        <div class="now-timer-value">{{ widget.timer.value }}</div>
        <div class="now-timer-label">{{ widget.timer.label }}</div>
      </div>
    </div>

    <!-- Мини-лента новостей внутри NowWidget -->
    <div v-if="newsItems.length > 0" class="now-news">
      <div class="now-news-head">
        <Icon name="newspaper" :size="16" />
        <span>Свежие новости</span>
      </div>
      <a
        v-for="item in newsItems"
        :key="item.id"
        class="now-news-item"
        :href="item.source_url || 'https://kraskrit.ru/news/'"
        target="_blank"
        rel="noopener"
        @click.stop
      >
        <div class="now-news-thumb">
          <img v-if="item.image_url" :src="item.image_url" :alt="item.title" />
          <Icon v-else name="newspaper" :size="18" />
        </div>
        <div class="now-news-body">
          <div class="now-news-title">{{ item.title }}</div>
          <div class="now-news-meta">{{ formatDate(item.published_date) }}</div>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import Icon from '../Icon.vue'
import { useScheduleStatus } from '../../composables/useScheduleStatus'
import { fetchNews } from '../../services/newsService'

export default {
  name: 'NowWidget',
  components: { Icon },
  setup() {
    const { nowStatus } = useScheduleStatus()
    const newsItems = ref([])

    onMounted(async () => {
      try {
        const items = await fetchNews()
        newsItems.value = (items || []).slice(0, 3)
      } catch (e) {
        newsItems.value = []
      }
    })

    function formatDate(dateStr) {
      if (!dateStr) return ''
      try {
        const d = new Date(dateStr)
        return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })
      } catch {
        return ''
      }
    }

    const widget = computed(() => {
      const s = nowStatus.value
      if (!s) return null

      if (s.status === 'weekend') {
        return {
          variant: 'rest',
          icon: 'coffee',
          chip: 'Выходной',
          title: 'Сегодня выходной',
          subtitle: 'Занятий нет — отдыхайте',
        }
      }

      if (s.status === 'before_classes' && s.next) {
        return {
          variant: 'upcoming',
          icon: 'clock',
          chip: 'До начала',
          title: `${s.next.label}`,
          subtitle: `${s.next.start} — ${s.next.end}`,
          timer: s.next.minutes_until != null
            ? { value: formatMinutes(s.next.minutes_until), label: 'до начала пар' }
            : null,
        }
      }

      if (s.status === 'break' && s.next) {
        return {
          variant: 'break',
          icon: 'coffee',
          chip: 'Перемена',
          title: `Следующая — ${s.next.label}`,
          subtitle: `${s.next.start} — ${s.next.end}`,
          timer: s.next.minutes_until != null
            ? { value: formatMinutes(s.next.minutes_until), label: 'до начала' }
            : null,
        }
      }

      if (s.status === 'after_classes') {
        return {
          variant: 'rest',
          icon: 'sparkles',
          chip: 'Завершено',
          title: 'Пары на сегодня закончились',
          subtitle: 'До встречи завтра!',
        }
      }

      if (s.status === 'in_progress' && s.current) {
        const groups = s.current.busy_groups
        return {
          variant: 'live',
          icon: 'bookOpen',
          chip: 'Идёт сейчас',
          title: s.current.label,
          subtitle: `${s.current.start} — ${s.current.end}${groups ? '  ·  занято групп: ' + groups : ''}`,
          timer: s.current.minutes_left != null
            ? { value: formatMinutes(s.current.minutes_left), label: 'осталось' }
            : null,
        }
      }

      return null
    })

    return { widget, newsItems, formatDate }
  },
}

function formatMinutes(mins) {
  if (mins < 60) return `${mins} мин`
  const h = Math.floor(mins / 60)
  const m = mins % 60
  if (m === 0) return `${h} ч`
  return `${h} ч ${m} мин`
}
</script>

<style scoped>
.now-widget {
  position: relative;
  padding: 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  overflow: hidden;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
  min-height: 220px;
  display: flex;
  flex-direction: column;
}

.now-widget:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* Декоративное свечение в углу */
.now-glow {
  position: absolute;
  top: -50%;
  right: -30%;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.25;
  pointer-events: none;
  z-index: 0;
  transition: opacity var(--transition);
}

.now-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.now-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.now-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.now-status-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.85rem;
  border-radius: var(--radius-pill);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.now-title {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: clamp(1.3rem, 1.8vw, 1.6rem);
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1.25;
}

.now-subtitle {
  font-size: 0.95rem;
  color: var(--text-muted);
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}

.now-timer {
  margin-top: auto;
  padding-top: 0.85rem;
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  border-top: 1px solid var(--border);
}

.now-timer-value {
  font-family: var(--font-display);
  font-size: clamp(2rem, 3.5vw, 2.75rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  font-variant-numeric: tabular-nums;
  line-height: 1;
}

.now-timer-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: lowercase;
}

/* ============= Варианты ============= */

/* Идёт пара — синий */
.now-widget--live {
  border-color: var(--accent-border, rgba(37, 99, 235, 0.3));
}
.now-widget--live .now-glow {
  background: radial-gradient(circle, #2563eb 0%, transparent 70%);
}
.now-widget--live .now-icon-wrap {
  background: var(--accent-gradient);
  color: #fff;
  box-shadow: 0 8px 24px -6px rgba(37, 99, 235, 0.5);
}
.now-widget--live .now-status-chip {
  background: var(--accent-gradient);
  color: #fff;
}
.now-widget--live .now-timer-value {
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* Скоро / до начала — оранжевый */
.now-widget--upcoming {
  border-color: rgba(245, 158, 11, 0.3);
}
.now-widget--upcoming .now-glow {
  background: radial-gradient(circle, #f59e0b 0%, transparent 70%);
}
.now-widget--upcoming .now-icon-wrap {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  color: #fff;
  box-shadow: 0 8px 24px -6px rgba(245, 158, 11, 0.5);
}
.now-widget--upcoming .now-status-chip {
  background: rgba(245, 158, 11, 0.15);
  color: #b45309;
}
.now-widget--upcoming .now-timer-value {
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* Перемена — зелёный */
.now-widget--break {
  border-color: rgba(16, 185, 129, 0.3);
}
.now-widget--break .now-glow {
  background: radial-gradient(circle, #10b981 0%, transparent 70%);
}
.now-widget--break .now-icon-wrap {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  box-shadow: 0 8px 24px -6px rgba(16, 185, 129, 0.5);
}
.now-widget--break .now-status-chip {
  background: rgba(16, 185, 129, 0.15);
  color: #047857;
}
.now-widget--break .now-timer-value {
  background: linear-gradient(135deg, #10b981, #059669);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* Отдых / закончилось / выходной — серый */
.now-widget--rest .now-glow {
  background: radial-gradient(circle, #6b7280 0%, transparent 70%);
  opacity: 0.15;
}
.now-widget--rest .now-icon-wrap {
  background: var(--surface-strong);
  color: var(--text-muted);
}
.now-widget--rest .now-status-chip {
  background: var(--surface-strong);
  color: var(--text-muted);
  border: 1px solid var(--border);
}

/* === Мини-лента новостей внутри NowWidget === */
.now-news {
  position: relative;
  z-index: 1;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px dashed var(--border);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.now-news-head {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}
.now-news-item {
  display: grid;
  grid-template-columns: 44px 1fr;
  align-items: center;
  gap: 0.7rem;
  padding: 0.55rem 0.65rem;
  background: var(--surface-strong, rgba(0, 0, 0, 0.02));
  border: 1px solid var(--border);
  border-radius: var(--radius-md, 10px);
  text-decoration: none;
  color: inherit;
  transition: background 0.15s ease, transform 0.15s ease, border-color 0.15s ease;
}
.now-news-item:hover {
  background: var(--surface-hover, rgba(37, 99, 235, 0.04));
  border-color: rgba(37, 99, 235, 0.25);
  transform: translateX(2px);
}
.now-news-thumb {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-strong, rgba(0, 0, 0, 0.04));
  color: var(--text-muted);
  flex-shrink: 0;
}
.now-news-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.now-news-body {
  min-width: 0;
}
.now-news-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0.15rem;
}
.now-news-meta {
  font-size: 0.72rem;
  color: var(--text-muted);
  font-weight: 500;
}

@media (orientation: portrait) and (min-height: 2400px) {
  .now-news-title {
    font-size: 1rem;
  }
  .now-news-thumb {
    width: 56px;
    height: 56px;
  }
}
</style>

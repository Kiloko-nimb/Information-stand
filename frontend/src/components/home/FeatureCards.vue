<!--
  FeatureCards — основной блок навигации главной: 4 крупные плитки
  («Расписание», «Сотрудники», «Навигация», «Частые вопросы»).
  Полностью статичный блок — только маршрутизация по router.push.

  Prop `accessibilityMode` отвечает за режим доступности:
    в нём плитки увеличиваются (см. .accessibility-active в стилях).
-->
<template>
  <div class="features" :class="{ 'accessibility-active': accessibilityMode }">
    <div class="feature-card" v-ripple="{ color: 'rgba(37, 99, 235, 0.22)' }" @click="$router.push('/schedule')">
      <div class="feature-icon"><Icon name="calendar" :size="34" /></div>
      <h2>Расписание</h2>
      <p>Найдите расписание по группе или преподавателю</p>
    </div>

    <div class="feature-card" v-ripple="{ color: 'rgba(37, 99, 235, 0.22)' }" @click="$router.push('/staff')">
      <div class="feature-icon"><Icon name="users" :size="34" /></div>
      <h2>Сотрудники</h2>
      <p>Информация о преподавателях и администрации</p>
    </div>

    <div class="feature-card" v-ripple="{ color: 'rgba(37, 99, 235, 0.22)' }" @click="$router.push('/map')">
      <div class="feature-icon"><Icon name="map" :size="34" /></div>
      <h2>Навигация</h2>
      <p>Найдите нужный кабинет на карте колледжа</p>
    </div>

    <div class="feature-card" v-ripple="{ color: 'rgba(37, 99, 235, 0.22)' }" @click="$router.push('/faq')">
      <div class="feature-icon"><Icon name="help" :size="34" /></div>
      <h2>Частые вопросы</h2>
      <p>Справки, документы, поступление</p>
    </div>
  </div>
</template>

<script>
import Icon from '../Icon.vue'

export default {
  name: 'FeatureCards',
  components: { Icon },
  props: {
    accessibilityMode: { type: Boolean, default: false },
  },
}
</script>

<style scoped>
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

/* Портретный 4K: 4 карточки в ряд сжимаются в узкие полоски — делаем
   2×2 сетку с увеличенными карточками. */
@media (orientation: portrait) and (min-height: 2400px) {
  .features {
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
  }
  .feature-card {
    min-height: 360px;
    padding: 3.5rem 2.5rem;
  }
}

.feature-card {
  position: relative;
  padding: 2.5rem 2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition),
    transform var(--transition), box-shadow var(--transition);
  box-shadow: var(--shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 260px;
  justify-content: center;
}

.feature-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--accent-gradient);
  opacity: 0;
  transition: opacity var(--transition);
  pointer-events: none;
  mix-blend-mode: overlay;
}

.feature-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--accent-gradient);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--transition-slow);
}

.feature-card:hover {
  transform: translateY(-4px);
  background: var(--surface-hover);
  border-color: var(--accent-border);
  box-shadow: var(--shadow-lg), var(--accent-glow);
}

.feature-card:hover::before {
  opacity: 0.05;
}

.feature-card:hover::after {
  transform: scaleX(1);
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin-bottom: 1.25rem;
  border-radius: 18px;
  background: var(--accent-soft);
  color: var(--accent);
  transition: transform var(--transition-slow), background var(--transition),
    color var(--transition);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.18);
}

.feature-card:hover .feature-icon {
  transform: translateY(-3px) rotate(-3deg);
  background: var(--accent);
  color: #ffffff;
}

.feature-card h2 {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.feature-card p {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.5;
  max-width: 280px;
}

/* ── Режим доступности ── */
.features.accessibility-active {
  order: 2;
  margin-top: 0;
  margin-bottom: 6rem;
  gap: 1.25rem;
}

.features.accessibility-active .feature-card {
  min-height: 220px;
  padding: 2rem 1.5rem;
}

.features.accessibility-active .feature-icon {
  width: 72px;
  height: 72px;
}

.features.accessibility-active .feature-card h2 {
  font-size: 1.5rem;
}

.features.accessibility-active .feature-card p {
  font-size: 0.95rem;
}
</style>

<!--
  Home — главный экран киоска. Шапка с приветствием и часами,
  виджет «Сейчас идёт», расписание звонков, контакты, блок
  «Абитуриенту», навигация по разделам, новости и кнопка
  включения режима доступности.

  Сами виджеты вынесены в `components/home/*` — этот файл сейчас
  отвечает только за компоновку, плавающую кнопку доступности и
  макетные стили (`.top-section` / `.middle-section` / `.bottom-section`,
  поведение в режиме доступности).
-->
<template>
  <div class="home" :class="{ 'accessibility-active': accessibilityMode }">
    <div class="top-section">
      <BentoHero />
      <NowWidget />
      <BellsWidget />
    </div>

    <div class="middle-section">
      <!-- Резервное вертикальное пространство между шапкой и контактами -->
    </div>

    <div class="bottom-section">
      <ContactInfo :accessibility-mode="accessibilityMode" />
      <ApplicantSection v-if="!accessibilityMode" />
      <FactWidget :hidden="accessibilityMode" />
      <FeatureCards :accessibility-mode="accessibilityMode" />
      <NewsSection v-if="!accessibilityMode" />
    </div>

    <button
      class="accessibility-button"
      :class="{ active: accessibilityMode }"
      @click="toggleAccessibilityMode"
    >
      <Icon v-if="!accessibilityMode" name="accessibility" :size="24" />
      <Icon v-else name="x" :size="24" />
    </button>
  </div>
</template>

<script>
import { ref } from 'vue'
import Icon from '../components/Icon.vue'
import BentoHero from '../components/home/BentoHero.vue'
import NowWidget from '../components/home/NowWidget.vue'
import BellsWidget from '../components/home/BellsWidget.vue'
import ContactInfo from '../components/home/ContactInfo.vue'
import ApplicantSection from '../components/home/ApplicantSection.vue'
import FactWidget from '../components/home/FactWidget.vue'
import FeatureCards from '../components/home/FeatureCards.vue'
import NewsSection from '../components/home/NewsSection.vue'

export default {
  name: 'Home',
  components: {
    Icon,
    BentoHero,
    NowWidget,
    BellsWidget,
    ContactInfo,
    ApplicantSection,
    FactWidget,
    FeatureCards,
    NewsSection,
  },
  setup() {
    const accessibilityMode = ref(false)

    const toggleAccessibilityMode = () => {
      accessibilityMode.value = !accessibilityMode.value
    }

    return { accessibilityMode, toggleAccessibilityMode }
  },
}
</script>

<style scoped>
.home {
  max-width: var(--content-max-width, 1400px);
  margin: 0 auto;
  position: relative;
  padding-bottom: 5rem;
}

.top-section {
  padding: 1.5rem 0 1rem;
  transition: all 0.6s var(--ease);
}

.middle-section {
  min-height: 0;
  transition: min-height 0.6s var(--ease);
}

.bottom-section {
  transform: translateY(0);
}

.subtitle {
  font-size: clamp(1rem, 1.6vw, 1.2rem);
  color: var(--text-muted);
  max-width: 640px;
  margin: 0 auto 2rem;
  font-weight: 500;
  line-height: 1.5;
}

/* ── Плавающая кнопка доступности ── */
.accessibility-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--surface-strong);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border-strong);
  color: var(--text);
  font-size: 1.75rem;
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: transform var(--transition-slow), background var(--transition),
    box-shadow var(--transition);
  z-index: 1000;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.accessibility-button:hover {
  transform: scale(1.08);
  background: var(--surface-hover);
  box-shadow: var(--shadow-lg);
}

.accessibility-button.active {
  background: var(--success-soft);
  border-color: rgba(52, 211, 153, 0.5);
  box-shadow: var(--shadow), 0 0 24px rgba(52, 211, 153, 0.3);
}

/* ========== РЕЖИМ ДОСТУПНОСТИ ==========
   Прижимаем интерактивные блоки к нижней трети экрана, чтобы
   пользователю на коляске было удобнее дотянуться. */
.home.accessibility-active {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-bottom: 7rem;
}

.home.accessibility-active .top-section {
  order: 1;
  margin-bottom: 1rem;
  padding-top: 1rem;
  flex: 0 0 auto;
}

.home.accessibility-active h1 {
  font-size: clamp(1.75rem, 3vw, 2.2rem);
  margin-bottom: 0.5rem;
}

.home.accessibility-active .subtitle {
  font-size: 1rem;
  margin-bottom: 1rem;
}

.home.accessibility-active .middle-section {
  order: 2;
  flex: 1 1 auto;
  min-height: 8vh;
  background: radial-gradient(ellipse at center, rgba(37, 99, 235, 0.06) 0%, transparent 70%);
}

.home.accessibility-active .bottom-section {
  order: 3;
  flex: 0 0 auto;
  animation: slideUp 0.6s var(--ease);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

<!--
  Home — главный экран киоска. 
  Переработан с использованием системы вкладок (Студент / Абитуриент / Преподаватель)
-->
<template>
  <div class="home">
    <div class="top-section">
      <BentoHero />
    </div>

    <!-- Переключатель ролей (Вкладки) -->
    <div class="role-tabs-wrapper">
      <div class="role-tabs">
        <button 
          :class="['tab-btn', { active: activeRole === 'student' }]" 
          @click="activeRole = 'student'"
        >
          <Icon name="bookOpen" :size="22" />
          <span>Студент</span>
        </button>
        <button 
          :class="['tab-btn', { active: activeRole === 'applicant' }]" 
          @click="activeRole = 'applicant'"
        >
          <Icon name="graduationCap" :size="22" />
          <span>Абитуриент</span>
        </button>
        <button 
          :class="['tab-btn', { active: activeRole === 'teacher' }]" 
          @click="activeRole = 'teacher'"
        >
          <Icon name="briefcase" :size="22" />
          <span>Преподаватель</span>
        </button>
      </div>
    </div>

    <div class="middle-section">
      <!-- КОНТЕНТ ДЛЯ СТУДЕНТА -->
      <transition name="fade-slide" mode="out-in">
        <div v-if="activeRole === 'student'" key="student" class="role-content">
          <div class="widgets-row">
            <NowWidget />
            <BellsWidget />
          </div>
          <FeatureCards />
          <NewsSection />
          <FactWidget />
        </div>

        <!-- КОНТЕНТ ДЛЯ АБИТУРИЕНТА -->
        <div v-else-if="activeRole === 'applicant'" key="applicant" class="role-content">
          <ApplicantSection />
          <ContactInfo />
        </div>

        <!-- КОНТЕНТ ДЛЯ ПРЕПОДАВАТЕЛЯ -->
        <div v-else-if="activeRole === 'teacher'" key="teacher" class="role-content">
          <div class="teacher-placeholder">
            <Icon name="briefcase" :size="48" class="placeholder-icon" />
            <h3>Раздел для преподавателей</h3>
            <p>Здесь скоро появится расписание преподавателей, список кабинетов и важные объявления.</p>
          </div>
          <div class="widgets-row">
            <BellsWidget />
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import BentoHero from '../components/home/BentoHero.vue'
import NowWidget from '../components/home/NowWidget.vue'
import BellsWidget from '../components/home/BellsWidget.vue'
import ContactInfo from '../components/home/ContactInfo.vue'
import ApplicantSection from '../components/home/ApplicantSection.vue'
import FactWidget from '../components/home/FactWidget.vue'
import FeatureCards from '../components/home/FeatureCards.vue'
import NewsSection from '../components/home/NewsSection.vue'
import Icon from '../components/Icon.vue'

export default {
  name: 'Home',
  components: {
    BentoHero,
    NowWidget,
    BellsWidget,
    ContactInfo,
    ApplicantSection,
    FactWidget,
    FeatureCards,
    NewsSection,
    Icon
  },
  setup() {
    // По умолчанию показываем вкладку студента (так как это самый частый сценарий для киоска)
    const activeRole = ref('student')

    return {
      activeRole
    }
  }
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

/* Стили для переключателя вкладок */
.role-tabs-wrapper {
  display: flex;
  justify-content: center;
  margin: 2rem 0 3rem;
  position: relative;
  z-index: 10;
}

.role-tabs {
  display: inline-flex;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  padding: 0.5rem;
  gap: 0.5rem;
  box-shadow: var(--shadow-sm);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: transparent;
  border: none;
  border-radius: var(--radius-pill);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.3s var(--ease);
}

.tab-btn:hover {
  color: var(--text);
  background: var(--surface-hover);
}

.tab-btn.active {
  background: var(--accent);
  color: white;
  box-shadow: 0 4px 12px rgba(var(--accent-rgb), 0.3);
}

.role-content {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.widgets-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.teacher-placeholder {
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius-xl);
  padding: 4rem 2rem;
  text-align: center;
  color: var(--text-muted);
}

.placeholder-icon {
  color: var(--border);
  margin-bottom: 1.5rem;
}

.teacher-placeholder h3 {
  color: var(--text);
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
}

/* Анимация переключения вкладок */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s var(--ease);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* ===== Портретный 4K-режим ===== */
@media (orientation: portrait) and (min-height: 2400px) {
  .home {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding-bottom: 8rem;
  }
  .top-section {
    padding: 3rem 0 2rem;
  }
  .role-tabs-wrapper {
    margin: 3rem 0 4rem;
  }
  .tab-btn {
    padding: 1.5rem 3rem;
    font-size: 1.4rem;
  }
  .role-content {
    gap: 3.5rem;
  }
}

@media (orientation: portrait) and (min-height: 3200px) {
  .top-section {
    padding: 4rem 0 2.5rem;
  }
  .home {
    padding-bottom: 10rem;
  }
}
</style>

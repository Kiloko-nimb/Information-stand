<!--
  Home — главный экран киоска. Шапка с приветствием и часами,
  виджет «Сейчас идёт», расписание звонков, контакты, блок
  «Абитуриенту», навигация по разделам, новости.

  Сами виджеты вынесены в `components/home/*` — этот файл сейчас
  отвечает только за компоновку и макетные стили
  (`.top-section` / `.middle-section` / `.bottom-section`).
-->
<template>
  <div class="home">
    <div class="top-section">
      <BentoHero />
      <NowWidget />
      <BellsWidget />
    </div>

    <div class="middle-section">
      <!-- Резервное вертикальное пространство между шапкой и контактами -->
    </div>

    <div class="bottom-section">
      <ContactInfo />
      <ApplicantSection />
      <FactWidget />
      <FeatureCards />
      <NewsSection />
    </div>
  </div>
</template>

<script>
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
    BentoHero,
    NowWidget,
    BellsWidget,
    ContactInfo,
    ApplicantSection,
    FactWidget,
    FeatureCards,
    NewsSection,
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

/* ===== Портретный 4K-режим =====
   На высоком вертикальном стенде (напр. 2160×3840) контент сам по
   себе не заполняет экран — остаётся огромная пустая область снизу.
   Делаем .home flex-колонкой на всю высоту, распираем middle-section
   и разводим ритм по секциям. */
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
  .middle-section {
    flex: 1 1 auto;
    min-height: 4rem;
  }
  .bottom-section {
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
  }
}

/* Ещё более «растянутый» режим для настоящего 4K-портрета */
@media (orientation: portrait) and (min-height: 3200px) {
  .top-section {
    padding: 4rem 0 2.5rem;
  }
  .bottom-section {
    gap: 3rem;
  }
  .home {
    padding-bottom: 10rem;
  }
}

.subtitle {
  font-size: clamp(1rem, 1.6vw, 1.2rem);
  color: var(--text-muted);
  max-width: 640px;
  margin: 0 auto 2rem;
  font-weight: 500;
  line-height: 1.5;
}

</style>

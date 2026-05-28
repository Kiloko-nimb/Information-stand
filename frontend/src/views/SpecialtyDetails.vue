<!--
  SpecialtyDetails — детальная страница специальности.
  Показывает: описание, предметы, полезные материалы, рынок труда
  (вакансии и средняя ЗП через trudvsem.ru).
-->
<template>
  <div class="sd" v-if="specialty">
    <button class="back-button" @click="$router.push('/')">
      <Icon name="arrowLeft" :size="20" />
      <span>На главную</span>
    </button>

    <!-- Hero -->
    <header class="sd-hero" :style="{ '--accent': specialty.accent }">
      <div class="sd-hero-icon">{{ specialty.icon }}</div>
      <div class="sd-hero-text">
        <div class="sd-code">{{ specialty.code }}</div>
        <h1>{{ specialty.name }}</h1>
        <p class="sd-qual">{{ specialty.qualification }}</p>
        <div class="sd-meta">
          <span class="sd-pill"><Icon name="clock" :size="16" /> {{ specialty.duration }}</span>
          <span v-if="specialty.note" class="sd-pill sd-pill--warn">{{ specialty.note }}</span>
        </div>
      </div>
    </header>

    <p class="sd-summary">{{ specialty.summary }}</p>

    <!-- Skills -->
    <section class="sd-section">
      <h2><Icon name="sparkles" :size="20" /> Ключевые навыки</h2>
      <div class="sd-skills">
        <span v-for="s in specialty.skills" :key="s" class="sd-skill" :style="{ '--accent': specialty.accent }">
          {{ s }}
        </span>
      </div>
    </section>

    <!-- Subjects -->
    <section class="sd-section">
      <h2><Icon name="bookOpen" :size="20" /> Учебные предметы</h2>
      <div class="sd-subjects">
        <div v-for="(subj, idx) in specialty.subjects" :key="subj" class="sd-subject">
          <span class="sd-subject-num">{{ idx + 1 }}</span>
          <span>{{ subj }}</span>
        </div>
      </div>
    </section>

    <!-- Materials -->
    <section class="sd-section">
      <h2><Icon name="lightbulb" :size="20" /> Полезные материалы</h2>
      <div class="sd-materials">
        <a v-for="m in specialty.materials" :key="m.url" :href="m.url" target="_blank" rel="noopener" class="sd-material">
          <div class="sd-material-icon"><Icon name="fileText" :size="20" /></div>
          <div class="sd-material-text">
            <div class="sd-material-title">{{ m.title }}</div>
            <div class="sd-material-source">{{ m.source }}</div>
          </div>
          <Icon name="arrowRight" :size="18" class="sd-material-arrow" />
        </a>
      </div>
    </section>

    <!-- Market -->
    <section class="sd-section sd-market" :style="{ '--accent': specialty.accent }">
      <h2><Icon name="trendingUp" :size="20" /> Рынок труда</h2>

      <div v-if="loadingMarket" class="sd-market-loading">
        Загружаем данные рынка…
      </div>

      <div v-else-if="market" class="sd-market-grid">
        <div class="sd-stat">
          <div class="sd-stat-value">
            {{ market.avg_salary ? formatSalary(market.avg_salary) : '—' }}
          </div>
          <div class="sd-stat-label">Средняя зарплата</div>
        </div>
        <div class="sd-stat">
          <div class="sd-stat-value">{{ market.total_ru ?? '—' }}</div>
          <div class="sd-stat-label">Вакансий по России</div>
        </div>
        <div class="sd-stat">
          <div class="sd-stat-value">{{ market.total_region ?? '—' }}</div>
          <div class="sd-stat-label">В Красноярском крае</div>
        </div>
      </div>

      <div v-else class="sd-market-loading">Данные временно недоступны</div>

      <div class="sd-market-source">
        Источник: <a href="https://trudvsem.ru/" target="_blank" rel="noopener">trudvsem.ru</a>
        · поиск по запросу «{{ specialty.hhQuery }}»
      </div>
    </section>

    <div class="sd-actions">
      <button class="sd-btn sd-btn--ghost" @click="$router.push('/specialties/compare')">
        <Icon name="barChart" :size="20" /> Сравнить специальности
      </button>
      <button class="sd-btn sd-btn--primary" :style="{ background: specialty.accent }" @click="$router.push('/quiz')">
        <Icon name="compass" :size="20" /> Подобрать профессию
      </button>
    </div>
  </div>

  <div v-else class="sd-empty">
    Специальность не найдена. <router-link to="/">Вернуться на главную</router-link>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { specialties } from '../data/specialties'
import { fetchMarketStats, formatSalary } from '../services/marketService'
import Icon from '../components/Icon.vue'

export default {
  name: 'SpecialtyDetails',
  components: { Icon },
  setup() {
    const route = useRoute()
    const key = computed(() => route.params.key)
    const specialty = computed(() => specialties[key.value] || null)

    const market = ref(null)
    const loadingMarket = ref(false)

    onMounted(async () => {
      if (!specialty.value) return
      loadingMarket.value = true
      market.value = await fetchMarketStats(specialty.value.hhQuery)
      loadingMarket.value = false
    })

    return { specialty, market, loadingMarket, formatSalary }
  },
}
</script>

<style scoped>
.sd {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1rem 2rem 4rem;
  --accent: #2563EB;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--text);
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 1.5rem;
}
.back-button:hover { background: var(--surface-hover); }

.sd-hero {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.5rem;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 14%, var(--surface)), var(--surface));
  border: 1px solid color-mix(in srgb, var(--accent) 30%, var(--border));
  border-radius: 24px;
  margin-bottom: 1.25rem;
}
.sd-hero-icon {
  width: 88px;
  height: 88px;
  border-radius: 22px;
  background: white;
  border: 1px solid var(--border);
  display: grid;
  place-items: center;
  font-size: 2.6rem;
  box-shadow: 0 8px 24px color-mix(in srgb, var(--accent) 25%, transparent);
}
.sd-code {
  font-family: var(--font-mono, monospace);
  font-size: 0.85rem;
  color: var(--accent);
  font-weight: 700;
  letter-spacing: 0.04em;
}
.sd-hero h1 {
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 2.6vw, 2rem);
  margin: 0.3rem 0 0.4rem;
  color: var(--text);
  line-height: 1.15;
}
.sd-qual {
  color: var(--text-muted);
  margin: 0 0 0.85rem;
  font-weight: 500;
}
.sd-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.sd-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.8rem;
  border-radius: 999px;
  background: white;
  border: 1px solid var(--border);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
}
.sd-pill--warn {
  background: #FEF3C7;
  border-color: #FDE68A;
  color: #92400E;
}

.sd-summary {
  font-size: 1.05rem;
  line-height: 1.6;
  color: var(--text-muted);
  padding: 0 0.5rem 0.5rem;
  margin-bottom: 1.5rem;
}

.sd-section {
  margin-bottom: 2rem;
}
.sd-section h2 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text);
  margin: 0 0 0.85rem;
}

.sd-skills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.sd-skill {
  padding: 0.45rem 0.95rem;
  border-radius: 999px;
  background: color-mix(in srgb, var(--accent) 10%, var(--surface));
  border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent);
  color: var(--text);
  font-weight: 600;
  font-size: 0.9rem;
}

.sd-subjects {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.6rem;
}
.sd-subject {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  padding: 0.7rem 0.85rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  font-size: 0.92rem;
  color: var(--text);
}
.sd-subject-num {
  flex-shrink: 0;
  width: 26px;
  height: 26px;
  border-radius: 8px;
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  color: var(--accent);
  font-weight: 800;
  font-size: 0.8rem;
  display: grid;
  place-items: center;
}

.sd-materials {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 0.7rem;
}
.sd-material {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.95rem 1.1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  text-decoration: none;
  color: var(--text);
  transition: all .2s ease;
}
.sd-material:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -10px color-mix(in srgb, var(--accent) 40%, transparent);
}
.sd-material-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  color: var(--accent);
  display: grid;
  place-items: center;
  flex-shrink: 0;
}
.sd-material-text { flex: 1; min-width: 0; }
.sd-material-title { font-weight: 700; font-size: 0.95rem; }
.sd-material-source { font-size: 0.78rem; color: var(--text-muted); margin-top: 0.15rem; }
.sd-material-arrow { color: var(--text-muted); flex-shrink: 0; }

.sd-market {
  background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 8%, var(--surface)), var(--surface));
  border: 1px solid color-mix(in srgb, var(--accent) 25%, var(--border));
  border-radius: 20px;
  padding: 1.5rem;
}
.sd-market-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 0.75rem;
}
.sd-stat {
  background: white;
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.1rem 1.25rem;
}
.sd-stat-value {
  font-family: var(--font-display);
  font-size: clamp(1.4rem, 2.4vw, 1.9rem);
  font-weight: 800;
  color: var(--accent);
  letter-spacing: -0.02em;
}
.sd-stat-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 0.15rem;
}
.sd-market-source {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 0.75rem;
}
.sd-market-source a { color: var(--accent); }
.sd-market-loading {
  padding: 1rem;
  color: var(--text-muted);
  font-style: italic;
}

.sd-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  margin-top: 1.5rem;
}
.sd-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.85rem 1.6rem;
  border-radius: 14px;
  border: none;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: transform .15s ease, box-shadow .2s ease;
}
.sd-btn:hover { transform: translateY(-2px); }
.sd-btn--primary { background: var(--accent); color: white; }
.sd-btn--ghost {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
}

.sd-empty {
  padding: 3rem;
  text-align: center;
  color: var(--text-muted);
}
</style>

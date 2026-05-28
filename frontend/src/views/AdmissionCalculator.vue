<!--
  AdmissionCalculator — калькулятор шансов поступления.
  Студент вводит средний балл аттестата (или баллы по 4 предметам),
  страница показывает шансы на бюджет для каждой специальности.
-->
<template>
  <div class="calc">
    <button class="back-button" @click="$router.push('/')">
      <Icon name="arrowLeft" :size="20" />
      <span>На главную</span>
    </button>

    <header class="calc-header">
      <h1><Icon name="calculator" :size="28" /> Калькулятор шансов на бюджет</h1>
      <p class="calc-subtitle">
        Введи свой средний балл аттестата за 9 классов — увидишь, на какие
        специальности у тебя есть шансы пройти на бюджет в 2026 году.
      </p>
    </header>

    <!-- Способы ввода -->
    <div class="calc-input-mode">
      <button :class="['mode-btn',{active:mode==='avg'}]" @click="mode='avg'">
        Средний балл
      </button>
      <button :class="['mode-btn',{active:mode==='subjects'}]" @click="mode='subjects'">
        По 4 предметам
      </button>
    </div>

    <!-- Ввод среднего балла -->
    <div v-if="mode==='avg'" class="calc-input-card">
      <label class="big-label">Твой средний балл аттестата</label>
      <div class="big-input-wrap">
        <input
          type="number"
          step="0.1"
          min="3.0"
          max="5.0"
          v-model.number="avgScore"
          class="big-input"
        />
        <div class="big-slider-wrap">
          <input type="range" min="3" max="5" step="0.1" v-model.number="avgScore" class="big-slider"/>
          <div class="slider-marks">
            <span>3.0</span><span>4.0</span><span>5.0</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Ввод по 4 предметам -->
    <div v-else class="calc-input-card">
      <label class="big-label">Оценки по предметам (1–5)</label>
      <div class="subjects-grid">
        <div v-for="(s, key) in subjects" :key="key" class="subj-row">
          <span>{{ subjectLabels[key] }}</span>
          <div class="subj-stepper">
            <button @click="adjustSubject(key, -1)">−</button>
            <span class="subj-value">{{ s }}</span>
            <button @click="adjustSubject(key, +1)">+</button>
          </div>
        </div>
      </div>
      <div class="subjects-avg">
        Средний: <strong>{{ computedAvg.toFixed(2) }}</strong>
      </div>
    </div>

    <!-- Результаты -->
    <section class="calc-results">
      <h2>Твои шансы по специальностям</h2>
      <div class="result-grid">
        <div
          v-for="r in results"
          :key="r.key"
          class="result-card"
          :class="`tier-${r.tier}`"
          @click="$router.push(`/specialty/${r.key}`)"
        >
          <div class="rc-header">
            <span class="rc-code">{{ r.code }}</span>
            <span class="rc-tier-badge">{{ tierLabel(r.tier) }}</span>
          </div>
          <h3 class="rc-name">{{ r.name }}</h3>
          <div class="rc-bar-wrap">
            <div class="rc-bar">
              <div class="rc-bar-fill" :style="{ width: r.chance + '%' }"></div>
            </div>
            <span class="rc-chance">{{ r.chance }}%</span>
          </div>
          <div class="rc-meta">
            <span>Нужно ≥ {{ r.passingScore.toFixed(1) }}</span>
            <span class="rc-gap" :class="{ pos: r.gap >= 0, neg: r.gap < 0 }">
              {{ r.gap >= 0 ? '+' : '' }}{{ r.gap.toFixed(1) }}
            </span>
          </div>
        </div>
      </div>

      <p class="calc-disclaimer">
        <Icon name="info" :size="16" />
        Расчёт основан на проходных баллах прошлых лет и носит справочный
        характер. Финальный список — после публикации приказа приёмной
        комиссии. Подробности: <strong>8 (391) 211-44-44</strong>
      </p>
    </section>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import Icon from '../components/Icon.vue'
import { specialties } from '../data/specialties'

export default {
  name: 'AdmissionCalculator',
  components: { Icon },
  setup() {
    const mode = ref('avg')
    const avgScore = ref(4.0)
    const subjects = ref({ math: 4, rus: 4, lang: 4, info: 4 })
    const subjectLabels = {
      math: 'Алгебра',
      rus: 'Русский язык',
      lang: 'Иностранный язык',
      info: 'Информатика',
    }

    function adjustSubject(key, delta) {
      const next = Math.min(5, Math.max(1, subjects.value[key] + delta))
      subjects.value[key] = next
    }

    const computedAvg = computed(() => {
      const vals = Object.values(subjects.value)
      return vals.reduce((a, b) => a + b, 0) / vals.length
    })

    const userScore = computed(() => {
      return mode.value === 'avg' ? avgScore.value : computedAvg.value
    })

    function chanceFor(passing, user) {
      const gap = user - passing
      // Логистическая кривая: +0.3 балла относительно проходного ≈ 90%
      // 0.0 — 50%, −0.3 — 10%
      const x = gap / 0.15
      const sigmoid = 1 / (1 + Math.exp(-x))
      return Math.round(sigmoid * 100)
    }
    function tierFor(chance) {
      if (chance >= 75) return 'high'
      if (chance >= 45) return 'mid'
      if (chance >= 20) return 'low'
      return 'none'
    }
    function tierLabel(tier) {
      return {
        high: '✓ Высокие',
        mid:  '~ Средние',
        low:  '!  Низкие',
        none: '✗ Минимальные',
      }[tier]
    }

    const results = computed(() => {
      const u = userScore.value
      return Object.entries(specialties)
        .map(([key, sp]) => {
          const passing = sp.passingScore || 4.0
          const chance = chanceFor(passing, u)
          return {
            key,
            code: sp.code,
            name: sp.name,
            passingScore: passing,
            chance,
            gap: u - passing,
            tier: tierFor(chance),
          }
        })
        .sort((a, b) => b.chance - a.chance)
    })

    return {
      mode, avgScore, subjects, subjectLabels,
      adjustSubject, computedAvg, results, tierLabel,
    }
  },
}
</script>

<style scoped>
.calc {
  max-width: 1100px;
  margin: 0 auto;
  padding-bottom: 4rem;
}
.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  color: var(--text);
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 1.5rem;
}
.calc-header h1 {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 800;
  margin: 0 0 0.5rem;
}
.calc-subtitle {
  color: var(--text-muted);
  max-width: 700px;
  line-height: 1.5;
  margin: 0 0 1.5rem;
}
.calc-input-mode {
  display: inline-flex;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  padding: 4px;
  margin-bottom: 1.25rem;
}
.mode-btn {
  padding: 0.55rem 1.25rem;
  background: transparent;
  border: 0;
  border-radius: var(--radius-pill);
  color: var(--text-muted);
  font-weight: 600;
  cursor: pointer;
}
.mode-btn.active {
  background: var(--accent-gradient);
  color: #fff;
}
.calc-input-card {
  background: var(--bg-raised);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem 1.75rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-sm);
}
.big-label {
  display: block;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}
.big-input-wrap {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 1.5rem;
  align-items: center;
}
.big-input {
  font-family: var(--font-display);
  font-size: 3.5rem;
  font-weight: 800;
  text-align: center;
  border: 2px solid var(--accent-border);
  background: var(--accent-soft);
  border-radius: var(--radius-md);
  color: var(--accent);
  padding: 0.5rem;
  width: 100%;
  letter-spacing: -0.02em;
}
.big-slider-wrap { display: flex; flex-direction: column; gap: 0.4rem; }
.big-slider {
  appearance: none;
  -webkit-appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 999px;
  background: linear-gradient(90deg, #EF4444 0%, #F59E0B 50%, #22C55E 100%);
  outline: 0;
}
.big-slider::-webkit-slider-thumb {
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #fff;
  border: 3px solid var(--accent);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
}
.slider-marks {
  display: flex;
  justify-content: space-between;
  color: var(--text-muted);
  font-size: 0.8rem;
  font-weight: 600;
}
.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.65rem;
  margin-bottom: 0.75rem;
}
.subj-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.85rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-weight: 600;
}
.subj-stepper {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}
.subj-stepper button {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--bg-raised);
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
}
.subj-value {
  display: inline-grid;
  place-items: center;
  width: 32px;
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--accent);
}
.subjects-avg {
  text-align: right;
  font-size: 0.95rem;
  color: var(--text-muted);
}
.calc-results h2 {
  font-family: var(--font-display);
  font-size: 1.25rem;
  margin: 0 0 1rem;
}
.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.85rem;
}
.result-card {
  background: var(--bg-raised);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1rem 1.15rem;
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition);
}
.result-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}
.result-card.tier-high  { border-color: rgba(34, 197, 94, 0.45); background: rgba(34, 197, 94, 0.06); }
.result-card.tier-mid   { border-color: rgba(245, 158, 11, 0.45); background: rgba(245, 158, 11, 0.06); }
.result-card.tier-low   { border-color: rgba(239, 68, 68, 0.45);  background: rgba(239, 68, 68, 0.06);  }
.result-card.tier-none  { opacity: 0.7; }
.rc-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  margin-bottom: 0.3rem;
}
.rc-code { color: var(--text-muted); font-weight: 700; }
.rc-tier-badge { font-weight: 800; }
.tier-high .rc-tier-badge { color: #16A34A; }
.tier-mid  .rc-tier-badge { color: #D97706; }
.tier-low  .rc-tier-badge { color: #DC2626; }
.tier-none .rc-tier-badge { color: var(--text-muted); }
.rc-name {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 0.65rem;
  line-height: 1.3;
}
.rc-bar-wrap {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.6rem;
  align-items: center;
  margin-bottom: 0.5rem;
}
.rc-bar {
  background: var(--surface);
  border-radius: 999px;
  height: 8px;
  overflow: hidden;
}
.rc-bar-fill {
  height: 100%;
  background: var(--accent-gradient);
  transition: width 350ms var(--ease-spring);
}
.tier-high .rc-bar-fill  { background: linear-gradient(90deg, #16A34A, #22C55E); }
.tier-mid  .rc-bar-fill  { background: linear-gradient(90deg, #D97706, #F59E0B); }
.tier-low  .rc-bar-fill  { background: linear-gradient(90deg, #DC2626, #EF4444); }
.rc-chance {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text);
  min-width: 50px;
  text-align: right;
}
.rc-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.rc-gap.pos { color: #16A34A; font-weight: 700; }
.rc-gap.neg { color: #DC2626; font-weight: 700; }
.calc-disclaimer {
  margin-top: 1.5rem;
  padding: 0.85rem 1rem;
  background: var(--accent-soft);
  border: 1px solid var(--accent-border);
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  color: var(--text-muted);
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  line-height: 1.5;
}
</style>

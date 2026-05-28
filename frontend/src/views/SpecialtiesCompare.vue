<!--
  SpecialtiesCompare — таблица сравнения специальностей ККРИТ.
  Подтягивает живые данные по вакансиям из trudvsem.ru через бэкенд.
-->
<template>
  <div class="sc">
    <button class="back-button" @click="$router.push('/')">
      <Icon name="arrowLeft" :size="20" />
      <span>На главную</span>
    </button>

    <header class="sc-header">
      <h1><Icon name="barChart" :size="28" /> Сравнение специальностей</h1>
      <p class="sc-subtitle">
        Длительность обучения, средняя зарплата и количество вакансий
        по данным «Работы России» (trudvsem.ru). Кликни по строке, чтобы перейти к детальной странице.
      </p>
    </header>

    <div class="sc-table-wrap">
      <table class="sc-table">
        <thead>
          <tr>
            <th>Специальность</th>
            <th>Срок обучения</th>
            <th>Средняя зарплата</th>
            <th>Вакансий по РФ</th>
            <th>В Красноярском крае</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="s in specialtyList"
            :key="s.key"
            class="sc-row"
            :style="{ '--accent': s.accent }"
            @click="$router.push(`/specialty/${s.key}`)"
          >
            <td class="sc-cell-name">
              <div class="sc-spec-icon">{{ s.icon }}</div>
              <div class="sc-spec-text">
                <div class="sc-spec-name">{{ s.name }}</div>
                <div class="sc-spec-code">{{ s.code }} · {{ s.qualification }}</div>
              </div>
            </td>
            <td>
              <span class="sc-pill"><Icon name="clock" :size="14" /> {{ s.duration }}</span>
            </td>
            <td>
              <span v-if="loading[s.key]" class="sc-loading">…</span>
              <span v-else-if="market[s.key]?.avg_salary" class="sc-value sc-value--accent">
                {{ formatSalary(market[s.key].avg_salary) }}
              </span>
              <span v-else class="sc-dash">—</span>
            </td>
            <td>
              <span v-if="loading[s.key]" class="sc-loading">…</span>
              <span v-else-if="market[s.key]?.total_ru != null" class="sc-value">
                {{ market[s.key].total_ru.toLocaleString('ru-RU') }}
              </span>
              <span v-else class="sc-dash">—</span>
            </td>
            <td>
              <span v-if="loading[s.key]" class="sc-loading">…</span>
              <span v-else-if="market[s.key]?.total_region != null" class="sc-value">
                {{ market[s.key].total_region }}
              </span>
              <span v-else class="sc-dash">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sc-footnote">
      Данные о рынке труда обновляются каждый час · источник:
      <a href="https://trudvsem.ru/" target="_blank" rel="noopener">trudvsem.ru</a>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { specialtyList } from '../data/specialties'
import { fetchMarketStats, formatSalary } from '../services/marketService'
import Icon from '../components/Icon.vue'

export default {
  name: 'SpecialtiesCompare',
  components: { Icon },
  setup() {
    const market = reactive({})
    const loading = reactive({})

    onMounted(async () => {
      for (const s of specialtyList) {
        loading[s.key] = true
      }
      await Promise.all(
        specialtyList.map(async (s) => {
          market[s.key] = await fetchMarketStats(s.hhQuery)
          loading[s.key] = false
        })
      )
    })

    return { specialtyList, market, loading, formatSalary }
  },
}
</script>

<style scoped>
.sc {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem 4rem;
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

.sc-header { margin-bottom: 1.5rem; }
.sc-header h1 {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 2.8vw, 2.2rem);
  letter-spacing: -0.02em;
  color: var(--text);
  margin: 0 0 0.5rem;
}
.sc-subtitle {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.5;
  max-width: 780px;
}

.sc-table-wrap {
  overflow-x: auto;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 0.5rem;
}
.sc-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}
.sc-table th {
  text-align: left;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 0.85rem 0.9rem;
  border-bottom: 1px solid var(--border);
}
.sc-row { cursor: pointer; transition: background .15s ease; }
.sc-row:hover { background: color-mix(in srgb, var(--accent) 7%, transparent); }
.sc-row td {
  padding: 0.95rem 0.9rem;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}
.sc-row:last-child td { border-bottom: none; }

.sc-cell-name {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.sc-spec-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: color-mix(in srgb, var(--accent) 15%, transparent);
  display: grid;
  place-items: center;
  font-size: 1.4rem;
  flex-shrink: 0;
}
.sc-spec-name {
  font-weight: 700;
  color: var(--text);
  font-size: 0.95rem;
}
.sc-spec-code {
  color: var(--text-muted);
  font-size: 0.78rem;
  margin-top: 0.15rem;
}

.sc-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.7rem;
  border-radius: 999px;
  background: white;
  border: 1px solid var(--border);
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text);
}

.sc-value {
  font-weight: 700;
  color: var(--text);
  font-size: 0.95rem;
}
.sc-value--accent { color: var(--accent); }
.sc-dash { color: var(--text-dim); }
.sc-loading {
  display: inline-block;
  width: 28px;
  height: 4px;
  background: color-mix(in srgb, var(--accent) 30%, var(--border));
  border-radius: 2px;
  animation: pulse 1.2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

.sc-footnote {
  margin-top: 1rem;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.82rem;
}
.sc-footnote a { color: var(--accent); }
</style>

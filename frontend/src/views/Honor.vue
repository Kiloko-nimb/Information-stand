<template>
  <div class="honor">
    <button class="back-button" @click="$router.push('/')">
      🔙 На главную
    </button>

    <header class="honor-header">
      <span class="honor-eyebrow">Аллея славы</span>
      <h1>Доска почёта ККРИТ</h1>
      <p class="honor-subtitle">
        Лучшие студенты колледжа — победители хакатонов, олимпиад, чемпионатов
        WorldSkills, киберспорта и спортивных соревнований.
      </p>
    </header>

    <nav class="honor-filters">
      <button
        v-for="cat in categories"
        :key="cat.id"
        class="honor-filter"
        :class="{ active: currentCategory === cat.id }"
        @click="currentCategory = cat.id"
      >
        <span class="honor-filter-icon">{{ cat.icon }}</span>
        <span>{{ cat.label }}</span>
        <span v-if="cat.id === 'all'" class="honor-filter-count">{{ entries.length }}</span>
        <span v-else class="honor-filter-count">{{ countByCategory(cat.id) }}</span>
      </button>
    </nav>

    <div v-if="filteredEntries.length === 0" class="honor-empty">
      В этой категории пока нет записей.
    </div>

    <div v-else class="honor-grid">
      <article
        v-for="entry in filteredEntries"
        :key="entry.id"
        class="honor-card"
        :style="{ '--honor-accent': entry.accent }"
      >
        <div class="honor-card-top">
          <div class="honor-avatar" v-if="!entry.photo">
            {{ getInitials(entry.name) }}
          </div>
          <img
            v-else
            class="honor-avatar honor-avatar--photo"
            :src="entry.photo"
            :alt="entry.name"
          />
          <div class="honor-card-meta">
            <div class="honor-name">{{ entry.name }}</div>
            <div class="honor-group">
              <span class="honor-group-pill">{{ entry.group }}</span>
              <span class="honor-year">{{ entry.year }}</span>
            </div>
          </div>
          <div class="honor-icon">{{ categoryIcon(entry.category) }}</div>
        </div>
        <div class="honor-achievement">
          <strong>{{ entry.achievement }}</strong>
        </div>
        <p v-if="entry.description" class="honor-description">{{ entry.description }}</p>
      </article>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { honorEntries, honorCategories, getInitials } from '../data/honor'

export default {
  name: 'Honor',
  setup() {
    const entries = honorEntries
    const categories = honorCategories
    const currentCategory = ref('all')

    const filteredEntries = computed(() => {
      const sorted = [...entries].sort((a, b) => b.year - a.year)
      if (currentCategory.value === 'all') return sorted
      return sorted.filter((e) => e.category === currentCategory.value)
    })

    const countByCategory = (catId) => {
      return entries.filter((e) => e.category === catId).length
    }

    const categoryIcon = (catId) => {
      const cat = categories.find((c) => c.id === catId)
      return cat ? cat.icon : '⭐'
    }

    return {
      entries,
      categories,
      currentCategory,
      filteredEntries,
      countByCategory,
      categoryIcon,
      getInitials,
    }
  },
}
</script>

<style scoped>
.honor {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 5rem;
  position: relative;
}

.back-button {
  position: fixed;
  top: 5.5rem;
  left: 1.5rem;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  padding: 0.7rem 1.1rem;
  border-radius: var(--radius-pill);
  font-weight: 600;
  cursor: pointer;
  z-index: 10;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  box-shadow: var(--shadow-sm);
}

.back-button:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: translateY(-1px);
}

.honor-header {
  text-align: center;
  margin-bottom: 2rem;
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
}

.honor-eyebrow {
  display: inline-block;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.75rem;
}

.honor-header h1 {
  font-family: var(--font-display);
  font-size: clamp(1.9rem, 4.2vw, 2.8rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.1;
  margin: 0 0 0.75rem;
  color: var(--text);
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
}

.honor-subtitle {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.55;
  margin: 0;
}

.honor-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.honor-filter {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 1.1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), color var(--transition);
}

.honor-filter:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
}

.honor-filter.active {
  background: var(--accent-gradient);
  color: #ffffff;
  border-color: transparent;
  box-shadow: var(--shadow-sm);
}

.honor-filter-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 0 0.4rem;
  background: var(--surface-strong);
  color: var(--text-muted);
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.honor-filter.active .honor-filter-count {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.honor-empty {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-muted);
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius-lg);
}

.honor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
  gap: 1.25rem;
}

.honor-card {
  position: relative;
  padding: 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
  overflow: hidden;
}

.honor-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--honor-accent);
}

.honor-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
  border-color: var(--border-hover);
}

.honor-card-top {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 1rem;
}

.honor-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--honor-accent) 100%, transparent), color-mix(in srgb, var(--honor-accent) 70%, transparent));
  color: #ffffff;
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  flex-shrink: 0;
  box-shadow: 0 4px 14px -4px color-mix(in srgb, var(--honor-accent) 60%, transparent);
}

.honor-avatar--photo {
  object-fit: cover;
  background: var(--surface-strong);
}

.honor-card-meta {
  flex: 1;
  min-width: 0;
}

.honor-name {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text);
  margin-bottom: 0.3rem;
  line-height: 1.2;
}

.honor-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.honor-group-pill {
  padding: 0.15rem 0.55rem;
  background: var(--surface-strong);
  border: 1px solid var(--border);
  border-radius: 999px;
  font-weight: 700;
  color: var(--text);
}

.honor-year {
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.honor-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  opacity: 0.8;
}

.honor-achievement {
  font-size: 0.95rem;
  line-height: 1.5;
  color: var(--text);
  margin-bottom: 0.5rem;
  padding: 0.6rem 0.85rem;
  background: color-mix(in srgb, var(--honor-accent) 10%, transparent);
  border-left: 3px solid var(--honor-accent);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

.honor-achievement strong {
  font-weight: 700;
}

.honor-description {
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--text-muted);
  margin: 0;
}

@media (max-width: 600px) {
  .honor-card {
    padding: 1.1rem;
  }
  .honor-avatar {
    width: 48px;
    height: 48px;
    font-size: 1.1rem;
  }
}
</style>

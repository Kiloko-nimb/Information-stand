<!--
  NewsSection — карточки с последними новостями из ВК (kraskrit).
  С поддержкой отображения изображений.
-->
<template>
  <section v-if="newsCards.length > 0" class="news-section">
    <div class="news-header">
      <h2><Icon name="newspaper" :size="22" /> Новости колледжа</h2>
      <a class="news-all-link" href="https://vk.com/kraskrit" target="_blank" rel="noopener">
        Все новости →
      </a>
    </div>
    <div class="news-grid">
      <a
        v-for="item in newsCards"
        :key="item.id"
        class="news-card"
        :href="item.source_url || 'https://vk.com/kraskrit'"
        target="_blank"
        rel="noopener"
      >
        <div class="news-image-container" v-if="item.image_url">
          <img :src="item.image_url" alt="News image" class="news-image" />
        </div>
        <div class="news-icon" v-else>
          <Icon name="newspaper" :size="22" />
        </div>
        
        <div class="news-body">
          <div class="news-date" v-if="item.published_date">{{ formatNewsDate(item.published_date) }}</div>
          <h3 class="news-title">{{ item.title }}</h3>
          <p v-if="item.description" class="news-desc">{{ item.description }}</p>
        </div>
      </a>
    </div>
  </section>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import Icon from '../Icon.vue'
import { fetchNews } from '../../services/newsService'

const NEWS_LIMIT = 5
const CARDS_LIMIT = 3

export default {
  name: 'NewsSection',
  components: { Icon },
  setup() {
    const newsItems = ref([])
    const newsCards = computed(() => newsItems.value.slice(0, CARDS_LIMIT))

    const loadNews = async () => {
      try {
        const data = await fetchNews(NEWS_LIMIT)
        newsItems.value = Array.isArray(data) ? data : []
      } catch (_) {
        newsItems.value = []
      }
    }

    const formatNewsDate = (raw) => {
      if (!raw) return ''
      try {
        return new Date(raw).toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'long',
          year: 'numeric',
        })
      } catch (_) {
        return ''
      }
    }

    onMounted(() => {
      loadNews()
    })

    return { newsCards, formatNewsDate }
  },
}
</script>

<style scoped>
.news-section {
  margin-top: 2.5rem;
}

.news-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.news-header h2 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 0;
}

.news-all-link {
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  padding: 0.45rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  background: var(--surface);
  transition: background var(--transition), border-color var(--transition),
    color var(--transition), transform var(--transition);
}

.news-all-link:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  color: var(--text);
  transform: translateX(2px);
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.news-card {
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: inherit;
  transition: background var(--transition), border-color var(--transition),
    transform var(--transition), box-shadow var(--transition);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  min-height: 140px;
}

.news-card:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}

.news-image-container {
  width: 100%;
  height: 140px;
  overflow: hidden;
  border-bottom: 1px solid var(--border);
  background-color: var(--background);
}

.news-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-icon {
  font-size: 2rem;
  padding: 1.5rem 1.5rem 0 1.5rem;
  line-height: 1;
}

.news-body {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.news-date {
  font-size: 0.8rem;
  color: var(--text-dim);
  font-weight: 500;
  text-transform: lowercase;
}

.news-title {
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--text);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-muted);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

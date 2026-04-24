<template>
  <div class="staff">
    <button class="back-button" @click="$router.push('/')">
      🔙 На главную
    </button>

    <h1>Сотрудники колледжа</h1>

    <div class="search-panel">
      <input
        v-model="searchQuery"
        placeholder="Поиск по ФИО"
        @input="search"
      />
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div v-else class="staff-grid">
      <div class="staff-card" v-for="person in staffList" :key="person.id">
        <div class="staff-avatar">
          <img :src="getAvatarUrl(person)" :alt="person.full_name" />
        </div>
        <div class="staff-info">
          <h3>{{ person.full_name }}</h3>
          <p class="position">{{ person.position }}</p>
          <p class="department">{{ person.department }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'Staff',
  setup() {
    const searchQuery = ref('')
    const staffList = ref([])
    const loading = ref(false)

    const loadStaff = async () => {
      loading.value = true
      try {
        const response = await api.get('/staff')
        staffList.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки:', error)
      } finally {
        loading.value = false
      }
    }

    const search = async () => {
      if (!searchQuery.value.trim()) {
        loadStaff()
        return
      }

      loading.value = true
      try {
        const response = await api.get(`/staff/search?query=${searchQuery.value}`)
        staffList.value = response.data
      } catch (error) {
        console.error('Ошибка поиска:', error)
      } finally {
        loading.value = false
      }
    }

    const getAvatarUrl = (person) => {
      // Если есть фото, используем его
      if (person.photo_url) {
        return person.photo_url
      }
      
      // Иначе генерируем аватарку с инициалами
      const name = encodeURIComponent(person.full_name)
      return `https://ui-avatars.com/api/?name=${name}&background=random&color=fff&size=200&bold=true&font-size=0.4`
    }

    onMounted(() => {
      loadStaff()
    })

    return {
      searchQuery,
      staffList,
      loading,
      search,
      getAvatarUrl
    }
  }
}
</script>


<style scoped>
.staff {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 0 6rem;
  position: relative;
}

/* ── Плавающая кнопка «На главную» ── */
.back-button {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  padding: 0.9rem 1.5rem;
  background: var(--surface-strong);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  color: var(--text);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-pill);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: transform var(--transition), background var(--transition), border-color var(--transition);
  z-index: 1000;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.back-button:hover {
  transform: translateX(-4px);
  background: var(--surface-hover);
  border-color: var(--accent-border);
}

h1 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 3.2vw, 2.4rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  margin-bottom: 1.5rem;
  color: var(--text);
}

.search-panel {
  margin-bottom: 2rem;
}

.search-panel input {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 1rem;
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  color: var(--text);
  transition: border-color var(--transition), background var(--transition), box-shadow var(--transition);
}

.search-panel input::placeholder {
  color: var(--text-dim);
}

.search-panel input:focus {
  outline: none;
  border-color: var(--accent-border);
  background: var(--surface-hover);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
  font-size: 1.1rem;
}

.staff-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
}

.staff-card {
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.75rem 1.25rem 1.5rem;
  box-shadow: var(--shadow-sm);
  transition: background var(--transition), border-color var(--transition), transform var(--transition), box-shadow var(--transition);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.staff-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: var(--accent-gradient);
  opacity: 0.1;
  transition: opacity var(--transition);
}

.staff-card:hover {
  transform: translateY(-4px);
  background: var(--surface-hover);
  border-color: var(--accent-border);
  box-shadow: var(--shadow-lg);
}

.staff-card:hover::before {
  opacity: 0.18;
}

.staff-avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 1rem;
  border: 3px solid var(--bg-base);
  box-shadow: 0 0 0 1px var(--border-strong), var(--shadow-sm);
  transition: transform var(--transition);
  position: relative;
  z-index: 1;
  background: var(--bg-raised);
}

.staff-card:hover .staff-avatar {
  transform: scale(1.05);
}

.staff-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.staff-info {
  position: relative;
  z-index: 1;
}

.staff-info h3 {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin-bottom: 0.4rem;
  color: var(--text);
  line-height: 1.3;
}

.position {
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 500;
  margin: 0 0 0.25rem;
  line-height: 1.4;
}

.department {
  color: var(--text-dim);
  font-size: 0.85rem;
  margin: 0;
  line-height: 1.4;
}
</style>

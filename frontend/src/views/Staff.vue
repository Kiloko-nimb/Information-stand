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

    onMounted(() => {
      loadStaff()
    })

    return {
      searchQuery,
      staffList,
      loading,
      search
    }
  }
}
</script>

<style scoped>
.staff {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.back-button {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  padding: 1.2rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.3rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s;
  z-index: 1000;
}

.back-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.search-panel {
  margin-bottom: 2rem;
}

.search-panel input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #ecf0f1;
  border-radius: 4px;
  font-size: 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.staff-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.staff-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.staff-card:hover {
  transform: translateY(-5px);
}

.staff-info h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.position {
  color: #3498db;
  font-weight: bold;
  margin-bottom: 0.3rem;
}

.department, .room {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}
</style>

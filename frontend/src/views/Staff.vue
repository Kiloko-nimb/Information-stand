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
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.back-button {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  padding: 1.2rem 2rem;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  font-size: 1.3rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1000;
}

.back-button:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 12px 45px rgba(0, 0, 0, 0.4);
  background: rgba(255, 255, 255, 0.35);
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: white;
  text-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.search-panel {
  margin-bottom: 2rem;
}

.search-panel input {
  width: 100%;
  padding: 1.2rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  color: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  transition: all 0.3s;
}

.search-panel input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.search-panel input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.25);
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.3);
}

.loading {
  text-align: center;
  padding: 2rem;
  color: white;
  font-size: 1.2rem;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.staff-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.staff-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.4s;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.staff-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.25);
}

.staff-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 1rem;
  border: 3px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: all 0.3s;
}

.staff-card:hover .staff-avatar {
  transform: scale(1.05);
  border-color: rgba(255, 255, 255, 0.6);
}

.staff-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.staff-info h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: white;
  font-weight: 600;
}

.position {
  color: rgba(255, 255, 255, 0.95);
  font-weight: bold;
  margin-bottom: 0.3rem;
}

.department, .room {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.9rem;
  margin-bottom: 0.3rem;
}
</style>

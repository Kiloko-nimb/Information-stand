<template>
  <div class="schedule">
    <button class="back-button" @click="$router.push('/')">
      🔙 На главную
    </button>

    <h1>Расписание занятий</h1>

    <div class="search-panel">
      <div class="search-tabs">
        <button
          :class="{ active: searchType === 'group' }"
          @click="searchType = 'group'"
        >
          По группе
        </button>
        <button
          :class="{ active: searchType === 'teacher' }"
          @click="searchType = 'teacher'"
        >
          По преподавателю
        </button>
      </div>

      <div class="search-input">
        <input
          v-model="searchQuery"
          :placeholder="searchType === 'group' ? 'Введите номер группы' : 'Введите ФИО преподавателя'"
          @keyup.enter="search"
          list="groups-list"
        />
        <datalist id="groups-list" v-if="searchType === 'group'">
          <option v-for="group in availableGroups" :key="group.name" :value="group.name"></option>
        </datalist>
        <button @click="search">Найти</button>
      </div>
    </div>

    <div v-if="!searched && availableGroups.length > 0" class="groups-list">
      <h2>Доступные группы</h2>
      <div class="groups-grid">
        <button
          v-for="group in availableGroups"
          :key="group.name"
          class="group-card"
          @click="selectGroup(group.name)"
        >
          {{ group.name }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div v-else-if="scheduleData.length > 0" class="schedule-results">
      <div class="schedule-header">
        <h2>{{ searchType === 'group' ? `Группа: ${searchQuery}` : `Преподаватель: ${searchQuery}` }}</h2>
        <div class="schedule-date">{{ formatDate(scheduleData[0]?.date) }}</div>
      </div>

      <div class="schedule-grid">
        <div class="schedule-row header-row">
          <div class="cell time-cell">Время</div>
          <div class="cell lesson-cell">№</div>
          <div class="cell subject-cell">Предмет</div>
          <div class="cell teacher-cell">Преподаватель</div>
          <div class="cell room-cell">Кабинет</div>
        </div>

        <div
          v-for="item in scheduleData"
          :key="item.id"
          class="schedule-row"
          :class="{ 'current-lesson': isCurrentLesson(item) }"
        >
          <div class="cell time-cell">
            <div class="time-range">
              <span class="time-start">{{ formatTime(item.time_start) }}</span>
              <span class="time-separator">-</span>
              <span class="time-end">{{ formatTime(item.time_end) }}</span>
            </div>
          </div>
          <div class="cell lesson-cell">
            <span class="lesson-number">{{ item.lesson_number }}</span>
          </div>
          <div class="cell subject-cell">
            <div class="subject-name">{{ item.subject }}</div>
          </div>
          <div class="cell teacher-cell">
            <span class="teacher-name">{{ item.teacher_name || '-' }}</span>
          </div>
          <div class="cell room-cell">
            <span class="room-number">{{ item.room_number || '-' }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="searched" class="no-results">
      Расписание не найдено
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'Schedule',
  setup() {
    const searchType = ref('group')
    const searchQuery = ref('')
    const scheduleData = ref([])
    const availableGroups = ref([])
    const loading = ref(false)
    const searched = ref(false)

    const loadGroups = async () => {
      try {
        const response = await api.get('/schedule/groups')
        availableGroups.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки групп:', error)
      }
    }

    const selectGroup = (groupName) => {
      searchQuery.value = groupName
      searchType.value = 'group'
      search()
    }

    const search = async () => {
      if (!searchQuery.value.trim()) return

      loading.value = true
      searched.value = true

      try {
        const endpoint = searchType.value === 'group'
          ? `/schedule/group/${searchQuery.value}`
          : `/schedule/teacher/${searchQuery.value}`

        const response = await api.get(endpoint)
        scheduleData.value = response.data.sort((a, b) => a.lesson_number - b.lesson_number)
      } catch (error) {
        console.error('Ошибка поиска:', error)
        scheduleData.value = []
      } finally {
        loading.value = false
      }
    }

    const formatTime = (timeStr) => {
      if (!timeStr) return '-'
      return timeStr.substring(0, 5)
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString('ru-RU', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const isCurrentLesson = (lesson) => {
      const now = new Date()
      const currentTime = now.getHours() * 60 + now.getMinutes()

      if (!lesson.time_start || !lesson.time_end) return false

      const [startH, startM] = lesson.time_start.split(':').map(Number)
      const [endH, endM] = lesson.time_end.split(':').map(Number)

      const startTime = startH * 60 + startM
      const endTime = endH * 60 + endM

      return currentTime >= startTime && currentTime <= endTime
    }

    onMounted(() => {
      loadGroups()
    })

    return {
      searchType,
      searchQuery,
      scheduleData,
      availableGroups,
      loading,
      searched,
      search,
      selectGroup,
      formatTime,
      formatDate,
      isCurrentLesson
    }
  }
}
</script>

<style scoped>
.schedule {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
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
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.search-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-tabs button {
  flex: 1;
  padding: 1rem;
  border: 2px solid #ecf0f1;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  font-weight: 500;
}

.search-tabs button.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.search-tabs button:hover:not(.active) {
  border-color: #3498db;
  background: #f8f9fa;
}

.search-input {
  display: flex;
  gap: 1rem;
}

.search-input input {
  flex: 1;
  padding: 1rem;
  border: 2px solid #ecf0f1;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input input:focus {
  outline: none;
  border-color: #3498db;
}

.search-input button {
  padding: 1rem 2rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background 0.3s;
}

.search-input button:hover {
  background: #2980b9;
}

.loading, .no-results {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
  font-size: 1.2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.groups-list {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.groups-list h2 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.group-card {
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.group-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.schedule-results {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.schedule-header {
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.schedule-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.schedule-date {
  font-size: 1rem;
  opacity: 0.9;
  text-transform: capitalize;
}

.schedule-grid {
  display: flex;
  flex-direction: column;
}

.schedule-row {
  display: grid;
  grid-template-columns: 140px 60px 1fr 250px 100px;
  border-bottom: 1px solid #ecf0f1;
  transition: background-color 0.2s;
}

.schedule-row:hover:not(.header-row) {
  background-color: #f8f9fa;
}

.schedule-row.current-lesson {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.header-row {
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
  position: sticky;
  top: 0;
  z-index: 10;
}

.cell {
  padding: 1rem;
  display: flex;
  align-items: center;
  border-right: 1px solid #ecf0f1;
}

.cell:last-child {
  border-right: none;
}

.time-cell {
  justify-content: center;
  background: #fafbfc;
}

.time-range {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.time-start, .time-end {
  font-weight: 600;
  color: #3498db;
  font-size: 0.95rem;
}

.time-separator {
  color: #bdc3c7;
  font-size: 0.8rem;
}

.lesson-cell {
  justify-content: center;
  background: #fafbfc;
}

.lesson-number {
  font-weight: 700;
  font-size: 1.2rem;
  color: #7f8c8d;
  background: white;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 2px solid #ecf0f1;
}

.subject-cell {
  padding-left: 1.5rem;
}

.subject-name {
  font-weight: 500;
  color: #2c3e50;
  line-height: 1.4;
}

.teacher-cell {
  color: #7f8c8d;
}

.teacher-name {
  font-size: 0.95rem;
}

.room-cell {
  justify-content: center;
  font-weight: 600;
  color: #e74c3c;
  background: #fafbfc;
}

.room-number {
  background: #fff5f5;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: 1px solid #fee;
}

@media (max-width: 1200px) {
  .schedule-row {
    grid-template-columns: 120px 50px 1fr 200px 80px;
  }

  .cell {
    padding: 0.8rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .schedule-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
    padding: 1rem;
  }

  .cell {
    border-right: none;
    border-bottom: 1px solid #ecf0f1;
    padding: 0.5rem;
  }

  .header-row {
    display: none;
  }

  .time-cell::before {
    content: 'Время: ';
    font-weight: 600;
    margin-right: 0.5rem;
  }

  .lesson-cell::before {
    content: 'Пара: ';
    font-weight: 600;
    margin-right: 0.5rem;
  }

  .teacher-cell::before {
    content: 'Преподаватель: ';
    font-weight: 600;
    margin-right: 0.5rem;
  }

  .room-cell::before {
    content: 'Кабинет: ';
    font-weight: 600;
    margin-right: 0.5rem;
  }
}
</style>

<template>
  <div class="schedule">
    <button class="back-button" @click="$router.push('/')">
      🔙 На главную
    </button>

    <h1>Расписание занятий</h1>

    <div class="date-carousel">
      <button class="carousel-arrow" @click="previousDay">‹</button>
      <div class="date-cards-container">
        <div class="date-cards">
          <button
            v-for="(day, index) in dateRange"
            :key="index"
            :class="['date-card', { active: isSelectedDate(day) }]"
            @click="selectDate(day)"
          >
            <div class="date-day">{{ formatDayName(day) }}</div>
            <div class="date-number">{{ formatDayNumber(day) }}</div>
            <div class="date-month">{{ formatMonthName(day) }}</div>
          </button>
        </div>
      </div>
      <button class="carousel-arrow" @click="nextDay">›</button>
    </div>

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
        <div class="schedule-date">{{ formatDate(selectedDate) }}</div>
      </div>

      <div class="timeline-container">
        <div
          v-for="item in scheduleData"
          :key="item.id"
          class="timeline-item"
          :class="{ 'current-lesson': isCurrentLesson(item) }"
        >
          <div class="timeline-marker">
            <div class="lesson-badge">{{ item.lesson_number }}</div>
            <div class="timeline-line"></div>
          </div>
          <div class="timeline-content">
            <div class="lesson-time">
              <span class="time-start">{{ formatTime(item.time_start) }}</span>
              <span class="time-separator">—</span>
              <span class="time-end">{{ formatTime(item.time_end) }}</span>
            </div>
            <div class="lesson-card">
              <div class="lesson-header">
                <h3 class="lesson-subject">{{ item.subject }}</h3>
                <span class="lesson-type">{{ item.lesson_type || 'Лекция' }}</span>
              </div>
              <div class="lesson-details">
                <div class="lesson-detail">
                  <span class="detail-icon">👨‍🏫</span>
                  <span class="detail-text">{{ item.teacher_name || 'Не указан' }}</span>
                </div>
                <div class="lesson-detail">
                  <span class="detail-icon">📍</span>
                  <span class="detail-text">Кабинет {{ item.room_number || '—' }}</span>
                  <button v-if="item.room_number" class="show-on-map-btn" @click="showRoomOnMap(item.room_number)">
                    Показать на карте
                  </button>
                </div>
              </div>
            </div>
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
    const selectedDate = ref(new Date())
    const dateRange = ref([])

    const generateDateRange = () => {
      const dates = []
      const today = new Date()
      for (let i = -1; i <= 5; i++) {
        const date = new Date(today)
        date.setDate(today.getDate() + i)
        dates.push(date)
      }
      dateRange.value = dates
    }

    const formatDayName = (date) => {
      const days = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(today.getDate() + 1)

      if (date.toDateString() === today.toDateString()) return 'Сегодня'
      if (date.toDateString() === tomorrow.toDateString()) return 'Завтра'
      return days[date.getDay()]
    }

    const formatDayNumber = (date) => {
      return date.getDate()
    }

    const formatMonthName = (date) => {
      const months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
      return months[date.getMonth()]
    }

    const isSelectedDate = (date) => {
      return date.toDateString() === selectedDate.value.toDateString()
    }

    const selectDate = (date) => {
      selectedDate.value = date
      if (searchQuery.value.trim()) {
        search()
      }
    }

    const previousDay = () => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() - 1)
      selectedDate.value = newDate
      generateDateRange()
    }

    const nextDay = () => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() + 1)
      selectedDate.value = newDate
      generateDateRange()
    }

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

    const formatDate = (date) => {
      if (!date) return ''
      const d = date instanceof Date ? date : new Date(date)
      return d.toLocaleDateString('ru-RU', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const showRoomOnMap = (roomNumber) => {
      alert(`Навигация к кабинету ${roomNumber}.\n\nЭта функция откроет карту с маршрутом до кабинета.`)
      // В будущем: this.$router.push({ path: '/map', query: { room: roomNumber } })
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
      generateDateRange()
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
      isCurrentLesson,
      dateRange,
      selectedDate,
      formatDayName,
      formatDayNumber,
      formatMonthName,
      isSelectedDate,
      selectDate,
      previousDay,
      nextDay,
      showRoomOnMap
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

.date-carousel {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 1.5rem;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.carousel-arrow {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  font-size: 2rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.carousel-arrow:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: scale(1.1);
}

.date-cards-container {
  flex: 1;
  overflow: hidden;
}

.date-cards {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0.5rem 0;
  scrollbar-width: none;
}

.date-cards::-webkit-scrollbar {
  display: none;
}

.date-card {
  min-width: 120px;
  padding: 1.2rem 1rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  color: white;
  flex-shrink: 0;
}

.date-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.date-card.active {
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.5) 0%, rgba(41, 128, 185, 0.5) 100%);
  border-color: rgba(52, 152, 219, 0.8);
  box-shadow: 0 8px 30px rgba(52, 152, 219, 0.4);
  transform: scale(1.05);
}

.date-day {
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  opacity: 0.9;
}

.date-number {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
}

.date-month {
  font-size: 0.85rem;
  opacity: 0.8;
  text-transform: uppercase;
}

.search-panel {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
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
  color: white;
  font-size: 1.2rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.groups-list {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 2rem;
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  margin-bottom: 2rem;
}

.groups-list h2 {
  margin: 0 0 1.5rem 0;
  color: white;
  font-size: 1.5rem;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
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
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
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

.timeline-container {
  padding: 2rem;
  position: relative;
}

.timeline-item {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  position: relative;
  transition: all 0.3s;
}

.timeline-item:last-child .timeline-line {
  display: none;
}

.timeline-item.current-lesson {
  animation: highlight 2s ease-in-out infinite;
}

@keyframes highlight {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex-shrink: 0;
}

.lesson-badge {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 800;
  color: white;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  border: 4px solid rgba(255, 255, 255, 0.3);
  z-index: 2;
}

.timeline-item.current-lesson .lesson-badge {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  box-shadow: 0 4px 30px rgba(245, 87, 108, 0.6);
  animation: pulse-badge 1.5s ease-in-out infinite;
}

@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.timeline-line {
  width: 4px;
  flex: 1;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.1) 100%);
  margin-top: 0.5rem;
  min-height: 80px;
  border-radius: 2px;
}

.timeline-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.lesson-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.time-start, .time-end {
  font-size: 1.3rem;
  font-weight: 700;
}

.time-separator {
  opacity: 0.6;
  margin: 0 0.3rem;
}

.lesson-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.lesson-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateX(10px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.timeline-item.current-lesson .lesson-card {
  background: rgba(245, 87, 108, 0.2);
  border-color: rgba(245, 87, 108, 0.5);
  box-shadow: 0 8px 30px rgba(245, 87, 108, 0.3);
}

.lesson-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.lesson-subject {
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
  margin: 0;
  line-height: 1.3;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.lesson-type {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.4rem 0.8rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: white;
  white-space: nowrap;
}

.lesson-details {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.lesson-detail {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: white;
}

.detail-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 2px 5px rgba(0,0,0,0.2));
}

.detail-text {
  font-size: 1.05rem;
  font-weight: 500;
}

.show-on-map-btn {
  margin-left: auto;
  padding: 0.5rem 1rem;
  background: rgba(52, 152, 219, 0.3);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(52, 152, 219, 0.5);
  border-radius: 10px;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.show-on-map-btn:hover {
  background: rgba(52, 152, 219, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
}

.schedule-grid {
  display: flex;
  flex-direction: column;
}

.schedule-row {
  display: grid;
  grid-template-columns: 140px 60px 1fr 250px 100px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: background-color 0.2s;
}

.schedule-row:hover:not(.header-row) {
  background-color: rgba(255, 255, 255, 0.1);
}

.schedule-row.current-lesson {
  background-color: rgba(52, 152, 219, 0.2);
  border-left: 4px solid #3498db;
}

.header-row {
  background: rgba(255, 255, 255, 0.2);
  font-weight: 600;
  color: white;
  position: sticky;
  top: 0;
  z-index: 10;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.cell {
  padding: 1rem;
  display: flex;
  align-items: center;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.cell:last-child {
  border-right: none;
}

.time-cell {
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
}

.time-range {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.time-start, .time-end {
  font-weight: 600;
  color: white;
  font-size: 0.95rem;
}

.time-separator {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

.lesson-cell {
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
}

.lesson-number {
  font-weight: 700;
  font-size: 1.2rem;
  color: white;
  background: rgba(255, 255, 255, 0.2);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.subject-cell {
  padding-left: 1.5rem;
}

.subject-name {
  font-weight: 500;
  color: white;
  line-height: 1.4;
}

.teacher-cell {
  color: rgba(255, 255, 255, 0.9);
}

.teacher-name {
  font-size: 0.95rem;
}

.room-cell {
  justify-content: center;
  font-weight: 600;
  color: #ff6b6b;
  background: rgba(255, 255, 255, 0.05);
}

.room-number {
  background: rgba(255, 107, 107, 0.2);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 107, 107, 0.3);
  color: #ff6b6b;
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

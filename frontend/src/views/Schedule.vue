<template>
  <div class="schedule">
    <button class="back-button" @click="$router.push('/')">
      🔙 На главную
    </button>

    <h1>Расписание занятий</h1>

    <div class="date-carousel">
      <button class="carousel-arrow" @click="previousDay" aria-label="Предыдущий день">‹</button>
      <div class="date-cards-container" ref="dateScrollEl" @wheel.prevent="onDateWheel">
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
      <button class="carousel-arrow" @click="nextDay" aria-label="Следующий день">›</button>
      <button class="carousel-picker" @click="openDatePicker" aria-label="Выбрать дату" title="Выбрать дату">📅</button>
      <input
        ref="datePickerEl"
        type="date"
        class="date-picker-input"
        :value="toDateParam(selectedDate)"
        @change="onDatePicked"
      />
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
          :list="searchType === 'group' ? 'groups-list' : 'teachers-list'"
          autocomplete="off"
        />
        <datalist id="groups-list">
          <option v-for="group in availableGroups" :key="group.name" :value="group.name"></option>
        </datalist>
        <datalist id="teachers-list">
          <option v-for="teacher in availableTeachers" :key="teacher.name" :value="teacher.name"></option>
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

      <div class="lesson-types-legend">
        <div class="legend-item">
          <div class="legend-badge badge-lecture"></div>
          <span>ЛК — Лекция</span>
        </div>
        <div class="legend-item">
          <div class="legend-badge badge-practice"></div>
          <span>ПР — Практика</span>
        </div>
        <div class="legend-item">
          <div class="legend-badge badge-lab"></div>
          <span>ЛР — Лабораторная</span>
        </div>
      </div>

      <div class="timeline-container">
        <div
          v-for="item in scheduleData"
          :key="item.id"
          class="timeline-item"
          :class="{
            'current-lesson': isCurrentLesson(item),
            'lesson-lecture': getLessonTypeClass(item.lesson_type) === 'lecture',
            'lesson-practice': getLessonTypeClass(item.lesson_type) === 'practice',
            'lesson-lab': getLessonTypeClass(item.lesson_type) === 'lab'
          }"
        >
          <div class="timeline-marker">
            <div class="lesson-badge" :class="'badge-' + getLessonTypeClass(item.lesson_type)">
              {{ formatLessonNumber(item.lesson_number) }}
            </div>
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
                <span class="lesson-type" :class="'type-' + getLessonTypeClass(item.lesson_type)">
                  {{ formatLessonType(item.lesson_type) }}
                </span>
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
    const availableTeachers = ref([])
    const loading = ref(false)
    const searched = ref(false)
    const selectedDate = ref(new Date())
    const dateRange = ref([])
    const datePickerEl = ref(null)
    const dateScrollEl = ref(null)

    const generateDateRange = () => {
      const dates = []
      const anchor = new Date(selectedDate.value)
      for (let i = -3; i <= 7; i++) {
        const date = new Date(anchor)
        date.setDate(anchor.getDate() + i)
        dates.push(date)
      }
      dateRange.value = dates
    }

    const openDatePicker = () => {
      const el = datePickerEl.value
      if (!el) return
      if (typeof el.showPicker === 'function') {
        try { el.showPicker(); return } catch (_) { /* fallback */ }
      }
      el.click()
      el.focus()
    }

    const onDatePicked = (event) => {
      const value = event.target.value
      if (!value) return
      const [yyyy, mm, dd] = value.split('-').map(Number)
      const picked = new Date(yyyy, mm - 1, dd)
      selectedDate.value = picked
      generateDateRange()
      if (searchQuery.value.trim()) search()
    }

    const onDateWheel = (event) => {
      const el = dateScrollEl.value
      if (!el) return
      el.scrollLeft += event.deltaY !== 0 ? event.deltaY : event.deltaX
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
      if (searchQuery.value.trim()) search()
    }

    const nextDay = () => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() + 1)
      selectedDate.value = newDate
      generateDateRange()
      if (searchQuery.value.trim()) search()
    }

    const loadTeachers = async () => {
      try {
        const response = await api.get('/schedule/teachers')
        availableTeachers.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки преподавателей:', error)
      }
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

    const toDateParam = (d) => {
      const yyyy = d.getFullYear()
      const mm = String(d.getMonth() + 1).padStart(2, '0')
      const dd = String(d.getDate()).padStart(2, '0')
      return `${yyyy}-${mm}-${dd}`
    }

    const search = async () => {
      if (!searchQuery.value.trim()) return

      loading.value = true
      searched.value = true

      try {
        const endpoint = searchType.value === 'group'
          ? `/schedule/group/${searchQuery.value}`
          : `/schedule/teacher/${searchQuery.value}`

        const response = await api.get(endpoint, {
          params: { date: toDateParam(selectedDate.value) }
        })
        scheduleData.value = response.data.sort((a, b) => a.lesson_number - b.lesson_number)
      } catch (error) {
        if (error.response && error.response.status === 404) {
          scheduleData.value = []
        } else {
          console.error('Ошибка поиска:', error)
          scheduleData.value = []
        }
      } finally {
        loading.value = false
      }
    }

    const formatLessonNumber = (n) => {
      if (n === 0 || n === '0') return 'КЧ'
      return String(n)
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

    const getLessonTypeClass = (lessonType) => {
      if (!lessonType) return 'lecture'
      const type = lessonType.toLowerCase()
      if (type.includes('лаб') || type.includes('lab')) return 'lab'
      if (type.includes('практ') || type.includes('practice')) return 'practice'
      return 'lecture'
    }

    const formatLessonType = (lessonType) => {
      if (!lessonType) return 'ЛК'
      const type = lessonType.toLowerCase()
      if (type.includes('лаб') || type.includes('lab')) return 'ЛР'
      if (type.includes('практ') || type.includes('practice')) return 'ПР'
      return 'ЛК'
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
      loadTeachers()
      generateDateRange()
    })

    return {
      searchType,
      searchQuery,
      scheduleData,
      availableGroups,
      availableTeachers,
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
      formatLessonNumber,
      toDateParam,
      datePickerEl,
      dateScrollEl,
      openDatePicker,
      onDatePicked,
      onDateWheel,
      showRoomOnMap,
      getLessonTypeClass,
      formatLessonType
    }
  }
}
</script>


<style scoped>
.schedule {
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

/* ── Заголовок ── */
h1 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 3.2vw, 2.4rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  margin-bottom: 1.5rem;
  color: var(--text);
}

/* ── Карусель дат ── */
.date-carousel {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 1rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
}

.carousel-arrow {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 1.5rem;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.carousel-arrow:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: scale(1.08);
}

.carousel-picker {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 1.2rem;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
}

.carousel-picker:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: scale(1.08);
}

.date-picker-input {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
  pointer-events: none;
}

.date-cards-container {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -ms-overflow-style: none;
  scroll-snap-type: x mandatory;
}

.date-cards-container::-webkit-scrollbar {
  display: none;
}

.date-cards {
  display: flex;
  gap: 0.6rem;
  scroll-snap-align: start;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0.25rem 0;
  scrollbar-width: none;
}

.date-cards::-webkit-scrollbar {
  display: none;
}

.date-card {
  min-width: 110px;
  padding: 0.9rem 0.75rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  color: var(--text);
  flex-shrink: 0;
}

.date-card:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateY(-2px);
}

.date-card.active {
  background: var(--accent-gradient);
  border-color: transparent;
  color: #0b0d1c;
  box-shadow: var(--accent-glow);
}

.date-day {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.date-card.active .date-day {
  color: rgba(11, 13, 28, 0.72);
}

.date-number {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.02em;
}

.date-month {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.date-card.active .date-month {
  color: rgba(11, 13, 28, 0.68);
}

/* ── Панель поиска ── */
.search-panel {
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  margin-bottom: 2rem;
}

.search-tabs {
  display: flex;
  gap: 0.5rem;
  padding: 0.25rem;
  margin-bottom: 1.25rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.search-tabs button {
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  color: var(--text-muted);
  border-radius: calc(var(--radius) - 4px);
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: background var(--transition), color var(--transition);
}

.search-tabs button.active {
  background: var(--accent-gradient);
  color: #0b0d1c;
  box-shadow: var(--shadow-sm);
}

.search-tabs button:hover:not(.active) {
  color: var(--text);
  background: var(--surface-hover);
}

.search-input {
  display: flex;
  gap: 0.75rem;
}

.search-input input {
  flex: 1;
  padding: 0.9rem 1.1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  font-size: 1rem;
  transition: border-color var(--transition), background var(--transition);
}

.search-input input::placeholder {
  color: var(--text-dim);
}

.search-input input:focus {
  outline: none;
  border-color: var(--accent-border);
  background: var(--surface-hover);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

.search-input button {
  padding: 0.9rem 1.75rem;
  background: var(--accent-gradient);
  color: #0b0d1c;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 1rem;
  font-weight: 700;
  transition: transform var(--transition), box-shadow var(--transition);
  box-shadow: var(--shadow-sm);
}

.search-input button:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow), var(--accent-glow);
}

/* ── Список групп / состояния ── */
.loading,
.no-results {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
  font-size: 1.1rem;
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
}

.groups-list {
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border);
  padding: 1.75rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  margin-bottom: 2rem;
}

.groups-list h2 {
  margin: 0 0 1.25rem 0;
  color: var(--text);
  font-size: 1.15rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.groups-list h2::before {
  content: '';
  width: 3px;
  height: 18px;
  background: var(--accent-gradient);
  border-radius: var(--radius-pill);
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 0.75rem;
}

.group-card {
  padding: 0.85rem 0.5rem;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: background var(--transition), border-color var(--transition), transform var(--transition), color var(--transition);
  font-family: var(--font-display);
}

.group-card:hover {
  background: var(--accent-soft);
  border-color: var(--accent-border);
  transform: translateY(-2px);
  color: var(--text);
}

/* ── Результаты расписания ── */
.schedule-results {
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.schedule-header {
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, rgba(139, 123, 255, 0.15), rgba(34, 211, 238, 0.10));
  border-bottom: 1px solid var(--border);
  color: var(--text);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.schedule-header h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.schedule-date {
  font-size: 0.95rem;
  color: var(--text-muted);
  text-transform: capitalize;
  font-weight: 500;
}

/* ── Легенда ── */
.lesson-types-legend {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  padding: 1rem 1.5rem;
  background: var(--surface);
  border-radius: var(--radius);
  margin: 1.25rem 1.5rem 0;
  border: 1px solid var(--border);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 600;
}

.legend-badge {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  box-shadow: 0 0 0 1px var(--border);
}

.legend-badge.badge-lecture {
  background: linear-gradient(135deg, #8b7bff 0%, #6366f1 100%);
}

.legend-badge.badge-practice {
  background: linear-gradient(135deg, #f472b6 0%, #fb7185 100%);
}

.legend-badge.badge-lab {
  background: linear-gradient(135deg, #22d3ee 0%, #38bdf8 100%);
}

/* ── Timeline ── */
.timeline-container {
  padding: 1.5rem;
  position: relative;
}

.timeline-item {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  position: relative;
}

.timeline-item:last-child .timeline-line {
  display: none;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.lesson-badge {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, #8b7bff 0%, #6366f1 100%);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 800;
  color: #fff;
  box-shadow: 0 6px 20px -4px rgba(139, 123, 255, 0.5);
  z-index: 2;
  transition: transform var(--transition);
}

.lesson-badge.badge-lecture {
  background: linear-gradient(135deg, #8b7bff 0%, #6366f1 100%);
  box-shadow: 0 6px 20px -4px rgba(139, 123, 255, 0.5);
}

.lesson-badge.badge-practice {
  background: linear-gradient(135deg, #f472b6 0%, #fb7185 100%);
  box-shadow: 0 6px 20px -4px rgba(244, 114, 182, 0.5);
}

.lesson-badge.badge-lab {
  background: linear-gradient(135deg, #22d3ee 0%, #38bdf8 100%);
  box-shadow: 0 6px 20px -4px rgba(34, 211, 238, 0.5);
}

.timeline-item.lesson-lecture .timeline-line {
  background: linear-gradient(180deg, rgba(139, 123, 255, 0.4), transparent);
}

.timeline-item.lesson-practice .timeline-line {
  background: linear-gradient(180deg, rgba(244, 114, 182, 0.4), transparent);
}

.timeline-item.lesson-lab .timeline-line {
  background: linear-gradient(180deg, rgba(34, 211, 238, 0.4), transparent);
}

.timeline-item.current-lesson .lesson-badge {
  animation: glow-badge 2.6s ease-in-out infinite;
}

@keyframes glow-badge {
  0%, 100% { box-shadow: 0 6px 20px -4px rgba(244, 114, 182, 0.45); }
  50%      { box-shadow: 0 6px 28px -2px rgba(244, 114, 182, 0.85); }
}

.timeline-line {
  width: 3px;
  flex: 1;
  background: linear-gradient(180deg, var(--border-hover), transparent);
  margin-top: 0.5rem;
  min-height: 72px;
  border-radius: var(--radius-pill);
}

.timeline-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.lesson-time {
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-muted);
  font-variant-numeric: tabular-nums;
}

.time-start,
.time-end {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
}

.time-separator {
  opacity: 0.5;
  margin: 0 0.2rem;
}

.lesson-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
}

.lesson-card:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateX(4px);
}

.timeline-item.current-lesson .lesson-card {
  background: rgba(244, 114, 182, 0.08);
  border-color: rgba(244, 114, 182, 0.35);
  box-shadow: 0 0 24px rgba(244, 114, 182, 0.15);
}

.lesson-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.9rem;
  gap: 0.75rem;
}

.lesson-subject {
  font-family: var(--font-display);
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.lesson-type {
  padding: 0.3rem 0.75rem;
  border-radius: var(--radius-pill);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
  border: 1px solid transparent;
}

.lesson-type.type-lecture {
  background: rgba(139, 123, 255, 0.15);
  border-color: rgba(139, 123, 255, 0.35);
  color: #b4a8ff;
}

.lesson-type.type-practice {
  background: rgba(244, 114, 182, 0.15);
  border-color: rgba(244, 114, 182, 0.35);
  color: #fbc0dc;
}

.lesson-type.type-lab {
  background: rgba(34, 211, 238, 0.15);
  border-color: rgba(34, 211, 238, 0.35);
  color: #7ee4f5;
}

.lesson-details {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.lesson-detail {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--text-muted);
}

.detail-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.detail-text {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text);
}

.show-on-map-btn {
  margin-left: auto;
  padding: 0.4rem 0.9rem;
  background: var(--info-soft);
  border: 1px solid rgba(34, 211, 238, 0.35);
  border-radius: var(--radius-pill);
  color: #7ee4f5;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition), transform var(--transition);
}

.show-on-map-btn:hover {
  background: rgba(34, 211, 238, 0.25);
  transform: translateY(-1px);
}

@media (max-width: 720px) {
  .timeline-container { padding: 1rem; }
  .timeline-item { gap: 1rem; }
  .lesson-badge { width: 44px; height: 44px; font-size: 1.1rem; }
  .search-input { flex-direction: column; }
  .lesson-header { flex-direction: column; }
}
</style>

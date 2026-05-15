<template>
  <div class="schedule">
    <button class="back-button" @click="$router.push('/')">
      <Icon name="arrowLeft" :size="20" />
      <span>На главную</span>
    </button>

    <h1>Расписание занятий</h1>

    <div class="date-carousel">
      <button class="carousel-arrow" @click="previousDay" aria-label="Предыдущий день">‹</button>
      <button
        v-if="!isToday"
        class="carousel-today"
        @click="goToToday"
        aria-label="Перейти к сегодняшней дате"
        title="Перейти к сегодняшней дате"
      >
        <span class="carousel-today-icon">↺</span>
        <span class="carousel-today-label">Сегодня</span>
      </button>
      <div
        class="date-cards-container"
        ref="dateScrollEl"
        @wheel.prevent="onDateWheel"
        @scroll.passive="onDateScroll"
      >
        <div class="date-cards">
          <button
            v-for="(day, index) in dateRange"
            :key="index"
            :class="['date-card', { active: isSelectedDate(day), 'has-schedule': hasScheduleOnDate(day) }]"
            @click="selectDate(day)"
          >
            <div class="date-day">{{ formatDayName(day) }}</div>
            <div class="date-number">{{ formatDayNumber(day) }}</div>
            <div class="date-month">{{ formatMonthName(day) }}</div>
          </button>
        </div>
      </div>
      <button class="carousel-arrow" @click="nextDay" aria-label="Следующий день">›</button>
      <button class="carousel-picker" @click="openDatePicker" aria-label="Выбрать дату" title="Выбрать дату"><Icon name="calendar" :size="20" /></button>
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
          @click="selectSearchType('group')"
        >
          По группе
        </button>
        <button
          :class="{ active: searchType === 'teacher' }"
          @click="selectSearchType('teacher')"
        >
          По преподавателю
        </button>
        <button
          :class="{ active: searchType === 'room' }"
          @click="selectSearchType('room')"
        >
          По кабинету
        </button>
      </div>

      <div class="search-input">
        <input
          v-model="searchQuery"
          :placeholder="searchPlaceholder"
          @keyup.enter="search"
          :list="datalistId"
          autocomplete="off"
        />
        <datalist id="groups-list">
          <option v-for="group in availableGroups" :key="group.name" :value="group.name"></option>
        </datalist>
        <datalist id="teachers-list">
          <option v-for="teacher in availableTeachers" :key="teacher.name" :value="teacher.name"></option>
        </datalist>
        <datalist id="rooms-list">
          <option v-for="room in availableRooms" :key="room.number" :value="room.number"></option>
        </datalist>
        <button @click="search">Найти</button>
      </div>
    </div>

    <div v-if="!searched && quickPickItems.length > 0" class="groups-list">
      <h2>{{ quickPickHeader }}</h2>
      <div class="groups-grid" :class="'groups-grid--' + searchType">
        <button
          v-for="item in quickPickItems"
          :key="item.value"
          class="group-card"
          :title="item.label"
          @click="selectQuickPick(item.value)"
        >
          {{ item.label }}
        </button>
      </div>
      <div v-if="quickPickTotal > quickPickItems.length" class="quick-pick-hint">
        Показаны первые {{ quickPickItems.length }} из {{ quickPickTotal }}.
        Начните вводить в поиске, чтобы отфильтровать.
      </div>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div v-else-if="scheduleData.length > 0" class="schedule-results">
      <div class="schedule-header">
        <h2>{{ scheduleHeader }}</h2>
        <div class="schedule-header-right">
          <div class="schedule-date">{{ formatDate(selectedDate) }}</div>
          <button
            class="qr-share-btn"
            type="button"
            title="Забрать расписание в телефон"
            @click="openShareQR"
          >
            <Icon name="smartphone" :size="18" />
            <span>Сканировать QR</span>
          </button>
        </div>
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
            'lesson-lab': getLessonTypeClass(item.lesson_type) === 'lab',
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
                  <button
                    v-if="item.teacher_name"
                    class="detail-link"
                    :title="`Открыть расписание преподавателя`"
                    @click="openTeacherSchedule(item.teacher_name)"
                  >{{ item.teacher_name }}</button>
                  <span v-else class="detail-text">Не указан</span>
                </div>
                <div class="lesson-detail">
                  <span class="detail-icon"><Icon name="mapPin" :size="18" /></span>
                  <span
                    v-if="isDistanceLesson(item.room_number)"
                    class="distance-badge"
                    title="Дистанционная пара"
                  >Дистанционно</span>
                  <template v-else>
                    <button
                      v-if="item.room_number"
                      class="detail-link"
                      :title="`Открыть расписание кабинета`"
                      @click="openRoomSchedule(item.room_number)"
                    >Кабинет {{ item.room_number }}</button>
                    <button
                      v-if="item.room_number"
                      class="detail-map-btn"
                      :title="`Показать кабинет ${item.room_number} на карте`"
                      aria-label="Показать на карте"
                      @click="openRoomOnMap(item.room_number)"
                    ><Icon name="target" :size="16" /></button>
                    <span v-else class="detail-text">Кабинет —</span>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="shareQR.open"
      class="share-qr-modal"
      @click.self="closeShareQR"
    >
      <div class="share-qr-card">
        <h3>Расписание — {{ shareQR.subtitle }}</h3>
        <p class="share-qr-hint">Наведите камеру телефона на код, чтобы забрать расписание.</p>
        <img v-if="shareQR.dataUrl" :src="shareQR.dataUrl" alt="QR с расписанием" class="share-qr-image" />
        <p v-else class="share-qr-hint">Генерируем…</p>
        <button class="share-qr-close" type="button" @click="closeShareQR">Закрыть</button>
      </div>
    </div>

    <div v-if="!loading && scheduleData.length === 0 && searched" class="no-results">
      <div v-if="searchType === 'teacher'">
        Преподаватель «{{ searchQuery }}» не найден на эту дату.
        <div class="no-results-hint">Попробуйте выбрать из подсказок — формат «Фамилия И.О.»</div>
      </div>
      <div v-else-if="searchType === 'room'">
        В кабинете «{{ searchQuery }}» ничего не запланировано на эту дату.
      </div>
      <div v-else>
        Группа «{{ searchQuery }}» не найдена на эту дату.
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import { generateQRCode } from '../utils/qrGenerator'
import Icon from '../components/Icon.vue'

export default {
  name: 'Schedule',
  components: { Icon },
  setup() {
    const searchType = ref('group')
    const searchQuery = ref('')
    const scheduleData = ref([])
    const availableGroups = ref([])
    const availableTeachers = ref([])
    const availableRooms = ref([])
    const loading = ref(false)
    const shareQR = ref({ open: false, dataUrl: '', subtitle: '' })
    let searchAbortController = null
    let searchDebounceTimer = null

    const searchPlaceholder = computed(() => {
      if (searchType.value === 'group') return 'Введите номер группы'
      if (searchType.value === 'teacher') return 'Введите ФИО преподавателя'
      return 'Введите номер кабинета'
    })
    const datalistId = computed(() => {
      if (searchType.value === 'group') return 'groups-list'
      if (searchType.value === 'teacher') return 'teachers-list'
      return 'rooms-list'
    })
    const scheduleHeader = computed(() => {
      if (searchType.value === 'group') return `Группа: ${searchQuery.value}`
      if (searchType.value === 'teacher') return `Преподаватель: ${searchQuery.value}`
      return `Кабинет ${searchQuery.value}`
    })

    const QUICK_PICK_LIMIT = 60

    const quickPickHeader = computed(() => {
      if (searchType.value === 'group') return 'Доступные группы'
      if (searchType.value === 'teacher') return 'Преподаватели'
      return 'Кабинеты'
    })

    const _allQuickPickItems = computed(() => {
      if (searchType.value === 'group') {
        return availableGroups.value.map((g) => ({
          value: g.name,
          label: g.name,
        }))
      }
      if (searchType.value === 'teacher') {
        return availableTeachers.value.map((t) => ({
          value: t.name,
          label: t.name,
        }))
      }
      return availableRooms.value.map((r) => ({
        value: String(r.number),
        label: String(r.number),
      }))
    })

    const _filteredQuickPickItems = computed(() => {
      const q = searchQuery.value.trim().toLowerCase()
      if (!q) return _allQuickPickItems.value
      return _allQuickPickItems.value.filter((item) =>
        item.label.toLowerCase().includes(q)
      )
    })

    const quickPickItems = computed(() =>
      _filteredQuickPickItems.value.slice(0, QUICK_PICK_LIMIT)
    )
    const quickPickTotal = computed(() => _filteredQuickPickItems.value.length)
    const searched = ref(false)
    const selectedDate = ref(new Date())
    const dateRange = ref([])
    const datePickerEl = ref(null)
    const dateScrollEl = ref(null)
    const datesWithSchedule = ref(new Set())

    // Сколько дней в обе стороны держим в карусели по умолчанию.
    // На сенсорном киоске пользователь свайпает довольно агрессивно,
    // поэтому даём приличный запас. Если упрётся в край — onDateScroll
    // дотянет ещё.
    const DATE_RANGE_BACKWARD = 7
    const DATE_RANGE_FORWARD = 14

    const generateDateRange = () => {
      const dates = []
      const anchor = new Date(selectedDate.value)
      for (let i = -DATE_RANGE_BACKWARD; i <= DATE_RANGE_FORWARD; i++) {
        const date = new Date(anchor)
        date.setDate(anchor.getDate() + i)
        dates.push(date)
      }
      dateRange.value = dates
    }

    // Расширяем диапазон вперёд/назад, не пересоздавая массив, чтобы
    // прокрутка не дёргалась и не теряла позицию (просто дописываем
    // новые `Date` к концу/началу).
    const extendDateRange = (direction) => {
      if (!dateRange.value.length) return
      const ADD = 7
      if (direction === 'forward') {
        const last = dateRange.value[dateRange.value.length - 1]
        const tail = []
        for (let i = 1; i <= ADD; i++) {
          const d = new Date(last)
          d.setDate(last.getDate() + i)
          tail.push(d)
        }
        dateRange.value = [...dateRange.value, ...tail]
      } else if (direction === 'backward') {
        const first = dateRange.value[0]
        const head = []
        for (let i = ADD; i >= 1; i--) {
          const d = new Date(first)
          d.setDate(first.getDate() - i)
          head.push(d)
        }
        // Сохраняем визуальную позицию: после prepend'а scrollLeft
        // нужно сместить на ширину добавленных карточек, иначе пользователь
        // «улетит» в начало.
        const el = dateScrollEl.value
        const before = el ? el.scrollWidth : 0
        dateRange.value = [...head, ...dateRange.value]
        if (el) {
          requestAnimationFrame(() => {
            const delta = el.scrollWidth - before
            el.scrollLeft += delta
          })
        }
      }
    }

    const onDateScroll = (event) => {
      const el = event.currentTarget
      if (!el) return
      const EDGE = 120
      const atStart = el.scrollLeft <= EDGE
      const atEnd = el.scrollLeft + el.clientWidth >= el.scrollWidth - EDGE
      if (atEnd) extendDateRange('forward')
      if (atStart) extendDateRange('backward')
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
      debouncedSearch()
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

    const hasScheduleOnDate = (date) => {
      return datesWithSchedule.value.has(toDateParam(date))
    }

    const loadAvailableDates = async () => {
      if (!searchQuery.value.trim()) {
        datesWithSchedule.value = new Set()
        return
      }
      try {
        const params = {}
        if (searchType.value === 'group') params.group = searchQuery.value
        else if (searchType.value === 'teacher') params.teacher = searchQuery.value
        else params.room = searchQuery.value
        const response = await api.get('/schedule/dates', { params })
        datesWithSchedule.value = new Set(response.data)
      } catch {
        datesWithSchedule.value = new Set()
      }
    }

    // Дебаунс для быстрых кликов по карусели дат — объединяем всплеск
    // GET'ов в один фактический запрос.
    const debouncedSearch = () => {
      if (!searchQuery.value.trim()) return
      if (searchDebounceTimer) {
        clearTimeout(searchDebounceTimer)
      }
      searchDebounceTimer = setTimeout(() => {
        searchDebounceTimer = null
        search()
      }, 180)
    }

    const selectDate = (date) => {
      selectedDate.value = date
      debouncedSearch()
    }

    const previousDay = () => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() - 1)
      selectedDate.value = newDate
      generateDateRange()
      debouncedSearch()
    }

    const nextDay = () => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() + 1)
      selectedDate.value = newDate
      generateDateRange()
      debouncedSearch()
    }

    const isToday = computed(() => {
      const t = new Date()
      return selectedDate.value.toDateString() === t.toDateString()
    })

    const goToToday = () => {
      selectedDate.value = new Date()
      generateDateRange()
      debouncedSearch()
    }

    const loadTeachers = async () => {
      try {
        const response = await api.get('/schedule/teachers')
        availableTeachers.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки преподавателей:', error)
      }
    }

    const loadRooms = async () => {
      try {
        const response = await api.get('/schedule/rooms')
        availableRooms.value = response.data
      } catch (error) {
        console.error('Ошибка загрузки кабинетов:', error)
      }
    }

    const openTeacherSchedule = (teacherName) => {
      if (!teacherName) return
      searchType.value = 'teacher'
      searchQuery.value = teacherName
      search()
    }

    const router = useRouter()

    const openRoomOnMap = (roomNumber) => {
      if (!roomNumber) return
      const value = String(roomNumber).trim()
      if (!value) return
      router.push({ path: '/map', query: { room: value } })
    }

    const openRoomSchedule = (roomNumber) => {
      if (!roomNumber) return
      searchType.value = 'room'
      searchQuery.value = String(roomNumber)
      search()
    }

    const buildShareText = () => {
      const dateStr = formatDate(selectedDate.value)
      const lines = [
        `ККРИТ · ${scheduleHeader.value}`,
        dateStr,
        '',
      ]
      const rows = scheduleData.value.slice().sort(
        (a, b) => a.lesson_number - b.lesson_number
      )
      for (const it of rows) {
        const lesson = formatLessonNumber(it.lesson_number)
        const time = `${formatTime(it.time_start)}–${formatTime(it.time_end)}`
        const subj = it.subject || ''
        const teacher = it.teacher_name ? ` · ${it.teacher_name}` : ''
        const room = it.room_number
          ? (String(it.room_number).trim().toUpperCase() === 'ДО'
              ? ' · дистанционно'
              : ` · ауд.${it.room_number}`)
          : ''
        const tag = ''
        lines.push(`${lesson}. ${time} · ${subj}${teacher}${room}${tag}`)
      }
      // QR надёжно читается до ~700 байт. Трим на 800 символов.
      let text = lines.join('\n')
      if (text.length > 800) text = text.slice(0, 797) + '…'
      return text
    }

    const openShareQR = async () => {
      if (scheduleData.value.length === 0) return
      shareQR.value = {
        open: true,
        dataUrl: '',
        subtitle: scheduleHeader.value,
      }
      const text = buildShareText()
      const dataUrl = await generateQRCode(text)
      shareQR.value = {
        ...shareQR.value,
        dataUrl: dataUrl || '',
      }
    }

    const closeShareQR = () => {
      shareQR.value = { open: false, dataUrl: '', subtitle: '' }
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

    const selectQuickPick = (value) => {
      searchQuery.value = value
      search()
    }

    const selectSearchType = (type) => {
      if (searchType.value === type) return
      searchType.value = type
      searchQuery.value = ''
      scheduleData.value = []
      searched.value = false
      datesWithSchedule.value = new Set()
    }

    const toDateParam = (d) => {
      const yyyy = d.getFullYear()
      const mm = String(d.getMonth() + 1).padStart(2, '0')
      const dd = String(d.getDate()).padStart(2, '0')
      return `${yyyy}-${mm}-${dd}`
    }

    // Счётчик «текущего» запроса. Только последний инициированный
    // search() имеет право снять loading. Это спасает от мигания
    // спиннера, когда отменённый запрос завершает finally уже после
    // того, как стартовал новый (см. Schedule.vue search()).
    let searchRequestId = 0

    const search = async () => {
      if (!searchQuery.value.trim()) return

      const myRequestId = ++searchRequestId
      loading.value = true
      searched.value = true

      try {
        let endpoint
        if (searchType.value === 'group') {
          endpoint = `/schedule/group/${searchQuery.value}`
        } else if (searchType.value === 'teacher') {
          endpoint = `/schedule/teacher/${searchQuery.value}`
        } else {
          endpoint = `/schedule/room/${searchQuery.value}`
        }

        // Отменяем предыдущий в полёте запрос — иначе
        // при быстром переключении даты улетает пачка
        // одинаковых GET'ов.
        if (searchAbortController) {
          searchAbortController.abort()
        }
        searchAbortController = new AbortController()
        const response = await api.get(endpoint, {
          params: { date: toDateParam(selectedDate.value) },
          signal: searchAbortController.signal,
        })
        scheduleData.value = response.data.sort((a, b) => a.lesson_number - b.lesson_number)
        loadAvailableDates()
      } catch (error) {
        // Запрос отменён более новым search() — тихо выходим, и пусть
        // новый запрос сам управляет loading.
        if (
          error?.code === 'ERR_CANCELED' ||
          error?.name === 'CanceledError' ||
          error?.name === 'AbortError'
        ) {
          return
        }
        // 404 — ожидаемый случай «ничего не найдено»,
        // показываем пользователю пустое состояние без шума в консоли.
        scheduleData.value = []
        if (!(error.response && error.response.status === 404)) {
          console.error('Ошибка поиска:', error)
        }
      } finally {
        // Снимаем loading только если с момента старта НИКТО более
        // новый не успел запуститься.
        if (myRequestId === searchRequestId) {
          loading.value = false
        }
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

    // «ДО» — маркер дистанционной пары в room_number. Показываем не как
    // номер кабинета, а как бейдж «Дистанционно»; на карте этажей не
    // отображаем. Слот «112/ДО» (часть очно, часть дистанционно)
    // обрабатывается парсером — оставляется только реальный кабинет.
    const isDistanceLesson = (room) => {
      if (!room) return false
      return String(room).trim().toUpperCase() === 'ДО'
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
      loadRooms()
      generateDateRange()
    })

    onUnmounted(() => {
      if (searchAbortController) searchAbortController.abort()
      if (searchDebounceTimer) clearTimeout(searchDebounceTimer)
    })

    return {
      searchType,
      selectSearchType,
      searchQuery,
      scheduleData,
      availableGroups,
      availableTeachers,
      availableRooms,
      quickPickItems,
      quickPickTotal,
      quickPickHeader,
      selectQuickPick,
      openTeacherSchedule,
      openRoomSchedule,
      openRoomOnMap,
      shareQR,
      openShareQR,
      closeShareQR,
      searchPlaceholder,
      datalistId,
      scheduleHeader,
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
      hasScheduleOnDate,
      selectDate,
      previousDay,
      nextDay,
      isToday,
      goToToday,
      formatLessonNumber,
      toDateParam,
      datePickerEl,
      dateScrollEl,
      openDatePicker,
      onDatePicked,
      onDateWheel,
      onDateScroll,
      getLessonTypeClass,
      formatLessonType,
      isDistanceLesson
    }
  }
}
</script>


<style scoped>
.schedule {
  max-width: var(--content-max-width, 1400px);
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

.carousel-today {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--accent-soft);
  border: 1px solid var(--accent-border);
  color: var(--accent);
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0 0.95rem;
  height: 44px;
  border-radius: var(--radius-pill);
  cursor: pointer;
  flex-shrink: 0;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
}

.carousel-today:hover {
  background: var(--accent);
  color: #ffffff;
  border-color: var(--accent);
  transform: translateY(-1px);
}

.carousel-today-icon {
  font-size: 1.05rem;
  line-height: 1;
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
  color: #ffffff;
  box-shadow: var(--accent-glow);
}

.date-card.has-schedule {
  position: relative;
}

.date-card.has-schedule::after {
  content: '';
  position: absolute;
  bottom: 6px;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 6px rgba(74, 222, 128, 0.5);
}

.date-card.active.has-schedule::after {
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 4px rgba(255, 255, 255, 0.4);
}

.date-day {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.date-card.active .date-day {
  color: rgba(255, 255, 255, 0.85);
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
  color: rgba(255, 255, 255, 0.78);
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
  color: #ffffff;
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
  color: #ffffff;
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
.no-results-hint {
  margin-top: 0.6rem;
  font-size: 0.9rem;
  color: var(--text-dim);
}

.detail-link {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  color: inherit;
  text-align: left;
  cursor: pointer;
  text-decoration: none;
  border-bottom: 1px dashed transparent;
  transition: color var(--transition), border-color var(--transition);
}

.detail-link:hover {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.detail-link:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 2px;
}

.detail-map-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  margin-left: 0.4rem;
  padding: 0;
  border: 1px solid var(--border);
  border-radius: 50%;
  background: var(--surface);
  color: var(--text-muted);
  cursor: pointer;
  transition: color var(--transition), border-color var(--transition), background var(--transition), transform var(--transition);
  flex-shrink: 0;
}

.detail-map-btn:hover {
  color: var(--accent);
  border-color: var(--accent-border);
  background: var(--surface-hover);
  transform: scale(1.05);
}

.detail-map-btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

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

.groups-grid--teacher {
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}

.groups-grid--room {
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
}

.quick-pick-hint {
  margin-top: 0.75rem;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.85rem;
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
  background: linear-gradient(135deg, var(--accent-soft), rgba(14, 165, 183, 0.08));
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

.schedule-header-right {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.qr-share-btn {
  background: var(--accent-gradient);
  color: #ffffff;
  border: none;
  padding: 0.5rem 0.95rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.qr-share-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 18px rgba(37, 99, 235, 0.35);
}


/* ── Модалка QR с расписанием ── */
.share-qr-modal {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1.5rem;
}

.share-qr-card {
  background: linear-gradient(160deg, #ffffff 0%, #f7f9fd 100%);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 1.75rem 2rem 1.5rem;
  max-width: 380px;
  width: 100%;
  text-align: center;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18);
}

.share-qr-card h3 {
  margin: 0 0 0.4rem;
  font-family: var(--font-display);
  font-size: 1.15rem;
  color: var(--text);
}

.share-qr-hint {
  margin: 0 0 1.1rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.share-qr-image {
  width: 240px;
  height: 240px;
  border-radius: 14px;
  background: #fff;
  padding: 8px;
  margin: 0 auto 1.1rem;
  display: block;
}

.share-qr-close {
  width: 100%;
  padding: 0.7rem 1.5rem;
  background: var(--accent-gradient);
  color: #ffffff;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.95rem;
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
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
}

.legend-badge.badge-practice {
  background: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
}

.legend-badge.badge-lab {
  background: linear-gradient(135deg, #0EA5B7 0%, #14B8A6 100%);
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
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 800;
  color: #fff;
  box-shadow: 0 6px 20px -4px rgba(37, 99, 235, 0.45);
  z-index: 2;
  transition: transform var(--transition);
}

.lesson-badge.badge-lecture {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  box-shadow: 0 6px 20px -4px rgba(37, 99, 235, 0.45);
}

.lesson-badge.badge-practice {
  background: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
  box-shadow: 0 6px 20px -4px rgba(245, 158, 11, 0.45);
}

.lesson-badge.badge-lab {
  background: linear-gradient(135deg, #0EA5B7 0%, #14B8A6 100%);
  box-shadow: 0 6px 20px -4px rgba(14, 165, 183, 0.45);
}

.timeline-item.lesson-lecture .timeline-line {
  background: linear-gradient(180deg, rgba(37, 99, 235, 0.35), transparent);
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
  background: rgba(37, 99, 235, 0.14);
  border-color: rgba(37, 99, 235, 0.30);
  color: var(--text);
}

.lesson-type.type-practice {
  background: rgba(245, 158, 11, 0.14);
  border-color: rgba(245, 158, 11, 0.32);
  color: var(--text);
}

.lesson-type.type-lab {
  background: rgba(14, 165, 183, 0.14);
  border-color: rgba(14, 165, 183, 0.32);
  color: var(--text);
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

.distance-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.7rem;
  background: rgba(168, 85, 247, 0.18);
  border: 1px solid rgba(168, 85, 247, 0.45);
  border-radius: var(--radius-pill);
  color: #1a1a1a;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}


@media (max-width: 720px) {
  .timeline-container { padding: 1rem; }
  .timeline-item { gap: 1rem; }
  .lesson-badge { width: 44px; height: 44px; font-size: 1.1rem; }
  .search-input { flex-direction: column; }
  .lesson-header { flex-direction: column; }
}
</style>

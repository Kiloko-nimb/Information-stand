<template>
  <div class="map">
    <button class="back-button" @click="$router.push('/')">
      <Icon name="arrowLeft" :size="20" />
      <span>На главную</span>
    </button>

    <h1>Навигация по колледжу</h1>

    <DateCarousel v-model="selectedDate" class="map-date-carousel" />

    <transition name="free-bar">
      <div v-if="highlightedRoom" class="route-bar">
        <div class="route-bar-text">
          <Icon name="target" :size="18" />
          <span>
            Маршрут до <strong>кабинета {{ highlightedRoom }}</strong>
            <template v-if="!isRoomOnInteractiveFloor">
              — подсветка на этом этаже пока не поддерживается
            </template>
          </span>
        </div>
        <button class="route-bar-clear" type="button" @click="clearHighlightedRoom">Сбросить</button>
      </div>
    </transition>

    <div class="map-controls">
      <div class="floor-selector">
        <button
          v-for="floor in floors"
          :key="floor"
          :class="{ active: currentFloor === floor }"
          @click="currentFloor = floor"
        >
          {{ floor }} этаж
        </button>
      </div>
      <button
        class="free-rooms-toggle"
        :class="{ active: freeRoomsMode }"
        @click="toggleFreeRooms"
        :disabled="freeRoomsLoading || !isTodaySelected"
        :title="freeRoomsToggleTitle"
      >
        <span class="free-rooms-dot" :class="{ on: freeRoomsMode }"></span>
        <span>{{ freeRoomsMode ? 'Свободные сейчас: ВКЛ' : 'Свободные сейчас' }}</span>
      </button>
    </div>

    <transition name="free-bar">
      <div
        v-if="freeRoomsMode"
        class="free-rooms-bar"
      >
        <div class="free-rooms-bar-head">
          <span v-if="freeRoomsStatus === 'in_progress' && freeRoomsCurrentPair">
            Идёт <strong>{{ freeRoomsCurrentPair.label }}</strong>
            ({{ freeRoomsCurrentPair.start }}–{{ freeRoomsCurrentPair.end }})
          </span>
          <span v-else-if="freeRoomsStatus === 'break'">Сейчас перерыв — формально все кабинеты свободны</span>
          <span v-else-if="freeRoomsStatus === 'before_classes'">Пары ещё не начались</span>
          <span v-else-if="freeRoomsStatus === 'after_classes'">Пары на сегодня закончились</span>
          <span v-else-if="freeRoomsStatus === 'weekend'">Сегодня выходной</span>
          <span v-else>Загружаю…</span>
        </div>
        <div v-if="freeRoomsForCurrentFloor.length > 0" class="free-rooms-list">
          <span class="free-rooms-list-label">Свободно на {{ currentFloor }} этаже:</span>
          <span
            v-for="room in freeRoomsForCurrentFloor"
            :key="room.number"
            class="free-room-chip"
          >{{ room.number }}</span>
        </div>
        <div v-else-if="!freeRoomsLoading" class="free-rooms-empty">
          На {{ currentFloor }} этаже сейчас нет свободных кабинетов
        </div>
      </div>
    </transition>

    <div class="map-container">
      <!-- 1–4 этажи — общий контейнер с zoom/pan -->
      <template v-if="floors.includes(currentFloor)">
        <div class="svg-floor-map" @wheel.prevent="handleWheel" @mousedown="startPan">
          <div
            class="svg-map-wrapper"
            :class="{ 'is-panning': isPanning }"
            :style="{ transform: `translate3d(${panX}px, ${panY}px, 0) scale(${zoomLevel})` }"
          >
            <MapFloor1
              v-if="currentFloor === 1"
              :highlight-free-rooms="freeRoomsMode"
              :free-rooms="freeRoomNumbers"
              :busy-rooms="busyRoomNumbers"
              :highlighted-room="highlightedRoom"
              :room-types="roomTypesByFloor[1] || {}"
              @room-click="onRoomClick"
            />
            <MapFloor2
              v-else-if="currentFloor === 2"
              :highlight-free-rooms="freeRoomsMode"
              :free-rooms="freeRoomNumbers"
              :busy-rooms="busyRoomNumbers"
              :highlighted-room="highlightedRoom"
              :room-types="roomTypesByFloor[2] || {}"
              @room-click="onRoomClick"
            />
            <MapFloor3
              v-else-if="currentFloor === 3"
              :highlight-free-rooms="freeRoomsMode"
              :free-rooms="freeRoomNumbers"
              :busy-rooms="busyRoomNumbers"
              :highlighted-room="highlightedRoom"
              :room-types="roomTypesByFloor[3] || {}"
              @room-click="onRoomClick"
            />
            <MapFloor4
              v-else-if="currentFloor === 4"
              :highlight-free-rooms="freeRoomsMode"
              :free-rooms="freeRoomNumbers"
              :busy-rooms="busyRoomNumbers"
              :highlighted-room="highlightedRoom"
              :room-types="roomTypesByFloor[4] || {}"
              @room-click="onRoomClick"
            />
          </div>
          <div class="zoom-controls">
            <button @click="zoom(0.2)" title="Приблизить">+</button>
            <button @click="zoom(-0.2)" title="Отдалить">−</button>
            <button @click="resetView" title="Сбросить">⟳</button>
          </div>
          <RoomInfoPanel
            :room-number="openRoomNumber"
            :room-type="openRoomNumber ? (roomTypesByNumber[openRoomNumber] || null) : null"
            :selected-date="selectedDate"
            @close="closeRoomPanel"
          />
        </div>
        <details class="map-legend-wrap" open>
          <summary class="map-legend-summary">
            Легенда
            <span class="map-legend-hint-inline">
              <b>Л</b> — лестница, <b>Ж</b>/<b>М</b> — туалет
            </span>
          </summary>
          <div class="map-legend" aria-label="Легенда по типам кабинетов">
            <span class="legend-item"><span class="legend-swatch legend-swatch--auditorium"></span>Аудитория</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--lab"></span>Лаборатория</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--sport"></span>Спортзал</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--hall"></span>Актовый зал</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--admin"></span>Приёмная</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--library"></span>Библиотека</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--medical"></span>Медпункт</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--food"></span>Буфет</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--garderob"></span>Гардероб</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--wc"></span>Туалет</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--stairs"></span>Лестница</span>
            <span class="legend-item"><span class="legend-swatch legend-swatch--stand"></span>Стенд</span>
          </div>
        </details>
      </template>


    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MapFloor1 from '../components/MapFloor1.vue'
import MapFloor2 from '../components/MapFloor2.vue'
import MapFloor3 from '../components/MapFloor3.vue'
import MapFloor4 from '../components/MapFloor4.vue'
import Icon from '../components/Icon.vue'
import RoomInfoPanel from '../components/RoomInfoPanel.vue'
import DateCarousel from '../components/DateCarousel.vue'
import api from '../services/api'

// Этажи, для которых есть интерактивная Vue-карта (с подсветкой/кликом).
const INTERACTIVE_FLOORS = new Set([1, 2, 3, 4])

export default {
  name: 'Map',
  components: {
    MapFloor1,
    MapFloor2,
    MapFloor3,
    MapFloor4,
    RoomInfoPanel,
    DateCarousel,
    Icon
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const floors = [1, 2, 3, 4]
    // По умолчанию открываем 1-й этаж — именно там физически стоит инфо-стенд, и
    // желает посетитель в большинстве случаев сначала видеть своё текущее расположение.
    const currentFloor = ref(1)
    const highlightedRoom = ref(null)

    // Выбранная пользователем дата (для фильтра расписания в поповере).
    // По умолчанию — сегодня. Меняется через <DateCarousel />.
    const selectedDate = ref(new Date())
    const isTodaySelected = computed(
      () => selectedDate.value.toDateString() === new Date().toDateString(),
    )
    const freeRoomsToggleTitle = computed(() => {
      if (!isTodaySelected.value) {
        return 'Доступно только когда выбрана сегодняшняя дата'
      }
      return freeRoomsMode.value
        ? 'Скрыть подсветку'
        : 'Показать кабинеты, в которых сейчас нет занятий'
    })

    const isRoomOnInteractiveFloor = computed(
      () => !!highlightedRoom.value && INTERACTIVE_FLOORS.has(currentFloor.value),
    )

    // ─── Свободные кабинеты «прямо сейчас» ───
    const freeRoomsMode = ref(false)
    const freeRoomsLoading = ref(false)
    const freeRoomsStatus = ref(null)
    const freeRoomsCurrentPair = ref(null)
    const freeRoomsList = ref([])
    const busyRoomsList = ref([])

    const freeRoomNumbers = computed(() => freeRoomsList.value.map((r) => r.number))
    const busyRoomNumbers = computed(() => busyRoomsList.value.map((r) => r.number))

    const freeRoomsForCurrentFloor = computed(() => {
      if (typeof currentFloor.value !== 'number') return []
      return freeRoomsList.value.filter((r) => r.floor === currentFloor.value)
    })

    const FALLBACK_FLOOR_BY_PREFIX = (number) => {
      const m = String(number).match(/^(\d)/)
      if (!m) return null
      const d = Number(m[1])
      return [1, 2, 3, 4].includes(d) ? d : null
    }

    const loadFreeRooms = async () => {
      freeRoomsLoading.value = true
      try {
        const { data } = await api.get('/schedule/rooms/free')
        freeRoomsStatus.value = data.status
        freeRoomsCurrentPair.value = data.current_pair || null
        // Если бэк не знает этажей — пытаемся определить по первой цифре номера.
        const fillFloor = (r) => ({
          number: String(r.number).trim(),
          floor: r.floor != null ? Number(r.floor) : FALLBACK_FLOOR_BY_PREFIX(r.number),
        })
        freeRoomsList.value = (data.free || []).map(fillFloor)
        busyRoomsList.value = (data.busy || []).map(fillFloor)
      } catch (e) {
        freeRoomsStatus.value = null
        freeRoomsList.value = []
        busyRoomsList.value = []
      } finally {
        freeRoomsLoading.value = false
      }
    }

    const toggleFreeRooms = async () => {
      // «Свободные сейчас» — это срез по текущей паре; для будущих/прошлых
      // дат бэк не отдаёт корректный ответ, поэтому тоггл доступен только
      // когда выбрана сегодняшняя дата.
      if (!isTodaySelected.value) return
      freeRoomsMode.value = !freeRoomsMode.value
      if (freeRoomsMode.value && freeRoomsList.value.length === 0) {
        await loadFreeRooms()
      }
    }

    // При смене выбранной даты выключаем подсветку свободных кабинетов,
    // если дата перестала быть сегодняшней — данные устарели и стали
    // неприменимыми.
    watch(isTodaySelected, (isToday) => {
      if (!isToday) {
        freeRoomsMode.value = false
      }
    })

    let freeRoomsRefresh = null
    onMounted(() => {
      // Обновляем каждые 60 секунд, пока режим включён.
      freeRoomsRefresh = setInterval(() => {
        if (freeRoomsMode.value) loadFreeRooms()
      }, 60000)
    })
    onUnmounted(() => {
      if (freeRoomsRefresh) clearInterval(freeRoomsRefresh)
    })
    const zoomLevel = ref(1)
    const panX = ref(0)
    const panY = ref(0)
    const isPanning = ref(false)
    const startX = ref(0)
    const startY = ref(0)

    const MIN_ZOOM = 0.5
    const MAX_ZOOM = 3

    const zoom = (delta) => {
      const next = Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, zoomLevel.value + delta))
      zoomLevel.value = Math.round(next * 100) / 100
    }

    const handleWheel = (event) => {
      const delta = event.deltaY > 0 ? -0.15 : 0.15
      zoom(delta)
    }

    const resetView = () => {
      zoomLevel.value = 1
      panX.value = 0
      panY.value = 0
    }

    const startPan = (event) => {
      // Не перехватываем клики с кнопок зума и интерактивных элементов.
      // .room-info-panel — это выехавшая панель расписания по кабинету:
      // без этого исключения mousedown на ней срабатывал бы как панование карты,
      // и при любом движении мыши внутри панели карта бы уезжала в сторону.
      if (event.target && event.target.closest && event.target.closest('.zoom-controls, button, a, [data-room], .room-info-panel, .map-legend')) return
      isPanning.value = true
      startX.value = event.clientX - panX.value
      startY.value = event.clientY - panY.value
      document.body.style.cursor = 'grabbing'
    }

    const onMouseMove = (event) => {
      if (!isPanning.value) return
      panX.value = event.clientX - startX.value
      panY.value = event.clientY - startY.value
    }

    const onMouseUp = () => {
      if (!isPanning.value) return
      isPanning.value = false
      document.body.style.cursor = 'default'
    }

    // При смене этажа сбрасываем zoom и позицию
    watch(currentFloor, () => {
      resetView()
    })

    onMounted(() => {
      document.addEventListener('mousemove', onMouseMove)
      document.addEventListener('mouseup', onMouseUp)
    })

    onUnmounted(() => {
      document.removeEventListener('mousemove', onMouseMove)
      document.removeEventListener('mouseup', onMouseUp)
    })

    // Наведение на кабинет из ?room=XXX. Этаж определяем по первой цифре
    // номера (201 → 2 этаж, 305 → 3 этаж и т.д.). Если справочник на бэке
    // отдаёт другой этаж — доверяем бэку.
    const resolveRoomFloor = async (roomNumber) => {
      try {
        const { data } = await api.get(`/rooms/${encodeURIComponent(roomNumber)}`)
        if (data && typeof data.floor === 'number' && floors.includes(data.floor)) {
          return data.floor
        }
      } catch (e) {
        // Кабинета нет в справочнике — фолбэк по первой цифре.
      }
      return FALLBACK_FLOOR_BY_PREFIX(roomNumber)
    }

    const applyRoomFromQuery = async (raw) => {
      const value = typeof raw === 'string' ? raw.trim() : ''
      if (!value) {
        highlightedRoom.value = null
        return
      }
      highlightedRoom.value = value
      const floor = await resolveRoomFloor(value)
      if (floor && floor !== currentFloor.value) {
        currentFloor.value = floor
      }
    }

    const clearHighlightedRoom = () => {
      highlightedRoom.value = null
      const { room: _room, ...rest } = route.query
      router.replace({ path: route.path, query: rest })
    }

    // ── Справочник кабинетов по этажам: нужен для раскраски по типам и для
    //    заголовка панели с расписанием. Грузим параллельно для всех
    //    интерактивных этажей при монтировании. У нас ~20 комнат на этаж,
    //    отдельный список выгоднее, чем `/rooms/`.
    const roomTypesByFloor = ref({})
    // Плоский мап roomNumber → room_type для RoomInfoPanel-а (он не знает этажа).
    const roomTypesByNumber = computed(() => {
      const out = {}
      for (const floor of Object.keys(roomTypesByFloor.value)) {
        Object.assign(out, roomTypesByFloor.value[floor])
      }
      return out
    })
    const loadRoomTypes = async () => {
      const next = {}
      await Promise.all(
        Array.from(INTERACTIVE_FLOORS).map(async (floor) => {
          try {
            const { data } = await api.get(`/rooms/floor/${floor}`)
            const m = {}
            for (const r of data || []) {
              if (r && r.room_number) m[String(r.room_number).trim()] = r.room_type || null
            }
            next[floor] = m
          } catch (e) {
            next[floor] = {}
          }
        }),
      )
      roomTypesByFloor.value = next
    }

    // ── Открытая карточка расписания по кабинету (из клика по SVG-rect).
    //    Одновременно выставляем highlightedRoom, чтобы при открытой панели сам
    //    кабинет на карте пульсировал — визуальная связь «выбрано вот это».
    const openRoomNumber = ref(null)
    const onRoomClick = (roomNumber) => {
      const num = String(roomNumber || '').trim()
      if (!num) return
      openRoomNumber.value = num
      highlightedRoom.value = num
    }
    const closeRoomPanel = () => {
      openRoomNumber.value = null
    }

    onMounted(() => {
      loadRoomTypes()
      if (route.query.room) {
        applyRoomFromQuery(route.query.room)
      }
    })

    watch(
      () => route.query.room,
      (val) => {
        applyRoomFromQuery(val)
      },
    )

    return {
      floors,
      currentFloor,
      zoomLevel,
      zoom,
      handleWheel,
      panX,
      panY,
      isPanning,
      startPan,
      resetView,
      freeRoomsMode,
      freeRoomsLoading,
      freeRoomsStatus,
      freeRoomsCurrentPair,
      freeRoomsForCurrentFloor,
      freeRoomNumbers,
      busyRoomNumbers,
      toggleFreeRooms,
      freeRoomsToggleTitle,
      isTodaySelected,
      selectedDate,
      highlightedRoom,
      isRoomOnInteractiveFloor,
      clearHighlightedRoom,
      roomTypesByFloor,
      roomTypesByNumber,
      openRoomNumber,
      onRoomClick,
      closeRoomPanel,
    }
  }
}
</script>


<style scoped>
.map {
  max-width: 1500px;
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

.map-date-carousel {
  margin-bottom: 1.25rem;
}

/* ── Панель управления ── */
.map-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 0.75rem;
  border-radius: var(--radius-lg);
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
}

.floor-selector {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  flex: 1 1 auto;
  min-width: 0;
}

.floor-selector button {
  flex: 1;
  min-width: 110px;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-muted);
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: background var(--transition), border-color var(--transition), color var(--transition), transform var(--transition);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
}

.free-rooms-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.75rem 1.1rem;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-weight: 700;
  font-size: 0.92rem;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition), box-shadow var(--transition);
  white-space: nowrap;
}

.free-rooms-toggle:hover:not(:disabled) {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: translateY(-1px);
}

.free-rooms-toggle:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.free-rooms-toggle.active {
  background: linear-gradient(135deg, #16a34a, #22c55e);
  color: #ffffff;
  border-color: transparent;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.18);
}

.free-rooms-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--text-muted);
  box-shadow: 0 0 0 0 rgba(34, 197, 94, 0);
  transition: background var(--transition), box-shadow var(--transition);
}

.free-rooms-dot.on {
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.32);
  animation: free-dot-pulse 1.6s ease-in-out infinite;
}

@keyframes free-dot-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.45); }
  50%      { box-shadow: 0 0 0 6px rgba(255, 255, 255, 0); }
}

/* ── Полоса с информацией по свободным кабинетам ── */
.free-rooms-bar {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid #22c55e;
  border-radius: var(--radius-lg);
  padding: 0.85rem 1.1rem;
  margin: 0 0 1.25rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.free-rooms-bar-head {
  font-size: 0.92rem;
  color: var(--text-muted);
}

.free-rooms-bar-head strong {
  color: var(--text);
}

.free-rooms-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.4rem 0.5rem;
}

.free-rooms-list-label {
  font-weight: 700;
  color: var(--text);
  font-size: 0.95rem;
  margin-right: 0.4rem;
}

.free-room-chip {
  display: inline-flex;
  align-items: center;
  padding: 0.3rem 0.7rem;
  border-radius: var(--radius-pill);
  background: rgba(34, 197, 94, 0.14);
  color: #15803d;
  font-weight: 700;
  font-size: 0.88rem;
  border: 1px solid rgba(22, 163, 74, 0.35);
}

[data-theme="dark"] .free-room-chip {
  color: #4ade80;
  background: rgba(34, 197, 94, 0.22);
}

.free-rooms-empty {
  font-size: 0.92rem;
  color: var(--text-muted);
  font-style: italic;
}

/* ── Полоса «маршрут до кабинета XXX» ── */
.route-bar {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent, #2563eb);
  border-radius: var(--radius-lg);
  padding: 0.85rem 1.1rem;
  margin: 0 0 1.25rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.route-bar-text {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text);
  font-size: 0.95rem;
}

.route-bar-text strong {
  color: var(--accent, var(--text));
}

.route-bar-clear {
  padding: 0.45rem 0.9rem;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border-strong);
  background: var(--surface-strong);
  color: var(--text);
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition);
}

.route-bar-clear:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
}

.free-bar-enter-active,
.free-bar-leave-active {
  transition: opacity 200ms ease, transform 200ms ease;
}
.free-bar-enter-from,
.free-bar-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.floor-selector button:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  color: var(--text);
}

.floor-selector button.active {
  background: var(--accent-gradient);
  color: #ffffff;
  border-color: transparent;
  box-shadow: var(--shadow-sm), var(--accent-glow);
}

/* ── Контейнер карты ── */
.map-container {
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  min-height: 600px;
  box-shadow: var(--shadow);
}

.map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 480px;
  border: 1px dashed var(--border-hover);
  border-radius: var(--radius);
  color: var(--text-muted);
}

.map-placeholder p {
  font-size: 1.05rem;
  margin: 0.4rem 0;
  color: var(--text);
}

.hint {
  font-size: 0.85rem !important;
  color: var(--text-dim) !important;
}

/* ── SVG Floor Map ── */
.svg-floor-map {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius);
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface);
  user-select: none;
  cursor: grab;
  touch-action: none;
}

.svg-floor-map:active {
  cursor: grabbing;
}

.svg-map-wrapper {
  transform-origin: center center;
  transition: transform 180ms ease-out;
  will-change: transform;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: auto;
}

/* Во время перетаскивания отключаем анимацию — панорама без рывков */
.svg-map-wrapper.is-panning {
  transition: none;
}

.floor-svg-img {
  max-width: 100%;
  height: auto;
  display: block;
  border-radius: var(--radius-sm);
  filter: drop-shadow(0 12px 32px rgba(15, 23, 42, 0.18));
  user-select: none;
  background: #fff;
}

/* ── Контролы зума ── */
.zoom-controls {
  position: absolute;
  bottom: 1.25rem;
  right: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 10;
}

.zoom-controls button {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--surface-strong);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border-strong);
  color: var(--text);
  font-size: 1.25rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition), transform var(--transition), border-color var(--transition);
  box-shadow: var(--shadow-sm);
}

.zoom-controls button:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: scale(1.08);
}

/* ── Легенда: какой цвет = какой тип кабинета ── */
.legend-title {
  font-weight: 700;
  color: var(--text);
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.legend-swatch {
  width: 14px;
  height: 14px;
  border-radius: 4px;
  border: 1px solid rgba(15, 23, 42, 0.1);
  display: inline-block;
}

/* Цвета свотчей в легенде должны совпадать с .room--type-* в MapFloor*.vue. */
.legend-swatch--auditorium { background: rgba(59, 130, 246, 0.32);  border-color: rgba(29, 78, 216, 0.7); }
.legend-swatch--lab        { background: rgba(139, 92, 246, 0.36);  border-color: rgba(109, 40, 217, 0.75); }
.legend-swatch--sport      { background: rgba(34, 197, 94, 0.36);   border-color: rgba(21, 128, 61, 0.75); }
.legend-swatch--hall       { background: rgba(249, 115, 22, 0.36);  border-color: rgba(194, 65, 12, 0.75); }
.legend-swatch--admin      { background: rgba(245, 158, 11, 0.40);  border-color: rgba(180, 83, 9, 0.8); }
.legend-swatch--wc         { background: rgba(236, 72, 153, 0.32);  border-color: rgba(190, 24, 93, 0.7); }
.legend-swatch--stairs     { background: rgba(99, 102, 241, 0.36);  border-color: rgba(67, 56, 202, 0.75); background-image: repeating-linear-gradient(135deg, transparent 0, transparent 3px, rgba(67, 56, 202, 0.6) 3px, rgba(67, 56, 202, 0.6) 4px); }
.legend-swatch--library    { background: rgba(20, 184, 166, 0.34);  border-color: rgba(15, 118, 110, 0.75); }
.legend-swatch--medical    { background: rgba(239, 68, 68, 0.32);   border-color: rgba(185, 28, 28, 0.8); }
.legend-swatch--food       { background: rgba(234, 179, 8, 0.40);   border-color: rgba(161, 98, 7, 0.8); }
.legend-swatch--garderob   { background: rgba(100, 116, 139, 0.30); border-color: rgba(51, 65, 85, 0.7); }
.legend-swatch--stand      { background: rgba(37, 99, 235, 0.85);   border-color: #ffffff; box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.8); border-radius: 50%; }

/* Компактная легенда: сворачивающаяся панель вместо большого блока. */
.map-legend-wrap {
  margin: 1rem auto 0;
  max-width: 1100px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0.4rem 0.9rem;
  font-size: 0.85rem;
  color: var(--text);
}

.map-legend-summary {
  list-style: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.25rem 0;
  font-weight: 600;
  user-select: none;
}

.map-legend-summary::-webkit-details-marker {
  display: none;
}

.map-legend-summary::after {
  content: '▾';
  margin-left: 0.5rem;
  opacity: 0.55;
  transition: transform 0.2s ease;
}

.map-legend-wrap[open] .map-legend-summary::after {
  transform: rotate(180deg);
}

.map-legend-hint-inline {
  font-weight: 400;
  font-size: 0.78rem;
  opacity: 0.75;
  margin-left: 0.5rem;
  text-align: right;
}

.map-legend-wrap .map-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem 1rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border);
  margin-top: 0.4rem;
}

.map-legend-wrap .legend-item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
}

.map-legend-wrap .legend-swatch {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  border: 1px solid transparent;
  display: inline-block;
  flex-shrink: 0;
}

.map-legend-wrap .legend-swatch--stand {
  border-radius: 50%;
}

/* ── Заглушка для 1-го этажа ── */
.floor-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: var(--surface-strong);
  border: 1px dashed var(--border-strong);
  border-radius: var(--radius-lg);
  color: var(--text-muted);
  min-height: 320px;
  gap: 0.5rem;
}

.floor-placeholder h3 {
  font-size: 1.5rem;
  margin: 0;
  color: var(--text);
}

.floor-placeholder p {
  margin: 0;
  font-size: 1rem;
}

.floor-placeholder-hint {
  font-size: 0.9rem;
  opacity: 0.75;
}
</style>

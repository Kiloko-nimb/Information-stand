<template>
  <div class="map">
    <button class="back-button" @click="$router.push('/')">
      🔙 На главную
    </button>

    <h1>Навигация по колледжу</h1>

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
        <button
          :class="{ active: currentFloor === 'territory' }"
          @click="currentFloor = 'territory'"
          class="territory-btn"
        >
          🌳 Территория (Двор)
        </button>
      </div>
    </div>

    <div class="map-container">
      <!-- 1–4 этажи — общий контейнер с zoom/pan -->
      <template v-if="floors.includes(currentFloor)">
        <div class="svg-floor-map" @wheel.prevent="handleWheel" @mousedown="startPan">
          <div
            class="svg-map-wrapper"
            :class="{ 'is-panning': isPanning }"
            :style="{ transform: `translate3d(${panX}px, ${panY}px, 0) scale(${zoomLevel})` }"
          >
            <MapFloor2 v-if="currentFloor === 1" />
            <img v-else :src="`/floor${currentFloor}.svg`" :alt="`План ${currentFloor} этажа`" class="floor-svg-img" draggable="false" />
          </div>
          <div class="zoom-controls">
            <button @click="zoom(0.2)" title="Приблизить">+</button>
            <button @click="zoom(-0.2)" title="Отдалить">−</button>
            <button @click="resetView" title="Сбросить">⟳</button>
          </div>
        </div>
      </template>

      <!-- Территория -->
      <template v-else-if="currentFloor === 'territory'">
        <div class="territory-map">
          <h2>Территория колледжа</h2>
          <div class="territory-legend">
            <div class="legend-item">
              <span class="legend-icon">🚬</span>
              <span>Специально оборудованное место для курения</span>
            </div>
            <div class="legend-item">
              <span class="legend-icon">☕</span>
              <span>Точки питания рядом</span>
            </div>
            <div class="legend-item">
              <span class="legend-icon">🅿️</span>
              <span>Парковка</span>
            </div>
            <div class="legend-item">
              <span class="legend-icon">🚪</span>
              <span>Входы в здание</span>
            </div>
          </div>
          <div class="territory-content">
            <div class="territory-placeholder">
              <p>Интерактивная карта территории</p>
              <div class="territory-points">
                <div class="point smoking-area">
                  <span class="point-icon">🚬</span>
                  <span class="point-label">Место для курения</span>
                </div>
                <div class="point food-point">
                  <span class="point-icon">☕</span>
                  <span class="point-label">Кофейня "Бодрость" (50м)</span>
                </div>
                <div class="point food-point">
                  <span class="point-icon">🌯</span>
                  <span class="point-label">Шаурма "У Ашота" (100м)</span>
                </div>
                <div class="point parking">
                  <span class="point-icon">🅿️</span>
                  <span class="point-label">Парковка для посетителей</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import MapFloor2 from '../components/MapFloor2.vue'

export default {
  name: 'Map',
  components: {
    MapFloor2
  },
  setup() {
    const floors = [1, 2, 3, 4]
    const currentFloor = ref(1)
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
      // Не перехватываем клики с кнопок зума и интерактивных элементов
      if (event.target && event.target.closest && event.target.closest('.zoom-controls, button, a, [data-room]')) return
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
      resetView
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

/* ── Панель управления ── */
.map-controls {
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

.floor-selector button.territory-btn {
  background: rgba(5, 150, 105, 0.08);
  border-color: rgba(5, 150, 105, 0.30);
  color: #047857;
}

.floor-selector button.territory-btn:hover {
  background: rgba(5, 150, 105, 0.14);
  border-color: rgba(5, 150, 105, 0.45);
}

.floor-selector button.territory-btn.active {
  background: linear-gradient(135deg, #059669, #0ea5b7);
  color: #ffffff;
  border-color: transparent;
  box-shadow: 0 0 24px rgba(5, 150, 105, 0.30);
}

/* ── Территория ── */
.territory-map {
  width: 100%;
}

.territory-map h2 {
  font-family: var(--font-display);
  color: var(--text);
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin-bottom: 1.25rem;
}

.territory-legend {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 1.25rem;
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.legend-icon {
  font-size: 1.5rem;
}

.territory-content {
  min-height: 480px;
}

.territory-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 480px;
  border: 1px dashed var(--border-hover);
  border-radius: var(--radius-lg);
  color: var(--text-muted);
  padding: 2rem;
}

.territory-placeholder > p {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
  color: var(--text);
}

.territory-points {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  width: 100%;
  max-width: 900px;
}

.point {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  padding: 1.25rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  cursor: pointer;
}

.point:hover {
  transform: translateY(-3px);
  background: var(--surface-hover);
  border-color: var(--border-hover);
}

.point-icon {
  font-size: 2.25rem;
}

.point-label {
  font-size: 0.95rem;
  font-weight: 600;
  text-align: center;
  color: var(--text);
}

.smoking-area {
  border-color: rgba(244, 63, 94, 0.30);
}

.smoking-area:hover {
  border-color: rgba(244, 63, 94, 0.55);
  box-shadow: 0 6px 24px rgba(244, 63, 94, 0.15);
}

.food-point {
  border-color: rgba(251, 191, 36, 0.30);
}

.food-point:hover {
  border-color: rgba(251, 191, 36, 0.55);
  box-shadow: 0 6px 24px rgba(251, 191, 36, 0.15);
}

.parking {
  border-color: rgba(34, 211, 238, 0.30);
}

.parking:hover {
  border-color: rgba(34, 211, 238, 0.55);
  box-shadow: 0 6px 24px rgba(34, 211, 238, 0.15);
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
</style>

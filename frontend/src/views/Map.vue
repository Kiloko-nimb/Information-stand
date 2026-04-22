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
      <!-- 1 этаж - Интерактивный компонент -->
      <template v-if="currentFloor === 1">
        <MapFloor2 />
      </template>

      <!-- 2 этаж - SVG Карта -->
      <template v-else-if="currentFloor === 2">
        <div class="svg-floor-map" @wheel.prevent="handleWheel">
          <div
            class="svg-map-wrapper"
            :style="{ transform: `translate(${panX}px, ${panY}px) scale(${zoomLevel})` }"
            @mousedown="startPan"
          >
            <img src="/floor2.svg" alt="План 2 этажа" class="floor-svg-img" draggable="false" />
          </div>
          <div class="zoom-controls">
            <button @click="zoom(0.1)" title="Приблизить">+</button>
            <button @click="zoom(-0.1)" title="Отдалить">−</button>
            <button @click="resetView" title="Сбросить">⟳</button>
          </div>
        </div>
      </template>

      <!-- 3 этаж - SVG Карта -->
      <template v-else-if="currentFloor === 3">
        <div class="svg-floor-map" @wheel.prevent="handleWheel">
          <div
            class="svg-map-wrapper"
            :style="{ transform: `translate(${panX}px, ${panY}px) scale(${zoomLevel})` }"
            @mousedown="startPan"
          >
            <img src="/floor3.svg" alt="План 3 этажа" class="floor-svg-img" draggable="false" />
          </div>
          <div class="zoom-controls">
            <button @click="zoom(0.1)" title="Приблизить">+</button>
            <button @click="zoom(-0.1)" title="Отдалить">−</button>
            <button @click="resetView" title="Сбросить">⟳</button>
          </div>
        </div>
      </template>

      <!-- 4 этаж - SVG Карта -->
      <template v-else-if="currentFloor === 4">
        <div class="svg-floor-map" @wheel.prevent="handleWheel">
          <div
            class="svg-map-wrapper"
            :style="{ transform: `translate(${panX}px, ${panY}px) scale(${zoomLevel})` }"
            @mousedown="startPan"
          >
            <img src="/floor4.svg" alt="План 4 этажа" class="floor-svg-img" draggable="false" />
          </div>
          <div class="zoom-controls">
            <button @click="zoom(0.1)" title="Приблизить">+</button>
            <button @click="zoom(-0.1)" title="Отдалить">−</button>
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
import { ref, onMounted, onUnmounted } from 'vue'
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

    const zoom = (delta) => {
      const next = zoomLevel.value + delta
      if (next >= 0.5 && next <= 3) zoomLevel.value = Math.round(next * 10) / 10
    }

    const handleWheel = (event) => {
      const delta = event.deltaY > 0 ? -0.1 : 0.1
      zoom(delta)
    }

    const resetView = () => {
      zoomLevel.value = 1
      panX.value = 0
      panY.value = 0
    }

    const startPan = (event) => {
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
      isPanning.value = false
      document.body.style.cursor = 'default'
    }

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
      startPan,
      resetView
    }
  }
}
</script>

<style scoped>
.map {
  max-width: 1400px;
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

.map-controls {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 1.5rem;
  border-radius: 25px;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.floor-selector {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.floor-selector button {
  flex: 1;
  padding: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border-radius: 15px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.floor-selector button.active {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.floor-selector button.territory-btn {
  background: linear-gradient(135deg, rgba(46, 204, 113, 0.3) 0%, rgba(39, 174, 96, 0.3) 100%);
  border-color: rgba(46, 204, 113, 0.5);
}

.floor-selector button.territory-btn.active {
  background: linear-gradient(135deg, rgba(46, 204, 113, 0.5) 0%, rgba(39, 174, 96, 0.5) 100%);
  border-color: rgba(46, 204, 113, 0.8);
  box-shadow: 0 4px 20px rgba(46, 204, 113, 0.3);
}

.territory-map {
  width: 100%;
}

.territory-map h2 {
  color: white;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.territory-legend {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: white;
  font-size: 1rem;
}

.legend-icon {
  font-size: 1.8rem;
  filter: drop-shadow(0 2px 5px rgba(0,0,0,0.2));
}

.territory-content {
  min-height: 500px;
}

.territory-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 500px;
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  color: white;
}

.territory-placeholder > p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.territory-points {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  width: 100%;
  max-width: 900px;
  padding: 2rem;
}

.point {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s;
  cursor: pointer;
}

.point:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.25);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.point-icon {
  font-size: 3rem;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));
}

.point-label {
  font-size: 1.05rem;
  font-weight: 600;
  text-align: center;
  color: white;
}

.smoking-area {
  border-color: rgba(231, 76, 60, 0.5);
}

.smoking-area:hover {
  border-color: rgba(231, 76, 60, 0.8);
  box-shadow: 0 8px 25px rgba(231, 76, 60, 0.3);
}

.food-point {
  border-color: rgba(241, 196, 15, 0.5);
}

.food-point:hover {
  border-color: rgba(241, 196, 15, 0.8);
  box-shadow: 0 8px 25px rgba(241, 196, 15, 0.3);
}

.parking {
  border-color: rgba(52, 152, 219, 0.5);
}

.parking:hover {
  border-color: rgba(52, 152, 219, 0.8);
  box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
}

.map-container {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  padding: 2rem;
  min-height: 600px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 500px;
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  color: white;
}

.map-placeholder p {
  font-size: 1.2rem;
  margin: 0.5rem 0;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.hint {
  font-size: 0.9rem !important;
  color: rgba(255, 255, 255, 0.8);
}

/* ── SVG Floor Map ── */
.svg-floor-map {
  position: relative;
  overflow: hidden;
  border-radius: 20px;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
}

.svg-map-wrapper {
  transform-origin: center center;
  transition: transform 0.25s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
}

.svg-map-wrapper:active {
  cursor: grabbing;
}

.floor-svg-img {
  max-width: 100%;
  height: auto;
  display: block;
  border-radius: 12px;
  filter: drop-shadow(0 4px 24px rgba(0,0,0,0.35));
  user-select: none;
}

.zoom-controls {
  position: absolute;
  bottom: 1.5rem;
  right: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 10;
}

.zoom-controls button {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(255, 255, 255, 0.4);
  color: white;
  font-size: 1.4rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.zoom-controls button:hover {
  background: rgba(255, 255, 255, 0.4);
  transform: scale(1.1);
}
</style>

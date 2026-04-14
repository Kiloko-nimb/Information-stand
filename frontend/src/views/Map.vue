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
      </div>

      <div class="room-search">
        <input
          v-model="roomSearch"
          placeholder="Введите номер кабинета"
          @keyup.enter="findRoom"
        />
        <button @click="findRoom">Найти</button>
      </div>
    </div>

    <div class="map-container">
      <div class="map-placeholder">
        <p>Здесь будет интерактивная карта {{ currentFloor }} этажа</p>
        <p class="hint">SVG карта с возможностью zoom и построения маршрута</p>
      </div>
    </div>

    <div v-if="selectedRoom" class="room-info">
      <h3>Кабинет {{ selectedRoom.room_number }}</h3>
      <p>{{ selectedRoom.room_type }}</p>
      <p>Вместимость: {{ selectedRoom.capacity }} человек</p>
      <p v-if="selectedRoom.equipment">Оборудование: {{ selectedRoom.equipment }}</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import api from '../services/api'

export default {
  name: 'Map',
  setup() {
    const floors = [1, 2, 3, 4]
    const currentFloor = ref(1)
    const roomSearch = ref('')
    const selectedRoom = ref(null)

    const findRoom = async () => {
      if (!roomSearch.value.trim()) return

      try {
        const response = await api.get(`/rooms/${roomSearch.value}`)
        selectedRoom.value = response.data
        currentFloor.value = response.data.floor
      } catch (error) {
        console.error('Кабинет не найден:', error)
        selectedRoom.value = null
      }
    }

    return {
      floors,
      currentFloor,
      roomSearch,
      selectedRoom,
      findRoom
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

.map-controls {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.floor-selector {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.floor-selector button {
  flex: 1;
  padding: 1rem;
  border: 2px solid #ecf0f1;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.floor-selector button.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.room-search {
  display: flex;
  gap: 1rem;
}

.room-search input {
  flex: 1;
  padding: 1rem;
  border: 2px solid #ecf0f1;
  border-radius: 4px;
  font-size: 1rem;
}

.room-search button {
  padding: 1rem 2rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.map-container {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  min-height: 600px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 500px;
  border: 2px dashed #ecf0f1;
  border-radius: 4px;
  color: #7f8c8d;
}

.map-placeholder p {
  font-size: 1.2rem;
  margin: 0.5rem 0;
}

.hint {
  font-size: 0.9rem !important;
  color: #95a5a6;
}

.room-info {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.room-info h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.room-info p {
  color: #7f8c8d;
  margin-bottom: 0.5rem;
}
</style>

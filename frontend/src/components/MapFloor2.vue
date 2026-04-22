<template>
  <div class="map-floor">
    <div class="map-header">
      <h2>1 этаж - Интерактивная карта</h2>
      <div v-if="currentRoom" class="selected-room-info">
        Выбран кабинет: <strong>{{ currentRoom }}</strong>
      </div>
    </div>

    <div class="map-container">
      <svg width="820" height="900" viewBox="0 0 820 900" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_9_2)">
          <rect width="820" height="900" fill="white"/>
          
          <!-- Основные линии здания -->
          <line x1="365" y1="538.75" x2="437" y2="538.75" stroke="#1A1A1A" stroke-width="2.5"/>
          <path d="M220 140H365V90H435V140H580V540H435V640H760V830H60V640H365V540H220V140Z" stroke="#1A1A1A" stroke-width="5" stroke-linecap="square"/>
          <path d="M365 140V540" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M435 140V540" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M220 250H365" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M220 360H365" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M220 440H365" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M435 250H580" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M435 360H580" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M435 440H580" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M320 540V500H365" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M180 710H365" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M435 710H620" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M60 750H760" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M220 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M300 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M162 710V750" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M205 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M285 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M395 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M435 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M505 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M568 639V709" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M620 710H760" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M500 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M564.5 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M597 709.5L620 685V641.5" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M605.5 750.5L620 773V830" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M410 665H390V675H410V665Z" stroke="#1A1A1A" stroke-width="1.5"/>
          
          <!-- Двери (белые линии) -->
          <path d="M365 220V240" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M365 260V280" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M365 410V430" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M365 450V470" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M435 220V240" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M435 260V280" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M435 410V430" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M435 450V470" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M309 710H324" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M162 720V735" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M185 750H200" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M235 750H250" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M330 750H345" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M405 750H420" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M460 710H475" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M630 710H645" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M605 701.066L615.127 690" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M445 750H460" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M520 750H535" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M630 750H645" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M184.5 709H199.5" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M410 539L390 539" stroke="#FCFCFC" stroke-width="9"/>
          <path d="M365 95H435M365 101H435M365 107H435M365 113H435M365 119H435M365 125H435M365 131H435" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M260 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M220 645H260M220 651H260M220 657H260M220 663H260M220 669H260M220 675H260M220 681H260M220 687H260M220 693H260M220 699H260M220 705H260" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M260 645H300M260 651H300M260 657H300M260 663H300M260 669H300M260 675H300M260 681H300M260 687H300M260 693H300M260 699H300M260 705H300" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M536.5 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M506 645H536M506 651H536M506 657H536M506 663H536M506 669H536M506 675H536M506 681H536M506 687H536M506 693H536M506 699H536M506 705H536" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M537 645H567M537 651H567M537 657H567M537 663H567M537 669H567M537 675H567M537 681H567M537 687H567M537 693H567M537 699H567M537 705H567" stroke="#1A1A1A" stroke-width="1.5"/>
          
          <!-- Интерактивные кабинеты ВЕРХНИЙ УРОВЕНЬ (левое крыло) -->
          <rect x="220" y="140" width="145" height="110" 
                class="room" 
                :class="{ 'active': currentRoom === '214' }"
                @click="selectRoom('214')"/>
          
          <rect x="220" y="250" width="145" height="110" 
                class="room" 
                :class="{ 'active': currentRoom === '213' }"
                @click="selectRoom('213')"/>
          
          <rect x="220" y="360" width="145" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === '212' }"
                @click="selectRoom('212')"/>
          
          <rect x="220" y="440" width="145" height="100" 
                class="room" 
                :class="{ 'active': currentRoom === '211' }"
                @click="selectRoom('211')"/>
          
          <!-- Интерактивные кабинеты ВЕРХНИЙ УРОВЕНЬ (правое крыло) -->
          <rect x="435" y="140" width="145" height="110" 
                class="room" 
                :class="{ 'active': currentRoom === '215' }"
                @click="selectRoom('215')"/>
          
          <rect x="435" y="250" width="145" height="110" 
                class="room" 
                :class="{ 'active': currentRoom === '216' }"
                @click="selectRoom('216')"/>
          
          <rect x="435" y="360" width="145" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === '217' }"
                @click="selectRoom('217')"/>
          
          <rect x="435" y="440" width="145" height="100" 
                class="room" 
                :class="{ 'active': currentRoom === '218' }"
                @click="selectRoom('218')"/>
          
          <!-- Интерактивные кабинеты НИЖНИЙ УРОВЕНЬ (первый ряд y=640-710) -->
          <!-- 209 - левый маленький -->
          <rect x="60" y="640" width="160" height="70" 
                class="room" 
                :class="{ 'active': currentRoom === '209' }"
                @click="selectRoom('209')"/>
          
          <!-- Лестница/коридор между 220-300 -->
          
          <!-- 219 - правый большой -->
          <rect x="435" y="640" width="185" height="70" 
                class="room" 
                :class="{ 'active': currentRoom === '219' }"
                @click="selectRoom('219')"/>
          
          <!-- 201 - правый крайний -->
          <rect x="620" y="640" width="140" height="70" 
                class="room" 
                :class="{ 'active': currentRoom === '201' }"
                @click="selectRoom('201')"/>
          
          <!-- Интерактивные кабинеты НИЖНИЙ УРОВЕНЬ (второй ряд y=710-750) -->
          <!-- Кабинет (левый маленький) -->
          <rect x="60" y="710" width="102" height="40" 
                class="room" 
                :class="{ 'active': currentRoom === 'Кабинет' }"
                @click="selectRoom('Кабинет')"/>
          
          <!-- 206 - рядом с Кабинетом -->
          <rect x="162" y="710" width="58" height="40" 
                class="room" 
                :class="{ 'active': currentRoom === '206' }"
                @click="selectRoom('206')"/>
          
          <!-- Приемная (центр) -->
          <rect x="365" y="640" width="70" height="70" 
                class="room special" 
                :class="{ 'active': currentRoom === 'Приемная' }"
                @click="selectRoom('Приемная')"/>
          
          <!-- 202 - правый верхний -->
          <rect x="620" y="710" width="140" height="40" 
                class="room" 
                :class="{ 'active': currentRoom === '202' }"
                @click="selectRoom('202')"/>
          
          <!-- Интерактивные кабинеты НИЖНИЙ УРОВЕНЬ (третий ряд y=750-830) -->
          <!-- 203 - левый крайний -->
          <rect x="60" y="750" width="145" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === '203' }"
                @click="selectRoom('203')"/>
          
          <!-- 204 -->
          <rect x="205" y="750" width="80" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === '204' }"
                @click="selectRoom('204')"/>
          
          <!-- 205 -->
          <rect x="285" y="750" width="110" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === '205' }"
                @click="selectRoom('205')"/>
          
          <!-- 207 -->
          <rect x="395" y="750" width="40" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === '207' }"
                @click="selectRoom('207')"/>
          
          <!-- 208 -->
          <rect x="435" y="750" width="65" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === '208' }"
                @click="selectRoom('208')"/>
          
          <!-- 210 -->
          <rect x="500" y="750" width="64" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === '210' }"
                @click="selectRoom('210')"/>
          
          <!-- Остальные помещения справа -->
          <rect x="564.5" y="750" width="195.5" height="80" 
                class="room" 
                :class="{ 'active': currentRoom === 'Помещение' }"
                @click="selectRoom('Помещение')"/>
          
          <!-- Номера кабинетов (текст) - ВЕРХНИЙ УРОВЕНЬ -->
          <text x="292" y="200" class="room-label">214</text>
          <text x="292" y="310" class="room-label">213</text>
          <text x="292" y="405" class="room-label">212</text>
          <text x="292" y="495" class="room-label">211</text>
          
          <text x="507" y="200" class="room-label">215</text>
          <text x="507" y="310" class="room-label">216</text>
          <text x="507" y="405" class="room-label">217</text>
          <text x="507" y="495" class="room-label">218</text>
          
          <!-- Номера кабинетов (текст) - НИЖНИЙ УРОВЕНЬ -->
          <text x="140" y="680" class="room-label">209</text>
          <text x="527" y="680" class="room-label">219</text>
          <text x="690" y="680" class="room-label">201</text>
          
          <text x="110" y="735" class="room-label small">Кабинет</text>
          <text x="191" y="735" class="room-label">206</text>
          <text x="400" y="680" class="room-label special">Приемная</text>
          <text x="690" y="735" class="room-label">202</text>
          
          <text x="132" y="795" class="room-label">203</text>
          <text x="245" y="795" class="room-label">204</text>
          <text x="340" y="795" class="room-label">205</text>
          <text x="415" y="795" class="room-label">207</text>
          <text x="467" y="795" class="room-label">208</text>
          <text x="532" y="795" class="room-label">210</text>
          
          <!-- Остальные элементы карты -->
          <path d="M223 180H217V210H223V180Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M220 180V210" stroke="#1A1A1A"/>
          <path d="M223 290H217V320H223V290Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M220 290V320" stroke="#1A1A1A"/>
          <path d="M223 385H217V415H223V385Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M220 385V415" stroke="#1A1A1A"/>
          <path d="M223 475H217V505H223V475Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M220 475V505" stroke="#1A1A1A"/>
          <path d="M60 660V690" stroke="#1A1A1A"/>
          <path d="M60 715V745" stroke="#1A1A1A"/>
          <path d="M583 180H577V210H583V180Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M580 180V210" stroke="#1A1A1A"/>
          <path d="M583 290H577V320H583V290Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M580 290V320" stroke="#1A1A1A"/>
          <path d="M583 385H577V415H583V385Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M580 385V415" stroke="#1A1A1A"/>
          <path d="M583 475H577V505H583V475Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5"/>
          <path d="M580 475V505" stroke="#1A1A1A"/>
          <path d="M760 660V690" stroke="#1A1A1A"/>
          <path d="M760 775V805" stroke="#1A1A1A"/>
          <path d="M62.5 709.5L179 710" stroke="#1A1A1A" stroke-width="2.5"/>
          <path d="M366 640V711" stroke="#1A1A1A" stroke-width="2"/>
          <path d="M434 640V711" stroke="#1A1A1A" stroke-width="2"/>
          <path d="M666 710V750" stroke="#1A1A1A" stroke-width="2"/>
          <path d="M666 722V737" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M577.5 641.5V710.5M576 749.5V828" stroke="#1A1A1A" stroke-width="2.5"/>
          <path d="M400.5 93V130.5" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square"/>
          <path d="M609 756L617.188 768.568" stroke="#FCFCFC" stroke-width="7"/>
          <path d="M220 173.75H364" stroke="#1A1A1A" stroke-width="2.5"/>
        </g>
        <defs>
          <clipPath id="clip0_9_2">
            <rect width="820" height="900" fill="white"/>
          </clipPath>
        </defs>
      </svg>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'MapFloor2',
  setup() {
    const currentRoom = ref(null)

    const selectRoom = (roomNumber) => {
      currentRoom.value = roomNumber
      console.log(`Выбран кабинет: ${roomNumber}`)
    }

    return {
      currentRoom,
      selectRoom
    }
  }
}
</script>

<style scoped>
.map-floor {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.map-header {
  margin-bottom: 2rem;
  text-align: center;
}

.map-header h2 {
  color: white;
  font-size: 2rem;
  margin-bottom: 1rem;
  text-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.selected-room-info {
  color: white;
  font-size: 1.2rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  display: inline-block;
}

.map-container {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  overflow: auto;
}

.map-container svg {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}

/* ВАЖНО: Отключаем pointer-events для текста и фиксируем черный цвет */
text {
  pointer-events: none;
  user-select: none;
  fill: #000000 !important;
}

.room-label {
  font-size: 24px;
  font-weight: bold;
  fill: #000000 !important;
  text-anchor: middle;
  pointer-events: none;
}

.room-label.small {
  font-size: 16px;
}

.room-label.special {
  font-size: 18px;
  fill: #f39c12 !important;
  font-weight: 600;
}

/* Интерактивные кабинеты - по умолчанию прозрачные */
.room {
  fill: transparent;
  stroke: transparent;
  cursor: pointer;
  transition: fill 0.2s ease, stroke 0.2s ease;
}

.room:hover {
  fill: rgba(100, 108, 255, 0.2) !important;
  stroke: rgba(100, 108, 255, 0.6) !important;
  stroke-width: 2 !important;
}

.room.active {
  fill: rgba(100, 108, 255, 0.5) !important;
  stroke: rgba(100, 108, 255, 1) !important;
  stroke-width: 3 !important;
  filter: drop-shadow(0 0 10px rgba(100, 108, 255, 0.8));
}

/* Специальные помещения (Приемная) - по умолчанию прозрачные */
.room.special {
  fill: transparent;
}

.room.special:hover {
  fill: rgba(241, 196, 15, 0.2) !important;
  stroke: rgba(241, 196, 15, 0.6) !important;
  stroke-width: 2 !important;
}

.room.special.active {
  fill: rgba(241, 196, 15, 0.5) !important;
  stroke: rgba(241, 196, 15, 1) !important;
  stroke-width: 3 !important;
  filter: drop-shadow(0 0 10px rgba(241, 196, 15, 0.8));
}
</style>

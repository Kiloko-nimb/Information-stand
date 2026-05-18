<template>
  <div class="map-floor">
    <div class="map-header">
      <h2>4 этаж</h2>
    </div>

    <div class="map-container">
      <svg
        width="820"
        height="900"
        viewBox="0 0 820 900"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        @click="handleSvgClick"
      >
        <defs>
          <!-- Точечный фон коридоров — снимает белизну чертёжной заливки. -->
          <pattern id="bg-dots-4" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
            <rect width="22" height="22" fill="#f8fafc"/>
            <circle cx="11" cy="11" r="1" fill="#cbd5e1" opacity="0.65"/>
          </pattern>
          <!-- Лёгкая тень под комнатами для объёма. -->
          <filter id="room-shadow-4" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08"/>
          </filter>
        </defs>

        <rect x="0" y="0" width="820" height="900" fill="url(#bg-dots-4)"/>

        <g>
          <!-- Стены, двери и прочая графика из исходного Inkscape-файла. -->
<line x1="365" y1="538.75" x2="437" y2="538.75" stroke="#1A1A1A" stroke-width="2.5" id="line1"/>
          <path d="M220 140H365V90H435V140H580V540H435V640H760V830H60V640H365V540H220V140Z" stroke="#1A1A1A" stroke-width="5" stroke-linecap="square" id="path2"/>
          <path d="M365 140V540" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path3"/>
          <path d="M435 140V540" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path4"/>
          <path d="M220 250H365" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path5"/>
          <path d="M 220.98209,323 H 363.90477" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path6"/>
          <path d="M 220.98693,487 H 364.47065" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path7"/>
          <path d="M435 250H580" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path8"/>
          <path d="m 435.6142,322.86367 h 145" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path9"/>
          <path d="M435 487H580" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path10"/>
          <path d="M180 710H400" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path11"/>
          <path d="M448 710H620" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path12"/>
          <path d="M60 750H760" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path13"/>
          <path d="M220 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path14"/>
          <path d="M287 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path15"/>
          <path d="M162 710V750" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path16"/>
          <path d="M205 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path17"/>
          <path d="M302 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path18"/>
          <path d="M435 750V830" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path19"/>
          <path d="M514 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path20"/>
          <path d="M620 710H760" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path21"/>
          <path d="M722 828.5L736.5 806V749" stroke="#1A1A1A" stroke-width="1.5" id="path22"/>
          <path d="M365 221V241" stroke="#FCFCFC" stroke-width="7" id="path23"/>
          <path d="M365 275V295" stroke="#FCFCFC" stroke-width="7" id="path24"/>
          <path d="M323.004 260.995H343.004" stroke="#FCFCFC" stroke-width="7" id="path25"/>
          <path d="M366 411V431" stroke="#FCFCFC" stroke-width="7" id="path27"/>
          <path d="M365 505V525" stroke="#FCFCFC" stroke-width="7" id="path28"/>
          <path d="M435 221V241" stroke="#FCFCFC" stroke-width="7" id="path29"/>
          <path d="M435 275V295" stroke="#FCFCFC" stroke-width="7" id="path30"/>
          <path d="M435 411V431" stroke="#FCFCFC" stroke-width="7" id="path31"/>
          <path d="M435 505V525" stroke="#FCFCFC" stroke-width="7" id="path32"/>
          <path d="M304 709H319" stroke="#FCFCFC" stroke-width="7" id="path33"/>
          <path d="M162 721V736" stroke="#FCFCFC" stroke-width="7" id="path34"/>
          <path d="M179 750H194" stroke="#FCFCFC" stroke-width="7" id="path35"/>
          <path d="M235 751H250" stroke="#FCFCFC" stroke-width="7" id="path36"/>
          <path d="M316 750H331" stroke="#FCFCFC" stroke-width="7" id="path37"/>
          <path d="M475 711H490" stroke="#FCFCFC" stroke-width="7" id="path38"/>
          <path d="M400 700V685" stroke="#FCFCFC" stroke-width="7" id="path39"/>
          <path d="M630 710H645" stroke="#FCFCFC" stroke-width="7" id="path40"/>
          <path d="M520 750H535" stroke="#FCFCFC" stroke-width="7" id="path41"/>
          <path d="M630 750H645" stroke="#FCFCFC" stroke-width="7" id="path42"/>
          <path d="M181 710H196" stroke="#FCFCFC" stroke-width="7" id="path43"/>
          <path d="M410 550L390 550" stroke="#FCFCFC" stroke-width="9" id="path44"/>
          <path d="M365 95H435M365 101H435M365 107H435M365 113H435M365 119H435M365 125H435M365 131H435" stroke="#1A1A1A" stroke-width="1.5" id="path45"/>
          <path d="M253 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path46"/>
          <path d="M254 645H286M254 651H286M254 657H286M254 663H286M254 669H286M254 675H286M254 681H286M254 687H286M254 693H286M254 699H286M254 705H286" stroke="#1A1A1A" stroke-width="1.5" id="path47"/>
          <path d="M545 640V710" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path48"/>
          <path d="M514 645H544M514 651H544M514 657H544M514 663H544M514 669H544M514 675H544M514 681H544M514 687H544M514 693H544M514 699H544M514 705H544" stroke="#1A1A1A" stroke-width="1.5" id="path49"/>
          <path d="m 546,645 h 31.09065 M 546,651 h 31.09065 M 546,657 h 31.09065 M 546,663 h 31.09065 M 546,669 h 31.09065 M 546,675 h 31.09065 M 546,681 h 31.09065 M 546,687 h 31.09065 M 546,693 h 31.09065 M 546,699 h 31.09065 M 546,705 h 31.09065" stroke="#1a1a1a" stroke-width="1.5" id="path50"/>
          <path d="M221 645H253M221 651H253M221 657H253M221 663H253M221 669H253M221 675H253M221 681H253M221 687H253M221 693H253M221 699H253M221 705H253" stroke="#1A1A1A" stroke-width="1.5" id="path51"/>
          <path d="M223 180H217V210H223V180Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path52"/>
          <path d="M220 180V210" stroke="#1A1A1A" id="path53"/>
          <path d="M223 270H217V300H223V270Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path54"/>
          <path d="M220 270V300" stroke="#1A1A1A" id="path55"/>
          <path d="M223 385H217V415H223V385Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path56"/>
          <path d="M220 385V415" stroke="#1A1A1A" id="path57"/>
          <path d="m 222.72734,497.90372 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path58"/>
          <path d="m 219.72734,497.90372 v 30" stroke="#1a1a1a" id="path59"/>
          <path d="M60 660V690" stroke="#1A1A1A" id="path60"/>
          <path d="M60 715V745" stroke="#1A1A1A" id="path61"/>
          <path d="M583 180H577V210H583V180Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path62"/>
          <path d="M580 180V210" stroke="#1A1A1A" id="path63"/>
          <path d="M583 270H577V300H583V270Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path64"/>
          <path d="M580 270V300" stroke="#1A1A1A" id="path65"/>
          <path d="M583 385H577V415H583V385Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path66"/>
          <path d="M580 385V415" stroke="#1A1A1A" id="path67"/>
          <path d="m 582.7108,498.13625 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path68"/>
          <path d="m 579.7108,498.13625 v 30" stroke="#1a1a1a" id="path69"/>
          <path d="M760 660V690" stroke="#1A1A1A" id="path70"/>
          <path d="M760 775V805" stroke="#1A1A1A" id="path71"/>
          <path d="M135 637H105V643H135V637Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path72"/>
          <path d="M105 640H135" stroke="#1A1A1A" id="path73"/>
          <path d="M215 637H185V643H215V637Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path74"/>
          <path d="M185 640H215" stroke="#1A1A1A" id="path75"/>
          <path d="M498 637H468V643H498V637Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path76"/>
          <path d="M468 640H498" stroke="#1A1A1A" id="path77"/>
          <path d="M390 638H368V642H390V638Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path78"/>
          <path d="M368 640H390" stroke="#1A1A1A" id="path79"/>
          <path d="M675 637H645V643H675V637Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path80"/>
          <path d="M645 640H675" stroke="#1A1A1A" id="path81"/>
          <path d="M735 637H705V643H735V637Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path82"/>
          <path d="M705 640H735" stroke="#1A1A1A" id="path83"/>
          <path d="M115 827H85V833H115V827Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path84"/>
          <path d="M85 830H115" stroke="#1A1A1A" id="path85"/>
          <path d="M175 827H145V833H175V827Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path86"/>
          <path d="M145 830H175" stroke="#1A1A1A" id="path87"/>
          <path d="M260 827H230V833H260V827Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path88"/>
          <path d="M230 830H260" stroke="#1A1A1A" id="path89"/>
          <path d="M355 827H325V833H355V827Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path90"/>
          <path d="M325 830H355" stroke="#1A1A1A" id="path91"/>
          <path d="M482 827H452V833H482V827Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path92"/>
          <path d="M452 830H482" stroke="#1A1A1A" id="path93"/>
          <path d="M545 827H515V833H545V827Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path94"/>
          <path d="M515 830H545" stroke="#1A1A1A" id="path95"/>
          <path d="M633 827H603V833H633V827Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path96"/>
          <path d="M603 830H633" stroke="#1A1A1A" id="path97"/>
          <path d="M691 827H661V833H691V827Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path98"/>
          <path d="M661 830H691" stroke="#1A1A1A" id="path99"/>
          <path d="M362 577V607H368V577H362Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path100"/>
          <path d="M365 607V577" stroke="#1A1A1A" id="path101"/>
          <path d="M432 577V607H438V577H432Z" fill="#FCFCFC" stroke="#1A1A1A" stroke-width="1.5" id="path102"/>
          <path d="M435 607V577" stroke="#1A1A1A" id="path103"/>
          <path d="M62.5 709.5L179 710" stroke="#1A1A1A" stroke-width="2.5" id="path123"/>
          <path d="M337 640L337 711" stroke="#1A1A1A" stroke-width="2" id="path124"/>
          <path d="M448 640L447.5 711" stroke="#1A1A1A" stroke-width="2" id="path125"/>
          <path d="M666 710V750" stroke="#1A1A1A" stroke-width="2" id="path126"/>
          <path d="M666 722V737" stroke="#FCFCFC" stroke-width="7" id="path127"/>
          <path d="M577.5 641.5V710.5M576 749.5V828" stroke="#1A1A1A" stroke-width="2.5" id="path128"/>
          <path d="M400.5 93V130.5" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="square" id="path129"/>
          <path d="M736 772V757" stroke="#FCFCFC" stroke-width="7" id="path130"/>

          <!-- Кабинеты и именованные помещения. -->
<rect x="435.44" y="140.97" width="142.6" height="108.25" rx="4" ry="4" class="room" v-bind="roomBind('415')"/>
          <rect x="435.72" y="250.3" width="142.6" height="72.8" rx="4" ry="4" class="room" v-bind="roomBind('416')"/>
          <rect x="221.68" y="141.51" width="142.88" height="108.52" rx="4" ry="4" class="room" v-bind="roomBind('414')"/>
          <rect x="221.68" y="250.58" width="142.6" height="72.53" rx="4" ry="4" class="room" v-bind="roomBind('413')"/>
          <rect x="221.95" y="323.65" width="142.33" height="162.78" rx="4" ry="4" class="room" v-bind="roomBind('412')"/>
          <rect x="435.44" y="323.65" width="142.6" height="162.78" rx="4" ry="4" class="room" v-bind="roomBind('417')"/>
          <rect x="221.72" y="487.79" width="143.06" height="50.9" rx="4" ry="4" class="room" v-bind="roomBind('411')"/>
          <rect x="61.7" y="641.84" width="158.1" height="67.29" rx="4" ry="4" class="room" v-bind="roomBind('409')"/>
          <rect x="62.08" y="750.39" width="142.48" height="78.08" rx="4" ry="4" class="room" v-bind="roomBind('407')"/>
          <rect x="205.53" y="750.77" width="95.82" height="77.51" rx="4" ry="4" class="room" v-bind="roomBind('406')"/>
          <rect x="302.51" y="750.96" width="131.88" height="76.93" rx="4" ry="4" class="room" v-bind="roomBind('405')"/>
          <rect x="435.73" y="750.96" width="139.4" height="77.12" rx="4" ry="4" class="room" v-bind="roomBind('404')"/>
          <rect x="576.48" y="750.58" width="181.81" height="77.7" rx="4" ry="4" class="room" v-bind="roomBind('403')"/>
          <rect x="578.02" y="641.65" width="180.46" height="67.29" rx="4" ry="4" class="room" v-bind="roomBind('401')"/>
          <rect x="666.32" y="710.48" width="91.58" height="39.14" rx="4" ry="4" class="room" v-bind="roomBind('402')"/>
          <rect x="514.4" y="641.26" width="62.66" height="68.64" rx="4" ry="4" class="room" v-bind="roomBind('rect-stairs-right')"/>
          <rect x="219.99" y="641.84" width="66.9" height="67.87" rx="4" ry="4" class="room" v-bind="roomBind('rect-stairs-left')"/>
          <rect x="366.71" y="91.58" width="67.29" height="39.33" rx="4" ry="4" class="room" v-bind="roomBind('rect-stairs-center')"/>
          <rect x="61.08" y="710.02" width="100.89" height="39.81" rx="4" ry="4" class="room" v-bind="roomBind('408')"/>

          <!-- Подписи кабинетов (центрированы поверх прямоугольников). -->
<text x="506.74" y="203.09" class="room-label">415</text>
          <text x="507.02" y="294.7" class="room-label">416</text>
          <text x="293.12" y="203.77" class="room-label">414</text>
          <text x="292.98" y="294.85" class="room-label">413</text>
          <text x="293.12" y="413.04" class="room-label">412</text>
          <text x="506.74" y="413.04" class="room-label">417</text>
          <text x="293.25" y="521.24" class="room-label">411</text>
          <text x="140.75" y="683.49" class="room-label">409</text>
          <text x="133.32" y="797.43" class="room-label">407</text>
          <text x="253.44" y="797.52" class="room-label">406</text>
          <text x="368.45" y="797.43" class="room-label">405</text>
          <text x="505.43" y="797.52" class="room-label">404</text>
          <text x="667.38" y="797.43" class="room-label">403</text>
          <text x="668.25" y="683.29" class="room-label">401</text>
          <text x="712.11" y="738.05" class="room-label">402</text>
          <text x="545.73" y="683.58" class="room-label">Л</text>
          <text x="253.44" y="683.78" class="room-label">Л</text>
          <text x="400.35" y="119.25" class="room-label">Л</text>
          <text x="111.53" y="737.92" class="room-label">408</text>
        </g>

        <!-- Точка инфо-стенда («вы здесь») — в координатах viewBox. -->

      </svg>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

// Маппинг room_type (из бэкенда) → CSS-класс цвета.
const TYPE_KEY_BY_LABEL = {
  'Аудитория': 'auditorium',
  'Лаборатория': 'lab',
  'Спортзал': 'sport',
  'Актовый зал': 'hall',
  'Приёмная': 'admin',
  'Приемная': 'admin',
}

// Карта именованных (не-числовых) кабинетов в типы — для подсветки и легенды.
const NAMED_TYPE_KEY = {
  'rect-reception': 'admin',
  'rect-wc-w': 'wc',
  'rect-wc-m': 'wc',
  'rect-stairs-left': 'stairs',
  'rect-stairs-center': 'stairs',
  'rect-stairs-right': 'stairs',
  'rect-hall': 'hall',
  'rect-gym': 'sport',
  'rect-library': 'library',
  'rect-reading': 'library',
  'rect-medical': 'medical',
  'rect-bufet': 'food',
  'rect-canteen': 'food',
  'rect-garderob': 'garderob',
}

export default {
  name: 'MapFloor4',
  props: {
    highlightFreeRooms: { type: Boolean, default: false },
    freeRooms: { type: Array, default: () => [] },
    busyRooms: { type: Array, default: () => [] },
    highlightedRoom: { type: String, default: null },
    // Мапа roomNumber → room_type из /rooms/floor/4.
    roomTypes: { type: Object, default: () => ({}) },
  },
  emits: ['room-click'],
  setup(props, { emit }) {
    const freeSet = computed(() => new Set(props.freeRooms.map((r) => String(r).trim())))
    const busySet = computed(() => new Set(props.busyRooms.map((r) => String(r).trim())))
    const target = computed(() => (props.highlightedRoom ? String(props.highlightedRoom).trim() : null))

    const roomBind = (label) => {
      const value = String(label).trim()
      const isNumeric = /^\d+$/.test(value)
      let typeKey
      if (isNumeric) {
        const typeLabel = props.roomTypes[value]
        typeKey = TYPE_KEY_BY_LABEL[typeLabel] || 'other'
      } else {
        typeKey = NAMED_TYPE_KEY[value] || 'other'
      }
      return {
        'data-room': isNumeric ? value : null,
        class: [
          `room--type-${typeKey}`,
          {
            'room--interactive': isNumeric,
            'room--free': props.highlightFreeRooms && freeSet.value.has(value),
            'room--busy': props.highlightFreeRooms && busySet.value.has(value),
            'room--target': target.value !== null && target.value === value,
          },
        ],
      }
    }

    const handleSvgClick = (event) => {
      const t = event.target
      if (!t || typeof t.getAttribute !== 'function') return
      const num = t.getAttribute('data-room')
      if (!num) return
      emit('room-click', num)
    }

    return {
      roomBind,
      handleSvgClick,
    }
  },
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
  color: var(--text);
  font-size: 2rem;
  margin-bottom: 1rem;
}

.map-container {
  background: var(--surface);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: 25px;
  padding: 2rem;
  box-shadow: var(--shadow);
  overflow: auto;
}

.map-container svg {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}

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
  font-size: 14px;
  fill: #475569 !important;
  font-weight: 600;
}

.room {
  fill: transparent;
  stroke: transparent;
  cursor: default;
  transition: fill 0.25s ease, stroke 0.25s ease, fill-opacity 0.25s ease, stroke-opacity 0.25s ease;
  filter: url(#room-shadow-4);
}

.room.room--interactive {
  cursor: pointer;
}

.room--type-auditorium { fill: #3b82f6; fill-opacity: 0.22; stroke: #1d4ed8; stroke-opacity: 0.7;  stroke-width: 1.3; }
.room--type-lab        { fill: #8b5cf6; fill-opacity: 0.26; stroke: #6d28d9; stroke-opacity: 0.75; stroke-width: 1.3; }
.room--type-sport      { fill: #22c55e; fill-opacity: 0.26; stroke: #15803d; stroke-opacity: 0.75; stroke-width: 1.3; }
.room--type-hall       { fill: #f97316; fill-opacity: 0.26; stroke: #c2410c; stroke-opacity: 0.75; stroke-width: 1.3; }
.room--type-admin      { fill: #f59e0b; fill-opacity: 0.30; stroke: #b45309; stroke-opacity: 0.8;  stroke-width: 1.3; }
/* Туалеты — отчётливый тёплый розовый, чтобы не сливаться с пустым (--other) и не путаться с лестницей. */
.room--type-wc         { fill: #ec4899; fill-opacity: 0.22; stroke: #be185d; stroke-opacity: 0.7;  stroke-width: 1.3; }
.room--type-stairs     { fill: #6366f1; fill-opacity: 0.26; stroke: #4338ca; stroke-opacity: 0.75; stroke-width: 1.3; stroke-dasharray: 6 4; }
/* Библиотека и читальный зал — бирюзовый. */
.room--type-library    { fill: #14b8a6; fill-opacity: 0.24; stroke: #0f766e; stroke-opacity: 0.75; stroke-width: 1.3; }
/* Медпункт — ярко-красный, чтобы было заметно в экстренном случае. */
.room--type-medical    { fill: #ef4444; fill-opacity: 0.22; stroke: #b91c1c; stroke-opacity: 0.8;  stroke-width: 1.3; }
/* Буфет и столовая — тёплый жёлтый. */
.room--type-food       { fill: #eab308; fill-opacity: 0.30; stroke: #a16207; stroke-opacity: 0.8;  stroke-width: 1.3; }
/* Гардероб — нейтральный сине-серый. */
.room--type-garderob   { fill: #64748b; fill-opacity: 0.20; stroke: #334155; stroke-opacity: 0.7;  stroke-width: 1.3; }
/* Кабинеты без известного типа — почти прозрачные, чтобы не конкурировать с цветными типами и не выглядеть «использованной» подсветкой. */
.room--type-other      { fill: #cbd5e1; fill-opacity: 0.10; stroke: #94a3b8; stroke-opacity: 0.55; stroke-width: 1; }

/* «Вы здесь» — маркер инфо-стенда. */
.stand-marker {
  pointer-events: none;
}

.stand-marker .stand-halo {
  fill: rgba(37, 99, 235, 0.25);
  animation: stand-halo-pulse-4 1.8s ease-in-out infinite;
}

.stand-marker .stand-dot {
  fill: #2563eb;
  stroke: #ffffff;
  stroke-width: 2;
}

@keyframes stand-halo-pulse-4 {
  0%, 100% { opacity: 0.55; transform: scale(1); }
  50%      { opacity: 0.15; transform: scale(1.6); }
}

.stand-marker .stand-halo {
  transform-origin: center;
  transform-box: fill-box;
}

.room.room--interactive:hover {
  fill-opacity: 0.25;
  stroke-opacity: 1;
  stroke-width: 2;
}

.room.room--target {
  fill: rgba(37, 99, 235, 0.35) !important;
  stroke: #2563eb !important;
  stroke-width: 3 !important;
  animation: room-target-pulse-4 1.6s ease-in-out infinite;
}

@keyframes room-target-pulse-4 {
  0%, 100% {
    fill: rgba(37, 99, 235, 0.35) !important;
    stroke-opacity: 1;
  }
  50% {
    fill: rgba(37, 99, 235, 0.55) !important;
    stroke-opacity: 0.6;
  }
}

.room.room--free {
  fill: rgba(34, 197, 94, 0.32) !important;
  stroke: rgba(22, 163, 74, 0.85) !important;
  stroke-width: 2 !important;
  animation: room-free-pulse-4 2.4s ease-in-out infinite;
}

.room.room--busy {
  fill: rgba(239, 68, 68, 0.18) !important;
  stroke: rgba(220, 38, 38, 0.6) !important;
  stroke-width: 1.5 !important;
}

@keyframes room-free-pulse-4 {
  0%, 100% { fill: rgba(34, 197, 94, 0.28) !important; }
  50%      { fill: rgba(34, 197, 94, 0.42) !important; }
}
</style>

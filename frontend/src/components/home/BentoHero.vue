<!--
  BentoHero — bento-карточки шапки главной: приветствие колледжа +
  цифровые часы с погодой по Красноярску. Полностью самодостаточный
  блок: сам тикает часами и подгружает погоду через open-meteo.
-->
<template>
  <div class="bento-hero">
    <div class="bento-card bento-welcome">
      <span class="bento-eyebrow">Добро пожаловать в</span>
      <h1>Красноярский колледж радиоэлектроники<br>и информационных технологий</h1>
      <div class="bento-day-row">
        <span class="bento-day-name">{{ currentDayName }}</span>
        <span class="bento-day-dot">·</span>
        <span class="bento-day-date">{{ currentDayShort }}</span>
      </div>
    </div>
    <div class="bento-card bento-clock">
      <div class="bento-clock-eyebrow">Сейчас</div>
      <div class="bento-clock-time">{{ currentTime }}</div>
      <div class="bento-clock-date">{{ currentDayName }}</div>
      <div v-if="weather" class="bento-weather" :title="weather.label">
        <Icon :name="weather.icon" :size="22" class="bento-weather-icon" />
        <span class="bento-weather-temp">{{ weather.temp }}°</span>
        <span class="bento-weather-label">{{ weather.label }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import Icon from '../Icon.vue'
import { useClock } from '../../composables/useClock'

const KRSK_LAT = 56.0153
const KRSK_LON = 92.8932
const WEATHER_REFRESH_MS = 15 * 60 * 1000

const weatherFromCode = (code) => {
  // WMO weather interpretation codes — https://open-meteo.com/en/docs
  if (code === 0) return { icon: 'sun', label: 'Ясно' }
  if (code === 1) return { icon: 'sun', label: 'Преим. ясно' }
  if (code === 2) return { icon: 'cloudSun', label: 'Перем. облачность' }
  if (code === 3) return { icon: 'cloud', label: 'Пасмурно' }
  if (code === 45 || code === 48) return { icon: 'fog', label: 'Туман' }
  if (code >= 51 && code <= 57) return { icon: 'cloudRain', label: 'Морось' }
  if (code >= 61 && code <= 67) return { icon: 'cloudRain', label: 'Дождь' }
  if (code >= 71 && code <= 77) return { icon: 'snow', label: 'Снег' }
  if (code >= 80 && code <= 82) return { icon: 'cloudRain', label: 'Ливень' }
  if (code === 85 || code === 86) return { icon: 'snow', label: 'Снегопад' }
  if (code >= 95 && code <= 99) return { icon: 'thunder', label: 'Гроза' }
  return { icon: 'cloud', label: 'Облачно' }
}

export default {
  name: 'BentoHero',
  components: { Icon },
  setup() {
    const { currentTime, currentDayName, currentDayShort } = useClock()
    const weather = ref(null)
    let weatherInterval = null

    const loadWeather = async () => {
      try {
        const url =
          `https://api.open-meteo.com/v1/forecast?latitude=${KRSK_LAT}&longitude=${KRSK_LON}` +
          `&current=temperature_2m,weather_code&timezone=Asia/Krasnoyarsk`
        const response = await fetch(url)
        if (!response.ok) return
        const data = await response.json()
        const c = data.current
        if (!c) return
        const meta = weatherFromCode(c.weather_code)
        weather.value = {
          temp: Math.round(c.temperature_2m),
          icon: meta.icon,
          label: meta.label,
        }
      } catch (_) {
        // тихо: если погода не загрузилась — просто не показываем
      }
    }

    onMounted(() => {
      loadWeather()
      weatherInterval = setInterval(loadWeather, WEATHER_REFRESH_MS)
    })

    onUnmounted(() => {
      if (weatherInterval) {
        clearInterval(weatherInterval)
        weatherInterval = null
      }
    })

    return { currentTime, currentDayName, currentDayShort, weather }
  },
}
</script>

<style scoped>
.bento-hero {
  display: grid;
  grid-template-columns: minmax(0, 2.1fr) minmax(0, 1fr);
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 900px) {
  .bento-hero {
    grid-template-columns: 1fr;
  }
}

.bento-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition), box-shadow var(--transition),
    border-color var(--transition);
  position: relative;
  overflow: hidden;
}

.bento-card:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow);
}

.bento-welcome {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.75rem;
  background:
    radial-gradient(120% 80% at 0% 0%, var(--accent-soft), transparent 55%),
    var(--surface);
}

.bento-eyebrow {
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-muted);
}

h1 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 3.4vw, 2.6rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.1;
  margin: 0;
  color: var(--text);
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
}

.bento-day-row {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: 0.75rem;
  padding: 0.55rem 1.1rem;
  background: var(--accent-gradient);
  color: #ffffff;
  border-radius: var(--radius-pill);
  font-weight: 700;
  font-size: clamp(1rem, 1.4vw, 1.2rem);
  text-transform: capitalize;
  letter-spacing: -0.01em;
  align-self: flex-start;
  box-shadow: var(--shadow-sm);
}

.bento-day-dot {
  opacity: 0.55;
}

.bento-day-date {
  font-weight: 600;
}

.bento-clock {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 0.4rem;
  background: linear-gradient(160deg, var(--accent) 0%, var(--accent-2) 100%);
  color: #ffffff;
  border-color: transparent;
  box-shadow: var(--shadow), var(--accent-glow);
}

.bento-clock::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.18), transparent 60%);
  pointer-events: none;
}

.bento-clock-eyebrow {
  position: relative;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.8;
}

.bento-clock-time {
  position: relative;
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5.5vw, 4rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.bento-weather {
  position: relative;
  margin-top: 0.85rem;
  padding-top: 0.85rem;
  border-top: 1px solid rgba(255, 255, 255, 0.22);
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.01em;
}

.bento-weather-icon {
  flex-shrink: 0;
}

.bento-weather-temp {
  font-family: var(--font-display);
  font-size: 1.45rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1;
}

.bento-weather-label {
  opacity: 0.92;
  font-weight: 500;
  font-size: 0.95rem;
  white-space: nowrap;
}

.bento-clock-date {
  position: relative;
  font-size: 1rem;
  opacity: 0.9;
  text-transform: capitalize;
  font-weight: 600;
}
</style>

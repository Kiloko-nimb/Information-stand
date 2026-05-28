<template>
  <Teleport to="body">
    <Transition name="screensaver">
      <div v-if="isIdle" class="screensaver" @click="handleDismiss" @touchstart="handleDismiss">
        <div class="screensaver-content">
          <div class="screensaver-logo-wrap">
            <img :src="logoSrc" alt="ККРИТ" class="screensaver-logo" />
          </div>
          <div class="clock-display">
            <div class="clock-time">{{ timeStr }}</div>
            <div class="clock-date">{{ dateStr }}</div>
          </div>
          <div class="screensaver-college">
            Красноярский колледж радиоэлектроники<br>и информационных технологий
          </div>
          <div class="screensaver-hint">Нажмите, чтобы начать</div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useScreensaver } from '../composables/useScreensaver'
import logoSrc from '../assets/logo.png'

const router = useRouter()
const { isIdle, dismiss } = useScreensaver()

function handleDismiss() {
  dismiss()
  router.push('/')
}

const timeStr = ref('')
const dateStr = ref('')
let clockInterval = null

function updateClock() {
  const now = new Date()
  timeStr.value = now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
  dateStr.value = now.toLocaleDateString('ru-RU', { weekday: 'long', day: 'numeric', month: 'long' })
}

onMounted(() => {
  updateClock()
  clockInterval = setInterval(updateClock, 1000)
})

onUnmounted(() => {
  clearInterval(clockInterval)
})
</script>

<style scoped>
.screensaver {
  position: fixed;
  inset: 0;
  z-index: 99999;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
}

.screensaver-content {
  text-align: center;
  animation: screensaver-pulse 4s ease-in-out infinite;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.screensaver-logo-wrap {
  width: clamp(180px, 22vw, 280px);
  height: clamp(180px, 22vw, 280px);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 70%, rgba(255, 255, 255, 0) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 20px 50px rgba(99, 102, 241, 0.35));
  animation: logo-float 6s ease-in-out infinite;
}

.screensaver-logo {
  width: 85%;
  height: 85%;
  object-fit: contain;
}

@keyframes logo-float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-12px); }
}

.screensaver-college {
  font-size: clamp(0.95rem, 1.4vw, 1.25rem);
  font-weight: 500;
  letter-spacing: 0.02em;
  color: rgba(226, 232, 240, 0.85);
  line-height: 1.4;
  margin-top: -0.5rem;
}

.clock-display {
  margin-bottom: 0;
}

.clock-time {
  font-size: 8rem;
  font-weight: 800;
  line-height: 1;
  background: linear-gradient(135deg, #818cf8, #6366f1, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

.clock-date {
  font-size: 1.8rem;
  color: rgba(148, 163, 184, 0.8);
  margin-top: 0.5rem;
  font-weight: 300;
  text-transform: capitalize;
}

.screensaver-hint {
  font-size: 1rem;
  color: rgba(148, 163, 184, 0.4);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-top: 3rem;
}

@keyframes screensaver-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.85; }
}

/* Transition */
.screensaver-enter-active {
  transition: opacity 0.8s ease;
}
.screensaver-leave-active {
  transition: opacity 0.3s ease;
}
.screensaver-enter-from,
.screensaver-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .clock-time {
    font-size: 4rem;
  }
  .clock-date {
    font-size: 1.2rem;
  }
}
</style>

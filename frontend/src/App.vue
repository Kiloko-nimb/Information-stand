<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <router-link
          v-if="$route.path !== '/'"
          to="/"
          class="logo-link"
          aria-label="На главную"
          @click="onLogoTap"
        >
          <img src="@/assets/logo.png" alt="ККРИТ" class="logo" />
        </router-link>
        <div
          v-else
          class="logo-link is-static"
          aria-hidden="true"
          @click="onLogoTap"
        >
          <img src="@/assets/logo.png" alt="ККРИТ" class="logo" />
        </div>
        <div class="header-text">
          <span class="header-eyebrow">Интерактивный стенд</span>
          <h1>ККРИТ</h1>
        </div>
      </div>
      <div v-if="!isOnline" class="offline-indicator">
        <span class="offline-dot"></span>
        Offline
      </div>
    </header>

    <main class="app-content">
      <router-view />
    </main>

    <SnakeGame v-if="snakeOpen" @close="snakeOpen = false" />
    <SettingsButton />
    <Screensaver />

    <transition name="kiosk-fade">
      <div
        v-if="warningVisible"
        class="kiosk-warning"
        role="alertdialog"
        aria-live="assertive"
        @click="dismissWarning"
        @touchstart="dismissWarning"
      >
        <div class="kiosk-warning__card" @click.stop>
          <div class="kiosk-warning__count">{{ warningCountdown }}</div>
          <div class="kiosk-warning__title">Возврат на главную</div>
          <div class="kiosk-warning__sub">
            Тапни в любом месте, чтобы остаться на странице.
          </div>
          <button
            type="button"
            class="kiosk-warning__btn"
            @click.stop="dismissWarning"
          >
            Остаться
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import SnakeGame from './components/SnakeGame.vue'
import Screensaver from './components/Screensaver.vue'
import SettingsButton from './components/SettingsButton.vue'
import { useSound } from './composables/useSound'

export default {
  name: 'App',
  components: { SnakeGame, Screensaver, SettingsButton },
  setup() {
    const isOnline = ref(navigator.onLine)
    const router = useRouter()
    const snakeOpen = ref(false)
    const { enabled: soundsOn, play } = useSound()

    // Пасхалка: 5 быстрых тапов по лого в пределах 1.8с → режим «Для своих».
    const TAP_THRESHOLD = 5
    const TAP_WINDOW_MS = 1800
    let logoTaps = []

    const onLogoTap = () => {
      const now = Date.now()
      logoTaps = logoTaps.filter((t) => now - t < TAP_WINDOW_MS)
      logoTaps.push(now)
      if (logoTaps.length >= TAP_THRESHOLD) {
        logoTaps = []
        snakeOpen.value = true
      }
    }
    
    // Таймер бездействия для киоска. Настраивается через .env:
    //   VITE_KIOSK_TIMEOUT_SEC — общее время бездействия до возврата (сек, по умолчанию 180)
    //   VITE_KIOSK_WARNING_SEC — за сколько секунд до возврата показывать предупреждение (по умолчанию 10)
    // VITE_KIOSK_WARNING_SEC=0 должен реально отключать предупреждение
    // (так задокументировано в .env.example). Поэтому НЕ используем
    // `|| 10` — для 0 это даёт 10. Защищаем только от NaN.
    const rawTimeout = parseInt(import.meta.env.VITE_KIOSK_TIMEOUT_SEC, 10)
    const TIMEOUT_SEC = Math.max(5, Number.isNaN(rawTimeout) ? 180 : rawTimeout)
    const rawWarning = parseInt(import.meta.env.VITE_KIOSK_WARNING_SEC, 10)
    const WARNING_SEC = Math.min(
      Math.max(0, Number.isNaN(rawWarning) ? 10 : rawWarning),
      TIMEOUT_SEC - 1,
    )

    const warningVisible = ref(false)
    const warningCountdown = ref(WARNING_SEC)

    let warningTimer = null     // setTimeout: «через X мс показать предупреждение»
    let countdownInterval = null // setInterval: тик обратного отсчёта
    let returnTimer = null      // setTimeout: «через X мс вернуться на главную»

    const clearAllTimers = () => {
      if (warningTimer) { clearTimeout(warningTimer); warningTimer = null }
      if (countdownInterval) { clearInterval(countdownInterval); countdownInterval = null }
      if (returnTimer) { clearTimeout(returnTimer); returnTimer = null }
    }

    const goHome = () => {
      clearAllTimers()
      warningVisible.value = false
      if (router.currentRoute.value.path !== '/') {
        router.push('/')
      }
    }

    const showWarning = () => {
      // VITE_KIOSK_WARNING_SEC=0 — режим «вернуться без предупреждения».
      // Без этой ветки overlay успевал моргнуть (Vue рендерит до того,
      // как setTimeout(goHome, 0) выстрелит) — а с transition-fade
      // вспышка ~200мс реально заметна.
      if (WARNING_SEC <= 0) {
        goHome()
        return
      }

      warningCountdown.value = WARNING_SEC
      warningVisible.value = true

      countdownInterval = setInterval(() => {
        warningCountdown.value -= 1
        if (warningCountdown.value <= 0) {
          clearInterval(countdownInterval)
          countdownInterval = null
        }
      }, 1000)

      returnTimer = setTimeout(goHome, WARNING_SEC * 1000)
    }

    const resetInactivityTimer = () => {
      clearAllTimers()
      warningVisible.value = false

      // На главной таймер всё равно крутится (на случай возврата), но никуда
      // не пушит. Чтобы не дёргать пользователя предупреждением — на главной
      // его не показываем вовсе.
      if (router.currentRoute.value.path === '/') return

      const preWarning = (TIMEOUT_SEC - WARNING_SEC) * 1000
      warningTimer = setTimeout(showWarning, preWarning)
    }

    const dismissWarning = () => {
      resetInactivityTimer()
    }

    const handleUserActivity = () => {
      // Если предупреждение видно — НЕ сбрасываем таймер от мелких касаний
      // экрана, иначе оно никогда не сработает у активного стенда. Сброс
      // только по явному клику/тапу по самому оверлею (см. dismissWarning).
      if (warningVisible.value) return
      resetInactivityTimer()
    }

    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click']

    onMounted(() => {
      window.addEventListener('online', () => { isOnline.value = true })
      window.addEventListener('offline', () => { isOnline.value = false })

      // Глобальный звуковой фидбек для тап-целей (кнопки, ссылки)
      const onTap = (e) => {
        if (!soundsOn.value) return
        const t = e.target
        if (t && t.closest && t.closest('button, a, [role="button"]')) {
          play.tap()
        }
      }
      document.addEventListener('pointerdown', onTap, true)

      events.forEach(event => {
        document.addEventListener(event, handleUserActivity, true)
      })

      // При смене маршрута — пересчитываем таймер (главная не показывает предупреждение)
      router.afterEach(() => resetInactivityTimer())

      resetInactivityTimer()

      // Принудительный 4K-режим для дебага с обычного монитора:
      // VITE_KIOSK_4K_MODE=true → масштабирует UI как на 4K-стенде.
      if (String(import.meta.env.VITE_KIOSK_4K_MODE).toLowerCase() === 'true') {
        document.documentElement.setAttribute('data-kiosk-4k', '1')
      }
      // Помечаем, что устройство сенсорное — на случай, если какие-то
      // CSS-эффекты в будущем захочется тонко настраивать только для тача.
      const mq = window.matchMedia('(hover: none), (pointer: coarse)')
      const applyTouch = () => {
        if (mq.matches) document.documentElement.setAttribute('data-touch', '1')
        else document.documentElement.removeAttribute('data-touch')
      }
      applyTouch()
      mq.addEventListener?.('change', applyTouch)
    })

    onUnmounted(() => {
      clearAllTimers()
      events.forEach(event => {
        document.removeEventListener(event, handleUserActivity, true)
      })
    })

    return {
      isOnline,
      snakeOpen,
      onLogoTap,
      warningVisible,
      warningCountdown,
      dismissWarning,
    }
  }
}
</script>

<style>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: saturate(180%) blur(18px);
  -webkit-backdrop-filter: saturate(180%) blur(18px);
  border-bottom: 1px solid var(--border);
}

[data-theme="dark"] .app-header {
  background: rgba(10, 13, 28, 0.72);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  padding: 6px;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.96);
  transition: transform var(--transition), box-shadow var(--transition);
  box-shadow: var(--shadow-xs);
}

.logo-link:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.logo-link:active {
  transform: translateY(0) scale(0.98);
}

.logo-link.is-static {
  cursor: default;
}

.logo-link.is-static:hover {
  transform: none;
  box-shadow: var(--shadow-xs);
}

.logo {
  height: 44px;
  width: auto;
  display: block;
}

.header-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.header-eyebrow {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.app-header h1 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.offline-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--danger);
  background: var(--danger-soft);
  border: 1px solid rgba(244, 63, 94, 0.35);
  border-radius: var(--radius-pill);
}

.offline-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--danger);
  box-shadow: 0 0 10px var(--danger);
  animation: pulse-dot 1.8s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}

.app-content {
  flex: 1;
  padding: 2rem;
  max-width: var(--content-max-width, 1600px);
  width: 100%;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .app-header {
    padding: 0.75rem 1rem;
  }
  .app-content {
    padding: 1rem;
  }
}

/* ───── Kiosk inactivity warning ───── */
.kiosk-warning {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(8, 12, 28, 0.62);
  backdrop-filter: saturate(160%) blur(10px);
  -webkit-backdrop-filter: saturate(160%) blur(10px);
  cursor: pointer;
  padding: 1.5rem;
}

.kiosk-warning__card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg, 24px);
  box-shadow: var(--shadow-lg, 0 30px 80px rgba(0, 0, 0, 0.35));
  padding: 2.5rem 3rem;
  text-align: center;
  max-width: 480px;
  width: 100%;
  cursor: default;
  animation: kiosk-pop 220ms ease-out;
}

.kiosk-warning__count {
  font-family: var(--font-display);
  font-size: 7rem;
  font-weight: 800;
  line-height: 1;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 0.5rem;
  font-variant-numeric: tabular-nums;
}

.kiosk-warning__title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.kiosk-warning__sub {
  font-size: 1rem;
  color: var(--text-muted);
  margin-bottom: 1.75rem;
  line-height: 1.45;
}

.kiosk-warning__btn {
  display: inline-block;
  padding: 0.85rem 2.25rem;
  font-family: var(--font-ui);
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  background: var(--accent);
  border: none;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition), background var(--transition);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35);
}

.kiosk-warning__btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 22px rgba(37, 99, 235, 0.45);
}

.kiosk-warning__btn:active {
  transform: translateY(0);
}

.kiosk-fade-enter-active,
.kiosk-fade-leave-active {
  transition: opacity 200ms ease;
}
.kiosk-fade-enter-from,
.kiosk-fade-leave-to {
  opacity: 0;
}

@keyframes kiosk-pop {
  from { transform: scale(0.92); opacity: 0; }
  to   { transform: scale(1);    opacity: 1; }
}
</style>

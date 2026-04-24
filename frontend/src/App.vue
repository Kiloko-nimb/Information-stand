<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <router-link to="/" class="logo-link" aria-label="На главную">
          <img src="@/assets/logo.png" alt="ККРИТ" class="logo" />
        </router-link>
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
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const isOnline = ref(navigator.onLine)
    const router = useRouter()
    
    // Таймер бездействия для киоска
    const INACTIVITY_TIMEOUT = 3 * 60 * 1000 // 3 минуты в миллисекундах
    let inactivityTimer = null

    const resetInactivityTimer = () => {
      // Очищаем предыдущий таймер
      if (inactivityTimer) {
        clearTimeout(inactivityTimer)
      }

      // Устанавливаем новый таймер
      inactivityTimer = setTimeout(() => {
        // Возвращаемся на главную страницу только если мы не на ней
        if (router.currentRoute.value.path !== '/') {
          console.log('Таймер бездействия: возврат на главную')
          router.push('/')
        }
      }, INACTIVITY_TIMEOUT)
    }

    const handleUserActivity = () => {
      resetInactivityTimer()
    }

    onMounted(() => {
      // Слушатели онлайн/офлайн статуса
      window.addEventListener('online', () => {
        isOnline.value = true
      })

      window.addEventListener('offline', () => {
        isOnline.value = false
      })

      // Слушатели активности пользователя для киоска
      const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click']
      
      events.forEach(event => {
        document.addEventListener(event, handleUserActivity, true)
      })

      // Запускаем таймер при загрузке
      resetInactivityTimer()
    })

    onUnmounted(() => {
      // Очищаем таймер при размонтировании
      if (inactivityTimer) {
        clearTimeout(inactivityTimer)
      }

      // Удаляем слушатели активности
      const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click']
      
      events.forEach(event => {
        document.removeEventListener(event, handleUserActivity, true)
      })
    })

    return {
      isOnline
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
  background: rgba(10, 13, 28, 0.72);
  backdrop-filter: saturate(180%) blur(18px);
  -webkit-backdrop-filter: saturate(180%) blur(18px);
  border-bottom: 1px solid var(--border);
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
  max-width: 1600px;
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
</style>

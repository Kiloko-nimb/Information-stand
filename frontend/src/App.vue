<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <router-link to="/" class="logo-link">
          <img src="@/assets/logo.png" alt="ККРИТ" class="logo" />
        </router-link>
        <h1>ККРИТ - Интерактивный стенд</h1>
      </div>
      <div v-if="!isOnline" class="offline-indicator">
        📡 Offline режим
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  cursor: pointer;
  padding: 8px;
  margin: -8px;
  border-radius: 12px;
  transition: all 0.3s;
  min-width: 80px;
  min-height: 80px;
  justify-content: center;
}

.logo-link:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.05);
}

.logo-link:active {
  transform: scale(0.95);
}

.logo {
  height: 60px;
  width: auto;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));
  background: rgba(255, 255, 255, 0.95);
  padding: 8px;
  border-radius: 12px;
  transition: transform 0.3s;
}

.logo:hover {
  transform: scale(1.05);
}

.app-header h1 {
  text-shadow: 0 2px 15px rgba(0,0,0,0.3);
  font-weight: 600;
}

.offline-indicator {
  background: rgba(231, 76, 60, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(231, 76, 60, 0.5);
  padding: 0.6rem 1.2rem;
  border-radius: 12px;
  font-size: 0.95rem;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.app-content {
  flex: 1;
  padding: 2rem;
}
</style>

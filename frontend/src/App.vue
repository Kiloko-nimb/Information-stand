<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <img src="@/assets/logo.png" alt="ККРИТ" class="logo" />
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
import { ref, onMounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const isOnline = ref(navigator.onLine)

    onMounted(() => {
      window.addEventListener('online', () => {
        isOnline.value = true
      })

      window.addEventListener('offline', () => {
        isOnline.value = false
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

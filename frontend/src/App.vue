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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.logo {
  height: 60px;
  width: auto;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
  background: white;
  padding: 8px;
  border-radius: 8px;
}

.offline-indicator {
  background: #e74c3c;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.app-content {
  flex: 1;
  padding: 2rem;
}
</style>

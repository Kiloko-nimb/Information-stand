import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import ripple from './directives/ripple'
import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.directive('ripple', ripple)
app.mount('#app')

// PWA: регистрация service worker для офлайн-режима.
// Полностью игнорируется на dev-сервере — работает только в production-сборке.
if ('serviceWorker' in navigator) {
  import('virtual:pwa-register').then(({ registerSW }) => {
    registerSW({
      immediate: true,
      onRegisteredSW(swUrl, reg) {
        console.log('[PWA] SW зарегистрирован:', swUrl)
      },
      onOfflineReady() {
        console.log('[PWA] Готов к работе в офлайн-режиме')
      },
    })
  }).catch(() => {
    // virtual:pwa-register отсутствует в dev — это нормально
  })
}
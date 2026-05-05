<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <Shield :size="32" />
        <h1>Панель администратора</h1>
        <p>ККРИТ — Интерактивный стенд</p>
      </div>

      <!-- Setup form (no admin exists yet) -->
      <form v-if="needsSetup" @submit.prevent="doSetup" class="login-form">
        <p class="setup-notice">Администратор ещё не создан. Задайте логин и пароль.</p>
        <div class="field">
          <label>Логин</label>
          <input v-model="username" type="text" required autocomplete="username" />
        </div>
        <div class="field">
          <label>Пароль</label>
          <input v-model="password" type="password" required autocomplete="new-password" />
        </div>
        <div class="field">
          <label>Повторите пароль</label>
          <input v-model="password2" type="password" required autocomplete="new-password" />
        </div>
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Создание...' : 'Создать администратора' }}
        </button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>

      <!-- Login form -->
      <form v-else @submit.prevent="doLogin" class="login-form">
        <div class="field">
          <label>Логин</label>
          <input v-model="username" type="text" required autocomplete="username" />
        </div>
        <div class="field">
          <label>Пароль</label>
          <input v-model="password" type="password" required autocomplete="current-password" />
        </div>
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>

      <router-link to="/" class="back-link"><ArrowLeft :size="14" /> Вернуться на стенд</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Shield, ArrowLeft } from 'lucide-vue-next'
import { login, setupAdmin, isAuthenticated } from '../../services/adminService'
import api from '../../services/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const password2 = ref('')
const error = ref('')
const loading = ref(false)
const needsSetup = ref(false)

onMounted(async () => {
  if (isAuthenticated()) {
    router.replace('/admin')
    return
  }
  try {
    const resp = await api.get('/auth/check')
    needsSetup.value = resp.data.needs_setup
  } catch {
    needsSetup.value = false
  }
})

async function doLogin() {
  error.value = ''
  loading.value = true
  try {
    await login(username.value, password.value)
    router.push('/admin')
  } catch (e) {
    if (e.response?.status === 401) {
      error.value = 'Неверный логин или пароль'
    } else {
      error.value = e.response?.data?.detail || 'Ошибка входа'
    }
  } finally {
    loading.value = false
  }
}

async function doSetup() {
  error.value = ''
  if (password.value !== password2.value) {
    error.value = 'Пароли не совпадают'
    return
  }
  if (password.value.length < 4) {
    error.value = 'Пароль должен быть не менее 4 символов'
    return
  }
  loading.value = true
  try {
    await setupAdmin(username.value, password.value)
    await login(username.value, password.value)
    router.push('/admin')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка создания'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface);
  padding: 1rem;
}
.login-card {
  background: var(--surface-elevated, #1e293b);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2.5rem;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.login-header {
  text-align: center;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}
.login-header h1 {
  font-size: 1.4rem;
  margin-bottom: 0;
}
.login-header p {
  color: var(--text-muted);
  font-size: 0.9rem;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.field label {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 500;
}
.field input {
  padding: 0.7rem 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface);
  color: var(--text);
  font-size: 1rem;
  transition: border-color 0.2s;
}
.field input:focus {
  outline: none;
  border-color: var(--accent, #6366f1);
}
.btn-primary {
  padding: 0.75rem 1.5rem;
  background: var(--accent-gradient, linear-gradient(135deg, #6366f1, #8b5cf6));
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  margin-top: 0.5rem;
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}
.error {
  color: #f87171;
  font-size: 0.9rem;
  text-align: center;
}
.setup-notice {
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
}
.back-link {
  display: block;
  text-align: center;
  margin-top: 1.5rem;
  color: var(--text-muted);
  font-size: 0.85rem;
  text-decoration: none;
}
.back-link:hover {
  color: var(--text);
}
</style>

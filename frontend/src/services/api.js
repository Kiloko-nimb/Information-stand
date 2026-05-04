import axios from 'axios'
import axiosRetry from 'axios-retry'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,  // Увеличили таймаут
  headers: {
    'Content-Type': 'application/json'
  }
})

// Настройка retry для axios
axiosRetry(api, {
  retries: 3,
  retryDelay: (retryCount) => {
    // Экспоненциальная задержка: 1s, 2s, 4s
    return Math.min(1000 * (2 ** retryCount), 10000)
  },
  retryCondition: (error) => {
    // Retry при таймаутах и 5xx ошибках
    return axiosRetry.isNetworkOrIdempotentRequestError(error) ||
           (error.response?.status >= 500 && error.response?.status < 600)
  },
  onRetry: (retryCount, error, requestConfig) => {
    console.warn(`Retry ${retryCount} for ${requestConfig.url}: ${error.message}`)
  }
})

// Request interceptor - добавляет таймстемп для кэшбастинга
api.interceptors.request.use(
  (config) => {
    // Добавляем timestamp для GET запросов чтобы избежать кэширования
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const { config, response, message } = error

    // Offline mode detection
    if (!navigator.onLine) {
      console.warn('Offline mode - request failed:', config?.url)
      error.isOffline = true
    }

    // Обработка различных типов ошибок
    if (response) {
      // Сервер вернул ошибку (4xx, 5xx)
      const status = response.status
      const errorData = response.data

      console.error(`API Error ${status}:`, errorData?.message || message)

      // Добавляем метаданные к ошибке
      error.isApiError = true
      error.statusCode = status
      error.errorMessage = errorData?.message || message
    } else if (error.request) {
      // Запрос был сделан, но ответ не получен (таймаут, CORS и т.д.)
      console.error('Network error:', message)
      error.isNetworkError = true
    }

    return Promise.reject(error)
  }
)

// Функция для проверки доступности API
export async function checkApiHealth() {
  try {
    const response = await api.get('/health', { timeout: 5000 })
    return response.data?.status === 'healthy'
  } catch {
    return false
  }
}

export default api

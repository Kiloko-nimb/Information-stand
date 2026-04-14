import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor для обработки ошибок
api.interceptors.response.use(
  response => response,
  error => {
    if (!navigator.onLine) {
      console.log('Offline mode - using cached data')
    }
    return Promise.reject(error)
  }
)

export default api

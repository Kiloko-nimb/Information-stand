import api from './api'

/**
 * Получить список новостей
 * @param {number} limit - Количество новостей
 * @returns {Promise} - Промис с данными новостей
 */
export async function fetchNews(limit = 3) {
  try {
    const response = await api.get(`/news/?limit=${limit}`)
    return response.data
  } catch (error) {
    console.error('Ошибка загрузки новостей:', error)
    throw error
  }
}

/**
 * Получить конкретную новость по ID
 * @param {number} id - ID новости
 * @returns {Promise} - Промис с данными новости
 */
export async function fetchNewsById(id) {
  try {
    const response = await api.get(`/news/${id}`)
    return response.data
  } catch (error) {
    console.error(`Ошибка загрузки новости ${id}:`, error)
    throw error
  }
}

/**
 * Принудительное обновление новостей с сайта
 * @returns {Promise} - Промис с результатом операции
 */
export async function refreshNews() {
  try {
    const response = await api.post('/news/refresh')
    return response.data
  } catch (error) {
    console.error('Ошибка обновления новостей:', error)
    throw error
  }
}

/**
 * Сохранить новости в localStorage для offline-режима
 * @param {Array} news - Массив новостей
 */
export function cacheNews(news) {
  try {
    localStorage.setItem('cached_news', JSON.stringify(news))
    localStorage.setItem('cached_news_timestamp', Date.now().toString())
  } catch (error) {
    console.error('Ошибка кэширования новостей:', error)
  }
}

/**
 * Получить закэшированные новости
 * @returns {Array|null} - Массив новостей или null
 */
export function getCachedNews() {
  try {
    const cached = localStorage.getItem('cached_news')
    if (cached) {
      return JSON.parse(cached)
    }
  } catch (error) {
    console.error('Ошибка чтения кэша новостей:', error)
  }
  return null
}

/**
 * Проверить, актуален ли кэш (не старше 24 часов)
 * @returns {boolean} - true если кэш актуален
 */
export function isCacheValid() {
  try {
    const timestamp = localStorage.getItem('cached_news_timestamp')
    if (!timestamp) return false

    const cacheAge = Date.now() - parseInt(timestamp)
    const maxAge = 24 * 60 * 60 * 1000 // 24 часа

    return cacheAge < maxAge
  } catch (error) {
    return false
  }
}

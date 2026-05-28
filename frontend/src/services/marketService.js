// Сервис для получения данных о рынке труда по специальностям
// через бэкенд (/api/v1/market/specialty).

const API_BASE = '/api/v1'

const cache = new Map()
const TTL_MS = 30 * 60 * 1000 // 30 минут на стороне клиента

export async function fetchMarketStats(query) {
  if (!query) return null

  const cached = cache.get(query)
  if (cached && Date.now() - cached.ts < TTL_MS) {
    return cached.data
  }

  try {
    const url = `${API_BASE}/market/specialty?query=${encodeURIComponent(query)}`
    const res = await fetch(url)
    if (!res.ok) return null
    const data = await res.json()
    cache.set(query, { ts: Date.now(), data })
    return data
  } catch (err) {
    console.warn('Failed to fetch market stats for', query, err)
    return null
  }
}

export function formatSalary(value) {
  if (!value) return null
  if (value >= 1000) {
    return `${(value / 1000).toFixed(0)} 000 ₽`
  }
  return `${value} ₽`
}

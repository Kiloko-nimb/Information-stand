import api from './api'

const TOKEN_KEY = 'admin_token'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
}

export function isAuthenticated() {
  return !!getToken()
}

export async function login(username, password) {
  const formData = new URLSearchParams()
  formData.append('username', username)
  formData.append('password', password)

  const response = await api.post('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
  setToken(response.data.access_token)
  return response.data
}

export async function setupAdmin(username, password) {
  const response = await api.post('/auth/setup', null, {
    params: { username, password }
  })
  return response.data
}

export async function getMe() {
  const response = await api.get('/auth/me', {
    headers: { Authorization: `Bearer ${getToken()}` }
  })
  return response.data
}

export async function logout() {
  removeToken()
}

// ── Admin CRUD helpers ──

function authHeaders() {
  return { Authorization: `Bearer ${getToken()}` }
}

// News
export async function adminListNews(skip = 0, limit = 50) {
  const { data } = await api.get(`/admin/news`, { params: { skip, limit }, headers: authHeaders() })
  return data
}

export async function adminCreateNews(payload) {
  const { data } = await api.post(`/admin/news`, payload, { headers: authHeaders() })
  return data
}

export async function adminUpdateNews(id, payload) {
  const { data } = await api.put(`/admin/news/${id}`, payload, { headers: authHeaders() })
  return data
}

export async function adminDeleteNews(id) {
  await api.delete(`/admin/news/${id}`, { headers: authHeaders() })
}

// Staff
export async function adminListStaff(skip = 0, limit = 100) {
  const { data } = await api.get(`/admin/staff`, { params: { skip, limit }, headers: authHeaders() })
  return data
}

export async function adminCreateStaff(payload) {
  const { data } = await api.post(`/admin/staff`, payload, { headers: authHeaders() })
  return data
}

export async function adminUpdateStaff(id, payload) {
  const { data } = await api.put(`/admin/staff/${id}`, payload, { headers: authHeaders() })
  return data
}

export async function adminDeleteStaff(id) {
  await api.delete(`/admin/staff/${id}`, { headers: authHeaders() })
}

// Rooms
export async function adminListRooms(skip = 0, limit = 100) {
  const { data } = await api.get(`/admin/rooms`, { params: { skip, limit }, headers: authHeaders() })
  return data
}

export async function adminCreateRoom(payload) {
  const { data } = await api.post(`/admin/rooms`, payload, { headers: authHeaders() })
  return data
}

export async function adminUpdateRoom(id, payload) {
  const { data } = await api.put(`/admin/rooms/${id}`, payload, { headers: authHeaders() })
  return data
}

export async function adminDeleteRoom(id) {
  await api.delete(`/admin/rooms/${id}`, { headers: authHeaders() })
}

export async function adminCleanupRooms() {
  const { data } = await api.delete(`/admin/rooms/invalid`, { headers: authHeaders() })
  return data
}

<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <Shield :size="22" />
        <h2>Админ</h2>
      </div>
      <nav class="sidebar-nav">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['nav-item', { active: currentTab === tab.key }]"
          @click="currentTab = tab.key"
        >
          <component :is="tab.icon" :size="18" class="nav-icon" />
          <span>{{ tab.label }}</span>
        </button>
      </nav>
      <div class="sidebar-footer">
        <button class="nav-item logout" @click="doLogout">
          <LogOut :size="18" class="nav-icon" />
          <span>Выход</span>
        </button>
        <router-link to="/" class="back-stand">← Стенд</router-link>
      </div>
    </aside>

    <!-- Main content -->
    <main class="admin-main">
      <!-- News -->
      <section v-if="currentTab === 'news'">
        <div class="section-header">
          <h2><Newspaper :size="22" class="section-icon" /> Новости</h2>
          <button class="btn-primary" @click="openNewsForm()"><Plus :size="16" /> Добавить</button>
        </div>
        <div class="data-table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Заголовок</th>
                <th>Иконка</th>
                <th>Дата</th>
                <th>Статус</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="n in newsList" :key="n.id">
                <td>{{ n.title }}</td>
                <td>{{ n.icon }}</td>
                <td>{{ formatDate(n.published_date) }}</td>
                <td><span :class="['badge', n.is_active ? 'badge-green' : 'badge-red']">
                  <component :is="n.is_active ? Eye : EyeOff" :size="12" />
                  {{ n.is_active ? 'Активна' : 'Скрыта' }}
                </span></td>
                <td class="actions">
                  <button @click="openNewsForm(n)" title="Редактировать"><Pencil :size="15" /></button>
                  <button @click="deleteNews(n.id)" title="Удалить"><Trash2 :size="15" /></button>
                </td>
              </tr>
              <tr v-if="!newsList.length"><td colspan="5" class="empty">Нет новостей</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Staff -->
      <section v-if="currentTab === 'staff'">
        <div class="section-header">
          <h2><Users :size="22" class="section-icon" /> Сотрудники</h2>
          <button class="btn-primary" @click="openStaffForm()"><Plus :size="16" /> Добавить</button>
        </div>
        <div class="data-table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>ФИО</th>
                <th>Должность</th>
                <th>Отдел</th>
                <th>Кабинет</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in staffList" :key="s.id">
                <td>{{ s.full_name }}</td>
                <td>{{ s.position || '—' }}</td>
                <td>{{ s.department || '—' }}</td>
                <td>{{ s.room_number || '—' }}</td>
                <td class="actions">
                  <button @click="openStaffForm(s)" title="Редактировать"><Pencil :size="15" /></button>
                  <button @click="deleteStaff(s.id)" title="Удалить"><Trash2 :size="15" /></button>
                </td>
              </tr>
              <tr v-if="!staffList.length"><td colspan="5" class="empty">Нет сотрудников</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Rooms -->
      <section v-if="currentTab === 'rooms'">
        <div class="section-header">
          <h2><School :size="22" class="section-icon" /> Кабинеты</h2>
          <button class="btn-primary" @click="openRoomForm()"><Plus :size="16" /> Добавить</button>
        </div>
        <div class="data-table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Номер</th>
                <th>Этаж</th>
                <th>Корпус</th>
                <th>Тип</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in roomList" :key="r.id">
                <td>{{ r.room_number }}</td>
                <td>{{ r.floor }}</td>
                <td>{{ r.building || '—' }}</td>
                <td>{{ r.room_type || '—' }}</td>
                <td class="actions">
                  <button @click="openRoomForm(r)" title="Редактировать"><Pencil :size="15" /></button>
                  <button @click="deleteRoom(r.id)" title="Удалить"><Trash2 :size="15" /></button>
                </td>
              </tr>
              <tr v-if="!roomList.length"><td colspan="5" class="empty">Нет кабинетов</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Analytics -->
      <section v-if="currentTab === 'analytics'">
        <div class="section-header">
          <h2><BarChart3 :size="22" class="section-icon" /> Аналитика посещений</h2>
        </div>
        <div v-if="stats" class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">{{ stats.total_visits }}</div>
            <div class="stat-label">Всего запросов</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ stats.visits_today }}</div>
            <div class="stat-label">Сегодня</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ stats.visits_week }}</div>
            <div class="stat-label">За неделю</div>
          </div>
        </div>
        <h3 style="margin-top:1.5rem">Популярные запросы</h3>
        <div class="data-table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Что искали</th>
                <th>Тип</th>
                <th>Запросов</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="q in humanReadableQueries" :key="q.label">
                <td>{{ q.label }}</td>
                <td><span class="badge badge-blue">{{ q.type }}</span></td>
                <td>{{ q.count }}</td>
              </tr>
              <tr v-if="!humanReadableQueries.length"><td colspan="3" class="empty">Нет данных</td></tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <!-- Modal overlay -->
    <div v-if="modalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button class="modal-close" @click="closeModal"><X :size="18" /></button>
        </div>
        <form @submit.prevent="saveModal" class="modal-body">
          <div v-for="field in modalFields" :key="field.key" class="field">
            <label>{{ field.label }}</label>
            <input
              v-if="field.type !== 'select' && field.type !== 'textarea'"
              v-model="modalData[field.key]"
              :type="field.type || 'text'"
              :required="field.required"
              :step="field.step"
            />
            <textarea
              v-else-if="field.type === 'textarea'"
              v-model="modalData[field.key]"
              :required="field.required"
              rows="3"
            />
            <select v-else v-model="modalData[field.key]">
              <option v-for="opt in field.options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="closeModal">Отмена</button>
            <button type="submit" class="btn-primary" :disabled="saving">{{ saving ? 'Сохранение...' : 'Сохранить' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Shield, Newspaper, Users, School, BarChart3, LogOut, Plus,
  Pencil, Trash2, X, Eye, EyeOff
} from 'lucide-vue-next'
import {
  isAuthenticated, logout as doLogoutService, getToken,
  adminListNews, adminCreateNews, adminUpdateNews, adminDeleteNews,
  adminListStaff, adminCreateStaff, adminUpdateStaff, adminDeleteStaff,
  adminListRooms, adminCreateRoom, adminUpdateRoom, adminDeleteRoom
} from '../../services/adminService'
import api from '../../services/api'

const router = useRouter()

const tabs = [
  { key: 'news', label: 'Новости', icon: Newspaper },
  { key: 'staff', label: 'Сотрудники', icon: Users },
  { key: 'rooms', label: 'Кабинеты', icon: School },
  { key: 'analytics', label: 'Аналитика', icon: BarChart3 },
]
const currentTab = ref('news')

// Data lists
const newsList = ref([])
const staffList = ref([])
const roomList = ref([])
const stats = ref(null)

const humanReadableQueries = computed(() => {
  if (!stats.value?.top_pages) return []
  return stats.value.top_pages.map(q => {
    const ep = q.endpoint
    let label = ''
    let type = 'Другое'
    if (ep.includes('/schedule/group/')) {
      label = decodeURIComponent(ep.split('/schedule/group/')[1] || '')
      type = 'Группа'
    } else if (ep.includes('/schedule/teacher/')) {
      label = decodeURIComponent(ep.split('/schedule/teacher/')[1] || '')
      type = 'Преподаватель'
    } else if (ep.includes('/schedule/room/')) {
      label = 'Кабинет ' + decodeURIComponent(ep.split('/schedule/room/')[1] || '')
      type = 'Кабинет'
    } else if (ep.includes('/schedule/groups')) {
      label = 'Список групп'
      type = 'Справочник'
    } else if (ep.includes('/schedule/teachers')) {
      label = 'Список преподавателей'
      type = 'Справочник'
    } else if (ep.includes('/schedule/rooms')) {
      label = 'Список кабинетов'
      type = 'Справочник'
    } else if (ep.includes('/schedule/now')) {
      label = 'Текущие занятия'
      type = 'Главная'
    } else if (ep.includes('/schedule/bells')) {
      label = 'Звонки'
      type = 'Справочник'
    } else if (ep.includes('/news')) {
      label = 'Новости'
      type = 'Контент'
    } else if (ep.includes('/staff')) {
      label = 'Сотрудники'
      type = 'Контент'
    } else {
      label = ep.replace('/api/v1', '')
    }
    return { label, type, count: q.hit_count }
  })
})

// Modal state
const modalOpen = ref(false)
const modalTitle = ref('')
const modalFields = ref([])
const modalData = reactive({})
const modalType = ref('')  // 'news' | 'staff' | 'room'
const modalEditId = ref(null)
const saving = ref(false)

onMounted(() => {
  if (!isAuthenticated()) {
    router.replace('/admin/login')
    return
  }
  loadData()
})

watch(currentTab, () => loadData())

async function loadData() {
  if (currentTab.value === 'news') newsList.value = await adminListNews()
  if (currentTab.value === 'staff') staffList.value = await adminListStaff()
  if (currentTab.value === 'rooms') roomList.value = await adminListRooms()
  if (currentTab.value === 'analytics') {
    try {
      const resp = await api.get('/admin/analytics/stats', { headers: { Authorization: `Bearer ${getToken()}` } })
      stats.value = resp.data
    } catch { stats.value = null }
  }
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('ru-RU')
}

function doLogout() {
  doLogoutService()
  router.replace('/admin/login')
}

// ── News ──
const NEWS_FIELDS = [
  { key: 'title', label: 'Заголовок', required: true },
  { key: 'description', label: 'Описание', type: 'textarea' },
  { key: 'icon', label: 'Иконка' },
  { key: 'source_url', label: 'Ссылка на источник' },
  { key: 'is_active', label: 'Активна', type: 'select', options: [{ value: true, label: 'Да' }, { value: false, label: 'Нет' }] },
]

function openNewsForm(item = null) {
  modalType.value = 'news'
  modalEditId.value = item?.id || null
  modalTitle.value = item ? 'Редактировать новость' : 'Новая новость'
  modalFields.value = NEWS_FIELDS
  Object.keys(modalData).forEach(k => delete modalData[k])
  if (item) {
    Object.assign(modalData, { title: item.title, description: item.description || '', icon: item.icon, source_url: item.source_url || '', is_active: item.is_active })
  } else {
    Object.assign(modalData, { title: '', description: '', icon: '📰', source_url: '', is_active: true })
  }
  modalOpen.value = true
}

async function deleteNews(id) {
  if (!confirm('Удалить новость?')) return
  await adminDeleteNews(id)
  newsList.value = await adminListNews()
}

// ── Staff ──
const STAFF_FIELDS = [
  { key: 'full_name', label: 'ФИО', required: true },
  { key: 'position', label: 'Должность' },
  { key: 'department', label: 'Отдел' },
  { key: 'room_number', label: 'Кабинет' },
  { key: 'email', label: 'Email' },
  { key: 'phone', label: 'Телефон' },
]

function openStaffForm(item = null) {
  modalType.value = 'staff'
  modalEditId.value = item?.id || null
  modalTitle.value = item ? 'Редактировать сотрудника' : 'Новый сотрудник'
  modalFields.value = STAFF_FIELDS
  Object.keys(modalData).forEach(k => delete modalData[k])
  if (item) {
    Object.assign(modalData, { full_name: item.full_name, position: item.position || '', department: item.department || '', room_number: item.room_number || '', email: item.email || '', phone: item.phone || '' })
  } else {
    Object.assign(modalData, { full_name: '', position: '', department: '', room_number: '', email: '', phone: '' })
  }
  modalOpen.value = true
}

async function deleteStaff(id) {
  if (!confirm('Удалить сотрудника?')) return
  await adminDeleteStaff(id)
  staffList.value = await adminListStaff()
}

// ── Rooms ──
const ROOM_FIELDS = [
  { key: 'room_number', label: 'Номер кабинета', required: true },
  { key: 'floor', label: 'Этаж', type: 'number', required: true, step: '1' },
  { key: 'building', label: 'Корпус' },
  { key: 'room_type', label: 'Тип' },
]

function openRoomForm(item = null) {
  modalType.value = 'room'
  modalEditId.value = item?.id || null
  modalTitle.value = item ? 'Редактировать кабинет' : 'Новый кабинет'
  modalFields.value = ROOM_FIELDS
  Object.keys(modalData).forEach(k => delete modalData[k])
  if (item) {
    Object.assign(modalData, { room_number: item.room_number, floor: item.floor, building: item.building || '', room_type: item.room_type || '' })
  } else {
    Object.assign(modalData, { room_number: '', floor: 2, building: '', room_type: '' })
  }
  modalOpen.value = true
}

async function deleteRoom(id) {
  if (!confirm('Удалить кабинет?')) return
  await adminDeleteRoom(id)
  roomList.value = await adminListRooms()
}

// ── Modal save ──
function closeModal() {
  modalOpen.value = false
}

async function saveModal() {
  saving.value = true
  try {
    const payload = { ...modalData }
    // Convert numeric fields
    if (modalType.value === 'room' && payload.floor) payload.floor = parseInt(payload.floor)
    if (modalType.value === 'news' && typeof payload.is_active === 'string') payload.is_active = payload.is_active === 'true'

    if (modalType.value === 'news') {
      if (modalEditId.value) await adminUpdateNews(modalEditId.value, payload)
      else await adminCreateNews(payload)
      newsList.value = await adminListNews()
    } else if (modalType.value === 'staff') {
      if (modalEditId.value) await adminUpdateStaff(modalEditId.value, payload)
      else await adminCreateStaff(payload)
      staffList.value = await adminListStaff()
    } else if (modalType.value === 'room') {
      if (modalEditId.value) await adminUpdateRoom(modalEditId.value, payload)
      else await adminCreateRoom(payload)
      roomList.value = await adminListRooms()
    }
    closeModal()
  } catch (e) {
    alert(e.response?.data?.detail || 'Ошибка сохранения')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--surface);
}

/* Sidebar */
.sidebar {
  width: 220px;
  background: var(--surface-elevated, #1e293b);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
  flex-shrink: 0;
}
.sidebar-header {
  padding: 0 1.2rem 1rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.sidebar-header h2 {
  font-size: 1.1rem;
}
.sidebar-nav {
  flex: 1;
  padding: 0.5rem 0;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  width: 100%;
  padding: 0.7rem 1.2rem;
  border: none;
  background: none;
  color: var(--text-muted);
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  text-align: left;
}
.nav-item:hover {
  background: rgba(255,255,255,0.05);
  color: var(--text);
}
.nav-item.active {
  background: rgba(99,102,241,0.15);
  color: var(--accent, #6366f1);
  font-weight: 600;
}
.nav-icon {
  font-size: 1.1rem;
  width: 1.4rem;
  text-align: center;
}
.sidebar-footer {
  padding: 0.5rem 0;
  border-top: 1px solid var(--border);
}
.logout {
  color: #f87171;
}
.back-stand {
  display: block;
  padding: 0.5rem 1.2rem;
  color: var(--text-muted);
  font-size: 0.85rem;
  text-decoration: none;
}
.back-stand:hover {
  color: var(--text);
}

/* Main */
.admin-main {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}
.section-header h2 {
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.section-icon {
  flex-shrink: 0;
}

/* Table */
.data-table-wrap {
  overflow-x: auto;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
.data-table th,
.data-table td {
  padding: 0.65rem 0.9rem;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
.data-table th {
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.data-table tr:hover td {
  background: rgba(255,255,255,0.02);
}
.actions {
  white-space: nowrap;
}
.actions button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  transition: background 0.15s;
}
.actions button:hover {
  background: rgba(255,255,255,0.08);
}
.empty {
  text-align: center;
  color: var(--text-muted);
  padding: 2rem !important;
}

/* Badges */
.badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}
.badge-green {
  background: rgba(34,197,94,0.15);
  color: #4ade80;
}
.badge-red {
  background: rgba(239,68,68,0.15);
  color: #f87171;
}
.badge-blue {
  background: rgba(99,102,241,0.12);
  color: #6366f1;
}
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

/* Buttons */
.btn-primary {
  padding: 0.55rem 1.2rem;
  background: var(--accent-gradient, linear-gradient(135deg, #6366f1, #8b5cf6));
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-primary:hover:not(:disabled) { opacity: 0.9; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-secondary {
  padding: 0.55rem 1.2rem;
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-secondary:hover { background: rgba(255,255,255,0.05); }

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}
.modal-card {
  background: var(--surface-elevated, #1e293b);
  border: 1px solid var(--border);
  border-radius: 12px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 16px 48px rgba(0,0,0,0.4);
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid var(--border);
}
.modal-header h3 {
  font-size: 1.1rem;
}
.modal-close {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}
.modal-close:hover { background: rgba(255,255,255,0.08); }
.modal-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.field label {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 500;
}
.field input,
.field textarea,
.field select {
  padding: 0.6rem 0.9rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
  font-size: 0.95rem;
  transition: border-color 0.2s;
  font-family: inherit;
}
.field input:focus,
.field textarea:focus,
.field select:focus {
  outline: none;
  border-color: var(--accent, #6366f1);
}
.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}
.stat-card {
  background: var(--surface-elevated, #1e293b);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.2rem;
  text-align: center;
}
.stat-value {
  font-size: 2rem;
  font-weight: 800;
  background: var(--accent-gradient, linear-gradient(135deg, #6366f1, #8b5cf6));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 0.3rem;
}

/* Responsive */
@media (max-width: 768px) {
  .admin-layout { flex-direction: column; }
  .sidebar {
    width: 100%;
    flex-direction: row;
    overflow-x: auto;
    padding: 0.5rem;
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
  .sidebar-header { display: none; }
  .sidebar-nav { display: flex; gap: 0; padding: 0; }
  .sidebar-footer { display: none; }
  .nav-item { padding: 0.5rem 0.8rem; font-size: 0.85rem; }
  .admin-main { padding: 1rem; }
}
</style>

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
          <button class="btn-primary" @click="openNewsForm()" title="Создать новую новость для стенда">
            <Plus :size="16" /> Добавить
          </button>
        </div>
        <p class="section-hint">
          <Info :size="14" /> Эти новости посетители видят на главной странице стенда. <strong>Активная</strong>
          новость публикуется, <strong>скрытая</strong> — остаётся в базе, но не показывается.
        </p>
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
                  <button @click="openNewsForm(n)" title="Изменить эту новость"><Pencil :size="15" /></button>
                  <button @click="deleteNews(n)" title="Удалить навсегда" class="action-danger"><Trash2 :size="15" /></button>
                </td>
              </tr>
              <tr v-if="!newsList.length"><td colspan="5" class="empty">
                Пока нет ни одной новости. Нажмите <strong>«Добавить»</strong>, чтобы создать первую.
              </td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Staff -->
      <section v-if="currentTab === 'staff'">
        <div class="section-header">
          <h2><Users :size="22" class="section-icon" /> Сотрудники</h2>
          <button class="btn-primary" @click="openStaffForm()" title="Добавить преподавателя или сотрудника">
            <Plus :size="16" /> Добавить
          </button>
        </div>
        <p class="section-hint">
          <Info :size="14" /> Справочник сотрудников для поиска на стенде: студенты и гости смогут найти
          преподавателя по ФИО и увидеть его кабинет. Чем полнее данные, тем полезнее поиск.
        </p>
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
                  <button @click="openStaffForm(s)" title="Изменить данные сотрудника"><Pencil :size="15" /></button>
                  <button @click="deleteStaff(s)" title="Удалить сотрудника" class="action-danger"><Trash2 :size="15" /></button>
                </td>
              </tr>
              <tr v-if="!staffList.length"><td colspan="5" class="empty">
                Пока нет сотрудников. Нажмите <strong>«Добавить»</strong>, чтобы внести первого.
              </td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Rooms -->
      <section v-if="currentTab === 'rooms'">
        <div class="section-header">
          <h2><School :size="22" class="section-icon" /> Кабинеты</h2>
          <div class="header-actions">
            <button class="btn-primary" @click="openRoomForm()" title="Добавить новый кабинет в справочник">
              <Plus :size="16" /> Добавить
            </button>
            <button class="btn-secondary" @click="confirmCleanupRooms()"
                    title="Удалить кабинеты с невалидными номерами (попавшие в БД из расписания)">
              <Eraser :size="16" /> Очистить мусор
            </button>
          </div>
        </div>
        <p class="section-hint">
          <Info :size="14" /> Справочник аудиторий для поиска на стенде и привязки сотрудников.
          Кнопка <strong>«Очистить мусор»</strong> удалит записи, которые случайно попали в базу при
          импорте расписания (например <code>Ауд.</code>, <code>1С:Предприятие</code>).
          Нормальные кабинеты (305, К-1, Сп1, Дистанционно) она не трогает.
        </p>
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
                  <button @click="openRoomForm(r)" title="Изменить этот кабинет"><Pencil :size="15" /></button>
                  <button @click="deleteRoom(r)" title="Удалить кабинет из справочника" class="action-danger"><Trash2 :size="15" /></button>
                </td>
              </tr>
              <tr v-if="!roomList.length"><td colspan="5" class="empty">
                Пока нет кабинетов. Нажмите <strong>«Добавить»</strong>, чтобы заполнить справочник.
              </td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Analytics -->
      <section v-if="currentTab === 'analytics'">
        <div class="section-header">
          <h2><BarChart3 :size="22" class="section-icon" /> Аналитика посещений</h2>
        </div>
        <p class="section-hint">
          <Info :size="14" /> Показывает, какими разделами стенда пользуются чаще всего и что ищут. Числа
          помогут решить, какие секции стенда выводить на видное место, а какие убрать.
        </p>
        <div v-if="stats" class="stats-grid">
          <div class="stat-card" title="Общее число обращений к АПИ стенда за всё время">
            <div class="stat-value">{{ stats.total_visits }}</div>
            <div class="stat-label">Всего запросов</div>
            <div class="stat-sub">за всё время</div>
          </div>
          <div class="stat-card" title="Запросы пользователей за текущий день">
            <div class="stat-value">{{ stats.visits_today }}</div>
            <div class="stat-label">Сегодня</div>
            <div class="stat-sub">с 00:00</div>
          </div>
          <div class="stat-card" title="Запросы за последние 7 дней">
            <div class="stat-value">{{ stats.visits_week }}</div>
            <div class="stat-label">За неделю</div>
            <div class="stat-sub">последние 7 дней</div>
          </div>
        </div>
        <h3 class="queries-heading">Популярные запросы</h3>
        <p class="section-hint compact">
          Что именно искали на стенде: группы, преподавателей, кабинеты.
        </p>
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
          <button class="modal-close" @click="closeModal" title="Закрыть без сохранения"><X :size="18" /></button>
        </div>
        <form @submit.prevent="saveModal" class="modal-body">
          <p v-if="modalIntro" class="modal-intro">
            <Info :size="14" /> {{ modalIntro }}
          </p>
          <div v-for="field in modalFields" :key="field.key" class="field">
            <label>
              {{ field.label }}
              <span v-if="field.required" class="required-mark" title="Обязательное поле">*</span>
            </label>
            <input
              v-if="field.type !== 'select' && field.type !== 'textarea'"
              v-model="modalData[field.key]"
              :type="field.type || 'text'"
              :required="field.required"
              :step="field.step"
              :placeholder="field.placeholder || ''"
            />
            <textarea
              v-else-if="field.type === 'textarea'"
              v-model="modalData[field.key]"
              :required="field.required"
              :placeholder="field.placeholder || ''"
              rows="3"
            />
            <select v-else v-model="modalData[field.key]">
              <option v-for="opt in field.options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
            <p v-if="field.hint" class="field-hint">{{ field.hint }}</p>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="closeModal">Отмена</button>
            <button type="submit" class="btn-primary" :disabled="saving">{{ saving ? 'Сохранение...' : 'Сохранить' }}</button>
          </div>
          <p v-if="formError" class="form-error">{{ formError }}</p>
        </form>
      </div>
    </div>

    <!-- Confirmation overlay (Да/Нет вместо браузерного confirm) -->
    <div v-if="confirmState.open" class="modal-overlay" @click.self="cancelConfirm">
      <div class="modal-card confirm-card">
        <div class="modal-header">
          <h3>
            <AlertTriangle :size="20" class="warn-icon" />
            {{ confirmState.title }}
          </h3>
          <button class="modal-close" @click="cancelConfirm" title="Отменить"><X :size="18" /></button>
        </div>
        <div class="modal-body">
          <p class="confirm-message" v-html="confirmState.message" />
          <p v-if="confirmState.detail" class="confirm-detail">{{ confirmState.detail }}</p>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="cancelConfirm">Отмена</button>
            <button type="button" class="btn-danger" @click="acceptConfirm">
              {{ confirmState.confirmLabel || 'Да, удалить' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast уведомления -->
    <transition name="toast-fade">
      <div v-if="toast.visible" :class="['toast', `toast-${toast.kind}`]" role="status">
        <component :is="toast.kind === 'success' ? CheckCircle2 : (toast.kind === 'error' ? AlertTriangle : Info)" :size="18" />
        <span>{{ toast.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Shield, Newspaper, Users, School, BarChart3, LogOut, Plus,
  Pencil, Trash2, X, Eye, EyeOff, Info, Eraser, AlertTriangle, CheckCircle2
} from 'lucide-vue-next'
import {
  isAuthenticated, logout as doLogoutService, getToken,
  adminListNews, adminCreateNews, adminUpdateNews, adminDeleteNews,
  adminListStaff, adminCreateStaff, adminUpdateStaff, adminDeleteStaff,
  adminListRooms, adminCreateRoom, adminUpdateRoom, adminDeleteRoom, adminCleanupRooms
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
const modalIntro = ref('')
const modalFields = ref([])
const modalData = reactive({})
const modalType = ref('')  // 'news' | 'staff' | 'room'
const modalEditId = ref(null)
const saving = ref(false)
const formError = ref('')

// Toast state
const toast = reactive({
  visible: false,
  message: '',
  kind: 'success', // 'success' | 'error' | 'info'
  timer: null,
})
function showToast(message, kind = 'success', durationMs = 3500) {
  if (toast.timer) clearTimeout(toast.timer)
  toast.message = message
  toast.kind = kind
  toast.visible = true
  toast.timer = setTimeout(() => { toast.visible = false }, durationMs)
}

// Confirmation modal state (заменяет браузерный confirm)
const confirmState = reactive({
  open: false,
  title: '',
  message: '',
  detail: '',
  confirmLabel: '',
  resolve: null,
})
function askConfirm({ title, message, detail = '', confirmLabel = 'Да, удалить' }) {
  return new Promise((resolve) => {
    confirmState.title = title
    confirmState.message = message
    confirmState.detail = detail
    confirmState.confirmLabel = confirmLabel
    confirmState.resolve = resolve
    confirmState.open = true
  })
}
function acceptConfirm() {
  confirmState.open = false
  if (confirmState.resolve) confirmState.resolve(true)
  confirmState.resolve = null
}
function cancelConfirm() {
  confirmState.open = false
  if (confirmState.resolve) confirmState.resolve(false)
  confirmState.resolve = null
}

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
  {
    key: 'title', label: 'Заголовок', required: true,
    placeholder: 'Например: «День открытых дверей в ККРИТ 14 мая»',
    hint: 'Главная строка, которую увидят на стенде. 1–2 коротких предложения.',
  },
  {
    key: 'description', label: 'Описание', type: 'textarea',
    placeholder: 'Краткий текст новости — будет виден при открытии карточки…',
    hint: 'Не обязательно. 1–3 абзаца. Подробности лучше писать именно здесь.',
  },
  {
    key: 'icon', label: 'Иконка',
    placeholder: '📰',
    hint: 'Один эмодзи рядом с заголовком. Например: 🎓 (выпуск), 📅 (событие), 🏢 (колледж), ⚠️ (важно).',
  },
  {
    key: 'source_url', label: 'Ссылка на источник',
    placeholder: 'https://kraskrit.ru/news/...',
    hint: 'Необязательно. Если заполнить, в QR-коде на стенде будет ссылка «Подробнее».',
  },
  {
    key: 'is_active', label: 'Статус',
    type: 'select',
    options: [{ value: true, label: 'Активна (видна на стенде)' }, { value: false, label: 'Скрыта (в архиве)' }],
    hint: '«Скрытая» новость остаётся в базе и её можно вернуть, но посетители её не видят.',
  },
]

function openNewsForm(item = null) {
  formError.value = ''
  modalType.value = 'news'
  modalEditId.value = item?.id || null
  modalTitle.value = item ? 'Редактировать новость' : 'Новая новость'
  modalIntro.value = item
    ? 'Изменения сразу появятся на главной стенда.'
    : 'Новая активная новость появится на стенде в блоке «Новости ККРИТ».'
  modalFields.value = NEWS_FIELDS
  Object.keys(modalData).forEach(k => delete modalData[k])
  if (item) {
    Object.assign(modalData, { title: item.title, description: item.description || '', icon: item.icon, source_url: item.source_url || '', is_active: item.is_active })
  } else {
    Object.assign(modalData, { title: '', description: '', icon: '📰', source_url: '', is_active: true })
  }
  modalOpen.value = true
}

async function deleteNews(item) {
  const ok = await askConfirm({
    title: 'Удалить новость?',
    message: `Новость <strong>«${escapeHtml(item.title)}»</strong> будет удалена навсегда.`,
    detail: 'Если нужно временно спрятать новость со стенда, лучше измените её статус на «Скрыта» — так её потом можно вернуть.',
  })
  if (!ok) return
  try {
    await adminDeleteNews(item.id)
    newsList.value = await adminListNews()
    showToast('Новость удалена', 'success')
  } catch (e) {
    showToast('Не удалось удалить новость', 'error')
  }
}

function escapeHtml(str) {
  return String(str ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]))
}

// ── Staff ──
const STAFF_FIELDS = [
  {
    key: 'full_name', label: 'ФИО', required: true,
    placeholder: 'Иванов Иван Иванович',
    hint: 'Полностью — именно так поиск на стенде и в расписании будет искать человека.',
  },
  {
    key: 'position', label: 'Должность',
    placeholder: 'Например: Преподаватель информатики',
    hint: 'Покажется в карточке сотрудника на стенде.',
  },
  {
    key: 'department', label: 'Отдел',
    placeholder: 'Например: ЦК информационных технологий',
    hint: 'Подразделение или кафедра. Не обязательно.',
  },
  {
    key: 'room_number', label: 'Кабинет',
    placeholder: '305',
    hint: 'Номер из справочника кабинетов: 305, К-1, Сп1, Дистанционно.',
  },
  {
    key: 'email', label: 'Email',
    placeholder: 'ivanov@kraskrit.ru',
    hint: 'Необязательно. Активная ссылка на стенде не появится — имейте в виду.',
  },
  {
    key: 'phone', label: 'Телефон',
    placeholder: '+7 (391) 123-45-67',
    hint: 'Необязательно. Используйте внутренний номер, если есть.',
  },
]

function openStaffForm(item = null) {
  formError.value = ''
  modalType.value = 'staff'
  modalEditId.value = item?.id || null
  modalTitle.value = item ? 'Редактировать сотрудника' : 'Новый сотрудник'
  modalIntro.value = 'Обязательно только ФИО. Чем больше полей заполнено, тем легче найти человека на стенде.'
  modalFields.value = STAFF_FIELDS
  Object.keys(modalData).forEach(k => delete modalData[k])
  if (item) {
    Object.assign(modalData, { full_name: item.full_name, position: item.position || '', department: item.department || '', room_number: item.room_number || '', email: item.email || '', phone: item.phone || '' })
  } else {
    Object.assign(modalData, { full_name: '', position: '', department: '', room_number: '', email: '', phone: '' })
  }
  modalOpen.value = true
}

async function deleteStaff(item) {
  const ok = await askConfirm({
    title: 'Удалить сотрудника?',
    message: `Сотрудник <strong>«${escapeHtml(item.full_name)}»</strong> будет удалён из справочника.`,
    detail: 'На отображении расписания это не скажется, но в поиске по Сотрудникам человек больше не найдётся.',
  })
  if (!ok) return
  try {
    await adminDeleteStaff(item.id)
    staffList.value = await adminListStaff()
    showToast('Сотрудник удалён', 'success')
  } catch (e) {
    showToast('Не удалось удалить сотрудника', 'error')
  }
}

// ── Rooms ──
const ROOM_FIELDS = [
  {
    key: 'room_number', label: 'Номер кабинета', required: true,
    placeholder: '305, К-1, Сп1, Дистанционно',
    hint: 'Будет показываться в расписании и поиске. Для спортзала используйте «Сп1», для корпуса — «К-1».',
  },
  {
    key: 'floor', label: 'Этаж', type: 'number', required: true, step: '1',
    placeholder: '2',
    hint: 'Число от 0 до 5. Для специальных помещений («Дистанционно») обычно ставят 0.',
  },
  {
    key: 'building', label: 'Корпус',
    placeholder: 'Главный',
    hint: 'Необязательно. Главный / Спортивный / Лабораторный и т.п.',
  },
  {
    key: 'room_type', label: 'Тип',
    placeholder: 'Лекционная',
    hint: 'Необязательно. Лекционная / Лаборатория / Актовый зал / Спортзал.',
  },
]

function openRoomForm(item = null) {
  formError.value = ''
  modalType.value = 'room'
  modalEditId.value = item?.id || null
  modalTitle.value = item ? 'Редактировать кабинет' : 'Новый кабинет'
  modalIntro.value = 'Аудитории обычно импортируются вместе с расписанием. Ручное добавление нужно только для особых помещений (спортзал, актовый).'
  modalFields.value = ROOM_FIELDS
  Object.keys(modalData).forEach(k => delete modalData[k])
  if (item) {
    Object.assign(modalData, { room_number: item.room_number, floor: item.floor, building: item.building || '', room_type: item.room_type || '' })
  } else {
    Object.assign(modalData, { room_number: '', floor: 2, building: '', room_type: '' })
  }
  modalOpen.value = true
}

async function deleteRoom(item) {
  const ok = await askConfirm({
    title: 'Удалить кабинет?',
    message: `Кабинет <strong>«${escapeHtml(item.room_number)}»</strong> будет удалён из справочника.`,
    detail: 'При следующем импорте расписания он может создаться заново автоматически.',
  })
  if (!ok) return
  try {
    await adminDeleteRoom(item.id)
    roomList.value = await adminListRooms()
    showToast('Кабинет удалён', 'success')
  } catch (e) {
    showToast('Не удалось удалить кабинет', 'error')
  }
}

async function confirmCleanupRooms() {
  const ok = await askConfirm({
    title: 'Очистить мусор в кабинетах?',
    message: 'Будут удалены все записи с невалидными номерами — в основном те, что случайно попали в базу из PDF/Excel расписания.',
    detail: 'Реальные номера (305, К-1, Сп1, Дистанционно и т.п.) останутся. Действие безопасно запускать повторно — при следующем импорте расписания мусор может появиться снова.',
    confirmLabel: 'Да, очистить',
  })
  if (!ok) return
  try {
    const resp = await adminCleanupRooms()
    roomList.value = await adminListRooms()
    const count = resp?.deleted ?? 0
    if (count === 0) {
      showToast('Мусорных кабинетов не найдено — справочник чист', 'info', 4500)
    } else {
      showToast(`Удалено ${count} ${pluralize(count, 'запись', 'записи', 'записей')}`, 'success', 4500)
    }
  } catch (e) {
    showToast('Не удалось очистить справочник', 'error')
  }
}

function pluralize(n, one, few, many) {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return one
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return few
  return many
}

// ── Modal save ──
function closeModal() {
  formError.value = ''
  modalOpen.value = false
}

async function saveModal() {
  formError.value = ''
  saving.value = true
  try {
    const payload = { ...modalData }
    // Convert numeric fields
    if (modalType.value === 'room' && payload.floor) payload.floor = parseInt(payload.floor)
    if (modalType.value === 'news' && typeof payload.is_active === 'string') payload.is_active = payload.is_active === 'true'

    const isEdit = !!modalEditId.value
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
    showToast(isEdit ? 'Изменения сохранены' : 'Запись добавлена', 'success')
    closeModal()
  } catch (e) {
    const detail = e?.response?.data?.detail
    if (Array.isArray(detail)) {
      formError.value = detail.map((x) => x?.msg).filter(Boolean).join('; ') || 'Ошибка валидации'
    } else if (typeof detail === 'string') {
      formError.value = detail
    } else {
      formError.value = 'Ошибка сохранения'
    }
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
.section-hint {
  margin: -0.4rem 0 1.2rem;
  padding: 0.7rem 0.9rem 0.7rem 2.4rem;
  background: rgba(99, 102, 241, 0.07);
  border: 1px solid rgba(99, 102, 241, 0.18);
  border-radius: 8px;
  color: var(--text-muted);
  font-size: 0.92rem;
  line-height: 1.5;
  position: relative;
}
.section-hint :deep(svg) {
  position: absolute;
  left: 0.85rem;
  top: 0.95rem;
  color: var(--accent, #6366f1);
}
.section-hint code {
  background: rgba(255,255,255,0.08);
  padding: 0.05rem 0.32rem;
  border-radius: 4px;
  font-size: 0.85em;
}
.section-hint.compact {
  padding: 0.5rem 0.8rem;
  font-size: 0.85rem;
  margin: 0.4rem 0 1rem;
}
.header-actions {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}
.queries-heading {
  margin-top: 1.5rem;
  font-size: 1rem;
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
  display: flex;
  gap: 0.3rem;
  justify-content: flex-end;
}
.actions button {
  background: none;
  border: 1px solid transparent;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.45rem 0.6rem;
  border-radius: 6px;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
  color: var(--text-muted);
  min-width: 38px;
  min-height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.actions button:hover {
  background: rgba(255,255,255,0.08);
  color: var(--text);
}
.actions button.action-danger:hover {
  background: rgba(239, 68, 68, 0.12);
  color: #f87171;
  border-color: rgba(239, 68, 68, 0.3);
}
.empty {
  text-align: center;
  color: var(--text-muted);
  padding: 2rem !important;
  line-height: 1.5;
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
  transition: background 0.15s, color 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.btn-secondary:hover { background: rgba(255,255,255,0.05); color: var(--text); }
.btn-primary,
.btn-secondary,
.btn-danger {
  min-height: 42px;
}
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.btn-danger {
  padding: 0.55rem 1.2rem;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-danger:hover { opacity: 0.9; }

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
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}
.required-mark {
  color: #f87171;
  font-weight: 700;
}
.field-hint {
  margin: 0.1rem 0 0;
  font-size: 0.78rem;
  color: var(--text-muted);
  line-height: 1.4;
  opacity: 0.85;
}
.modal-intro {
  margin: 0;
  padding: 0.65rem 0.85rem 0.65rem 2.2rem;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 8px;
  color: var(--text-muted);
  font-size: 0.85rem;
  line-height: 1.45;
  position: relative;
}
.modal-intro :deep(svg) {
  position: absolute;
  left: 0.7rem;
  top: 0.85rem;
  color: var(--accent, #6366f1);
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
  justify-content: flex-end;
  gap: 0.6rem;
  margin-top: 0.8rem;
}
.form-error {
  margin-top: 0.7rem;
  color: #ef4444;
  font-size: 0.9rem;
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
  font-size: 0.95rem;
  color: var(--text);
  margin-top: 0.3rem;
  font-weight: 500;
}
.stat-sub {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-top: 0.1rem;
  opacity: 0.8;
}
.stat-card {
  cursor: help;
}

/* Confirmation modal */
.confirm-card {
  max-width: 460px;
}
.confirm-card .modal-header h3 {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.warn-icon {
  color: #f59e0b;
  flex-shrink: 0;
}
.confirm-message {
  margin: 0;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--text);
}
.confirm-detail {
  margin: 0;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--text-muted);
  padding: 0.6rem 0.8rem;
  background: rgba(255,255,255,0.04);
  border-left: 3px solid var(--accent, #6366f1);
  border-radius: 4px;
}

/* Toast */
.toast {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.85rem 1.1rem;
  border-radius: 10px;
  font-size: 0.92rem;
  font-weight: 500;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  z-index: 10000;
  max-width: 360px;
  border: 1px solid var(--border);
  background: var(--surface-elevated, #1e293b);
  color: var(--text);
}
.toast :deep(svg) { flex-shrink: 0; }
.toast-success {
  border-color: rgba(34,197,94,0.4);
  background: linear-gradient(180deg, rgba(34,197,94,0.18), rgba(34,197,94,0.06)), var(--surface-elevated, #1e293b);
}
.toast-success :deep(svg) { color: #4ade80; }
.toast-error {
  border-color: rgba(239,68,68,0.45);
  background: linear-gradient(180deg, rgba(239,68,68,0.2), rgba(239,68,68,0.06)), var(--surface-elevated, #1e293b);
}
.toast-error :deep(svg) { color: #f87171; }
.toast-info {
  border-color: rgba(99,102,241,0.4);
  background: linear-gradient(180deg, rgba(99,102,241,0.18), rgba(99,102,241,0.06)), var(--surface-elevated, #1e293b);
}
.toast-info :deep(svg) { color: #818cf8; }
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: transform 0.25s ease, opacity 0.25s ease;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
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

<template>
  <div class="home" :class="{ 'accessibility-active': accessibilityMode }">
    <div class="top-section">
      <div class="bento-hero">
        <div class="bento-card bento-welcome">
          <span class="bento-eyebrow">Добро пожаловать в</span>
          <h1>Красноярский колледж радиоэлектроники<br>и информационных технологий</h1>
          <div class="bento-day-row">
            <span class="bento-day-name">{{ currentDayName }}</span>
            <span class="bento-day-dot">·</span>
            <span class="bento-day-date">{{ currentDayShort }}</span>
          </div>
        </div>
        <div class="bento-card bento-clock">
          <div class="bento-clock-eyebrow">Сейчас</div>
          <div class="bento-clock-time">{{ currentTime }}</div>
          <div class="bento-clock-date">{{ currentDayName }}</div>
          <div v-if="weather" class="bento-weather" :title="weather.label">
            <Icon :name="weather.icon" :size="22" class="bento-weather-icon" />
            <span class="bento-weather-temp">{{ weather.temp }}°</span>
            <span class="bento-weather-label">{{ weather.label }}</span>
          </div>
        </div>
      </div>

      <div v-if="nowWidget" class="now-widget" @click="$router.push('/schedule')">
        <div class="now-icon">{{ nowWidget.icon }}</div>
        <div class="now-text">
          <div class="now-title">{{ nowWidget.title }}</div>
          <div v-if="nowWidget.line1" class="now-line">{{ nowWidget.line1 }}</div>
          <div v-if="nowWidget.line2" class="now-line now-line-dim">{{ nowWidget.line2 }}</div>
        </div>
      </div>

      <div v-if="bellSchedule.length > 0" class="bells-widget" @click="$router.push('/schedule')">
        <div class="bells-head">
          <span class="bells-icon"><Icon name="bell" :size="24" /></span>
          <span class="bells-title">Расписание звонков</span>
          <span class="bells-day">{{ currentDayName }}</span>
        </div>
        <div class="bells-list">
          <div
            v-for="pair in bellSchedule"
            :key="pair.label + pair.start"
            class="bell-item"
            :class="{
              'bell-item--current': pair.lesson_number === currentBellNumber,
              'bell-item--next': pair.lesson_number === nextBellNumber,
            }"
          >
            <div class="bell-num">{{ pair.lesson_number > 0 ? pair.lesson_number : '·' }}</div>
            <div class="bell-info">
              <div class="bell-label">{{ pair.label }}</div>
              <div class="bell-time">{{ pair.start }}–{{ pair.end }}</div>
            </div>
            <div v-if="pair.lesson_number === currentBellNumber" class="bell-tag bell-tag--now">Сейчас</div>
            <div v-else-if="pair.lesson_number === nextBellNumber" class="bell-tag bell-tag--next">След.</div>
          </div>
        </div>
      </div>
    </div>

    <div class="middle-section">
      <!-- Резервное вертикальное пространство между шапкой и контактами -->
    </div>

    <div class="bottom-section">
      <div class="contact-info">
        <h2>Контактная информация</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <span class="icon"><Icon name="mapPin" :size="22" /></span>
            <div>
              <strong>Адреса</strong>
              <p>пр. Красноярский рабочий, 156</p>
              <p>пр. Свободный, 67</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="icon"><Icon name="phone" :size="22" /></span>
            <div>
              <strong>Телефон</strong>
              <p>8 (391) 218-17-99</p>
              <p class="additional-info">доб. 207, 216, 208</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="icon"><Icon name="messageCircle" :size="22" /></span>
            <div>
              <strong>Приёмная комиссия 2026</strong>
              <p>8-929-332-29-43</p>
              <p>8-933-327-02-09</p>
              <p>8-391-298-46-46</p>
              <p class="additional-info">kraskritpk@yandex.ru</p>
            </div>
          </div>
        </div>

        <div class="contacts-online">
          <div class="contacts-online-head">
            <span class="icon"><Icon name="globe" :size="22" /></span>
            <strong>Найти нас онлайн</strong>
          </div>
          <div class="contacts-online-body">
            <div class="social-list">
              <a
                class="social-link social-link--site"
                href="https://kraskrit.ru/"
                target="_blank"
                rel="noopener"
                aria-label="Официальный сайт"
              >
                <span class="social-badge"><Icon name="globe" :size="20" /></span>
                <span class="social-text">kraskrit.ru</span>
              </a>
              <a
                class="social-link social-link--vk"
                href="https://vk.com/kraskrit"
                target="_blank"
                rel="noopener"
                aria-label="ВКонтакте"
              >
                <span class="social-badge">VK</span>
                <span class="social-text">vk.com/kraskrit</span>
              </a>
              <a
                class="social-link social-link--mail"
                href="mailto:priem@kraskrit.ru"
                aria-label="Электронная почта приёмной"
              >
                <span class="social-badge">@</span>
                <span class="social-text">priem@kraskrit.ru</span>
              </a>
              <a
                class="social-link social-link--feedback"
                href="https://kraskrit.ru/contact-us/obr-svaz/"
                target="_blank"
                rel="noopener"
                aria-label="Обратная связь"
              >
                <span class="social-badge"><Icon name="edit" :size="20" /></span>
                <span class="social-text">Обратная связь</span>
              </a>
            </div>
            <div class="qr-codes">
              <div class="qr-item">
                <img v-if="qrWebsite" :src="qrWebsite" alt="QR код сайта" class="qr-code" />
                <p class="qr-label">Сайт</p>
              </div>
              <div class="qr-item">
                <img v-if="qrVK" :src="qrVK" alt="QR код VK" class="qr-code" />
                <p class="qr-label">VK</p>
              </div>
              <div class="qr-item">
                <img v-if="qrFeedback" :src="qrFeedback" alt="QR код формы" class="qr-code" />
                <p class="qr-label">Обратная связь</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-widgets">
        <div class="widget applicant-widget">
          <h3><Icon name="graduation" :size="22" /> Абитуриенту 2026</h3>
          <div class="countdown-timer">
            <div class="countdown-label">До начала приемной кампании осталось:</div>
            <div class="countdown-value">{{ daysUntilAdmission }} дней</div>
          </div>
          <div class="applicant-actions">
            <button class="applicant-btn" @click="showPassingScores">
              <span class="btn-icon"><Icon name="barChart" :size="22" /></span>
              <span class="btn-text">Проходные баллы</span>
            </button>
            <button class="applicant-btn" @click="showSpecialties">
              <span class="btn-icon"><Icon name="target" :size="22" /></span>
              <span class="btn-text">Специальности</span>
            </button>
            <button class="applicant-btn" @click="showApplicationQR">
              <span class="btn-icon"><Icon name="smartphone" :size="22" /></span>
              <span class="btn-text">Подать документы</span>
            </button>
            <button class="applicant-btn applicant-btn--accent" @click="$router.push('/quiz')">
              <span class="btn-icon"><Icon name="compass" :size="22" /></span>
              <span class="btn-text">Подобрать профессию</span>
            </button>
          </div>
        </div>
      </div>

      <div class="fun-facts-widget">
        <div class="fun-fact">
          <span class="fact-icon"><Icon name="lightbulb" :size="24" /></span>
          <span class="fact-text">{{ currentFact }}</span>
        </div>
      </div>

      <div class="features">
        <div class="feature-card" @click="$router.push('/schedule')">
          <div class="feature-icon"><Icon name="calendar" :size="34" /></div>
          <h2>Расписание</h2>
          <p>Найдите расписание по группе или преподавателю</p>
        </div>

        <div class="feature-card" @click="$router.push('/staff')">
          <div class="feature-icon"><Icon name="users" :size="34" /></div>
          <h2>Сотрудники</h2>
          <p>Информация о преподавателях и администрации</p>
        </div>

        <div class="feature-card" @click="$router.push('/map')">
          <div class="feature-icon"><Icon name="map" :size="34" /></div>
          <h2>Навигация</h2>
          <p>Найдите нужный кабинет на карте колледжа</p>
        </div>

        <div class="feature-card" @click="$router.push('/faq')">
          <div class="feature-icon"><Icon name="help" :size="34" /></div>
          <h2>Частые вопросы</h2>
          <p>Справки, документы, Wi-Fi, поступление</p>
        </div>
      </div>

      <section v-if="newsItems.length > 0" class="news-section">
        <div class="news-header">
          <h2><Icon name="newspaper" :size="22" /> Новости колледжа</h2>
          <a class="news-all-link" href="https://kraskrit.ru/news/" target="_blank" rel="noopener">
            Все новости →
          </a>
        </div>
        <div class="news-grid">
          <a
            v-for="item in newsCards"
            :key="item.id"
            class="news-card"
            :href="item.source_url || 'https://kraskrit.ru/news/'"
            target="_blank"
            rel="noopener"
          >
            <div class="news-icon"><Icon name="newspaper" :size="22" /></div>
            <div class="news-body">
              <div class="news-date" v-if="item.published_date">{{ formatNewsDate(item.published_date) }}</div>
              <h3 class="news-title">{{ item.title }}</h3>
              <p v-if="item.description" class="news-desc">{{ item.description }}</p>
            </div>
          </a>
        </div>
      </section>
    </div>

    <button class="accessibility-button" @click="toggleAccessibilityMode" :class="{ active: accessibilityMode }">
      <Icon v-if="!accessibilityMode" name="accessibility" :size="24" />
      <Icon v-else name="x" :size="24" />
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { generateQRCode } from '../utils/qrGenerator'
import { fetchNews } from '../services/newsService'
import api from '../services/api'
import Icon from '../components/Icon.vue'

export default {
  name: 'Home',
  components: { Icon },
  setup() {
    const currentTime = ref('')
    const currentDate = ref('')
    const currentDayName = ref('')
    const currentDayShort = ref('')
    const bellSchedule = ref([])
    const qrWebsite = ref('')
    const qrFeedback = ref('')
    const qrVK = ref('')
    const accessibilityMode = ref(false)
    const daysUntilAdmission = ref(0)
    const newsItems = ref([])
    const newsCards = computed(() => newsItems.value.slice(0, 3))

    // ─── Погода (open-meteo, без ключа) ───
    const weather = ref(null)
    const KRSK_LAT = 56.0153
    const KRSK_LON = 92.8932

    const weatherFromCode = (code) => {
      // WMO Weather interpretation codes
      // https://open-meteo.com/en/docs
      if (code === 0) return { icon: 'sun', label: 'Ясно' }
      if (code === 1) return { icon: 'sun', label: 'Преим. ясно' }
      if (code === 2) return { icon: 'cloudSun', label: 'Перем. облачность' }
      if (code === 3) return { icon: 'cloud', label: 'Пасмурно' }
      if (code === 45 || code === 48) return { icon: 'fog', label: 'Туман' }
      if (code >= 51 && code <= 57) return { icon: 'cloudRain', label: 'Морось' }
      if (code >= 61 && code <= 67) return { icon: 'cloudRain', label: 'Дождь' }
      if (code >= 71 && code <= 77) return { icon: 'snow', label: 'Снег' }
      if (code >= 80 && code <= 82) return { icon: 'cloudRain', label: 'Ливень' }
      if (code === 85 || code === 86) return { icon: 'snow', label: 'Снегопад' }
      if (code >= 95 && code <= 99) return { icon: 'thunder', label: 'Гроза' }
      return { icon: 'cloud', label: 'Облачно' }
    }

    const loadWeather = async () => {
      try {
        const url =
          `https://api.open-meteo.com/v1/forecast?latitude=${KRSK_LAT}&longitude=${KRSK_LON}` +
          `&current=temperature_2m,weather_code&timezone=Asia/Krasnoyarsk`
        const response = await fetch(url)
        if (!response.ok) return
        const data = await response.json()
        const c = data.current
        if (!c) return
        const meta = weatherFromCode(c.weather_code)
        weather.value = {
          temp: Math.round(c.temperature_2m),
          icon: meta.icon,
          label: meta.label,
        }
      } catch (_) {
        // тихо: если погода не загрузилась — просто не показываем виджет
      }
    }
    const nowStatus = ref(null)

    const loadNowStatus = async () => {
      try {
        const response = await api.get('/schedule/now')
        nowStatus.value = response.data
      } catch (_) {
        nowStatus.value = null
      }
    }

    const nowWidget = computed(() => {
      const s = nowStatus.value
      if (!s) return null
      if (s.status === 'weekend') {
        return {
          icon: '☕',
          title: 'Сегодня выходной',
          line1: 'Занятий в воскресенье нет',
          line2: null,
        }
      }
      if (s.status === 'before_classes' && s.next) {
        return {
          icon: '🕔',
          title: 'До начала пар',
          line1: `${s.next.label}: ${s.next.start}—${s.next.end}`,
          line2: s.next.minutes_until != null
            ? `Начало через ${s.next.minutes_until} мин`
            : null,
        }
      }
      if (s.status === 'break' && s.next) {
        return {
          icon: '☕',
          title: 'Сейчас перерыв',
          line1: `Следующая — ${s.next.label}: ${s.next.start}—${s.next.end}`,
          line2: s.next.minutes_until != null
            ? `Через ${s.next.minutes_until} мин`
            : null,
        }
      }
      if (s.status === 'after_classes') {
        return {
          icon: '🌙',
          title: 'Пары на сегодня закончились',
          line1: 'До встречи завтра!',
          line2: null,
        }
      }
      if (s.status === 'in_progress' && s.current) {
        const groups = s.current.busy_groups
        const groupsLabel = groups
          ? `занято групп: ${groups}`
          : ''
        const left = s.current.minutes_left != null
          ? `Осталось ${s.current.minutes_left} мин`
          : ''
        return {
          icon: '📚',
          title: `Сейчас идёт ${s.current.label}`,
          line1: `${s.current.start}—${s.current.end}${groups ? '  ·  ' + groupsLabel : ''}`,
          line2: left,
        }
      }
      return null
    })

    const loadNews = async () => {
      try {
        const data = await fetchNews(5)
        newsItems.value = Array.isArray(data) ? data : []
      } catch (_) {
        newsItems.value = []
      }
    }

    const formatNewsDate = (raw) => {
      if (!raw) return ''
      try {
        return new Date(raw).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
      } catch (_) {
        return ''
      }
    }
    const currentFact = ref('')
    const facts = [
      '🤖 В стенах ККРИТ проложено более 50 километров витой пары. Этого хватит, чтобы обмотать колледж 100 раз!',
      '☕ Во время регионального хакатона наши студенты выпили 120 литров кофе за 24 часа',
      '💾 Суммарный объем кода, который пишут наши студенты за один семестр, превышает код управления космическим шаттлом',
      '🏆 85% наших выпускников находят работу по специальности еще до получения диплома',
      '🏃 От входа до кабинета 415 ровно 342 шага. Мы проверяли',
      '📡 В колледже работает более 500 компьютеров, объединенных в единую сеть',
      '🎓 ККРИТ выпустил более 15 000 специалистов за всю историю существования',
      '🚌 До корпуса на пр. Свободный, 67 можно доехать на 10 маршрутах: автобусы №2, 5, 26, 32, 34, 51, 52, 53, 71, 76, 85, 87 и троллейбусы №5, 6'
    ]
    let timeInterval = null
    let factInterval = null

    const updateDateTime = () => {
      const now = new Date()
      currentTime.value = now.toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
      currentDate.value = now.toLocaleDateString('ru-RU', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
      currentDayName.value = now.toLocaleDateString('ru-RU', { weekday: 'long' })
      currentDayShort.value = now.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })
    }

    const loadBellSchedule = async () => {
      try {
        const response = await api.get('/schedule/bells')
        bellSchedule.value = Array.isArray(response.data?.pairs) ? response.data.pairs : []
      } catch (_) {
        bellSchedule.value = []
      }
    }

    const currentBellNumber = computed(() => {
      const s = nowStatus.value
      if (!s) return null
      if (s.status === 'in_progress' && s.current?.lesson_number != null) {
        return s.current.lesson_number
      }
      return null
    })

    const nextBellNumber = computed(() => {
      const s = nowStatus.value
      if (!s) return null
      if ((s.status === 'before_classes' || s.status === 'break') && s.next?.lesson_number != null) {
        return s.next.lesson_number
      }
      return null
    })

    const generateQRCodes = async () => {
      qrWebsite.value = await generateQRCode('https://kraskrit.ru/')
      qrFeedback.value = await generateQRCode('https://kraskrit.ru/contact-us/obr-svaz/')
      qrVK.value = await generateQRCode('https://vk.com/kraskrit')
    }

    const toggleAccessibilityMode = () => {
      accessibilityMode.value = !accessibilityMode.value
    }

    const calculateDaysUntilAdmission = () => {
      const admissionDate = new Date('2026-06-15') // Прием документов начинается 15 июня
      const today = new Date()
      const diffTime = admissionDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      daysUntilAdmission.value = diffDays > 0 ? diffDays : 0
    }

    const rotateFact = () => {
      const randomIndex = Math.floor(Math.random() * facts.length)
      currentFact.value = facts[randomIndex]
    }

    const showPassingScores = () => {
      const modal = document.createElement('div')
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;overflow-y:auto;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(160deg,#ffffff 0%,#f7f9fd 100%);padding:2.25rem;border-radius:24px;max-width:680px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 24px 60px rgba(15,23,42,0.18);border:1px solid rgba(15,23,42,0.10);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#0f172a;margin:0 0 1.5rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">📊 Проходные баллы</h2>
          <div style="background:#f5f7fb;padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(15,23,42,0.10);">
            <p style="color:rgba(15,23,42,0.88);line-height:1.7;font-size:1rem;margin:0;">
              В ККРИТ нет вступительных экзаменов — зачисление проходит по конкурсу <strong style="color:#b45309;">среднего балла аттестата</strong>.<br><br>
              На специальности «Пожарная безопасность» — дополнительно психологическое тестирование и нормативы физподготовки.
            </p>
          </div>
          <div style="background:#f5f7fb;padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(15,23,42,0.10);">
            <h3 style="color:#0f172a;margin:0 0 0.9rem;font-size:1.1rem;font-weight:700;">📈 Средний балл аттестата 2025 (справочно)</h3>
            <div style="color:rgba(15,23,42,0.85);line-height:1.8;font-size:0.95rem;">
              • Бюджет (ИТ-специальности): <strong style="color:#b45309;">4.0–4.5</strong><br>
              • Бюджет (экономика, электроника): <strong style="color:#b45309;">3.8–4.2</strong><br>
              • Платные места: <strong style="color:#b45309;">от 3.0</strong><br><br>
              <span style="color:rgba(15,23,42,0.55);font-size:0.85rem;">Цифры ориентировочные — точный проходной балл формируется по итогам конкурса.</span>
            </div>
          </div>
          <div style="background:#f5f7fb;padding:1.5rem;border-radius:18px;margin-bottom:1.5rem;border:1px solid rgba(15,23,42,0.10);">
            <h3 style="color:#0f172a;margin:0 0 0.9rem;font-size:1.1rem;font-weight:700;">📆 Сроки приёма 2026</h3>
            <div style="color:rgba(15,23,42,0.85);line-height:1.8;font-size:0.95rem;">
              • Начало приёма: <strong style="color:#b45309;">15 июня 2026</strong><br>
              • Окончание (основное): <strong style="color:#b45309;">14 августа 2026</strong><br>
              • Пожарная безопасность: <strong style="color:#b45309;">до 10 августа 2026</strong><br>
              • При наличии свободных мест: <strong style="color:#b45309;">до 25 ноября 2026</strong>
            </div>
          </div>
          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:0.9rem 2rem;background:linear-gradient(135deg,#2563EB 0%,#0EA5B7 100%);color:#ffffff;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(37,99,235,0.35)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    const showSpecialties = () => {
      const modal = document.createElement('div')
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;overflow-y:auto;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(160deg,#ffffff 0%,#f7f9fd 100%);padding:2.25rem;border-radius:24px;max-width:900px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 24px 60px rgba(15,23,42,0.18);border:1px solid rgba(15,23,42,0.10);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#0f172a;margin:0 0 0.5rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">Специальности ККРИТ 2026/27</h2>
          <p style="color:rgba(15,23,42,0.6);text-align:center;margin:0 0 1.5rem;font-size:0.92rem;">Поступление на базе 9 классов, срок обучения в скобках</p>

          <div style="background:#f5f7fb;padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(15,23,42,0.10);">
            <h3 style="color:#0f172a;margin:0 0 0.9rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.15rem;font-weight:700;">📍 пр. Красноярский рабочий, 156 — IT и экономика</h3>
            <div style="color:rgba(15,23,42,0.82);line-height:1.75;font-size:0.95rem;">
              <strong style="color:#b45309;">Бюджет:</strong><br>
              • 38.02.01 Экономика и бухгалтерский учёт — 25 мест (2 г. 10 мес.)<br>
              • 38.02.07 Банковское дело — 25 мест (2 г. 10 мес.)<br><br>
              <strong style="color:#b45309;">Платно:</strong><br>
              • 09.02.09 Веб-разработка — 25 мест (2 г. 10 мес.)<br>
              • 09.02.09 Веб-разработка (после 11 кл.) — 25 мест (1 г. 10 мес.)<br>
              • 09.02.10 Разработка игр, AR/VR — 25 мест (3 г. 10 мес.)<br>
              • 09.02.11 Разработка ПО (программист) — 25 мест (3 г. 10 мес.)<br>
              • 09.02.13 Искусственный интеллект — 25 мест (3 г. 10 мес.)
            </div>
          </div>

          <div style="background:#f5f7fb;padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(15,23,42,0.10);">
            <h3 style="color:#0f172a;margin:0 0 0.9rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.15rem;font-weight:700;">📍 пр. Свободный, 67 — инфраструктура и электроника</h3>
            <div style="color:rgba(15,23,42,0.82);line-height:1.75;font-size:0.95rem;">
              <strong style="color:#b45309;">Бюджет:</strong><br>
              • 09.02.01 Компьютерные системы и комплексы — 50 мест (3 г. 10 мес.)<br>
              • 09.02.06 Сетевое и системное администрирование — 50 мест (3 г. 10 мес.)<br>
              • 10.02.05 Информационная безопасность АС — 25 мест (3 г. 10 мес.)<br>
              • 11.02.16 Монтаж электронных приборов — 50 мест (3 г. 10 мес.)<br>
              • 20.02.04 Пожарная безопасность — 50 мест (3 г. 10 мес.)<br><br>
              <strong style="color:#b45309;">Платно:</strong><br>
              • 09.02.01 Компьютерные системы и комплексы — 25 мест<br>
              • 09.02.06 Сетевое и системное администрирование — 25 мест<br>
              • 10.02.05 Информационная безопасность АС — 25 мест<br>
              • 20.02.04 Пожарная безопасность (после 11 кл.) — 25 мест (2 г. 10 мес.)
            </div>
          </div>

          <div style="background:linear-gradient(135deg,rgba(37,99,235,0.10),rgba(14,165,183,0.08));padding:1.25rem 1.5rem;border-radius:18px;margin-bottom:1.5rem;border:1px solid rgba(37,99,235,0.30);color:rgba(15,23,42,0.92);font-size:0.95rem;line-height:1.7;">
            📊 <strong>Итого на 2026/27:</strong> 225 бюджетных + 275 платных мест. <br>Три специальности появились впервые в этом году: <strong style="color:#b45309;">ИИ, игры/AR‑VR и веб-разработка</strong>.
          </div>

          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:0.9rem 2rem;background:linear-gradient(135deg,#2563EB 0%,#0EA5B7 100%);color:#ffffff;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(37,99,235,0.35)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    const showApplicationQR = async () => {
      const qr = await generateQRCode('https://kraskrit.ru/abitur/')
      const modal = document.createElement('div')
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;overflow-y:auto;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(160deg,#ffffff 0%,#f7f9fd 100%);padding:2.25rem;border-radius:24px;max-width:760px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 24px 60px rgba(15,23,42,0.18);border:1px solid rgba(15,23,42,0.10);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#0f172a;margin:0 0 1.5rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">📱 Подать документы</h2>

          <div style="display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:1.5rem;background:#f5f7fb;padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(15,23,42,0.10);">
            <div style="flex:0 1 240px;min-width:0;text-align:center;">
              <img src="${qr}" style="width:100%;max-width:220px;height:auto;aspect-ratio:1/1;border-radius:14px;background:#fff;padding:8px;box-sizing:border-box;"/>
              <p style="color:rgba(15,23,42,0.7);font-size:0.85rem;margin:0.6rem 0 0;">Отсканируйте —<br>откроется раздел «Абитуриенту»</p>
            </div>
            <div style="flex:1 1 280px;min-width:0;color:rgba(15,23,42,0.88);font-size:0.97rem;line-height:1.7;">
              <strong style="color:#b45309;">Приём документов:</strong><br>
              c 15 июня по 14 августа 2026<br>
              Пожарная безопасность — до 10 августа<br><br>
              <strong style="color:#b45309;">Адрес приёмной комиссии:</strong><br>
              пр. Свободный, 67<br>
              пн–чт 09:00–15:30, пт 09:00–12:00<br><br>
              <strong style="color:#b45309;">Телефоны:</strong><br>
              8-929-332-29-43<br>
              8-933-327-02-09<br>
              8-391-298-46-46<br>
              <strong style="color:#b45309;">E-mail:</strong> kraskritpk@yandex.ru
            </div>
          </div>

          <div style="background:#f5f7fb;padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(15,23,42,0.10);">
            <h3 style="color:#0f172a;margin:0 0 0.9rem;font-size:1.1rem;font-weight:700;">📋 Перечень документов</h3>
            <div style="color:rgba(15,23,42,0.85);line-height:1.85;font-size:0.95rem;">
              • Заявление о приёме на обучение (одно на все специальности)<br>
              • Согласие на обработку персональных данных<br>
              • Паспорт — копия разворота с фото и прописки<br>
              • Документ об образовании (аттестат / диплом) — оригинал или копия<br>
              • СНИЛС (копия)<br>
              • 4 фотографии 3×4 см (без головного убора)<br>
              • Справка 086/у<br>
              • Копия полиса ОМС<br>
              • Для несовершеннолетних — копия паспорта родителя / законного представителя<br>
              • Для ОВЗ / инвалидности — копии подтверждающих документов
            </div>
          </div>

          <div style="background:linear-gradient(135deg,rgba(14,165,183,0.12),rgba(37,99,235,0.08));padding:1.25rem 1.5rem;border-radius:18px;margin-bottom:1.5rem;border:1px solid rgba(14,165,183,0.30);color:rgba(15,23,42,0.92);font-size:0.93rem;line-height:1.7;">
            ℹ️ Заявление можно подать <strong>лично</strong> на пр. Свободный 67, <strong>почтой</strong> или <strong>через Госуслуги</strong> (в тестовом режиме).<br>Для зачисления оригинал аттестата нужно сдать до <strong>14 августа 2026</strong>.
          </div>

          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:0.9rem 2rem;background:linear-gradient(135deg,#2563EB 0%,#0EA5B7 100%);color:#ffffff;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(37,99,235,0.35)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    let nowInterval = null
    let weatherInterval = null

    onMounted(() => {
      updateDateTime()
      timeInterval = setInterval(updateDateTime, 1000)
      generateQRCodes()
      calculateDaysUntilAdmission()
      loadNews()
      rotateFact()
      factInterval = setInterval(rotateFact, 18000) // Меняем факт каждые 18 секунд
      loadNowStatus()
      nowInterval = setInterval(loadNowStatus, 30000)
      loadBellSchedule()
      loadWeather()
      weatherInterval = setInterval(loadWeather, 15 * 60 * 1000)
    })

    onUnmounted(() => {
      if (timeInterval) {
        clearInterval(timeInterval)
      }
      if (factInterval) {
        clearInterval(factInterval)
      }
      if (nowInterval) {
        clearInterval(nowInterval)
      }
      if (weatherInterval) {
        clearInterval(weatherInterval)
      }
    })

    return {
      weather,
      currentTime,
      currentDate,
      qrWebsite,
      qrFeedback,
      qrVK,
      accessibilityMode,
      toggleAccessibilityMode,
      daysUntilAdmission,
      currentFact,
      showPassingScores,
      showSpecialties,
      showApplicationQR,
      newsItems,
      newsCards,
      formatNewsDate,
      nowWidget,
      currentDayName,
      currentDayShort,
      bellSchedule,
      currentBellNumber,
      nextBellNumber,
    }
  }
}
</script>


<style scoped>
.home {
  max-width: var(--content-max-width, 1400px);
  margin: 0 auto;
  position: relative;
  padding-bottom: 5rem;
}

.top-section {
  padding: 1.5rem 0 1rem;
  transition: all 0.6s var(--ease);
}

.middle-section {
  min-height: 0;
  transition: min-height 0.6s var(--ease);
}

.bottom-section {
  transform: translateY(0);
}

/* ── Bento hero: приветствие + часы ── */
.bento-hero {
  display: grid;
  grid-template-columns: minmax(0, 2.1fr) minmax(0, 1fr);
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 900px) {
  .bento-hero {
    grid-template-columns: 1fr;
  }
}

.bento-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
  position: relative;
  overflow: hidden;
}

.bento-card:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow);
}

.bento-welcome {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.75rem;
  background:
    radial-gradient(120% 80% at 0% 0%, var(--accent-soft), transparent 55%),
    var(--surface);
}

.bento-eyebrow {
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-muted);
}

/* ── Заголовок ── */
h1 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 3.4vw, 2.6rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.1;
  margin: 0;
  color: var(--text);
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
}

.bento-day-row {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: 0.75rem;
  padding: 0.55rem 1.1rem;
  background: var(--accent-gradient);
  color: #ffffff;
  border-radius: var(--radius-pill);
  font-weight: 700;
  font-size: clamp(1rem, 1.4vw, 1.2rem);
  text-transform: capitalize;
  letter-spacing: -0.01em;
  align-self: flex-start;
  box-shadow: var(--shadow-sm);
}

.bento-day-dot {
  opacity: 0.55;
}

.bento-day-date {
  font-weight: 600;
}

.bento-clock {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 0.4rem;
  background:
    linear-gradient(160deg, var(--accent) 0%, var(--accent-2) 100%);
  color: #ffffff;
  border-color: transparent;
  box-shadow: var(--shadow), var(--accent-glow);
}

.bento-clock::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.18), transparent 60%);
  pointer-events: none;
}

.bento-clock-eyebrow {
  position: relative;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.8;
}

.bento-clock-time {
  position: relative;
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5.5vw, 4rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.bento-weather {
  position: relative;
  margin-top: 0.85rem;
  padding-top: 0.85rem;
  border-top: 1px solid rgba(255, 255, 255, 0.22);
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.01em;
}

.bento-weather-icon {
  flex-shrink: 0;
}

.bento-weather-temp {
  font-family: var(--font-display);
  font-size: 1.45rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1;
}

.bento-weather-label {
  opacity: 0.92;
  font-weight: 500;
  font-size: 0.95rem;
  white-space: nowrap;
}

.bento-clock-date {
  position: relative;
  font-size: 1rem;
  opacity: 0.9;
  text-transform: capitalize;
  font-weight: 600;
}

/* ── Расписание звонков ── */
.bells-widget {
  margin: 1.25rem auto 0;
  max-width: 880px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem 1.5rem;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: box-shadow var(--transition), border-color var(--transition);
}

.bells-widget:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow);
}

.bells-head {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px dashed var(--border);
}

.bells-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.bells-title {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: var(--text);
}

.bells-day {
  margin-left: auto;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: capitalize;
}

.bells-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 0.5rem;
}

.bell-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.75rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  position: relative;
  transition: border-color var(--transition), background var(--transition);
}

.bell-num {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-strong);
  color: var(--text-muted);
  border-radius: 50%;
  font-size: 0.85rem;
  font-weight: 800;
}

.bell-info {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  min-width: 0;
  flex: 1;
}

.bell-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bell-time {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  font-variant-numeric: tabular-nums;
}

.bell-tag {
  position: absolute;
  top: -8px;
  right: 8px;
  padding: 0.1rem 0.55rem;
  border-radius: 999px;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #ffffff;
}

.bell-tag--now {
  background: var(--accent-gradient);
  box-shadow: 0 4px 12px -2px rgba(37, 99, 235, 0.5);
}

.bell-tag--next {
  background: linear-gradient(135deg, var(--accent-3), #EF4444);
}

.bell-item--current {
  background: var(--accent-soft);
  border-color: var(--accent-border);
}

.bell-item--current .bell-num {
  background: var(--accent-gradient);
  color: #ffffff;
}

.bell-item--current .bell-label {
  color: var(--accent);
}

.bell-item--next {
  background: rgba(245, 158, 11, 0.08);
  border-color: rgba(245, 158, 11, 0.30);
}

.bell-item--next .bell-num {
  background: linear-gradient(135deg, var(--accent-3), #EF4444);
  color: #ffffff;
}

.subtitle {
  font-size: clamp(1rem, 1.6vw, 1.2rem);
  color: var(--text-muted);
  max-width: 640px;
  margin: 0 auto 2rem;
  font-weight: 500;
  line-height: 1.5;
}

/* ── Единая карточка / «стекло» ── */
.widget,
.contact-info,
.fun-facts-widget,
.datetime-widget-top {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  transition: background var(--transition), border-color var(--transition), transform var(--transition), box-shadow var(--transition);
}

.widget:hover,
.contact-info:hover,
.fun-facts-widget:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
}

/* ── Контакты ── */
.contact-info {
  padding: 2.5rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow);
}

.contact-info h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.75rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text);
}

.contact-info h2::before {
  content: '';
  width: 4px;
  height: 24px;
  background: var(--accent-gradient);
  border-radius: var(--radius-pill);
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
  text-align: left;
}

/* ── Онлайн-контакты: вторая строка в блоке Контакты ── */
.contacts-online {
  margin-top: 1.25rem;
  padding: 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.contacts-online-head {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.contacts-online-head .icon {
  font-size: 1.75rem;
  flex-shrink: 0;
}

.contacts-online-head strong {
  color: var(--text);
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.contacts-online-body {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr);
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 760px) {
  .contacts-online-body {
    grid-template-columns: 1fr;
  }
}

.contact-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 1.25rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: background var(--transition), border-color var(--transition);
}

.contact-item:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
}

.contact-item .icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.contact-item strong {
  display: block;
  color: var(--text);
  margin-bottom: 0.4rem;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: -0.01em;
}

.contact-item p {
  color: var(--text-muted);
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

.additional-info {
  font-size: 0.85rem !important;
  color: var(--text-dim) !important;
}

/* ── QR-коды ── */
.contact-item > div { min-width: 0; flex: 1; }

.qr-codes {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0;
  justify-content: flex-start;
  max-width: 100%;
}

.qr-item {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 0 0 auto;
  min-width: 0;
}

.qr-code {
  width: clamp(72px, 9vw, 110px);
  height: clamp(72px, 9vw, 110px);
  border-radius: var(--radius-sm);
  padding: 6px;
  background: #ffffff;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition);
  object-fit: contain;
  display: block;
}

.qr-code:hover {
  transform: scale(1.04);
}

.qr-label {
  font-size: 0.75rem;
  margin-top: 0.4rem;
  color: var(--text-muted);
  font-weight: 500;
  line-height: 1.3;
  max-width: 130px;
  word-break: break-word;
}

/* ── Соцсети колледжа ── */
.social-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.6rem;
  margin: 0;
}

.social-link {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 0.75rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
}

.social-link:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateX(2px);
}

.social-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.85rem;
  height: 1.85rem;
  border-radius: 50%;
  font-size: 0.85rem;
  font-weight: 700;
  flex-shrink: 0;
}

.social-link--vk .social-badge {
  background: linear-gradient(135deg, #4a76a8 0%, #5181b8 100%);
  color: #fff;
}

.social-link--mail .social-badge {
  background: linear-gradient(135deg, #2563EB 0%, #0EA5B7 100%);
  color: #fff;
}

.social-link--site .social-badge {
  background: linear-gradient(135deg, #0EA5B7 0%, #2563EB 100%);
  color: #fff;
}

.social-link--feedback .social-badge {
  background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
  color: #fff;
}

.social-text {
  word-break: break-word;
}

/* ── Нижние виджеты ── */
.bottom-widgets {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin: 2rem 0;
}

.widget {
  padding: 1.75rem;
  box-shadow: var(--shadow);
}

.datetime-widget {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background:
    linear-gradient(135deg, var(--accent-soft), transparent 70%),
    var(--surface);
  border-color: var(--accent-border);
}

.time {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5vw, 3.6rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.date {
  font-size: 0.95rem;
  color: var(--text-muted);
  text-transform: capitalize;
  font-weight: 500;
}

.datetime-widget-top {
  display: none;
  padding: 2rem;
  margin: 2rem auto;
  max-width: 420px;
  text-align: center;
}

/* ── Абитуриент-виджет ── */
.applicant-widget {
  position: relative;
  background:
    linear-gradient(135deg, rgba(245, 158, 11, 0.10), rgba(239, 68, 68, 0.06)),
    var(--surface);
  border-color: rgba(245, 158, 11, 0.25);
  overflow: hidden;
}

.applicant-widget::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--accent-gradient-warm);
  z-index: 1;
}

.applicant-widget h3 {
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  color: var(--text);
}

.countdown-timer {
  text-align: center;
  margin-bottom: 1.5rem;
  padding: 1.25rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.countdown-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.countdown-value {
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: var(--accent-gradient-warm);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.applicant-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.applicant-btn {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 1rem 1.25rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition);
  font-size: 1rem;
  font-weight: 600;
  text-align: left;
}

.applicant-btn:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: translateX(4px);
  box-shadow: var(--shadow-sm);
}

.applicant-btn--accent {
  background: var(--accent-gradient);
  border-color: transparent;
  color: #ffffff;
  box-shadow: var(--shadow-sm);
}

.applicant-btn--accent:hover {
  background: var(--accent-gradient);
  border-color: transparent;
  transform: translateX(4px) translateY(-1px);
  box-shadow: var(--shadow);
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  line-height: 1;
}

.btn-text {
  flex: 1;
}

/* ── Fun facts ── */
.fun-facts-widget {
  padding: 1.25rem 1.75rem;
  margin: 1.5rem 0;
  box-shadow: var(--shadow-sm);
}

.fun-fact {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  animation: fadeIn 0.6s var(--ease);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.fact-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.fact-text {
  font-size: 1rem;
  color: var(--text-muted);
  line-height: 1.5;
  font-weight: 500;
}

.home.accessibility-active .fun-facts-widget {
  display: none;
}

/* ── Главные карточки / навигация ── */
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.feature-card {
  position: relative;
  padding: 2.5rem 2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), transform var(--transition), box-shadow var(--transition);
  box-shadow: var(--shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 260px;
  justify-content: center;
}

.feature-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--accent-gradient);
  opacity: 0;
  transition: opacity var(--transition);
  pointer-events: none;
  mix-blend-mode: overlay;
}

.feature-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--accent-gradient);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--transition-slow);
}

.feature-card:hover {
  transform: translateY(-4px);
  background: var(--surface-hover);
  border-color: var(--accent-border);
  box-shadow: var(--shadow-lg), var(--accent-glow);
}

.feature-card:hover::before {
  opacity: 0.05;
}

.feature-card:hover::after {
  transform: scaleX(1);
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin-bottom: 1.25rem;
  border-radius: 18px;
  background: var(--accent-soft);
  color: var(--accent);
  transition: transform var(--transition-slow), background var(--transition), color var(--transition);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.18);
}

.feature-card:hover .feature-icon {
  transform: translateY(-3px) rotate(-3deg);
  background: var(--accent);
  color: #ffffff;
}

.feature-card h2 {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.feature-card p {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.5;
  max-width: 280px;
}

/* ── Виджет «Сейчас идёт» ──
   Находится внутри .top-section, под заголовком, чтобы визуально
   не налезать на блок контактов ниже. */
.now-widget {
  position: relative;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem 2rem;
  margin: 2rem auto 0.75rem;
  max-width: 880px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow);
  cursor: pointer;
  overflow: hidden;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
}

.now-widget::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--accent-gradient);
  opacity: 0.06;
  pointer-events: none;
  z-index: 0;
}

.now-widget::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 6px;
  background: var(--accent-gradient);
  border-radius: var(--radius-xl) 0 0 var(--radius-xl);
  z-index: 1;
}

.now-widget > * {
  position: relative;
  z-index: 2;
}

.now-widget:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent-border);
}

.now-icon {
  font-size: 3rem;
  flex-shrink: 0;
  filter: drop-shadow(0 4px 10px rgba(37, 99, 235, 0.20));
}

.now-text {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 0;
  flex: 1;
}

.now-title {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: clamp(1.25rem, 1.8vw, 1.6rem);
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1.2;
}

.now-line {
  font-size: clamp(1rem, 1.2vw, 1.1rem);
  color: var(--text-muted);
  font-weight: 500;
}

.now-line-dim {
  font-size: 0.95rem;
  color: var(--text-dim);
}

/* ── Новости колледжа ── */
.news-section {
  margin-top: 2.5rem;
}

.news-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
}

.news-header h2 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 0;
}

.news-all-link {
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  padding: 0.45rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  background: var(--surface);
  transition: background var(--transition), border-color var(--transition), color var(--transition), transform var(--transition);
}

.news-all-link:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  color: var(--text);
  transform: translateX(2px);
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.news-card {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: inherit;
  transition: background var(--transition), border-color var(--transition), transform var(--transition), box-shadow var(--transition);
  box-shadow: var(--shadow-sm);
  align-items: flex-start;
  min-height: 140px;
}

.news-card:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}

.news-icon {
  font-size: 2rem;
  flex-shrink: 0;
  line-height: 1;
}

.news-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.news-date {
  font-size: 0.8rem;
  color: var(--text-dim);
  font-weight: 500;
  text-transform: lowercase;
}

.news-title {
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--text);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-desc {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-muted);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ── Ticker (если используется) ── */
.ticker {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 1rem 0;
  overflow: hidden;
  margin: 2rem 0;
  border-radius: var(--radius);
}

.ticker-content {
  display: inline-block;
  white-space: nowrap;
  animation: scroll 30s linear infinite;
  font-size: 1rem;
  padding-left: 100%;
  font-weight: 500;
  color: var(--text-muted);
}

@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-100%); }
}

/* ── Плавающая кнопка доступности ── */
.accessibility-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--surface-strong);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border-strong);
  color: var(--text);
  font-size: 1.75rem;
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: transform var(--transition-slow), background var(--transition), box-shadow var(--transition);
  z-index: 1000;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.accessibility-button:hover {
  transform: scale(1.08);
  background: var(--surface-hover);
  box-shadow: var(--shadow-lg);
}

.accessibility-button.active {
  background: var(--success-soft);
  border-color: rgba(52, 211, 153, 0.5);
  box-shadow: var(--shadow), 0 0 24px rgba(52, 211, 153, 0.3);
}

/* ========== РЕЖИМ ДОСТУПНОСТИ ========== */
/* Прижимаем интерактивные блоки к нижней трети экрана,
   чтобы пользователю на коляске было удобнее дотянуться. */
.home.accessibility-active {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-bottom: 7rem;
}

.home.accessibility-active .top-section { order: 1; margin-bottom: 1rem; padding-top: 1rem; flex: 0 0 auto; }
.home.accessibility-active .datetime-widget-top { display: block; animation: slideDown 0.6s var(--ease); }
.home.accessibility-active h1 { font-size: clamp(1.75rem, 3vw, 2.2rem); margin-bottom: 0.5rem; }
.home.accessibility-active .subtitle { font-size: 1rem; margin-bottom: 1rem; }

.home.accessibility-active .middle-section {
  order: 2;
  flex: 1 1 auto;
  min-height: 8vh;
  background: radial-gradient(ellipse at center, rgba(37,99,235,0.06) 0%, transparent 70%);
}

.home.accessibility-active .bottom-section {
  order: 3;
  flex: 0 0 auto;
  animation: slideUp 0.6s var(--ease);
}
.home.accessibility-active .bottom-widgets { display: none; }

.home.accessibility-active .contact-info {
  order: 1;
  margin-bottom: 1.5rem;
  padding: 1.75rem;
  animation: slideUp 0.6s var(--ease);
}

.home.accessibility-active .contact-info h2 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.home.accessibility-active .contact-grid { gap: 1rem; }
.home.accessibility-active .contact-item { padding: 0.9rem; }
.home.accessibility-active .features { order: 2; margin-top: 0; margin-bottom: 6rem; gap: 1.25rem; }
.home.accessibility-active .feature-card { min-height: 220px; padding: 2rem 1.5rem; }
.home.accessibility-active .feature-icon { width: 72px; height: 72px; }
.home.accessibility-active .feature-card h2 { font-size: 1.5rem; }
.home.accessibility-active .feature-card p { font-size: 0.95rem; }

@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 900px) {
  .bottom-widgets { grid-template-columns: 1fr; }
  .contact-info { padding: 1.75rem; }
}
</style>

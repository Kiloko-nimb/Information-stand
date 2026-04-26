<template>
  <div class="home" :class="{ 'accessibility-active': accessibilityMode }">
    <div class="top-section">
      <h1>Добро пожаловать в ККРИТ!</h1>
      <p class="subtitle">Красноярский колледж радиоэлектроники и информационных технологий</p>

      <div class="widget datetime-widget-top">
        <div class="time">{{ currentTime }}</div>
        <div class="date">{{ currentDate }}</div>
      </div>

      <div v-if="nowWidget" class="now-widget" @click="$router.push('/schedule')">
        <div class="now-icon">{{ nowWidget.icon }}</div>
        <div class="now-text">
          <div class="now-title">{{ nowWidget.title }}</div>
          <div v-if="nowWidget.line1" class="now-line">{{ nowWidget.line1 }}</div>
          <div v-if="nowWidget.line2" class="now-line now-line-dim">{{ nowWidget.line2 }}</div>
        </div>
      </div>

      <transition name="ticker-fade" mode="out-in">
        <a
          v-if="tickerNews"
          :key="tickerNews.id"
          class="ticker-plate"
          :href="tickerNews.source_url || 'https://kraskrit.ru/news/'"
          target="_blank"
          rel="noopener"
          :title="tickerNews.title"
        >
          <span class="ticker-icon">{{ tickerNews.icon || '📰' }}</span>
          <span class="ticker-title">{{ tickerNews.title }}</span>
        </a>
      </transition>
    </div>

    <div class="middle-section">
      <!-- Резервное вертикальное пространство между шапкой и контактами -->
    </div>

    <div class="bottom-section">
      <div class="contact-info">
        <h2>Контактная информация</h2>
        <div class="contact-grid">
          <div class="contact-item">
            <span class="icon">📍</span>
            <div>
              <strong>Адреса:</strong>
              <p>пр. Красноярский рабочий, 156</p>
              <p>пр. Свободный, 67</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="icon">📞</span>
            <div>
              <strong>Телефон:</strong>
              <p>8 (391) 218-17-99</p>
              <p class="additional-info">(доб. 207, 216, 208)</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="icon">💬</span>
            <div>
              <strong>Приемная комиссия 2026:</strong>
              <p>8-929-332-29-43</p>
              <p>8-933-327-02-09</p>
              <p>8-391-298-46-46</p>
              <p class="additional-info">kraskritpk@yandex.ru</p>
            </div>
          </div>
          <div class="contact-item">
            <span class="icon">🌐</span>
            <div>
              <strong>Сайт и обратная связь:</strong>
              <div class="qr-codes">
                <div class="qr-item">
                  <img v-if="qrWebsite" :src="qrWebsite" alt="QR код сайта" class="qr-code" />
                  <p class="qr-label">kraskrit.ru</p>
                </div>
                <div class="qr-item">
                  <img v-if="qrFeedback" :src="qrFeedback" alt="QR код формы" class="qr-code" />
                  <p class="qr-label">Форма обратной связи</p>
                </div>
              </div>
            </div>
          </div>
          <div class="contact-item">
            <span class="icon">📱</span>
            <div>
              <strong>Мы в соцсетях:</strong>
              <div class="social-list">
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
                  class="social-link social-link--site"
                  href="https://kraskrit.ru/"
                  target="_blank"
                  rel="noopener"
                  aria-label="Официальный сайт"
                >
                  <span class="social-badge">🌍</span>
                  <span class="social-text">kraskrit.ru</span>
                </a>
              </div>
              <div class="qr-codes">
                <div class="qr-item">
                  <img v-if="qrVK" :src="qrVK" alt="QR код VK" class="qr-code" />
                  <p class="qr-label">VK</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-widgets">
        <div class="widget datetime-widget">
          <div class="time">{{ currentTime }}</div>
          <div class="date">{{ currentDate }}</div>
        </div>

        <div class="widget applicant-widget">
          <h3>🎓 Абитуриенту 2026</h3>
          <div class="countdown-timer">
            <div class="countdown-label">До начала приемной кампании осталось:</div>
            <div class="countdown-value">{{ daysUntilAdmission }} дней</div>
          </div>
          <div class="applicant-actions">
            <button class="applicant-btn" @click="showPassingScores">
              <span class="btn-icon">📊</span>
              <span class="btn-text">Проходные баллы</span>
            </button>
            <button class="applicant-btn" @click="showSpecialties">
              <span class="btn-icon">🎯</span>
              <span class="btn-text">Специальности</span>
            </button>
            <button class="applicant-btn" @click="showApplicationQR">
              <span class="btn-icon">📱</span>
              <span class="btn-text">Подать документы</span>
            </button>
          </div>
        </div>
      </div>

      <div class="fun-facts-widget">
        <div class="fun-fact">
          <span class="fact-icon">💡</span>
          <span class="fact-text">{{ currentFact }}</span>
        </div>
      </div>

      <div class="features">
        <div class="feature-card" @click="$router.push('/schedule')">
          <div class="feature-icon">📅</div>
          <h2>Расписание</h2>
          <p>Найдите расписание по группе или преподавателю</p>
        </div>

        <div class="feature-card" @click="$router.push('/staff')">
          <div class="feature-icon">👥</div>
          <h2>Сотрудники</h2>
          <p>Информация о преподавателях и администрации</p>
        </div>

        <div class="feature-card" @click="$router.push('/map')">
          <div class="feature-icon">🗺️</div>
          <h2>Навигация</h2>
          <p>Найдите нужный кабинет на карте колледжа</p>
        </div>
      </div>

      <section v-if="newsItems.length > 0" class="news-section">
        <div class="news-header">
          <h2>📰 Новости колледжа</h2>
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
            <div class="news-icon">{{ item.icon || '📰' }}</div>
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
      <span v-if="!accessibilityMode">♿</span>
      <span v-else>✖</span>
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { generateQRCode } from '../utils/qrGenerator'
import { fetchNews } from '../services/newsService'
import api from '../services/api'

export default {
  name: 'Home',
  setup() {
    const currentTime = ref('')
    const currentDate = ref('')
    const qrWebsite = ref('')
    const qrFeedback = ref('')
    const qrVK = ref('')
    const accessibilityMode = ref(false)
    const daysUntilAdmission = ref(0)
    const newsItems = ref([])
    const tickerIndex = ref(0)
    const newsCards = computed(() => newsItems.value.slice(0, 3))
    const tickerNews = computed(() => {
      if (newsItems.value.length === 0) return null
      return newsItems.value[tickerIndex.value % newsItems.value.length] || null
    })
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
    }

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
        <div style="background:linear-gradient(160deg,#151a32 0%,#0f1224 100%);padding:2.25rem;border-radius:24px;max-width:680px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 30px 80px rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.08);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#eceef5;margin:0 0 1.5rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">📊 Проходные баллы</h2>
          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.08);">
            <p style="color:rgba(236,238,245,0.88);line-height:1.7;font-size:1rem;margin:0;">
              В ККРИТ нет вступительных экзаменов — зачисление проходит по конкурсу <strong style="color:#fbbf24;">среднего балла аттестата</strong>.<br><br>
              На специальности «Пожарная безопасность» — дополнительно психологическое тестирование и нормативы физподготовки.
            </p>
          </div>
          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#eceef5;margin:0 0 0.9rem;font-size:1.1rem;font-weight:700;">📈 Средний балл аттестата 2025 (справочно)</h3>
            <div style="color:rgba(236,238,245,0.85);line-height:1.8;font-size:0.95rem;">
              • Бюджет (ИТ-специальности): <strong style="color:#fbbf24;">4.0–4.5</strong><br>
              • Бюджет (экономика, электроника): <strong style="color:#fbbf24;">3.8–4.2</strong><br>
              • Платные места: <strong style="color:#fbbf24;">от 3.0</strong><br><br>
              <span style="color:rgba(236,238,245,0.55);font-size:0.85rem;">Цифры ориентировочные — точный проходной балл формируется по итогам конкурса.</span>
            </div>
          </div>
          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.5rem;border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#eceef5;margin:0 0 0.9rem;font-size:1.1rem;font-weight:700;">📆 Сроки приёма 2026</h3>
            <div style="color:rgba(236,238,245,0.85);line-height:1.8;font-size:0.95rem;">
              • Начало приёма: <strong style="color:#fbbf24;">15 июня 2026</strong><br>
              • Окончание (основное): <strong style="color:#fbbf24;">14 августа 2026</strong><br>
              • Пожарная безопасность: <strong style="color:#fbbf24;">до 10 августа 2026</strong><br>
              • При наличии свободных мест: <strong style="color:#fbbf24;">до 25 ноября 2026</strong>
            </div>
          </div>
          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:0.9rem 2rem;background:linear-gradient(135deg,#8b7bff 0%,#22d3ee 100%);color:#0b0d1c;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(139,123,255,0.45)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    const showSpecialties = () => {
      const modal = document.createElement('div')
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:flex-start;justify-content:center;z-index:9999;overflow-y:auto;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(160deg,#151a32 0%,#0f1224 100%);padding:2.25rem;border-radius:24px;max-width:900px;width:100%;box-shadow:0 30px 80px rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.08);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#eceef5;margin:0 0 0.5rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">Специальности ККРИТ 2026/27</h2>
          <p style="color:rgba(236,238,245,0.6);text-align:center;margin:0 0 1.5rem;font-size:0.92rem;">Поступление на базе 9 классов, срок обучения в скобках</p>

          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#eceef5;margin:0 0 0.9rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.15rem;font-weight:700;">📍 пр. Красноярский рабочий, 156 — IT и экономика</h3>
            <div style="color:rgba(236,238,245,0.82);line-height:1.75;font-size:0.95rem;">
              <strong style="color:#fbbf24;">Бюджет:</strong><br>
              • 38.02.01 Экономика и бухгалтерский учёт — 25 мест (2 г. 10 мес.)<br>
              • 38.02.07 Банковское дело — 25 мест (2 г. 10 мес.)<br><br>
              <strong style="color:#fbbf24;">Платно:</strong><br>
              • 09.02.09 Веб-разработка — 25 мест (2 г. 10 мес.)<br>
              • 09.02.09 Веб-разработка (после 11 кл.) — 25 мест (1 г. 10 мес.)<br>
              • 09.02.10 Разработка игр, AR/VR — 25 мест (3 г. 10 мес.)<br>
              • 09.02.11 Разработка ПО (программист) — 25 мест (3 г. 10 мес.)<br>
              • 09.02.13 Искусственный интеллект — 25 мест (3 г. 10 мес.)
            </div>
          </div>

          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#eceef5;margin:0 0 0.9rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.15rem;font-weight:700;">📍 пр. Свободный, 67 — инфраструктура и электроника</h3>
            <div style="color:rgba(236,238,245,0.82);line-height:1.75;font-size:0.95rem;">
              <strong style="color:#fbbf24;">Бюджет:</strong><br>
              • 09.02.01 Компьютерные системы и комплексы — 50 мест (3 г. 10 мес.)<br>
              • 09.02.06 Сетевое и системное администрирование — 50 мест (3 г. 10 мес.)<br>
              • 10.02.05 Информационная безопасность АС — 25 мест (3 г. 10 мес.)<br>
              • 11.02.16 Монтаж электронных приборов — 50 мест (3 г. 10 мес.)<br>
              • 20.02.04 Пожарная безопасность — 50 мест (3 г. 10 мес.)<br><br>
              <strong style="color:#fbbf24;">Платно:</strong><br>
              • 09.02.01 Компьютерные системы и комплексы — 25 мест<br>
              • 09.02.06 Сетевое и системное администрирование — 25 мест<br>
              • 10.02.05 Информационная безопасность АС — 25 мест<br>
              • 20.02.04 Пожарная безопасность (после 11 кл.) — 25 мест (2 г. 10 мес.)
            </div>
          </div>

          <div style="background:linear-gradient(135deg,rgba(139,123,255,0.12),rgba(34,211,238,0.08));padding:1.25rem 1.5rem;border-radius:18px;margin-bottom:1.5rem;border:1px solid rgba(139,123,255,0.25);color:rgba(236,238,245,0.92);font-size:0.95rem;line-height:1.7;">
            📊 <strong>Итого на 2026/27:</strong> 225 бюджетных + 275 платных мест. <br>Три специальности появились впервые в этом году: <strong style="color:#fbbf24;">ИИ, игры/AR‑VR и веб-разработка</strong>.
          </div>

          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:0.9rem 2rem;background:linear-gradient(135deg,#8b7bff 0%,#22d3ee 100%);color:#0b0d1c;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(139,123,255,0.45)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    const showApplicationQR = async () => {
      const qr = await generateQRCode('https://kraskrit.ru/abitur/')
      const modal = document.createElement('div')
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:flex-start;justify-content:center;z-index:9999;overflow-y:auto;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(160deg,#151a32 0%,#0f1224 100%);padding:2.25rem;border-radius:24px;max-width:760px;width:100%;box-shadow:0 30px 80px rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.08);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#eceef5;margin:0 0 1.5rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">📱 Подать документы</h2>

          <div style="display:grid;grid-template-columns:240px 1fr;gap:1.5rem;background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.08);align-items:center;">
            <div style="text-align:center;">
              <img src="${qr}" style="width:220px;height:220px;border-radius:14px;background:#fff;padding:8px;"/>
              <p style="color:rgba(236,238,245,0.7);font-size:0.85rem;margin:0.6rem 0 0;">Отсканируйте —<br>откроется раздел «Абитуриенту»</p>
            </div>
            <div style="color:rgba(236,238,245,0.88);font-size:0.97rem;line-height:1.7;">
              <strong style="color:#fbbf24;">Приём документов:</strong><br>
              c 15 июня по 14 августа 2026<br>
              Пожарная безопасность — до 10 августа<br><br>
              <strong style="color:#fbbf24;">Адрес приёмной комиссии:</strong><br>
              пр. Свободный, 67<br>
              пн–чт 09:00–15:30, пт 09:00–12:00<br><br>
              <strong style="color:#fbbf24;">Телефоны:</strong><br>
              8-929-332-29-43<br>
              8-933-327-02-09<br>
              8-391-298-46-46<br>
              <strong style="color:#fbbf24;">E-mail:</strong> kraskritpk@yandex.ru
            </div>
          </div>

          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#eceef5;margin:0 0 0.9rem;font-size:1.1rem;font-weight:700;">📋 Перечень документов</h3>
            <div style="color:rgba(236,238,245,0.85);line-height:1.85;font-size:0.95rem;">
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

          <div style="background:linear-gradient(135deg,rgba(34,211,238,0.12),rgba(139,123,255,0.08));padding:1.25rem 1.5rem;border-radius:18px;margin-bottom:1.5rem;border:1px solid rgba(34,211,238,0.25);color:rgba(236,238,245,0.92);font-size:0.93rem;line-height:1.7;">
            ℹ️ Заявление можно подать <strong>лично</strong> на пр. Свободный 67, <strong>почтой</strong> или <strong>через Госуслуги</strong> (в тестовом режиме).<br>Для зачисления оригинал аттестата нужно сдать до <strong>14 августа 2026</strong>.
          </div>

          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:0.9rem 2rem;background:linear-gradient(135deg,#8b7bff 0%,#22d3ee 100%);color:#0b0d1c;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(139,123,255,0.45)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    let nowInterval = null
    let tickerInterval = null

    const rotateTicker = () => {
      if (newsItems.value.length === 0) return
      tickerIndex.value = (tickerIndex.value + 1) % newsItems.value.length
    }

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
      tickerInterval = setInterval(rotateTicker, 54000)
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
      if (tickerInterval) {
        clearInterval(tickerInterval)
      }
    })

    return {
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
      tickerNews,
      formatNewsDate,
      nowWidget
    }
  }
}
</script>


<style scoped>
.home {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  padding-bottom: 5rem;
}

.top-section {
  text-align: center;
  padding: 3rem 0 2rem;
  transition: all 0.6s var(--ease);
}

.middle-section {
  min-height: 0;
  transition: min-height 0.6s var(--ease);
}

.bottom-section {
  transform: translateY(0);
}

/* ── Заголовок ── */
h1 {
  font-family: var(--font-display);
  font-size: clamp(2rem, 4.5vw, 3.2rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  margin-bottom: 0.75rem;
  background: linear-gradient(135deg, #ffffff 0%, #c4c6d8 50%, #8b7bff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
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
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  text-align: left;
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
  margin-top: 0.75rem;
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
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
  margin-bottom: 0.75rem;
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
  background: linear-gradient(135deg, #8b7bff 0%, #22d3ee 100%);
  color: #fff;
}

.social-link--site .social-badge {
  background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
  color: #fff;
}

.social-text {
  word-break: break-word;
}

/* ── Нижние виджеты ── */
.bottom-widgets {
  display: grid;
  grid-template-columns: 1fr 1.8fr;
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
  background: linear-gradient(135deg, rgba(139, 123, 255, 0.08), rgba(34, 211, 238, 0.06));
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
  background: linear-gradient(135deg, rgba(139, 123, 255, 0.12), rgba(244, 114, 182, 0.08));
  border-color: rgba(139, 123, 255, 0.25);
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
}

.btn-icon {
  font-size: 1.5rem;
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
  font-size: 4rem;
  margin-bottom: 1.25rem;
  transition: transform var(--transition-slow);
  filter: drop-shadow(0 4px 12px rgba(139, 123, 255, 0.3));
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(-4deg);
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

/* ── Бегущая строка новостей (статичная, смена каждые 54с) ── */
.ticker-plate {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: 1.25rem;
  padding: 0.55rem 1.1rem;
  border-radius: 999px;
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 0.95rem;
  text-decoration: none;
  max-width: min(680px, calc(100% - 2rem));
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition), border-color var(--transition), box-shadow var(--transition);
}

.ticker-plate:hover {
  transform: translateY(-1px);
  border-color: var(--border-hover);
  box-shadow: var(--shadow), var(--accent-glow);
}

.ticker-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.ticker-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.ticker-fade-enter-active,
.ticker-fade-leave-active {
  transition: opacity 380ms ease, transform 380ms ease;
}
.ticker-fade-enter-from,
.ticker-fade-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

/* ── Виджет «Сейчас идёт» ──
   Находится внутри .top-section, под заголовком, чтобы визуально
   не налезать на блок контактов ниже. */
.now-widget {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1rem 1.5rem;
  margin: 1.5rem auto 0.5rem;
  max-width: 720px;
  background: var(--surface);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
}

.now-widget:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow), var(--accent-glow);
  border-color: var(--border-hover);
}

.now-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.now-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.now-title {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--text);
}

.now-line {
  font-size: 0.95rem;
  color: var(--text-muted);
}

.now-line-dim {
  font-size: 0.85rem;
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
  background: radial-gradient(ellipse at center, rgba(139,123,255,0.08) 0%, transparent 70%);
}

.home.accessibility-active .bottom-section {
  order: 3;
  flex: 0 0 auto;
  animation: slideUp 0.6s var(--ease);
}
.home.accessibility-active .bottom-widgets { display: none; }
.home.accessibility-active .ticker { display: none; }

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
.home.accessibility-active .feature-icon { font-size: 3.25rem; }
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

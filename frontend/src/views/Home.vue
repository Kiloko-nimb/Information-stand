<template>
  <div class="home" :class="{ 'accessibility-active': accessibilityMode }">
    <div class="top-section">
      <h1>Добро пожаловать в ККРИТ!</h1>
      <p class="subtitle">Красноярский колледж радиоэлектроники и информационных технологий</p>

      <div class="widget datetime-widget-top">
        <div class="time">{{ currentTime }}</div>
        <div class="date">{{ currentDate }}</div>
      </div>
    </div>

    <div class="middle-section">
      <!-- Декоративное пространство -->
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
            v-for="item in newsItems"
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
import { ref, onMounted, onUnmounted } from 'vue'
import { generateQRCode } from '../utils/qrGenerator'
import { fetchNews } from '../services/newsService'

export default {
  name: 'Home',
  setup() {
    const currentTime = ref('')
    const currentDate = ref('')
    const qrWebsite = ref('')
    const qrFeedback = ref('')
    const accessibilityMode = ref(false)
    const daysUntilAdmission = ref(0)
    const newsItems = ref([])

    const loadNews = async () => {
      try {
        const data = await fetchNews(3)
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
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(160deg,#151a32 0%,#0f1224 100%);padding:2.25rem;border-radius:24px;max-width:600px;width:100%;box-shadow:0 30px 80px rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.08);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#eceef5;margin:0 0 1.5rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">📊 Проходные баллы 2025</h2>
          <div style="background:rgba(255,255,255,0.04);padding:1.75rem;border-radius:18px;margin-bottom:1.5rem;border:1px solid rgba(255,255,255,0.08);">
            <p style="color:rgba(236,238,245,0.88);line-height:1.7;font-size:1rem;text-align:center;margin:0;">
              Проходные баллы формируются по результатам конкурса аттестатов.<br><br>
              <strong style="color:#fbbf24;">Средний балл аттестата 2025:</strong><br>
              Бюджетные места: от 3.8 до 4.5<br>
              Платные места: от 3.0<br><br>
              <span style="font-size:0.9rem;color:rgba(236,238,245,0.55);">Точные проходные баллы будут известны после завершения приемной кампании</span>
            </p>
          </div>
          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:0.9rem 2rem;background:linear-gradient(135deg,#8b7bff 0%,#22d3ee 100%);color:#0b0d1c;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(139,123,255,0.45)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    const showSpecialties = () => {
      const modal = document.createElement('div')
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;overflow-y:auto;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(160deg,#151a32 0%,#0f1224 100%);padding:2.25rem;border-radius:24px;max-width:900px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 30px 80px rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.08);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#eceef5;margin:0 0 1.75rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">Специальности ККРИТ 2026</h2>

          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#eceef5;margin:0 0 0.9rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.15rem;font-weight:700;">📍 пр. Красноярский рабочий, 156</h3>
            <div style="color:rgba(236,238,245,0.82);line-height:1.75;font-size:0.95rem;">
              <strong style="color:#fbbf24;">Бюджет:</strong><br>
              • 38.02.01 Экономика и бухгалтерский учет (25 мест)<br>
              • 38.02.07 Банковское дело (25 мест)<br><br>
              <strong style="color:#fbbf24;">Платно:</strong><br>
              • 09.02.09 Веб-разработка (25 мест)<br>
              • 09.02.10 Разработка компьютерных игр, AR/VR (25 мест)<br>
              • 09.02.11 Разработка ПО (25 мест)<br>
              • 09.02.13 Искусственный интеллект (25 мест)
            </div>
          </div>

          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.25rem;border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#eceef5;margin:0 0 0.9rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.15rem;font-weight:700;">📍 пр. Свободный, 67</h3>
            <div style="color:rgba(236,238,245,0.82);line-height:1.75;font-size:0.95rem;">
              <strong style="color:#fbbf24;">Бюджет:</strong><br>
              • 09.02.01 Компьютерные системы и комплексы (50 мест)<br>
              • 09.02.06 Сетевое и системное администрирование (50 мест)<br>
              • 10.02.05 Информационная безопасность (25 мест)<br>
              • 11.02.16 Монтаж электронных приборов (50 мест)<br><br>
              <strong style="color:#fbbf24;">Платно:</strong><br>
              • 20.02.04 Пожарная безопасность (50 мест)
            </div>
          </div>

          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;margin-top:0.75rem;padding:0.9rem 2rem;background:linear-gradient(135deg,#8b7bff 0%,#22d3ee 100%);color:#0b0d1c;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(139,123,255,0.45)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    const showApplicationQR = async () => {
      const qr = await generateQRCode('https://kraskrit.ru/abitur/')
      const modal = document.createElement('div')
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(160deg,#151a32 0%,#0f1224 100%);padding:2.25rem;border-radius:24px;max-width:600px;width:100%;box-shadow:0 30px 80px rgba(0,0,0,0.6);border:1px solid rgba(255,255,255,0.08);font-family:'Inter',system-ui,sans-serif;">
          <h2 style="color:#eceef5;margin:0 0 1.5rem;font-family:'Manrope','Inter',system-ui,sans-serif;font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;text-align:center;">📱 Подать документы</h2>
          <div style="background:rgba(255,255,255,0.04);padding:1.5rem;border-radius:18px;margin-bottom:1.5rem;text-align:center;border:1px solid rgba(255,255,255,0.08);">
            <img src="${qr}" style="width:240px;height:240px;margin-bottom:1.25rem;border-radius:14px;background:#fff;padding:8px;"/>
            <p style="color:rgba(236,238,245,0.88);font-size:1rem;line-height:1.7;margin:0;">
              <strong style="color:#fbbf24;">Прием документов:</strong><br>
              с 15 июня по 14 августа 2026<br><br>
              <strong style="color:#fbbf24;">Адрес приемной комиссии:</strong><br>
              пр. Свободный, 67<br><br>
              <strong style="color:#fbbf24;">Телефоны:</strong><br>
              8-929-332-29-43<br>
              8-933-327-02-09<br>
              8-391-298-46-46
            </p>
          </div>
          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:0.9rem 2rem;background:linear-gradient(135deg,#8b7bff 0%,#22d3ee 100%);color:#0b0d1c;border:none;border-radius:999px;cursor:pointer;font-size:1rem;font-weight:700;transition:transform .2s ease,box-shadow .2s ease;" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 0 24px rgba(139,123,255,0.45)'" onmouseout="this.style.transform='';this.style.boxShadow=''">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    onMounted(() => {
      updateDateTime()
      timeInterval = setInterval(updateDateTime, 1000)
      generateQRCodes()
      calculateDaysUntilAdmission()
      loadNews()
      rotateFact()
      factInterval = setInterval(rotateFact, 18000) // Меняем факт каждые 18 секунд
    })

    onUnmounted(() => {
      if (timeInterval) {
        clearInterval(timeInterval)
      }
      if (factInterval) {
        clearInterval(factInterval)
      }
    })

    return {
      currentTime,
      currentDate,
      qrWebsite,
      qrFeedback,
      accessibilityMode,
      toggleAccessibilityMode,
      daysUntilAdmission,
      currentFact,
      showPassingScores,
      showSpecialties,
      showApplicationQR,
      newsItems,
      formatNewsDate
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

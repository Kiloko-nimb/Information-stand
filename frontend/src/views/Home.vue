<template>
  <div class="home">
    <h1>Добро пожаловать в ККРИТ!</h1>
    <p class="subtitle">Красноярский колледж радиоэлектроники и информационных технологий</p>

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
            <strong>У Вас остались вопросы?</strong>
            <p>8 (391) 218-14-99</p>
            <p>priem@kraskrit.ru</p>
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
            <p class="qr-hint">📱 Наведите камеру смартфона для перехода</p>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-widgets">
      <div class="widget datetime-widget">
        <div class="time">{{ currentTime }}</div>
        <div class="date">{{ currentDate }}</div>
      </div>

      <div class="widget news-widget">
        <h3>📰 Новости колледжа</h3>
        <div class="news-items">
          <div class="news-card">
            <div class="news-icon">🎓</div>
            <div class="news-content">
              <h4>День открытых дверей</h4>
              <p>15 мая 2026 года приглашаем абитуриентов</p>
            </div>
          </div>
          <div class="news-card">
            <div class="news-icon">🏆</div>
            <div class="news-content">
              <h4>Победа в конкурсе</h4>
              <p>Студенты заняли 1 место в региональном хакатоне</p>
            </div>
          </div>
          <div class="news-card">
            <div class="news-icon">📚</div>
            <div class="news-content">
              <h4>Новые специальности</h4>
              <p>Открыт набор на направление "Искусственный интеллект"</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="ticker">
      <div class="ticker-content">
        ⚠️ Внимание! 15 мая состоится день открытых дверей • 📢 Запись на подготовительные курсы открыта • 🎉 Поздравляем победителей регионального хакатона • 📅 Расписание экзаменов доступно в разделе "Расписание"
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

    <button class="accessibility-button" @click="toggleAccessibilityMode" :class="{ active: accessibilityMode }">
      ♿
    </button>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { generateQRCode } from '../utils/qrGenerator'

export default {
  name: 'Home',
  setup() {
    const currentTime = ref('')
    const currentDate = ref('')
    const qrWebsite = ref('')
    const qrFeedback = ref('')
    const accessibilityMode = ref(false)
    let timeInterval = null

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
      document.body.classList.toggle('accessibility-mode', accessibilityMode.value)
    }

    onMounted(() => {
      updateDateTime()
      timeInterval = setInterval(updateDateTime, 1000)
      generateQRCodes()
    })

    onUnmounted(() => {
      if (timeInterval) {
        clearInterval(timeInterval)
      }
    })

    return {
      currentTime,
      currentDate,
      qrWebsite,
      qrFeedback,
      accessibilityMode,
      toggleAccessibilityMode
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 3rem;
}

.contact-info {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 16px;
  padding: 3rem;
  margin-bottom: 3rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
  transition: transform 0.3s, box-shadow 0.3s;
  min-height: 320px;
}

.contact-info:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.contact-info h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  text-align: left;
}

.contact-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 1rem;
  border-radius: 8px;
  transition: background 0.3s;
}

.contact-item:hover {
  background: rgba(102, 126, 234, 0.05);
}

.contact-item .icon {
  font-size: 2.5rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.contact-item strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 0.3rem;
}

.contact-item p {
  color: #7f8c8d;
  margin: 0;
}

.contact-item a {
  color: #3498db;
  text-decoration: none;
}

.contact-item a:hover {
  text-decoration: underline;
}

.additional-info {
  font-size: 0.9rem;
  color: #95a5a6 !important;
  font-style: italic;
}

.qr-codes {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
  flex-wrap: wrap;
  align-items: flex-start;
}

.qr-item {
  text-align: center;
  flex: 1;
  min-width: 120px;
}

.qr-code {
  width: 120px;
  height: 120px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 4px;
  background: white;
}

.qr-label {
  font-size: 0.9rem;
  margin-top: 0.5rem;
  color: #2c3e50 !important;
  font-weight: 500;
  line-height: 1.3;
}

.qr-hint {
  font-size: 1rem;
  color: #3498db !important;
  margin-top: 1rem;
  font-style: normal;
  font-weight: 500;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  margin-bottom: 3rem;
}

.feature-card {
  background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
  border: none;
  border-radius: 20px;
  padding: 3rem 2.5rem;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 6px 25px rgba(0,0,0,0.1);
  position: relative;
  overflow: hidden;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.feature-card::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.3);
  background: linear-gradient(180deg, #ffffff 0%, #f0f4ff 100%);
}

.feature-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}

.feature-card h2 {
  font-size: 2rem;
  margin-bottom: 0.8rem;
  color: #2c3e50;
  font-weight: 600;
}

.feature-card p {
  color: #5a6c7d;
  font-size: 1.1rem;
  line-height: 1.5;
}

.bottom-widgets {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin: 3rem 0;
}

.widget {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.datetime-widget {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.time {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-variant-numeric: tabular-nums;
}

.date {
  font-size: 1.2rem;
  opacity: 0.9;
  text-transform: capitalize;
}

.news-widget h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.news-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.news-card {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  transition: transform 0.2s;
}

.news-card:hover {
  transform: translateX(5px);
}

.news-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.news-content h4 {
  font-size: 1rem;
  color: #2c3e50;
  margin: 0 0 0.3rem 0;
}

.news-content p {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0;
}

.ticker {
  background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
  color: white;
  padding: 1rem 0;
  overflow: hidden;
  margin: 2rem 0;
  border-radius: 8px;
}

.ticker-content {
  display: inline-block;
  white-space: nowrap;
  animation: scroll 30s linear infinite;
  font-size: 1.1rem;
  padding-left: 100%;
}

@keyframes scroll {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-100%);
  }
}

.accessibility-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-size: 2.5rem;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.accessibility-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6);
}

.accessibility-button.active {
  background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
  box-shadow: 0 4px 20px rgba(39, 174, 96, 0.4);
}

/* Режим доступности */
body.accessibility-mode .contact-info {
  display: none;
}

body.accessibility-mode .features {
  margin-top: 2rem;
}

body.accessibility-mode .bottom-widgets {
  order: 10;
  margin-top: 3rem;
}
</style>

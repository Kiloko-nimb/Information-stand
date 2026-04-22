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

export default {
  name: 'Home',
  setup() {
    const currentTime = ref('')
    const currentDate = ref('')
    const qrWebsite = ref('')
    const qrFeedback = ref('')
    const accessibilityMode = ref(false)
    const daysUntilAdmission = ref(0)
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
        <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);padding:2.5rem;border-radius:25px;max-width:600px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,0.5);">
          <h2 style="color:white;margin-bottom:1.5rem;font-size:2rem;text-align:center;">📊 Проходные баллы 2025</h2>
          <div style="background:rgba(255,255,255,0.15);padding:2rem;border-radius:20px;margin-bottom:1.5rem;">
            <p style="color:rgba(255,255,255,0.95);line-height:1.8;font-size:1.1rem;text-align:center;">
              Проходные баллы формируются по результатам конкурса аттестатов.<br><br>
              <strong style="color:#ffd700;">Средний балл аттестата 2025:</strong><br>
              Бюджетные места: от 3.8 до 4.5<br>
              Платные места: от 3.0<br><br>
              <span style="font-size:0.95rem;opacity:0.9;">Точные проходные баллы будут известны после завершения приемной кампании</span>
            </p>
          </div>
          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:1rem 2rem;background:rgba(255,255,255,0.25);color:white;border:2px solid rgba(255,255,255,0.4);border-radius:15px;cursor:pointer;font-size:1.1rem;font-weight:600;transition:all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.35)'" onmouseout="this.style.background='rgba(255,255,255,0.25)'">Закрыть</button>
        </div>
      `
      document.body.appendChild(modal)
      modal.onclick = (e) => { if (e.target === modal) modal.remove() }
    }

    const showSpecialties = () => {
      const modal = document.createElement('div')
      modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;overflow-y:auto;padding:2rem;'
      modal.innerHTML = `
        <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);padding:2.5rem;border-radius:25px;max-width:900px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.5);">
          <h2 style="color:white;margin-bottom:2rem;font-size:2rem;text-align:center;">Специальности ККРИТ 2026</h2>

          <div style="background:rgba(255,255,255,0.15);padding:1.5rem;border-radius:20px;margin-bottom:1.5rem;">
            <h3 style="color:#fff;margin-bottom:1rem;font-size:1.3rem;">📍 пр. Красноярский рабочий, 156</h3>
            <div style="color:rgba(255,255,255,0.95);line-height:1.8;font-size:1rem;">
              <strong style="color:#ffd700;">Бюджет:</strong><br>
              • 38.02.01 Экономика и бухгалтерский учет (25 мест)<br>
              • 38.02.07 Банковское дело (25 мест)<br><br>
              <strong style="color:#ffd700;">Платно:</strong><br>
              • 09.02.09 Веб-разработка (25 мест)<br>
              • 09.02.10 Разработка компьютерных игр, AR/VR (25 мест)<br>
              • 09.02.11 Разработка ПО (25 мест)<br>
              • 09.02.13 Искусственный интеллект (25 мест)
            </div>
          </div>

          <div style="background:rgba(255,255,255,0.15);padding:1.5rem;border-radius:20px;margin-bottom:1.5rem;">
            <h3 style="color:#fff;margin-bottom:1rem;font-size:1.3rem;">📍 пр. Свободный, 67</h3>
            <div style="color:rgba(255,255,255,0.95);line-height:1.8;font-size:1rem;">
              <strong style="color:#ffd700;">Бюджет:</strong><br>
              • 09.02.01 Компьютерные системы и комплексы (50 мест)<br>
              • 09.02.06 Сетевое и системное администрирование (50 мест)<br>
              • 10.02.05 Информационная безопасность (25 мест)<br>
              • 11.02.16 Монтаж электронных приборов (50 мест)<br><br>
              <strong style="color:#ffd700;">Платно:</strong><br>
              • 20.02.04 Пожарная безопасность (50 мест)
            </div>
          </div>

          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;margin-top:1rem;padding:1rem 2rem;background:rgba(255,255,255,0.25);color:white;border:2px solid rgba(255,255,255,0.4);border-radius:15px;cursor:pointer;font-size:1.1rem;font-weight:600;transition:all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.35)'" onmouseout="this.style.background='rgba(255,255,255,0.25)'">Закрыть</button>
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
        <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);padding:2.5rem;border-radius:25px;max-width:600px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,0.5);">
          <h2 style="color:white;margin-bottom:1.5rem;font-size:2rem;text-align:center;">📱 Подать документы</h2>
          <div style="background:rgba(255,255,255,0.15);padding:2rem;border-radius:20px;margin-bottom:1.5rem;text-align:center;">
            <img src="${qr}" style="width:250px;height:250px;margin-bottom:1.5rem;"/>
            <p style="color:white;font-size:1.1rem;line-height:1.6;margin-bottom:1rem;">
              <strong style="color:#ffd700;">Прием документов:</strong><br>
              с 15 июня по 14 августа 2026<br><br>
              <strong style="color:#ffd700;">Адрес приемной комиссии:</strong><br>
              пр. Свободный, 67<br><br>
              <strong style="color:#ffd700;">Телефоны:</strong><br>
              8-929-332-29-43<br>
              8-933-327-02-09<br>
              8-391-298-46-46
            </p>
          </div>
          <button onclick="this.parentElement.parentElement.remove()" style="width:100%;padding:1rem 2rem;background:rgba(255,255,255,0.25);color:white;border:2px solid rgba(255,255,255,0.4);border-radius:15px;cursor:pointer;font-size:1.1rem;font-weight:600;transition:all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.35)'" onmouseout="this.style.background='rgba(255,255,255,0.25)'">Закрыть</button>
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
      showApplicationQR
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  position: relative;
}

.top-section,
.middle-section,
.bottom-section {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.top-section {
  opacity: 1;
  transform: translateY(0);
}

.middle-section {
  min-height: 0;
  transition: min-height 0.8s ease;
}

.bottom-section {
  transform: translateY(0);
}

/* Виджет времени в верхней секции (скрыт по умолчанию) */
.datetime-widget-top {
  display: none;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 30px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  margin: 2rem auto;
  max-width: 400px;
  color: white;
  text-align: center;
}

h1 {
  font-size: 2.8rem;
  color: white;
  text-shadow: 0 4px 20px rgba(0,0,0,0.3);
  margin-bottom: 1rem;
  font-weight: 700;
  transition: all 0.8s ease;
}

.subtitle {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
  margin-bottom: 3rem;
  font-weight: 500;
  transition: all 0.8s ease;
}

.contact-info {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 30px;
  padding: 3.5rem;
  margin-bottom: 3rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 380px;
  transform: translateY(0);
  opacity: 1;
}

.contact-info:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.2);
}

.contact-info h2 {
  font-size: 2rem;
  color: white;
  margin-bottom: 2rem;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  text-align: left;
}

.contact-item {
  display: flex;
  gap: 1.2rem;
  align-items: flex-start;
  padding: 1.2rem;
  border-radius: 8px;
  transition: background 0.3s;
}

.contact-item:hover {
  background: rgba(102, 126, 234, 0.05);
}

.contact-item .icon {
  font-size: 3rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.contact-item strong {
  display: block;
  color: white;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 1.1rem;
}

.contact-item p {
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-size: 1.05rem;
  line-height: 1.6;
}

.contact-item a {
  color: #3498db;
  text-decoration: none;
}

.contact-item a:hover {
  text-decoration: underline;
}

.additional-info {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.8) !important;
  font-style: italic;
}

.qr-codes {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  margin-top: 1.2rem;
  justify-content: flex-start;
  align-items: flex-start;
}

.qr-item {
  text-align: center;
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.qr-code {
  width: 130px;
  height: 130px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 18px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.3s;
}

.qr-code:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.qr-label {
  font-size: 0.9rem;
  margin-top: 0.6rem;
  color: white !important;
  font-weight: 600;
  line-height: 1.3;
  max-width: 130px;
}

.qr-hint {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.95) !important;
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
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateY(0);
}

.feature-card {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 35px;
  padding: 3rem 2.5rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
  min-height: 300px;
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
  height: 8px;
  background: linear-gradient(90deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0.8) 100%);
  transform: scaleX(0);
  transition: transform 0.4s;
}

.feature-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  opacity: 0;
  transition: opacity 0.4s;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover::after {
  opacity: 1;
}

.feature-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.feature-icon {
  font-size: 5.5rem;
  margin-bottom: 1.2rem;
  filter: drop-shadow(0 6px 12px rgba(0,0,0,0.2));
  transition: transform 0.4s;
  z-index: 1;
}

.feature-card:hover .feature-icon {
  transform: scale(1.15) rotate(5deg);
}

.feature-card h2 {
  font-size: 2.2rem;
  margin-bottom: 0.8rem;
  color: white;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
  z-index: 1;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.15rem;
  line-height: 1.6;
  text-shadow: 0 1px 5px rgba(0,0,0,0.1);
  z-index: 1;
}

.bottom-widgets {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin: 3rem 0;
}

.widget {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 30px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s;
}

.widget:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.datetime-widget {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.time {
  font-size: 3.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-variant-numeric: tabular-nums;
  text-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.date {
  font-size: 1.3rem;
  opacity: 0.95;
  text-transform: capitalize;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.applicant-widget {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
}

.applicant-widget h3 {
  font-size: 1.8rem;
  color: white;
  margin-bottom: 1.5rem;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
  font-weight: 700;
}

.countdown-timer {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.countdown-label {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.8rem;
  font-weight: 500;
}

.countdown-value {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  text-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.applicant-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.applicant-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 15px;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1.05rem;
  font-weight: 600;
  text-align: left;
}

.applicant-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateX(8px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.btn-icon {
  font-size: 2rem;
  filter: drop-shadow(0 2px 5px rgba(0,0,0,0.2));
}

.btn-text {
  flex: 1;
}

.fun-facts-widget {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  padding: 1.5rem 2rem;
  margin: 2rem 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.5s ease;
}

.fun-fact {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  animation: fadeIn 0.8s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fact-icon {
  font-size: 3rem;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));
  flex-shrink: 0;
}

.fact-text {
  font-size: 1.15rem;
  color: white;
  line-height: 1.6;
  font-weight: 500;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

/* Скрываем виджет с фактами в режиме доступности */
.home.accessibility-active .fun-facts-widget {
  display: none;
}

.ticker {
  background: rgba(44, 62, 80, 0.3);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 1.2rem 0;
  overflow: hidden;
  margin: 2rem 0;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.ticker-content {
  display: inline-block;
  white-space: nowrap;
  animation: scroll 30s linear infinite;
  font-size: 1.15rem;
  padding-left: 100%;
  font-weight: 500;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
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
  width: 75px;
  height: 75px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.4);
  font-size: 2.8rem;
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.accessibility-button:hover {
  transform: scale(1.15) rotate(10deg);
  box-shadow: 0 12px 45px rgba(0, 0, 0, 0.4);
  background: rgba(255, 255, 255, 0.35);
}

.accessibility-button.active {
  background: rgba(39, 174, 96, 0.3);
  border-color: rgba(39, 174, 96, 0.6);
  box-shadow: 0 8px 32px rgba(39, 174, 96, 0.4);
}

.accessibility-button.active:hover {
  background: rgba(255, 255, 255, 0.45);
}

/* ========== РЕЖИМ ДОСТУПНОСТИ ========== */

/* Верхняя секция - зона чтения */
.home.accessibility-active .top-section {
  order: 1;
  margin-bottom: 2rem;
}

.home.accessibility-active .datetime-widget-top {
  display: block;
  animation: slideDown 0.8s ease;
}

.home.accessibility-active h1 {
  font-size: 2.2rem;
  margin-bottom: 0.8rem;
}

.home.accessibility-active .subtitle {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

/* Средняя секция - декоративное пространство */
.home.accessibility-active .middle-section {
  order: 2;
  min-height: 15vh;
  background: radial-gradient(circle at center, rgba(255,255,255,0.05) 0%, transparent 70%);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Нижняя секция - зона действий */
.home.accessibility-active .bottom-section {
  order: 3;
  animation: slideUp 0.8s ease;
}

/* Скрываем виджеты времени и новостей из нижней секции */
.home.accessibility-active .bottom-widgets {
  display: none;
}

/* Скрываем бегущую строку */
.home.accessibility-active .ticker {
  display: none;
}

/* Контакты с QR-кодами опускаются вниз */
.home.accessibility-active .contact-info {
  order: 1;
  margin-bottom: 2rem;
  padding: 2rem;
  min-height: auto;
  animation: slideUp 0.8s ease;
}

.home.accessibility-active .contact-info h2 {
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
}

.home.accessibility-active .contact-grid {
  gap: 1.2rem;
}

.home.accessibility-active .contact-item {
  padding: 0.8rem;
}

/* Главные кнопки остаются внизу */
.home.accessibility-active .features {
  order: 2;
  margin-top: 0;
  margin-bottom: 6rem;
  gap: 1.5rem;
}

.home.accessibility-active .feature-card {
  min-height: 260px;
  padding: 2.5rem 2rem;
}

.home.accessibility-active .feature-icon {
  font-size: 5rem;
}

.home.accessibility-active .feature-card h2 {
  font-size: 2rem;
}

.home.accessibility-active .feature-card p {
  font-size: 1.05rem;
}

/* Анимации */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

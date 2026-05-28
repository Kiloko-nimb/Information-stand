<!--
  ApplicantSection — блок «Абитуриенту 2026» на главной.

  Содержит:
    * виджет с обратным отсчётом до начала приёмной кампании;
    * четыре кнопки: «Проходные баллы», «Специальности», «Подать
      документы» (открывают модалки), «Подобрать профессию» (роутинг
      на /quiz);
    * три модалки на BaseModal со статичным контентом про приём 2026/27.
-->
<template>
  <div class="bottom-widgets">
    <div class="widget applicant-widget">
      <h3><Icon name="graduation" :size="22" /> Абитуриенту 2026</h3>
      <div class="countdown-timer">
        <div class="countdown-label">До начала приемной кампании осталось:</div>
        <div class="countdown-value">{{ daysUntilAdmission }} дней</div>
      </div>
      <div class="applicant-actions">
        <button class="applicant-btn" v-ripple="{ color: 'rgba(37, 99, 235, 0.22)' }" @click="passingScoresOpen = true">
          <span class="btn-icon"><Icon name="barChart" :size="22" /></span>
          <span class="btn-text">Проходные баллы</span>
        </button>
        <button class="applicant-btn" v-ripple="{ color: 'rgba(37, 99, 235, 0.22)' }" @click="specialtiesOpen = true">
          <span class="btn-icon"><Icon name="target" :size="22" /></span>
          <span class="btn-text">Специальности</span>
        </button>
        <button class="applicant-btn" v-ripple="{ color: 'rgba(37, 99, 235, 0.22)' }" @click="$router.push('/specialties/compare')">
          <span class="btn-icon"><Icon name="barChart" :size="22" /></span>
          <span class="btn-text">Сравнить</span>
        </button>
        <button class="applicant-btn" v-ripple="{ color: 'rgba(37, 99, 235, 0.22)' }" @click="openApplicationQR">
          <span class="btn-icon"><Icon name="smartphone" :size="22" /></span>
          <span class="btn-text">Подать документы</span>
        </button>
        <button class="applicant-btn applicant-btn--accent" v-ripple="{ color: 'rgba(255, 255, 255, 0.30)' }" @click="$router.push('/quiz')">
          <span class="btn-icon"><Icon name="compass" :size="22" /></span>
          <span class="btn-text">Подобрать профессию</span>
        </button>
      </div>
    </div>
  </div>

  <BaseModal v-model="passingScoresOpen" title="Проходные баллы" title-icon="barChart" :max-width="680">
    <div class="modal-section">
      <p class="modal-text">
        В ККРИТ нет вступительных экзаменов — зачисление проходит по конкурсу
        <strong class="modal-accent">среднего балла аттестата</strong>.<br><br>
        На специальности «Пожарная безопасность» — дополнительно психологическое
        тестирование и нормативы физподготовки.
      </p>
    </div>
    <div class="modal-section">
      <h3 class="modal-h3"><Icon name="trendingUp" :size="18" /> Средний балл аттестата 2025 (справочно)</h3>
      <div class="modal-text modal-text--small">
        • Бюджет (ИТ-специальности): <strong class="modal-accent">4.0–4.5</strong><br>
        • Бюджет (экономика, электроника): <strong class="modal-accent">3.8–4.2</strong><br>
        • Платные места: <strong class="modal-accent">от 3.0</strong><br><br>
        <span class="modal-muted">Цифры ориентировочные — точный проходной балл формируется по итогам конкурса.</span>
      </div>
    </div>
    <div class="modal-section">
      <h3 class="modal-h3"><Icon name="calendar" :size="18" /> Сроки приёма 2026</h3>
      <div class="modal-text modal-text--small">
        • Начало приёма: <strong class="modal-accent">15 июня 2026</strong><br>
        • Окончание (основное): <strong class="modal-accent">14 августа 2026</strong><br>
        • Пожарная безопасность: <strong class="modal-accent">до 10 августа 2026</strong><br>
        • При наличии свободных мест: <strong class="modal-accent">до 25 ноября 2026</strong>
      </div>
    </div>
  </BaseModal>

  <BaseModal
    v-model="specialtiesOpen"
    title="Специальности ККРИТ 2026/27"
    subtitle="Нажмите на карточку — узнаете о предметах, материалах и рынке труда"
    :max-width="980"
  >
    <div class="spec-grid">
      <button
        v-for="s in specialtyList"
        :key="s.key"
        class="spec-card"
        :style="{ '--accent': s.accent }"
        @click="goToSpecialty(s.key)"
      >
        <div class="spec-card-icon">{{ s.icon }}</div>
        <div class="spec-card-body">
          <div class="spec-card-code">{{ s.code }}</div>
          <div class="spec-card-name">{{ s.name }}</div>
          <div class="spec-card-meta">
            <span><Icon name="clock" :size="12" /> {{ s.duration }}</span>
            <span v-if="s.note" class="spec-card-note">{{ s.note }}</span>
          </div>
        </div>
        <Icon name="arrowRight" :size="18" class="spec-card-arrow" />
      </button>
    </div>
    <div class="modal-callout">
      <Icon name="info" :size="18" /> Кликайте по специальности — увидите учебные предметы, полезные материалы и
      актуальные вакансии с зарплатами.
    </div>
  </BaseModal>

  <BaseModal v-model="applicationQROpen" title="Подать документы" title-icon="smartphone" :max-width="760">
    <div class="modal-section modal-qr-row">
      <div class="modal-qr-block">
        <img v-if="applicationQR" :src="applicationQR" alt="QR на kraskrit.ru/abitur" class="modal-qr-img"/>
        <p class="modal-qr-caption">Отсканируйте —<br>откроется раздел «Абитуриенту»</p>
      </div>
      <div class="modal-text">
        <strong class="modal-accent">Приём документов:</strong><br>
        c 15 июня по 14 августа 2026<br>
        Пожарная безопасность — до 10 августа<br><br>
        <strong class="modal-accent">Адрес приёмной комиссии:</strong><br>
        пр. Свободный, 67<br>
        пн–чт 09:00–15:30, пт 09:00–12:00<br><br>
        <strong class="modal-accent">Телефоны:</strong><br>
        8-929-332-29-43<br>
        8-933-327-02-09<br>
        8-391-298-46-46<br>
        <strong class="modal-accent">E-mail:</strong> kraskritpk@yandex.ru
      </div>
    </div>
    <div class="modal-section">
      <h3 class="modal-h3"><Icon name="clipboard" :size="18" /> Перечень документов</h3>
      <div class="modal-text modal-text--small modal-text--loose">
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
    <div class="modal-callout modal-callout--info">
      <Icon name="info" :size="18" /> Заявление можно подать <strong>лично</strong> на пр. Свободный 67,
      <strong>почтой</strong> или <strong>через Госуслуги</strong> (в тестовом режиме).<br>
      Для зачисления оригинал аттестата нужно сдать до
      <strong>14 августа 2026</strong>.
    </div>
  </BaseModal>
</template>

<script>
import { ref, onMounted } from 'vue'
import Icon from '../Icon.vue'
import BaseModal from '../BaseModal.vue'
import { generateQRCode } from '../../utils/qrGenerator'
import { useRouter } from 'vue-router'
import { specialtyList } from '../../data/specialties'

const ADMISSION_DATE = new Date('2026-06-15') // приём документов начинается 15 июня

export default {
  name: 'ApplicantSection',
  components: { Icon, BaseModal },
  setup() {
    const router = useRouter()
    const passingScoresOpen = ref(false)
    const specialtiesOpen = ref(false)
    const applicationQROpen = ref(false)
    const applicationQR = ref('')
    const daysUntilAdmission = ref(0)

    const goToSpecialty = (key) => {
      specialtiesOpen.value = false
      router.push(`/specialty/${key}`)
    }

    const calculateDaysUntilAdmission = () => {
      const today = new Date()
      const diffMs = ADMISSION_DATE - today
      const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24))
      daysUntilAdmission.value = diffDays > 0 ? diffDays : 0
    }

    const openApplicationQR = async () => {
      // QR генерируем лениво — не на каждом открытии, а один раз.
      if (!applicationQR.value) {
        applicationQR.value = await generateQRCode('https://kraskrit.ru/abitur/')
      }
      applicationQROpen.value = true
    }

    onMounted(() => {
      calculateDaysUntilAdmission()
    })

    return {
      daysUntilAdmission,
      passingScoresOpen,
      specialtiesOpen,
      applicationQROpen,
      applicationQR,
      openApplicationQR,
      specialtyList,
      goToSpecialty,
    }
  },
}
</script>

<style scoped>
/* ── Контейнер виджетов «Абитуриенту» ── */
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

/* ── Абитуриент-виджет ── */
.applicant-widget {
  position: relative;
  background:
    linear-gradient(135deg, rgba(245, 158, 11, 0.10), rgba(239, 68, 68, 0.06)),
    var(--surface);
  border: 1px solid rgba(245, 158, 11, 0.25);
  border-radius: var(--radius-lg);
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

/* ─── Стили содержимого <BaseModal> ─── */
.modal-section {
  background: #f5f7fb;
  padding: 1.5rem;
  border-radius: 18px;
  margin-bottom: 1.25rem;
  border: 1px solid rgba(15, 23, 42, 0.10);
}

.modal-h3 {
  color: #0f172a;
  margin: 0 0 0.9rem;
  font-family: 'Manrope', 'Inter', system-ui, sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.modal-h3 :deep(svg) {
  color: #2563EB;
  flex-shrink: 0;
}

.modal-callout :deep(svg) {
  color: #2563EB;
  vertical-align: middle;
  margin-right: 0.25rem;
  flex-shrink: 0;
}

.modal-text {
  color: rgba(15, 23, 42, 0.88);
  line-height: 1.7;
  font-size: 0.97rem;
  margin: 0;
}

.modal-text--small {
  font-size: 0.95rem;
  line-height: 1.8;
  color: rgba(15, 23, 42, 0.85);
}

.modal-text--loose {
  line-height: 1.85;
}

.modal-accent {
  color: #b45309;
}

.modal-muted {
  color: rgba(15, 23, 42, 0.55);
  font-size: 0.85rem;
}

.modal-callout {
  padding: 1.25rem 1.5rem;
  border-radius: 18px;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
  line-height: 1.7;
  color: rgba(15, 23, 42, 0.92);
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.10), rgba(14, 165, 183, 0.08));
  border: 1px solid rgba(37, 99, 235, 0.30);
}

.modal-callout--info {
  background: linear-gradient(135deg, rgba(14, 165, 183, 0.12), rgba(37, 99, 235, 0.08));
  border-color: rgba(14, 165, 183, 0.30);
  font-size: 0.93rem;
}

/* QR + текст: широкий экран — рядом, узкий — стопкой. */
.modal-qr-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
}

.modal-qr-block {
  flex: 0 1 240px;
  min-width: 0;
  text-align: center;
}

.modal-qr-img {
  width: 100%;
  max-width: 220px;
  height: auto;
  aspect-ratio: 1 / 1;
  border-radius: 14px;
  background: #fff;
  padding: 8px;
  box-sizing: border-box;
}

.modal-qr-caption {
  color: rgba(15, 23, 42, 0.7);
  font-size: 0.85rem;
  margin: 0.6rem 0 0;
}

.modal-qr-row .modal-text {
  flex: 1 1 280px;
  min-width: 0;
  font-size: 0.97rem;
}

@media (max-width: 900px) {
  .bottom-widgets {
    grid-template-columns: 1fr;
  }
}

/* === Grid карточек специальностей в модалке === */
.spec-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}
.spec-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 0.85rem;
  padding: 0.95rem 1.1rem;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: 14px;
  cursor: pointer;
  text-align: left;
  transition: all .2s ease;
  font-family: inherit;
}
.spec-card:hover {
  border-color: var(--accent, #2563EB);
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -10px color-mix(in srgb, var(--accent, #2563EB) 50%, transparent);
}
.spec-card-icon {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: color-mix(in srgb, var(--accent, #2563EB) 15%, transparent);
  display: grid;
  place-items: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}
.spec-card-body { min-width: 0; }
.spec-card-code {
  font-family: var(--font-mono, monospace);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--accent, #2563EB);
  letter-spacing: 0.04em;
}
.spec-card-name {
  font-weight: 700;
  font-size: 0.94rem;
  color: var(--text);
  margin: 0.15rem 0 0.35rem;
  line-height: 1.25;
}
.spec-card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.spec-card-meta span {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}
.spec-card-note {
  color: #92400E;
  background: #FEF3C7;
  padding: 0.05rem 0.45rem;
  border-radius: 999px;
  font-weight: 600;
}
.spec-card-arrow {
  color: var(--text-muted);
  flex-shrink: 0;
}
</style>

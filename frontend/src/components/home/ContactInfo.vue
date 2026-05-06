<!--
  ContactInfo — блок «Контактная информация»: адреса, телефоны, e-mail,
  соцсети + три QR-кода (сайт, VK, обратная связь).

  Сам отвечает за генерацию QR-кодов через qrGenerator. Через prop
  `accessibilityMode` поджимает отступы в режиме доступности.
-->
<template>
  <div class="contact-info" :class="{ 'accessibility-active': accessibilityMode }">
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
          <div
            class="social-link social-link--mail"
            aria-label="Электронная почта приёмной"
          >
            <span class="social-badge">@</span>
            <span class="social-text">priem@kraskrit.ru</span>
          </div>
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
</template>

<script>
import { ref, onMounted } from 'vue'
import Icon from '../Icon.vue'
import { generateQRCode } from '../../utils/qrGenerator'

export default {
  name: 'ContactInfo',
  components: { Icon },
  props: {
    accessibilityMode: { type: Boolean, default: false },
  },
  setup() {
    const qrWebsite = ref('')
    const qrFeedback = ref('')
    const qrVK = ref('')

    onMounted(async () => {
      qrWebsite.value = await generateQRCode('https://kraskrit.ru/')
      qrFeedback.value = await generateQRCode('https://kraskrit.ru/contact-us/obr-svaz/')
      qrVK.value = await generateQRCode('https://vk.com/kraskrit')
    })

    return { qrWebsite, qrFeedback, qrVK }
  },
}
</script>

<style scoped>
.contact-info {
  padding: 2.5rem;
  margin-bottom: 2rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: var(--shadow);
  transition: background var(--transition), border-color var(--transition),
    transform var(--transition), box-shadow var(--transition);
}

.contact-info:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
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

.contact-item > div {
  min-width: 0;
  flex: 1;
}

/* ── QR-коды ── */
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

div.social-link {
  cursor: default;
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

.social-link--mail .social-badge {
  background: linear-gradient(135deg, #2563EB 0%, #0EA5B7 100%);
  color: #fff;
}

.social-text {
  word-break: break-word;
}

/* ── Режим доступности ── */
.contact-info.accessibility-active {
  order: 1;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  font-size: 1rem;
}

.contact-info.accessibility-active h2 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.contact-info.accessibility-active .contact-grid {
  gap: 1rem;
}

.contact-info.accessibility-active .contact-item {
  padding: 0.9rem;
}
</style>

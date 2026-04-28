<template>
  <div class="faq">
    <button class="back-button" @click="$router.push('/')">
      <Icon name="arrowLeft" :size="20" />
      <span>На главную</span>
    </button>

    <header class="faq-header">
      <span class="faq-eyebrow">База знаний</span>
      <h1>Частые вопросы</h1>
      <p class="faq-subtitle">
        Справки, документы, Wi-Fi, поступление, общежитие — короткие ответы на самые
        популярные вопросы студентов и абитуриентов ККРИТ.
      </p>
    </header>

    <div class="faq-search">
      <span class="faq-search-icon"><Icon name="search" :size="20" /></span>
      <input
        v-model="searchQuery"
        class="faq-search-input"
        type="search"
        placeholder="Поиск по вопросам…"
        autocomplete="off"
      />
    </div>

    <nav class="faq-filters">
      <button
        v-for="cat in categories"
        :key="cat.id"
        class="faq-filter"
        :class="{ active: currentCategory === cat.id }"
        @click="currentCategory = cat.id"
      >
        <span class="faq-filter-icon"><Icon :name="cat.iconName" :size="18" /></span>
        <span>{{ cat.label }}</span>
        <span class="faq-filter-count">{{ countByCategory(cat.id) }}</span>
      </button>
    </nav>

    <div v-if="filteredItems.length === 0" class="faq-empty">
      По запросу ничего не нашлось. Попробуй другие слова или сбрось фильтр.
    </div>

    <div v-else class="faq-list">
      <article
        v-for="item in filteredItems"
        :key="item.id"
        class="faq-item"
        :class="{ open: openItem === item.id }"
      >
        <button
          class="faq-question"
          :aria-expanded="openItem === item.id"
          @click="toggle(item.id)"
        >
          <span class="faq-question-icon"><Icon :name="categoryIconName(item.category)" :size="20" /></span>
          <span class="faq-question-text">{{ item.question }}</span>
          <span class="faq-question-chevron"><Icon name="chevronRight" :size="22" /></span>
        </button>
        <transition name="faq-accordion" @before-enter="beforeEnter" @enter="enter" @leave="leave">
          <div v-show="openItem === item.id" class="faq-answer">
            <div class="faq-answer-inner">
              <p>{{ item.answer }}</p>
              <div v-if="item.link" class="faq-answer-actions">
                <a
                  class="faq-answer-link"
                  :href="item.link"
                  target="_blank"
                  rel="noopener"
                >
                  {{ item.linkLabel || 'Подробнее' }}
                  <Icon name="arrowRight" :size="16" />
                </a>
                <button
                  class="faq-answer-qr"
                  type="button"
                  @click="showQR(item)"
                >
                  <Icon name="qr" :size="18" />
                  QR на телефон
                </button>
              </div>
            </div>
          </div>
        </transition>
      </article>
    </div>

    <div v-if="qrModal" class="faq-modal" @click.self="qrModal = null">
      <div class="faq-modal-card">
        <button class="faq-modal-close" @click="qrModal = null" aria-label="Закрыть"><Icon name="x" :size="20" /></button>
        <div class="faq-modal-eyebrow">Открой ссылку на телефоне</div>
        <h3>{{ qrModal.question }}</h3>
        <img v-if="qrModal.qr" :src="qrModal.qr" alt="QR-код" class="faq-modal-qr" />
        <div v-else class="faq-modal-loading">Готовим QR…</div>
        <div class="faq-modal-url">{{ qrModal.link }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { faqItems, faqCategories } from '../data/faq'
import { generateQRCode } from '../utils/qrGenerator'
import Icon from '../components/Icon.vue'

export default {
  name: 'Faq',
  components: { Icon },
  setup() {
    const items = faqItems
    const categories = faqCategories
    const currentCategory = ref('all')
    const searchQuery = ref('')
    const openItem = ref(null)
    const qrModal = ref(null)

    const filteredItems = computed(() => {
      let result = items
      if (currentCategory.value !== 'all') {
        result = result.filter((it) => it.category === currentCategory.value)
      }
      const q = searchQuery.value.trim().toLowerCase()
      if (q) {
        result = result.filter(
          (it) =>
            it.question.toLowerCase().includes(q) ||
            it.answer.toLowerCase().includes(q),
        )
      }
      return result
    })

    const countByCategory = (catId) => {
      if (catId === 'all') return items.length
      return items.filter((it) => it.category === catId).length
    }

    const categoryIcon = (catId) => {
      const cat = categories.find((c) => c.id === catId)
      return cat ? cat.icon : '📄'
    }

    const categoryIconName = (catId) => {
      const cat = categories.find((c) => c.id === catId)
      return cat ? cat.iconName : 'fileText'
    }

    // Плавное раскрытие/закрытие аккордеона по фактической высоте контента
    const beforeEnter = (el) => {
      el.style.height = '0'
      el.style.opacity = '0'
    }
    const enter = (el, done) => {
      const h = el.scrollHeight
      requestAnimationFrame(() => {
        el.style.transition = 'height 280ms cubic-bezier(0.4, 0, 0.2, 1), opacity 220ms ease-out 60ms'
        el.style.height = `${h}px`
        el.style.opacity = '1'
      })
      el.addEventListener('transitionend', function handler(e) {
        if (e.propertyName !== 'height') return
        el.style.height = ''
        el.style.transition = ''
        el.removeEventListener('transitionend', handler)
        done()
      })
    }
    const leave = (el, done) => {
      const h = el.scrollHeight
      el.style.height = `${h}px`
      el.style.opacity = '1'
      // форсируем рефлоу
      void el.offsetHeight
      requestAnimationFrame(() => {
        el.style.transition = 'height 240ms cubic-bezier(0.4, 0, 0.2, 1), opacity 160ms ease-in'
        el.style.height = '0'
        el.style.opacity = '0'
      })
      el.addEventListener('transitionend', function handler(e) {
        if (e.propertyName !== 'height') return
        el.style.transition = ''
        el.removeEventListener('transitionend', handler)
        done()
      })
    }

    const toggle = (id) => {
      openItem.value = openItem.value === id ? null : id
    }

    const showQR = async (item) => {
      qrModal.value = {
        question: item.question,
        link: item.link,
        qr: '',
      }
      const qr = await generateQRCode(item.link)
      if (qrModal.value && qrModal.value.link === item.link) {
        qrModal.value.qr = qr
      }
    }

    return {
      categories,
      currentCategory,
      searchQuery,
      filteredItems,
      openItem,
      qrModal,
      toggle,
      showQR,
      countByCategory,
      categoryIcon,
      categoryIconName,
      beforeEnter,
      enter,
      leave,
    }
  },
}
</script>

<style scoped>
.faq {
  max-width: 920px;
  margin: 0 auto;
  padding: 1.5rem 1.25rem 5rem;
  position: relative;
}

/* ── Плавающая кнопка «На главную» ── */
.back-button {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  padding: 0.9rem 1.5rem;
  background: var(--surface-strong);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  color: var(--text);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-pill);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: transform var(--transition), background var(--transition), border-color var(--transition);
  z-index: 1000;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.back-button:hover {
  transform: translateX(-4px);
  background: var(--surface-hover);
  border-color: var(--accent-border);
}

.faq-header {
  text-align: center;
  margin-bottom: 1.5rem;
  max-width: 720px;
  margin-left: auto;
  margin-right: auto;
}

.faq-eyebrow {
  display: inline-block;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.75rem;
}

.faq-header h1 {
  font-family: var(--font-display);
  font-size: clamp(1.9rem, 4.2vw, 2.8rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.1;
  margin: 0 0 0.75rem;
  color: var(--text);
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
}

.faq-subtitle {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.55;
  margin: 0;
}

.faq-search {
  margin-bottom: 1rem;
  position: relative;
}

.faq-search-icon {
  position: absolute;
  left: 1.1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  display: inline-flex;
  pointer-events: none;
}

.faq-search-input {
  width: 100%;
  padding: 0.95rem 1.25rem 0.95rem 3rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  background: var(--surface);
  color: var(--text);
  font-size: 1rem;
  font-family: inherit;
  box-shadow: var(--shadow-xs);
  transition: border-color var(--transition), box-shadow var(--transition);
}

.faq-search-input:focus + .faq-search-icon,
.faq-search:hover .faq-search-icon {
  color: var(--accent);
}

.faq-search-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: var(--accent-glow);
}

.faq-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.faq-filter {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 1.1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text);
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition), color var(--transition);
}

.faq-filter-icon {
  display: inline-flex;
  color: var(--text-muted);
  transition: color var(--transition);
}

.faq-filter:hover .faq-filter-icon {
  color: var(--accent);
}

.faq-filter.active .faq-filter-icon {
  color: #ffffff;
}

.faq-filter:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
}

.faq-filter.active {
  background: var(--accent-gradient);
  color: #ffffff;
  border-color: transparent;
  box-shadow: var(--shadow-sm);
}

.faq-filter-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 0 0.4rem;
  background: var(--surface-strong);
  color: var(--text-muted);
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.faq-filter.active .faq-filter-count {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.faq-empty {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text-muted);
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius-lg);
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.faq-item {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xs);
  transition: box-shadow var(--transition), border-color var(--transition);
  overflow: hidden;
}

.faq-item.open {
  border-color: var(--accent-border);
  box-shadow: var(--shadow-sm);
}

.faq-question {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  width: 100%;
  padding: 1.1rem 1.25rem;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  color: var(--text);
}

.faq-question:hover {
  background: var(--surface-hover);
}

.faq-question-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: var(--accent-soft);
  color: var(--accent);
  flex-shrink: 0;
  transition: background var(--transition), color var(--transition), transform var(--transition);
}

.faq-item.open .faq-question-icon {
  background: var(--accent);
  color: #ffffff;
  transform: rotate(-4deg);
}

.faq-question-text {
  flex: 1;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.4;
}

.faq-question-chevron {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  transition: transform 240ms cubic-bezier(0.4, 0, 0.2, 1), color var(--transition);
}

.faq-item.open .faq-question-chevron {
  transform: rotate(90deg);
  color: var(--accent);
}

.faq-answer {
  overflow: hidden;
  will-change: height, opacity;
}

.faq-answer-inner {
  padding: 0 1.25rem 1.25rem 3.85rem;
}

.faq-answer p {
  margin: 0 0 1rem;
  line-height: 1.6;
  color: var(--text);
  font-size: 0.97rem;
}

.faq-answer-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.faq-answer-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.55rem 1.1rem;
  background: var(--accent-soft);
  color: var(--accent);
  border: 1px solid var(--accent-border);
  border-radius: var(--radius-pill);
  font-weight: 700;
  font-size: 0.9rem;
  text-decoration: none;
  transition: background var(--transition), color var(--transition), transform var(--transition);
}

.faq-answer-link:hover {
  background: var(--accent);
  color: #ffffff;
}

.faq-answer-qr {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.55rem 1.1rem;
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  font-family: inherit;
  transition: background var(--transition), border-color var(--transition);
}

.faq-answer-qr:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
}

/* QR-модалка */
.faq-modal {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1.5rem;
}

.faq-modal-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  max-width: 380px;
  width: 100%;
  text-align: center;
  position: relative;
  box-shadow: var(--shadow-lg);
}

.faq-modal-close {
  position: absolute;
  top: 0.5rem;
  right: 0.75rem;
  background: transparent;
  border: none;
  font-size: 1.75rem;
  line-height: 1;
  color: var(--text-muted);
  cursor: pointer;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  transition: background var(--transition);
}

.faq-modal-close:hover {
  background: var(--surface-hover);
}

.faq-modal-eyebrow {
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.5rem;
}

.faq-modal-card h3 {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.3;
  margin: 0 0 1.25rem;
  color: var(--text);
}

.faq-modal-qr {
  width: 220px;
  height: 220px;
  margin: 0 auto 1rem;
  background: #ffffff;
  padding: 8px;
  border-radius: var(--radius-sm);
  display: block;
}

.faq-modal-loading {
  padding: 3rem 0;
  color: var(--text-muted);
}

.faq-modal-url {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  word-break: break-all;
}

@media (max-width: 600px) {
  .faq-answer-inner {
    padding: 0 1rem 1rem 1rem;
  }
}
</style>

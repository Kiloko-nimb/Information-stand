<template>
  <div class="quiz">
    <button class="back-button" @click="$router.push('/')">
      <Icon name="arrowLeft" :size="20" />
      <span>На главную</span>
    </button>

    <div class="quiz-container">
      <header class="quiz-header">
        <span class="quiz-eyebrow">Абитуриенту 2026</span>
        <h1>Какая IT-профессия тебе подойдёт?</h1>
        <p class="quiz-subtitle">
          5 быстрых вопросов — и узнаешь, какая специальность ККРИТ ближе всего к тебе.
        </p>
      </header>

      <div v-if="!finished" class="quiz-stage">
        <div class="quiz-progress">
          <div class="quiz-progress-track">
            <div class="quiz-progress-fill" :style="{ width: progressPercent + '%' }" />
          </div>
          <div class="quiz-progress-text">
            Вопрос {{ currentIndex + 1 }} из {{ questions.length }}
          </div>
        </div>

        <div class="quiz-card" :key="currentQuestion.id">
          <h2 class="quiz-question">{{ currentQuestion.text }}</h2>
          <div class="quiz-options">
            <button
              v-for="option in currentQuestion.options"
              :key="option.id"
              class="quiz-option"
              :class="{ selected: answers[currentQuestion.id] === option.id }"
              @click="selectOption(option.id)"
            >
              <span class="quiz-option-marker"></span>
              <span class="quiz-option-label">{{ option.label }}</span>
            </button>
          </div>

          <div class="quiz-actions">
            <button
              v-if="currentIndex > 0"
              class="quiz-btn quiz-btn--ghost"
              @click="previousQuestion"
            >
              ← Назад
            </button>
            <div class="quiz-spacer"></div>
            <button
              v-if="!isLastQuestion"
              class="quiz-btn quiz-btn--primary"
              :disabled="!answers[currentQuestion.id]"
              @click="nextQuestion"
            >
              Далее →
            </button>
            <button
              v-else
              class="quiz-btn quiz-btn--primary"
              :disabled="!answers[currentQuestion.id]"
              @click="finishQuiz"
            >
              Узнать результат
            </button>
          </div>
        </div>
      </div>

      <div v-else class="quiz-result">
        <div class="result-hero" :style="{ '--result-accent': primarySpecialty.accent }">
          <div class="result-icon">{{ primarySpecialty.icon }}</div>
          <span class="result-eyebrow">Тебе подойдёт</span>
          <h2>{{ primarySpecialty.name }}</h2>
          <div class="result-meta">
            <span class="result-code">{{ primarySpecialty.code }}</span>
            <span class="result-dot">·</span>
            <span>{{ primarySpecialty.qualification }}</span>
            <span class="result-dot">·</span>
            <span>{{ primarySpecialty.duration }}</span>
          </div>
          <p class="result-summary">{{ primarySpecialty.summary }}</p>
          <div class="result-skills">
            <span
              v-for="skill in primarySpecialty.skills"
              :key="skill"
              class="result-skill"
            >
              {{ skill }}
            </span>
          </div>
          <div v-if="primarySpecialty.note" class="result-note">{{ primarySpecialty.note }}</div>
        </div>

        <div v-if="qrCode" class="result-qr">
          <div class="result-qr-label">Сохрани специальность в телефон:</div>
          <img :src="qrCode" alt="QR-код" />
          <div class="result-qr-url">{{ primarySpecialty.url }}</div>
        </div>

        <div v-if="secondarySpecialty" class="result-secondary">
          <span class="result-secondary-eyebrow">Также присмотрись к</span>
          <div class="result-secondary-card">
            <div class="result-secondary-icon">{{ secondarySpecialty.icon }}</div>
            <div>
              <div class="result-secondary-name">{{ secondarySpecialty.name }}</div>
              <div class="result-secondary-qual">{{ secondarySpecialty.qualification }}</div>
            </div>
          </div>
        </div>

        <div class="result-actions">
          <button class="quiz-btn quiz-btn--ghost" @click="restart">
            ↺ Пройти ещё раз
          </button>
          <button class="quiz-btn quiz-btn--primary" @click="$router.push('/')">
            На главную
          </button>
        </div>

        <div class="result-disclaimer">
          Это игровой тест — он подсказывает, в какую сторону смотреть. Окончательный
          выбор лучше обсудить с приёмной комиссией: 8 (391) 218-17-99.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { quizQuestions, calculateQuizResult } from '../data/quiz'
import { specialties } from '../data/specialties'
import { generateQRCode } from '../utils/qrGenerator'
import Icon from '../components/Icon.vue'

export default {
  name: 'Quiz',
  components: { Icon },
  setup() {
    const questions = quizQuestions
    const currentIndex = ref(0)
    const answers = ref({})
    const finished = ref(false)
    const result = ref(null)
    const qrCode = ref('')

    const currentQuestion = computed(() => questions[currentIndex.value])
    const isLastQuestion = computed(() => currentIndex.value === questions.length - 1)
    const progressPercent = computed(() => {
      const answered = Object.keys(answers.value).length
      return Math.round((answered / questions.length) * 100)
    })

    const primarySpecialty = computed(() => {
      if (!result.value || !result.value.primary) return null
      return specialties[result.value.primary]
    })

    const secondarySpecialty = computed(() => {
      if (!result.value || !result.value.secondary) return null
      if (result.value.secondary === result.value.primary) return null
      return specialties[result.value.secondary]
    })

    const selectOption = (optionId) => {
      answers.value = { ...answers.value, [currentQuestion.value.id]: optionId }
    }

    const nextQuestion = () => {
      if (currentIndex.value < questions.length - 1) {
        currentIndex.value += 1
      }
    }

    const previousQuestion = () => {
      if (currentIndex.value > 0) {
        currentIndex.value -= 1
      }
    }

    const finishQuiz = async () => {
      result.value = calculateQuizResult(answers.value)
      finished.value = true
    }

    const restart = () => {
      currentIndex.value = 0
      answers.value = {}
      finished.value = false
      result.value = null
      qrCode.value = ''
    }

    watch(primarySpecialty, async (specialty) => {
      if (specialty?.url) {
        qrCode.value = await generateQRCode(specialty.url)
      } else {
        qrCode.value = ''
      }
    })

    onMounted(() => {
      window.scrollTo({ top: 0 })
    })

    return {
      questions,
      currentIndex,
      answers,
      finished,
      currentQuestion,
      isLastQuestion,
      progressPercent,
      primarySpecialty,
      secondarySpecialty,
      qrCode,
      selectOption,
      nextQuestion,
      previousQuestion,
      finishQuiz,
      restart,
    }
  },
}
</script>

<style scoped>
.quiz {
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

.quiz-header {
  text-align: center;
  margin-bottom: 2rem;
}

.quiz-eyebrow {
  display: inline-block;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.75rem;
}

.quiz-header h1 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 4vw, 2.6rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.15;
  margin: 0 0 0.75rem;
  color: var(--text);
  background: none;
  -webkit-background-clip: initial;
  background-clip: initial;
}

.quiz-subtitle {
  color: var(--text-muted);
  font-size: 1.05rem;
  max-width: 560px;
  margin: 0 auto;
}

.quiz-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.quiz-progress-track {
  flex: 1;
  height: 8px;
  background: var(--surface-strong);
  border: 1px solid var(--border);
  border-radius: 999px;
  overflow: hidden;
}

.quiz-progress-fill {
  height: 100%;
  background: var(--accent-gradient);
  transition: width 0.4s var(--ease);
}

.quiz-progress-text {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-muted);
  white-space: nowrap;
}

.quiz-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: var(--shadow-sm);
}

.quiz-question {
  font-family: var(--font-display);
  font-size: clamp(1.3rem, 2.5vw, 1.75rem);
  font-weight: 700;
  letter-spacing: -0.015em;
  line-height: 1.3;
  margin: 0 0 1.5rem;
  color: var(--text);
}

.quiz-options {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}

.quiz-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  text-align: left;
  cursor: pointer;
  transition: border-color var(--transition), background var(--transition), transform var(--transition);
  font-family: inherit;
  color: var(--text);
}

.quiz-option:hover {
  border-color: var(--accent-border);
  background: var(--surface-hover);
  transform: translateY(-1px);
}

.quiz-option.selected {
  border-color: var(--accent);
  background: var(--accent-soft);
}

.quiz-option-marker {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid var(--border-hover);
  flex-shrink: 0;
  position: relative;
  transition: border-color var(--transition);
}

.quiz-option.selected .quiz-option-marker {
  border-color: var(--accent);
}

.quiz-option.selected .quiz-option-marker::after {
  content: '';
  position: absolute;
  inset: 4px;
  border-radius: 50%;
  background: var(--accent);
}

.quiz-option-label {
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.4;
}

.quiz-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.quiz-spacer {
  flex: 1;
}

.quiz-btn {
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-pill);
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: transform var(--transition), background var(--transition), box-shadow var(--transition);
  font-family: inherit;
  border: 1px solid transparent;
}

.quiz-btn--primary {
  background: var(--accent-gradient);
  color: #ffffff;
  box-shadow: var(--shadow-sm);
}

.quiz-btn--primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.quiz-btn--primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.quiz-btn--ghost {
  background: var(--surface);
  border-color: var(--border);
  color: var(--text);
}

.quiz-btn--ghost:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
}

/* ── Результат ── */
.quiz-result {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.result-hero {
  position: relative;
  padding: 2.5rem 2rem;
  border-radius: var(--radius-xl);
  background:
    radial-gradient(80% 60% at 50% 0%, color-mix(in srgb, var(--result-accent) 18%, transparent), transparent 70%),
    var(--surface);
  border: 1px solid var(--border);
  text-align: center;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.result-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: var(--result-accent);
}

.result-icon {
  font-size: 3.5rem;
  margin-bottom: 0.75rem;
}

.result-eyebrow {
  display: block;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.result-hero h2 {
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 3.2vw, 2.2rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 0.75rem;
  color: var(--text);
}

.result-meta {
  display: inline-flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.4rem 0.6rem;
  font-size: 0.95rem;
  color: var(--text-muted);
  font-weight: 500;
  margin-bottom: 1rem;
}

.result-code {
  font-weight: 800;
  color: var(--result-accent);
  font-variant-numeric: tabular-nums;
}

.result-dot {
  opacity: 0.5;
}

.result-summary {
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--text);
  max-width: 580px;
  margin: 0 auto 1.25rem;
}

.result-skills {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.result-skill {
  padding: 0.4rem 0.85rem;
  background: var(--surface-strong);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
}

.result-note {
  margin-top: 1rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--accent-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.result-qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.result-qr-label {
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.result-qr img {
  width: 180px;
  height: 180px;
  background: #ffffff;
  padding: 8px;
  border-radius: var(--radius-sm);
}

.result-qr-url {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  word-break: break-all;
  text-align: center;
}

.result-secondary {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem;
  box-shadow: var(--shadow-sm);
}

.result-secondary-eyebrow {
  display: block;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.result-secondary-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.result-secondary-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.result-secondary-name {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
}

.result-secondary-qual {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-top: 0.15rem;
}

.result-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
}

.result-disclaimer {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
  line-height: 1.5;
  max-width: 600px;
  margin: 0 auto;
}

@media (max-width: 600px) {
  .quiz-card {
    padding: 1.25rem;
  }
  .quiz-option {
    padding: 0.85rem 1rem;
  }
  .result-hero {
    padding: 1.75rem 1.25rem;
  }
}
</style>

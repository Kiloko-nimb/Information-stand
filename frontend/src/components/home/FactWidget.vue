<!--
  FactWidget — карточка с ротирующимся «интересным фактом» о ККРИТ.
  Меняет факт каждые 18 секунд. Скрывается, когда родитель ставит
  prop `hidden` (используется в режиме доступности).
-->
<template>
  <div v-if="!hidden" class="fun-facts-widget">
    <div class="fun-fact">
      <span class="fact-icon"><Icon name="lightbulb" :size="24" /></span>
      <span class="fact-text">{{ currentFact }}</span>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import Icon from '../Icon.vue'

const FACTS = [
  '🤖 В стенах ККРИТ проложено более 50 километров витой пары. Этого хватит, чтобы обмотать колледж 100 раз!',
  '☕ Во время регионального хакатона наши студенты выпили 120 литров кофе за 24 часа',
  '💾 Суммарный объем кода, который пишут наши студенты за один семестр, превышает код управления космическим шаттлом',
  '🏆 85% наших выпускников находят работу по специальности еще до получения диплома',
  '🏃 От входа до кабинета 415 ровно 342 шага. Мы проверяли',
  '📡 В колледже работает более 500 компьютеров, объединенных в единую сеть',
  '🎓 ККРИТ выпустил более 15 000 специалистов за всю историю существования',
  '🚌 До корпуса на пр. Свободный, 67 можно доехать на 10 маршрутах: автобусы №2, 5, 26, 32, 34, 51, 52, 53, 71, 76, 85, 87 и троллейбусы №5, 6',
]

const ROTATE_MS = 18_000

export default {
  name: 'FactWidget',
  components: { Icon },
  props: {
    hidden: { type: Boolean, default: false },
  },
  setup() {
    const currentFact = ref('')
    let interval = null

    const rotate = () => {
      const idx = Math.floor(Math.random() * FACTS.length)
      currentFact.value = FACTS[idx]
    }

    onMounted(() => {
      rotate()
      interval = setInterval(rotate, ROTATE_MS)
    })

    onUnmounted(() => {
      if (interval) {
        clearInterval(interval)
        interval = null
      }
    })

    return { currentFact }
  },
}
</script>

<style scoped>
.fun-facts-widget {
  padding: 1.25rem 1.75rem;
  margin: 1.5rem 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: var(--shadow-sm);
  transition: background var(--transition), border-color var(--transition),
    transform var(--transition), box-shadow var(--transition);
}

.fun-facts-widget:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
}

.fun-fact {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  animation: fadeIn 0.6s var(--ease);
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

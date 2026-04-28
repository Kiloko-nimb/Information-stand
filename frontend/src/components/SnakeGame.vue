<template>
  <div class="snake-overlay" @click.self="confirmExit">
    <div class="snake-modal">
      <header class="snake-head">
        <div class="snake-eyebrow">🥚 Пасхалка ККРИТ</div>
        <h2>Змейка</h2>
        <button class="snake-close" @click="confirmExit" aria-label="Закрыть">×</button>
      </header>

      <div class="snake-stats">
        <div class="snake-stat">
          <span class="snake-stat-label">Счёт</span>
          <span class="snake-stat-value">{{ score }}</span>
        </div>
        <div class="snake-stat">
          <span class="snake-stat-label">Рекорд</span>
          <span class="snake-stat-value">{{ highScore }}</span>
        </div>
        <div class="snake-stat">
          <span class="snake-stat-label">Скорость</span>
          <span class="snake-stat-value">{{ speedLabel }}</span>
        </div>
      </div>

      <div class="snake-board-wrap">
        <canvas
          ref="canvasEl"
          class="snake-board"
          :width="boardSize"
          :height="boardSize"
          tabindex="0"
        ></canvas>

        <div v-if="state === 'idle'" class="snake-state-overlay">
          <div class="snake-state-card">
            <div class="snake-state-icon">🐍</div>
            <h3>Готов?</h3>
            <p>Управление: <kbd>←</kbd> <kbd>↑</kbd> <kbd>↓</kbd> <kbd>→</kbd> или <kbd>WASD</kbd></p>
            <p class="snake-hint">Соберёшь яблоко — вырастешь, врежешься в себя — конец.</p>
            <button class="snake-btn snake-btn--primary" @click="start">Начать</button>
          </div>
        </div>

        <div v-else-if="state === 'paused'" class="snake-state-overlay">
          <div class="snake-state-card">
            <div class="snake-state-icon">⏸</div>
            <h3>Пауза</h3>
            <button class="snake-btn snake-btn--primary" @click="resume">Продолжить</button>
          </div>
        </div>

        <div v-else-if="state === 'gameover'" class="snake-state-overlay">
          <div class="snake-state-card">
            <div class="snake-state-icon">💀</div>
            <h3>Игра окончена</h3>
            <p class="snake-gameover-score">Счёт: <strong>{{ score }}</strong></p>
            <p v-if="newRecord" class="snake-gameover-record">🏆 Новый рекорд!</p>
            <button class="snake-btn snake-btn--primary" @click="restart">Ещё раз</button>
          </div>
        </div>
      </div>

      <!-- Контролы для тач-стенда -->
      <div class="snake-controls">
        <div class="snake-dpad">
          <button
            class="snake-pad snake-pad--up"
            aria-label="Вверх"
            @click="setDirection('up')"
          >▲</button>
          <button
            class="snake-pad snake-pad--left"
            aria-label="Влево"
            @click="setDirection('left')"
          >◀</button>
          <button
            class="snake-pad snake-pad--right"
            aria-label="Вправо"
            @click="setDirection('right')"
          >▶</button>
          <button
            class="snake-pad snake-pad--down"
            aria-label="Вниз"
            @click="setDirection('down')"
          >▼</button>
        </div>
        <div class="snake-actions">
          <button
            v-if="state === 'running'"
            class="snake-btn snake-btn--ghost"
            @click="pause"
          >⏸ Пауза</button>
          <button
            v-else-if="state === 'paused'"
            class="snake-btn snake-btn--ghost"
            @click="resume"
          >▶ Продолжить</button>
          <button class="snake-btn snake-btn--ghost" @click="restart">↺ Заново</button>
        </div>
      </div>

      <div class="snake-footer">
        Окно закроется автоматически через {{ idleSeconds }}&nbsp;с бездействия.
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const GRID = 20 // 20x20 ячеек
const BOARD_SIZE = 480 // canvas px
const STORAGE_KEY = 'kkrit:snake:highscore'
const IDLE_AUTO_CLOSE_MS = 90 * 1000 // 1.5 минуты бездействия

export default {
  name: 'SnakeGame',
  emits: ['close'],
  setup(_, { emit }) {
    const canvasEl = ref(null)
    const score = ref(0)
    const highScore = ref(parseInt(localStorage.getItem(STORAGE_KEY) || '0', 10) || 0)
    const state = ref('idle') // idle | running | paused | gameover
    const newRecord = ref(false)
    const idleSeconds = ref(Math.round(IDLE_AUTO_CLOSE_MS / 1000))

    let snake = []
    let direction = { x: 1, y: 0 }
    let queuedDirection = { x: 1, y: 0 }
    let food = { x: 10, y: 10 }
    let tickInterval = null
    let speedMs = 130
    let lastInteraction = Date.now()
    let idleInterval = null

    const cell = computed(() => BOARD_SIZE / GRID)
    const boardSize = BOARD_SIZE

    const speedLabel = computed(() => {
      if (speedMs >= 130) return '🐢'
      if (speedMs >= 100) return '🚶'
      if (speedMs >= 75) return '🏃'
      return '⚡️'
    })

    const reset = () => {
      snake = [
        { x: 8, y: 10 },
        { x: 9, y: 10 },
        { x: 10, y: 10 },
      ]
      direction = { x: 1, y: 0 }
      queuedDirection = { x: 1, y: 0 }
      score.value = 0
      newRecord.value = false
      speedMs = 130
      placeFood()
      draw()
    }

    const placeFood = () => {
      while (true) {
        const f = {
          x: Math.floor(Math.random() * GRID),
          y: Math.floor(Math.random() * GRID),
        }
        if (!snake.some((s) => s.x === f.x && s.y === f.y)) {
          food = f
          return
        }
      }
    }

    const draw = () => {
      const ctx = canvasEl.value?.getContext('2d')
      if (!ctx) return
      const c = cell.value

      // фон
      ctx.fillStyle = getCSS('--snake-bg', '#0F172A')
      ctx.fillRect(0, 0, BOARD_SIZE, BOARD_SIZE)

      // сетка (тонкие линии)
      ctx.strokeStyle = 'rgba(255,255,255,0.04)'
      ctx.lineWidth = 1
      for (let i = 1; i < GRID; i += 1) {
        ctx.beginPath()
        ctx.moveTo(i * c, 0)
        ctx.lineTo(i * c, BOARD_SIZE)
        ctx.stroke()
        ctx.beginPath()
        ctx.moveTo(0, i * c)
        ctx.lineTo(BOARD_SIZE, i * c)
        ctx.stroke()
      }

      // еда
      ctx.fillStyle = '#F59E0B'
      drawCell(ctx, food.x, food.y, c, 0.3)

      // змея
      snake.forEach((seg, i) => {
        const isHead = i === snake.length - 1
        ctx.fillStyle = isHead ? '#2563EB' : `hsl(${200 + i * 4}, 70%, ${55 + (i % 3) * 4}%)`
        drawCell(ctx, seg.x, seg.y, c, isHead ? 0.18 : 0.22)
      })
    }

    const drawCell = (ctx, x, y, c, radius) => {
      const r = Math.max(2, c * radius)
      const px = x * c + 1
      const py = y * c + 1
      const w = c - 2
      const h = c - 2
      ctx.beginPath()
      ctx.moveTo(px + r, py)
      ctx.lineTo(px + w - r, py)
      ctx.quadraticCurveTo(px + w, py, px + w, py + r)
      ctx.lineTo(px + w, py + h - r)
      ctx.quadraticCurveTo(px + w, py + h, px + w - r, py + h)
      ctx.lineTo(px + r, py + h)
      ctx.quadraticCurveTo(px, py + h, px, py + h - r)
      ctx.lineTo(px, py + r)
      ctx.quadraticCurveTo(px, py, px + r, py)
      ctx.closePath()
      ctx.fill()
    }

    const getCSS = (varName, fallback) => {
      const value = getComputedStyle(document.documentElement).getPropertyValue(varName).trim()
      return value || fallback
    }

    const tick = () => {
      direction = queuedDirection
      const head = snake[snake.length - 1]
      const next = { x: head.x + direction.x, y: head.y + direction.y }

      // стены
      if (next.x < 0 || next.x >= GRID || next.y < 0 || next.y >= GRID) {
        gameover()
        return
      }
      // в себя
      if (snake.some((s) => s.x === next.x && s.y === next.y)) {
        gameover()
        return
      }

      snake.push(next)

      if (next.x === food.x && next.y === food.y) {
        score.value += 1
        if (score.value % 5 === 0 && speedMs > 60) {
          speedMs -= 8
          stopTick()
          startTick()
        }
        placeFood()
      } else {
        snake.shift()
      }
      draw()
    }

    const startTick = () => {
      tickInterval = setInterval(tick, speedMs)
    }
    const stopTick = () => {
      if (tickInterval) {
        clearInterval(tickInterval)
        tickInterval = null
      }
    }

    const start = () => {
      reset()
      state.value = 'running'
      startTick()
      canvasEl.value?.focus()
    }

    const pause = () => {
      if (state.value !== 'running') return
      state.value = 'paused'
      stopTick()
    }

    const resume = () => {
      if (state.value !== 'paused') return
      state.value = 'running'
      startTick()
      canvasEl.value?.focus()
    }

    const restart = () => {
      stopTick()
      start()
    }

    const gameover = () => {
      stopTick()
      state.value = 'gameover'
      if (score.value > highScore.value) {
        highScore.value = score.value
        newRecord.value = true
        try {
          localStorage.setItem(STORAGE_KEY, String(score.value))
        } catch (_) { /* noop */ }
      }
    }

    const setDirection = (dir) => {
      noteInteraction()
      const map = {
        up: { x: 0, y: -1 },
        down: { x: 0, y: 1 },
        left: { x: -1, y: 0 },
        right: { x: 1, y: 0 },
      }
      const next = map[dir]
      if (!next) return
      // запрещаем разворот на 180°
      if (snake.length > 1 && next.x === -direction.x && next.y === -direction.y) return
      queuedDirection = next
      if (state.value === 'idle') start()
    }

    const onKeydown = (e) => {
      noteInteraction()
      const k = e.key.toLowerCase()
      if (['arrowup', 'w', 'ц'].includes(k)) {
        setDirection('up')
        e.preventDefault()
      } else if (['arrowdown', 's', 'ы'].includes(k)) {
        setDirection('down')
        e.preventDefault()
      } else if (['arrowleft', 'a', 'ф'].includes(k)) {
        setDirection('left')
        e.preventDefault()
      } else if (['arrowright', 'd', 'в'].includes(k)) {
        setDirection('right')
        e.preventDefault()
      } else if (k === ' ' || k === 'p') {
        if (state.value === 'running') pause()
        else if (state.value === 'paused') resume()
        e.preventDefault()
      } else if (k === 'escape') {
        confirmExit()
      }
    }

    const noteInteraction = () => {
      lastInteraction = Date.now()
    }

    const confirmExit = () => {
      stopTick()
      emit('close')
    }

    const tickIdle = () => {
      const elapsed = Date.now() - lastInteraction
      idleSeconds.value = Math.max(0, Math.round((IDLE_AUTO_CLOSE_MS - elapsed) / 1000))
      if (elapsed >= IDLE_AUTO_CLOSE_MS) {
        confirmExit()
      }
    }

    onMounted(() => {
      document.addEventListener('keydown', onKeydown)
      idleInterval = setInterval(tickIdle, 1000)
      reset()
      // фокус на canvas, чтобы клавиатура работала сразу
      setTimeout(() => canvasEl.value?.focus(), 100)
    })

    onBeforeUnmount(() => {
      document.removeEventListener('keydown', onKeydown)
      stopTick()
      if (idleInterval) clearInterval(idleInterval)
    })

    return {
      canvasEl,
      boardSize,
      score,
      highScore,
      state,
      newRecord,
      idleSeconds,
      speedLabel,
      start,
      pause,
      resume,
      restart,
      setDirection,
      confirmExit,
    }
  },
}
</script>

<style scoped>
.snake-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.78);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1.5rem;
  animation: snake-fade-in 0.25s ease;
}

@keyframes snake-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.snake-modal {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 1.75rem;
  max-width: 600px;
  width: 100%;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  max-height: 92vh;
  overflow-y: auto;
}

.snake-head {
  position: relative;
  text-align: center;
}

.snake-eyebrow {
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.4rem;
}

.snake-head h2 {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0;
  color: var(--text);
}

.snake-close {
  position: absolute;
  top: -0.5rem;
  right: -0.5rem;
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

.snake-close:hover {
  background: var(--surface-hover);
}

.snake-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.snake-stat {
  background: var(--surface-strong);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.6rem 0.85rem;
  text-align: center;
}

.snake-stat-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 0.2rem;
}

.snake-stat-value {
  display: block;
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  color: var(--text);
  letter-spacing: -0.02em;
}

.snake-board-wrap {
  position: relative;
  align-self: center;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: #0F172A;
  border: 1px solid var(--border);
  width: 100%;
  max-width: 480px;
  aspect-ratio: 1 / 1;
}

.snake-board {
  display: block;
  width: 100% !important;
  height: 100% !important;
  outline: none;
}

.snake-state-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.snake-state-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem 2rem;
  text-align: center;
  max-width: 360px;
  box-shadow: var(--shadow);
}

.snake-state-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.snake-state-card h3 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 0.75rem;
  color: var(--text);
}

.snake-state-card p {
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 0.5rem;
  color: var(--text);
}

.snake-state-card kbd {
  display: inline-block;
  padding: 0.1rem 0.45rem;
  background: var(--surface-strong);
  border: 1px solid var(--border);
  border-bottom-width: 2px;
  border-radius: 4px;
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.85rem;
  color: var(--text);
}

.snake-hint {
  font-size: 0.85rem !important;
  color: var(--text-muted) !important;
  margin-top: 0.5rem !important;
  margin-bottom: 1rem !important;
}

.snake-gameover-score {
  font-size: 1.05rem !important;
}

.snake-gameover-score strong {
  color: var(--accent);
  font-size: 1.2rem;
  font-variant-numeric: tabular-nums;
}

.snake-gameover-record {
  color: var(--accent-3);
  font-weight: 700;
  margin: 0.5rem 0 1rem !important;
}

.snake-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.snake-dpad {
  display: grid;
  grid-template-columns: 44px 44px 44px;
  grid-template-rows: 44px 44px;
  gap: 0.3rem;
  grid-template-areas:
    ".  up    ."
    "left down right";
}

.snake-pad {
  background: var(--surface-strong);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text);
  cursor: pointer;
  transition: background var(--transition), transform var(--transition);
}

.snake-pad:hover {
  background: var(--accent-soft);
  border-color: var(--accent-border);
}

.snake-pad:active {
  transform: scale(0.92);
}

.snake-pad--up { grid-area: up; }
.snake-pad--down { grid-area: down; }
.snake-pad--left { grid-area: left; }
.snake-pad--right { grid-area: right; }

.snake-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.snake-btn {
  padding: 0.7rem 1.25rem;
  border-radius: var(--radius-pill);
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  font-family: inherit;
  border: 1px solid transparent;
  transition: transform var(--transition), background var(--transition), box-shadow var(--transition);
}

.snake-btn--primary {
  background: var(--accent-gradient);
  color: #ffffff;
  box-shadow: var(--shadow-sm);
}

.snake-btn--primary:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.snake-btn--ghost {
  background: var(--surface);
  border-color: var(--border);
  color: var(--text);
}

.snake-btn--ghost:hover {
  background: var(--surface-hover);
  border-color: var(--accent-border);
}

.snake-footer {
  font-size: 0.8rem;
  color: var(--text-muted);
  text-align: center;
}

@media (max-width: 480px) {
  .snake-modal {
    padding: 1.25rem;
  }
  .snake-controls {
    justify-content: center;
  }
}
</style>

// Лёгкие звуковые эффекты через Web Audio API (без аудио-файлов).
// Сохраняем настройку on/off в localStorage. По умолчанию ВЫКЛЮЧЕНО,
// чтобы не пугать пользователей при первом запуске.

import { ref, watch } from 'vue'

const STORAGE_KEY = 'kkrit_sounds_enabled'
const enabled = ref(false)

if (typeof localStorage !== 'undefined') {
  enabled.value = localStorage.getItem(STORAGE_KEY) === '1'
}

watch(enabled, (v) => {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(STORAGE_KEY, v ? '1' : '0')
  }
})

let audioCtx = null
function getCtx() {
  if (typeof window === 'undefined') return null
  if (!audioCtx) {
    try {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)()
    } catch {
      return null
    }
  }
  if (audioCtx.state === 'suspended') audioCtx.resume()
  return audioCtx
}

// Простой синтезатор: огибающая + основная частота
function playTone({ freq = 440, duration = 0.08, type = 'sine', gain = 0.04 }) {
  if (!enabled.value) return
  const ctx = getCtx()
  if (!ctx) return
  const t0 = ctx.currentTime
  const osc = ctx.createOscillator()
  const env = ctx.createGain()
  osc.type = type
  osc.frequency.value = freq
  env.gain.setValueAtTime(0, t0)
  env.gain.linearRampToValueAtTime(gain, t0 + 0.01)
  env.gain.exponentialRampToValueAtTime(0.0001, t0 + duration)
  osc.connect(env).connect(ctx.destination)
  osc.start(t0)
  osc.stop(t0 + duration + 0.02)
}

// Готовые звуки
export const sounds = {
  tap:     () => playTone({ freq: 880, duration: 0.06, type: 'triangle', gain: 0.03 }),
  click:   () => playTone({ freq: 1200, duration: 0.05, type: 'sine', gain: 0.03 }),
  success: () => {
    playTone({ freq: 660, duration: 0.08, type: 'sine', gain: 0.04 })
    setTimeout(() => playTone({ freq: 990, duration: 0.12, type: 'sine', gain: 0.05 }), 70)
  },
  error:   () => playTone({ freq: 220, duration: 0.18, type: 'sawtooth', gain: 0.03 }),
  open:    () => playTone({ freq: 740, duration: 0.10, type: 'sine', gain: 0.035 }),
  close:   () => playTone({ freq: 520, duration: 0.10, type: 'sine', gain: 0.03 }),
}

export function useSound() {
  function toggle() { enabled.value = !enabled.value }
  function setEnabled(v) { enabled.value = !!v }
  return { enabled, toggle, setEnabled, play: sounds }
}

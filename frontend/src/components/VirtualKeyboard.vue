<template>
  <div class="virtual-keyboard" v-if="visible">
    <div class="kb-row" v-for="(row, ri) in layout" :key="ri">
      <button
        v-for="key in row"
        :key="key.label"
        :class="['kb-key', key.wide ? 'kb-wide' : '']"
        @click.prevent="onKey(key)"
      >
        <component v-if="key.icon" :is="key.icon" :size="16" />
        <span v-else>{{ key.label }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { Delete, Keyboard } from 'lucide-vue-next'

const props = defineProps({
  visible: { type: Boolean, default: true },
  modelValue: { type: String, default: '' },
  target: { type: String, default: '' }, // 'text' | 'password'
})

const emit = defineEmits(['update:modelValue', 'toggle-target'])

const layout = [
  [
    { label: '1' }, { label: '2' }, { label: '3' }, { label: '4' },
    { label: '5' }, { label: '6' }, { label: '7' }, { label: '8' },
    { label: '9' }, { label: '0' },
  ],
  [
    { label: 'й' }, { label: 'ц' }, { label: 'у' }, { label: 'к' },
    { label: 'е' }, { label: 'н' }, { label: 'г' }, { label: 'ш' },
    { label: 'щ' }, { label: 'з' }, { label: 'х' },
  ],
  [
    { label: 'ф' }, { label: 'ы' }, { label: 'в' }, { label: 'а' },
    { label: 'п' }, { label: 'р' }, { label: 'о' }, { label: 'л' },
    { label: 'д' }, { label: 'ж' }, { label: 'э' },
  ],
  [
    { label: 'я' }, { label: 'ч' }, { label: 'с' }, { label: 'м' },
    { label: 'и' }, { label: 'т' }, { label: 'ь' }, { label: 'б' },
    { label: 'ю' }, { label: '.' }, { label: '@' },
  ],
  [
    { label: 'ABC', action: 'toggle-lang', wide: true },
    { label: ' ', action: 'space', wide: true },
    { icon: Delete, action: 'backspace', wide: true },
  ],
]

let isLatin = false
const latinLayout = [
  [
    { label: '1' }, { label: '2' }, { label: '3' }, { label: '4' },
    { label: '5' }, { label: '6' }, { label: '7' }, { label: '8' },
    { label: '9' }, { label: '0' },
  ],
  [
    { label: 'q' }, { label: 'w' }, { label: 'e' }, { label: 'r' },
    { label: 't' }, { label: 'y' }, { label: 'u' }, { label: 'i' },
    { label: 'o' }, { label: 'p' },
  ],
  [
    { label: 'a' }, { label: 's' }, { label: 'd' }, { label: 'f' },
    { label: 'g' }, { label: 'h' }, { label: 'j' }, { label: 'k' },
    { label: 'l' },
  ],
  [
    { label: 'z' }, { label: 'x' }, { label: 'c' }, { label: 'v' },
    { label: 'b' }, { label: 'n' }, { label: 'm' }, { label: '.' },
    { label: '@' },
  ],
  [
    { label: 'РУС', action: 'toggle-lang', wide: true },
    { label: ' ', action: 'space', wide: true },
    { icon: Delete, action: 'backspace', wide: true },
  ],
]

function onKey(key) {
  if (key.action === 'toggle-lang') {
    isLatin = !isLatin
    // Swap layout reference — hacky but works for this simple case
    if (isLatin) {
      layout.splice(0, layout.length, ...latinLayout)
    } else {
      const ru = [
        [{ label: '1' }, { label: '2' }, { label: '3' }, { label: '4' }, { label: '5' }, { label: '6' }, { label: '7' }, { label: '8' }, { label: '9' }, { label: '0' }],
        [{ label: 'й' }, { label: 'ц' }, { label: 'у' }, { label: 'к' }, { label: 'е' }, { label: 'н' }, { label: 'г' }, { label: 'ш' }, { label: 'щ' }, { label: 'з' }, { label: 'х' }],
        [{ label: 'ф' }, { label: 'ы' }, { label: 'в' }, { label: 'а' }, { label: 'п' }, { label: 'р' }, { label: 'о' }, { label: 'л' }, { label: 'д' }, { label: 'ж' }, { label: 'э' }],
        [{ label: 'я' }, { label: 'ч' }, { label: 'с' }, { label: 'м' }, { label: 'и' }, { label: 'т' }, { label: 'ь' }, { label: 'б' }, { label: 'ю' }, { label: '.' }, { label: '@' }],
        [{ label: 'ABC', action: 'toggle-lang', wide: true }, { label: ' ', action: 'space', wide: true }, { icon: Backspace, action: 'backspace', wide: true }],
      ]
      layout.splice(0, layout.length, ...ru)
    }
    return
  }
  if (key.action === 'backspace') {
    emit('update:modelValue', props.modelValue.slice(0, -1))
    return
  }
  if (key.action === 'space') {
    emit('update:modelValue', props.modelValue + ' ')
    return
  }
  emit('update:modelValue', props.modelValue + key.label)
}
</script>

<style scoped>
.virtual-keyboard {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 4px;
  user-select: none;
}
.kb-row {
  display: flex;
  gap: 4px;
  justify-content: center;
}
.kb-key {
  min-width: 32px;
  height: 38px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 6px;
  transition: background 0.1s;
  flex: 1;
  max-width: 42px;
}
.kb-key:active {
  background: var(--accent, #6366f1);
  color: #fff;
}
.kb-wide {
  flex: 2;
  max-width: none;
}
</style>

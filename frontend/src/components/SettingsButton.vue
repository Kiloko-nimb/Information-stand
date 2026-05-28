<!--
  SettingsButton — плавающая кнопка-настройки в углу экрана.
  При нажатии открывает выпадашку с переключателями темы, языка и звука.
-->
<template>
  <div class="settings-wrap">
    <button class="settings-btn" @click="togglePanel" :title="'Настройки'">
      <Icon name="settings" :size="22" />
    </button>

    <transition name="fade-pop">
      <div v-if="open" class="settings-panel" @click.stop>
        <!-- Тема -->
        <div class="panel-section">
          <div class="panel-label">Тема</div>
          <div class="panel-row">
            <button
              v-for="th in themes"
              :key="th.id"
              class="opt"
              :class="{ active: theme === th.id }"
              @click="onTheme(th.id)"
            >
              <Icon :name="th.icon" :size="16" />
              <span>{{ th.name }}</span>
            </button>
          </div>
        </div>

        <!-- Язык -->
        <div class="panel-section">
          <div class="panel-label">Язык / Language</div>
          <div class="panel-row">
            <button
              v-for="loc in locales"
              :key="loc.id"
              class="opt"
              :class="{ active: locale === loc.id }"
              @click="onLocale(loc.id)"
            >
              <span class="opt-flag">{{ loc.short }}</span>
              <span>{{ loc.name }}</span>
            </button>
          </div>
        </div>

        <!-- Звуки -->
        <div class="panel-section">
          <div class="panel-label">Звуковые эффекты</div>
          <button class="opt opt-toggle" :class="{ active: soundsOn }" @click="onSound">
            <Icon :name="soundsOn ? 'bell' : 'bellOff'" :size="16" />
            <span>{{ soundsOn ? 'Включены' : 'Выключены' }}</span>
          </button>
        </div>
      </div>
    </transition>

    <!-- Невидимый клик-перехватчик для закрытия -->
    <div v-if="open" class="settings-overlay" @click="open = false"></div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Icon from './Icon.vue'
import { useTheme, AVAILABLE_THEMES } from '../composables/useTheme'
import { useI18n } from '../composables/useI18n'
import { useSound } from '../composables/useSound'

export default {
  name: 'SettingsButton',
  components: { Icon },
  setup() {
    const open = ref(false)
    const { theme, setTheme } = useTheme()
    const { locale, setLocale } = useI18n()
    const { enabled: soundsOn, toggle: toggleSound, play } = useSound()

    function togglePanel() {
      open.value = !open.value
      play.click()
    }
    function onTheme(id) { setTheme(id); play.tap() }
    function onLocale(id) { setLocale(id); play.tap() }
    function onSound() {
      // если включаем — после переключения тоже играем (приятный фидбек)
      toggleSound()
      if (soundsOn.value) play.success()
    }

    return {
      open, theme, locale, soundsOn,
      themes: AVAILABLE_THEMES,
      locales: useI18n().locales,
      togglePanel, onTheme, onLocale, onSound,
    }
  },
}
</script>

<style scoped>
.settings-wrap {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9000;
}
.settings-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--bg-raised);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  color: var(--text);
  display: grid;
  place-items: center;
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition);
}
.settings-btn:hover {
  transform: rotate(60deg);
  box-shadow: var(--shadow);
}
.settings-overlay {
  position: fixed;
  inset: 0;
  z-index: 8999;
}
.settings-panel {
  position: absolute;
  top: 56px;
  right: 0;
  width: 280px;
  background: var(--bg-raised);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  z-index: 9001;
}
.panel-section { display: flex; flex-direction: column; gap: 0.45rem; }
.panel-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}
.panel-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}
.opt {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.55rem 0.7rem;
  border-radius: var(--radius-md);
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 0.85rem;
  cursor: pointer;
  transition: background var(--transition), border-color var(--transition);
}
.opt:hover { background: var(--surface-hover); }
.opt.active {
  background: var(--accent-soft);
  border-color: var(--accent-border);
  color: var(--accent);
  font-weight: 700;
}
.opt-toggle {
  width: 100%;
  justify-content: center;
}
.opt-flag {
  font-weight: 800;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
}
.fade-pop-enter-from { opacity: 0; transform: translateY(-6px) scale(0.96); }
.fade-pop-leave-to { opacity: 0; transform: translateY(-6px) scale(0.96); }
.fade-pop-enter-active, .fade-pop-leave-active {
  transition: opacity 180ms var(--ease), transform 180ms var(--ease-spring);
}
</style>

<!--
  BaseModal — общий компонент модалки.

  Заменяет три копии-вставки в Home.vue (showPassingScores / showSpecialties /
  showApplicationQR), которые до этого собирались императивно через
  document.createElement + innerHTML. Из-за копипасты у двух из трёх модалок
  расходились стили (см. PR #2: align-items:flex-start vs center).

  Использование::

      <BaseModal v-model="open" title="Заголовок" :max-width="900">
        <template #default>
          ...любой HTML / Vue-разметка...
        </template>
      </BaseModal>

  Закрывается:
    * кликом по фону (только по самому overlay, не по карточке внутри)
    * кнопкой «Закрыть» внизу карточки
    * клавишей Escape
-->
<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div
        v-if="modelValue"
        class="modal-overlay"
        role="dialog"
        aria-modal="true"
        @click.self="close"
      >
        <div class="modal-card" :style="cardStyle">
          <h2 v-if="title || $slots.title" class="modal-title">
            <slot name="title">
              <Icon v-if="titleIcon" :name="titleIcon" :size="26" class="modal-title-icon" />
              <span>{{ title }}</span>
            </slot>
          </h2>
          <p v-if="subtitle" class="modal-subtitle">{{ subtitle }}</p>
          <div class="modal-body">
            <slot />
          </div>
          <button class="modal-close" type="button" @click="close">
            {{ closeLabel }}
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
import { computed, onBeforeUnmount, watch } from 'vue'
import Icon from './Icon.vue'

export default {
  name: 'BaseModal',
  components: { Icon },
  props: {
    modelValue: { type: Boolean, default: false },
    title: { type: String, default: '' },
    /* Имя иконки из Icon.vue для отображения слева от заголовка. */
    titleIcon: { type: String, default: '' },
    subtitle: { type: String, default: '' },
    maxWidth: { type: [Number, String], default: 760 },
    closeLabel: { type: String, default: 'Закрыть' },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const close = () => emit('update:modelValue', false)

    const cardStyle = computed(() => {
      const v = props.maxWidth
      const value = typeof v === 'number' ? `${v}px` : v
      return { maxWidth: value }
    })

    const onKeydown = (e) => {
      if (e.key === 'Escape' && props.modelValue) {
        close()
      }
    }

    watch(
      () => props.modelValue,
      (open) => {
        if (typeof window === 'undefined') return
        if (open) {
          window.addEventListener('keydown', onKeydown)
        } else {
          window.removeEventListener('keydown', onKeydown)
        }
      },
      { immediate: true },
    )

    onBeforeUnmount(() => {
      if (typeof window !== 'undefined') {
        window.removeEventListener('keydown', onKeydown)
      }
    })

    return { close, cardStyle }
  },
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  overflow-y: auto;
  padding: 2rem;
}

.modal-card {
  background: linear-gradient(160deg, #ffffff 0%, #f7f9fd 100%);
  padding: 2.25rem;
  border-radius: 24px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18);
  border: 1px solid rgba(15, 23, 42, 0.10);
  font-family: 'Inter', system-ui, sans-serif;
}

.modal-title {
  color: #0f172a;
  margin: 0 0 0.5rem;
  font-family: 'Manrope', 'Inter', system-ui, sans-serif;
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  text-align: center;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
  width: 100%;
}

.modal-title-icon {
  color: #2563EB;
  flex-shrink: 0;
}

/* Когда подзаголовка нет — даём заголовку обычный нижний отступ. */
.modal-title:last-of-type {
  margin-bottom: 1.5rem;
}

.modal-subtitle {
  color: rgba(15, 23, 42, 0.6);
  text-align: center;
  margin: 0 0 1.5rem;
  font-size: 0.92rem;
}

.modal-body {
  /* Дочерним блокам (карточкам с фоном #f5f7fb) отступ задаётся
     самим контентом — не вмешиваемся. */
}

.modal-close {
  width: 100%;
  padding: 0.9rem 2rem;
  background: linear-gradient(135deg, #2563EB 0%, #0EA5B7 100%);
  color: #ffffff;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 700;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.modal-close:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 24px rgba(37, 99, 235, 0.35);
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.15s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>

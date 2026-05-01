/*
  v-ripple — сенсорная Material-like анимация «волны» от точки касания.
  Интересна в первую очередь для нашего киоска с touch-экраном: даёт
  явный визуальный отклик на тап, когда :hover физически не работает.

  Использование:
    <button v-ripple>…</button>
    <div class="feature-card" v-ripple="{ color: 'rgba(37,99,235,.25)' }">…</div>

  Директива самостоятельно:
    - делает position: relative на хосте (если не было),
    - устанавливает overflow: hidden (иначе волна вылезет за радиус),
    - вешает pointerdown-обработчик, создаёт span с анимацией,
    - чистит span после окончания анимации,
    - на размонтировании корректно снимает слушатели.

  Активируется только на сенсорных устройствах (html[data-touch="1"]) —
  на обычном мониторе с мышью мы не хотим перекрашивать hover/ripple'ом,
  там :hover и так работает. Флаг ставит App.vue при монтировании.
*/

const DEFAULT_COLOR = 'currentColor'
const DEFAULT_OPACITY = 0.22
const DURATION = 550

function isTouchMode() {
  return document.documentElement.getAttribute('data-touch') === '1'
}

function onPointerDown(event) {
  const el = this
  if (!isTouchMode()) return
  // Не мешаем жестам в элементах, где ripple будет визуально мешать:
  // поля ввода, textarea и т.д. CSS-хинт через data-no-ripple.
  if (el.hasAttribute('data-no-ripple')) return

  const rect = el.getBoundingClientRect()
  const size = Math.max(rect.width, rect.height) * 2
  const x = (event.clientX ?? rect.left + rect.width / 2) - rect.left
  const y = (event.clientY ?? rect.top + rect.height / 2) - rect.top

  const opts = el._rippleOptions || {}
  const color = opts.color || DEFAULT_COLOR
  const opacity = opts.opacity ?? DEFAULT_OPACITY

  const span = document.createElement('span')
  span.className = '__ripple'
  span.style.cssText = `
    position: absolute;
    left: ${x}px;
    top: ${y}px;
    width: ${size}px;
    height: ${size}px;
    margin-left: ${-size / 2}px;
    margin-top: ${-size / 2}px;
    border-radius: 50%;
    background: ${color};
    opacity: ${opacity};
    pointer-events: none;
    transform: scale(0);
    transition: transform ${DURATION}ms cubic-bezier(0.4, 0, 0.2, 1),
                opacity ${DURATION}ms ease-out;
    z-index: 0;
  `
  // Гарантируем нужный хост-стейт (position + overflow) один раз.
  if (el.__rippleHostApplied !== true) {
    const host = getComputedStyle(el)
    if (host.position === 'static') el.style.position = 'relative'
    if (host.overflow === 'visible') el.style.overflow = 'hidden'
    el.__rippleHostApplied = true
  }
  el.appendChild(span)

  // Запускаем анимацию на следующем кадре.
  requestAnimationFrame(() => {
    span.style.transform = 'scale(1)'
    span.style.opacity = '0'
  })
  window.setTimeout(() => {
    span.remove()
  }, DURATION + 50)
}

export const ripple = {
  mounted(el, binding) {
    el._rippleOptions = binding.value || {}
    el._rippleHandler = onPointerDown
    el.addEventListener('pointerdown', el._rippleHandler)
  },
  updated(el, binding) {
    el._rippleOptions = binding.value || {}
  },
  unmounted(el) {
    if (el._rippleHandler) {
      el.removeEventListener('pointerdown', el._rippleHandler)
      delete el._rippleHandler
    }
  },
}

export default ripple

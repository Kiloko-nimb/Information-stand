#!/usr/bin/env python3
"""
Generate MapFloor{N}.vue components from Inkscape-labeled SVG files.

Input: tools/floor-svgs/floor{N}.svg, each with rect elements that have
       inkscape:label = "rect<number>" (cabinet) or "rect-<name>" (named).
Output: frontend/src/components/MapFloor{N}.vue.

The script:
- Normalizes transform="scale(1,-1)" on rects (Inkscape flips).
- Strips Inkscape/Sodipodi namespace clutter.
- Replaces each labeled rect with a Vue-bound rect (`class="room"`,
  `v-bind="roomBind('NNN')"` or `v-bind="roomBind('rect-NAME')"`).
- Adds a centered <text> label on each room (room number for cabinets, a
  Russian short word for named ones — "Лестница", "Туалет", "Приёмная").
- Preserves all walls/doors/etc paths from the source SVG verbatim.

This script is meant to be re-run any time the floor SVGs change; the
generated .vue files are committed to git.
"""
from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "tools" / "floor-svgs"
OUT_DIR = ROOT / "frontend" / "src" / "components"

# Register namespaces so ET preserves them in lookups (we'll strip them out
# of output ourselves).
NS = {
    "svg": "http://www.w3.org/2000/svg",
    "inkscape": "http://www.inkscape.org/namespaces/inkscape",
    # Inkscape's own namespace URI for sodipodi:nodetypes etc. has shifted
    # between Inkscape 0.x and 1.x; both forms appear in the wild. The strip
    # logic below matches any sodipodi-* URL anyway, but we keep the canonical
    # one here so ET.register_namespace serializes the prefix.
    "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix if prefix != "svg" else "", uri)

INKSCAPE_LABEL = f"{{{NS['inkscape']}}}label"

# Vue-side labels for named (non-numbered) rects. Keys are the suffix after
# "rect-" in the canonical Inkscape label. Короткие односимвольные
# подписи лучше читаются на карте; расшифровка живёт в легенде на странице.
NAMED_LABEL_TEXT = {
    "stairs-left": "Л",
    "stairs-center": "Л",
    "stairs-right": "Л",
    "wc-w": "Ж",
    "wc-m": "М",
    "reception": "Приёмная",
    "hall": "Актовый зал",
    "gym": "Спортзал",
    "library": "Библиотека",
    "reading": "Читальный зал",
    "medical": "Медпункт",
    "bufet": "Буфет",
    "canteen": "Столовая",
    "garderob": "Гардероб",
}

# Алиасы для лейблов, которые пользователь может нарисовать без префикса
# "rect-" и/или в другой раскладке. Ключ — исходный лейбл в ловеркейсе,
# значение — канонический ключ из NAMED_LABEL_TEXT.
NAMED_ALIASES = {
    "assembly-hall": "hall",
    "sports-hall": "gym",
    "sport-hall": "gym",
    "reading-room": "reading",
    "medical-office": "medical",
    "stolovai": "canteen",
    "stolovaya": "canteen",
}

# Подписи, которые рисуются крупно (как и номера кабинетов) — единичные
# буквы достаточно короткие, чтобы поместиться, и заметнее «крупным» шрифтом.
LARGE_NAMED_LABELS = {"Л", "Ж", "М"}

# Russian floor names for the header.
FLOOR_NAME = {1: "1 этаж", 2: "2 этаж", 3: "3 этаж", 4: "4 этаж"}


def _strip_ns(tag: str) -> str:
    """Strip XML namespace from a tag name."""
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _attrib_no_ns(elem: ET.Element) -> dict[str, str]:
    """Return element attributes with the inkscape/sodipodi namespace stripped.

    Any attribute key of the form `{namespace-uri}local-name` is rewritten to
    `prefix:local-name` if the namespace is one of inkscape/sodipodi (those
    get dropped from output downstream), and dropped entirely otherwise so
    that no stray Clark-notation keys leak into the rendered Vue template.
    """
    out: dict[str, str] = {}
    for key, value in elem.attrib.items():
        if key.startswith("{") and "}" in key:
            uri, local = key[1:].split("}", 1)
            if uri == NS["inkscape"]:
                out[f"inkscape:{local}"] = value
            elif "sodipodi.sourceforge.net" in uri:
                out[f"sodipodi:{local}"] = value
            # Unknown namespace — silently drop it.
            continue
        out[key] = value
    return out


def _normalize_rect_geometry(elem: ET.Element) -> dict[str, float]:
    """Return normalized x/y/width/height (Inkscape transform=scale(1,-1) folded in).

    Some Inkscape edits leave a transform="scale(1,-1)" on the rect with a
    negative y coordinate. Visually correct, but a pain for downstream tools.
    Fold it into plain coordinates.
    """
    x = float(elem.attrib.get("x", "0"))
    y = float(elem.attrib.get("y", "0"))
    w = float(elem.attrib.get("width", "0"))
    h = float(elem.attrib.get("height", "0"))
    transform = elem.attrib.get("transform", "").strip()
    if transform:
        # We only know how to fold scale(1,-1); anything else, bail loudly.
        if re.fullmatch(r"scale\(\s*1\s*,\s*-1\s*\)", transform):
            y = -(y + h)
        else:
            raise RuntimeError(
                f"rect has unsupported transform={transform!r}; please normalize it in Inkscape first"
            )
    return {"x": x, "y": y, "width": w, "height": h}


def _serialize_attrs(attrs: dict[str, str]) -> str:
    parts = []
    for k, v in attrs.items():
        # Skip Inkscape-only attributes — they're irrelevant in the browser.
        if k.startswith("inkscape:") or k.startswith("sodipodi:"):
            continue
        # Skip XML namespace declarations (they live on the root <svg>).
        if k.startswith("xmlns"):
            continue
        parts.append(f'{k}="{v}"')
    return " ".join(parts)


def _serialize_element(elem: ET.Element, depth: int = 0) -> str:
    """Recursively serialize an element to SVG markup, with Inkscape junk stripped."""
    tag = _strip_ns(elem.tag)
    if tag in ("namedview", "metadata"):
        return ""
    attrs = _attrib_no_ns(elem)
    attrs_str = _serialize_attrs(attrs)
    children = list(elem)
    if children:
        inner = "".join(_serialize_element(c, depth + 1) for c in children)
        text = (elem.text or "").strip()
        return f"<{tag} {attrs_str}>{text}{inner}</{tag}>"
    # Self-closing where possible.
    text = (elem.text or "").strip()
    if text:
        return f"<{tag} {attrs_str}>{text}</{tag}>"
    return f"<{tag} {attrs_str}/>"


def _parse_room_rects(root: ET.Element) -> list[tuple[str, dict[str, float], ET.Element]]:
    """Find all rect[inkscape:label] and return (canonical_label, geometry, element).

    Skips the unlabeled background rect (820×900 white) and any rect whose label
    is not a room (e.g. `stand`, handled separately).
    """
    out = []
    for rect in root.iter(f"{{{NS['svg']}}}rect"):
        raw_label = rect.attrib.get(INKSCAPE_LABEL)
        if not raw_label:
            continue
        canonical = _canonicalize_label(raw_label)
        if canonical is None:
            continue
        geom = _normalize_rect_geometry(rect)
        out.append((canonical, geom, rect))
    return out


def _parse_stand(root: ET.Element) -> dict[str, float] | None:
    """Find the inkscape:label="stand" element (ellipse/circle/rect).

    Returns its center as {"cx": float, "cy": float} in source-svg coordinates
    (i.e. before any parent <g transform> is applied; we keep the transform
    on the wrapper in the rendered output, so coords stay consistent).
    None if no stand marker was placed on this floor.
    """
    for elem in root.iter():
        if elem.attrib.get(INKSCAPE_LABEL) != "stand":
            continue
        tag = _strip_ns(elem.tag)
        if tag in ("ellipse", "circle"):
            return {
                "cx": float(elem.attrib.get("cx", "0")),
                "cy": float(elem.attrib.get("cy", "0")),
            }
        if tag == "rect":
            geom = _normalize_rect_geometry(elem)
            return {
                "cx": geom["x"] + geom["width"] / 2,
                "cy": geom["y"] + geom["height"] / 2,
            }
    return None


def _canonicalize_label(label: str) -> str | None:
    """Bring a free-form Inkscape label to canonical form.

    Returns one of:
      - "rect<digits>"     for numbered cabinets,
      - "rect-<key>"       for named rooms (key from NAMED_LABEL_TEXT),
      - None               for labels we don't care about (e.g. "stand",
                           which is rendered as a separate marker, not a room).

    Raises if the label looks like a room label but we don't recognize it.
    """
    raw = label.strip()
    if not raw:
        return None
    if raw == "stand":
        return None
    if re.fullmatch(r"rect\d+", raw):
        return raw
    # Strip optional "rect-" prefix and normalize case for named rooms.
    key = raw[5:] if raw.startswith("rect-") else raw
    key = key.lower()
    key = NAMED_ALIASES.get(key, key)
    if key in NAMED_LABEL_TEXT:
        return f"rect-{key}"
    raise RuntimeError(
        f"Unknown room label {label!r}: not a numbered cabinet (rectNNN) and not"
        f" a known named-room key (one of {sorted(NAMED_LABEL_TEXT)}) or an alias"
        f" of one (one of {sorted(NAMED_ALIASES)})."
    )


def _bind_name_for_label(label: str) -> str:
    """Convert a canonical label into the argument passed to roomBind(...) in Vue."""
    if re.fullmatch(r"rect\d+", label):
        return label[len("rect"):]  # "rect215" -> "215"
    if label.startswith("rect-"):
        return label  # keep "rect-stairs-left", "rect-wc-w" verbatim
    return label


def _label_text(bind_name: str) -> str | None:
    """Visible text for the room label on the map."""
    if bind_name.isdigit():
        return bind_name
    if bind_name.startswith("rect-"):
        key = bind_name[len("rect-"):]
        return NAMED_LABEL_TEXT.get(key)
    return None


# Средняя ширина глифа в долях font-size. Для кириллицы и цифр
# в обычных sans-serif (которые браузер подберёт) это ± 0.55.
GLYPH_WIDTH_EM = 0.55
# Отступ от стенок кабинета при измерении "влезёт ли подпись".
LABEL_PADDING = 6  # по пикселей с каждой стороны
# Границы font-size для авто-фита.
MIN_LABEL_FONT = 9
MAX_LABEL_FONT_LARGE = 24  # цифры/Л/Ж/М
MAX_LABEL_FONT_SMALL = 14  # длинные слова


def _fit_font_size(text: str, max_width: float, ideal_size: float) -> float:
    """Найти максимальный font-size ≤ ideal_size, при котором text влезает в max_width."""
    if not text or max_width <= 0:
        return ideal_size
    needed = len(text) * GLYPH_WIDTH_EM
    if needed * ideal_size <= max_width:
        return ideal_size
    fitted = max_width / needed
    return max(MIN_LABEL_FONT, fitted)


def _split_two_lines(text: str) -> tuple[str, str] | None:
    """Попытаться разбить подпись на две ровные строки по пробелу.

    "Актовый зал" → ("Актовый", "зал").
    "Читальный зал" → ("Читальный", "зал").
    Если пробелов нет — возвращаем None (одна строка останется).
    """
    if " " not in text:
        return None
    words = text.split(" ")
    if len(words) == 2:
        return words[0], words[1]
    # Эвристика «пополам»: берём точку разбивки, при которой длины
    # строк максимально близки. На наших подписях всё равно в худшем случае
    # 2-3 слова, поэтому брутфорсъем.
    best = None
    target = sum(len(w) for w in words) / 2
    for i in range(1, len(words)):
        left = " ".join(words[:i])
        right = " ".join(words[i:])
        diff = abs(len(left) - target) + abs(len(right) - target)
        if best is None or diff < best[0]:
            best = (diff, left, right)
    assert best is not None
    return best[1], best[2]


def _render_room_block(label: str, geom: dict[str, float]) -> tuple[str, str]:
    """Return (rect_markup, text_markup) for a single room.

    Подпись автоматически уменьшается до ширины кабинета,
    а если и после уменьшения не влезает — разбивается на две строки.
    """
    bind_name = _bind_name_for_label(label)
    # Round to 2 decimals to keep the file readable; Inkscape generates
    # ridiculous precision otherwise.
    x = round(geom["x"], 2)
    y = round(geom["y"], 2)
    w = round(geom["width"], 2)
    h = round(geom["height"], 2)
    # Add `rx`/`ry` for slightly rounded corners — looks softer with the
    # drop-shadow filter.
    rect = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" '
        f'class="room" v-bind="roomBind(\'{bind_name}\')"/>'
    )
    text_content = _label_text(bind_name)
    if text_content is None:
        return rect, ""

    cx = x + w / 2
    cy = y + h / 2
    available_width = max(w - 2 * LABEL_PADDING, 1)
    is_large = bind_name.isdigit() or text_content in LARGE_NAMED_LABELS
    ideal = MAX_LABEL_FONT_LARGE if is_large else MAX_LABEL_FONT_SMALL

    # Однострочный вариант.
    single_size = _fit_font_size(text_content, available_width, ideal)
    # Если влезает приёмлемым шрифтом — строим одной строкой.
    if single_size >= ideal * 0.7 or " " not in text_content:
        size_attr = f' font-size="{_fmt(round(single_size, 2))}"' if single_size < ideal else ""
        # +0.36*size — примерное вертикальное центрирование базовой линии.
        text_y = round(cy + single_size * 0.36, 2)
        css_class = "room-label" if is_large else "room-label small"
        text = (
            f'<text x="{round(cx, 2)}" y="{text_y}" class="{css_class}"{size_attr}>'
            f"{text_content}</text>"
        )
        return rect, text

    # Двухстрочный вариант: «Читальный\nзал».
    split = _split_two_lines(text_content)
    if split is None:
        # Не разбивается — оставляем одной строкой на минимальном шрифте.
        size_attr = f' font-size="{_fmt(round(single_size, 2))}"'
        text_y = round(cy + single_size * 0.36, 2)
        text = (
            f'<text x="{round(cx, 2)}" y="{text_y}" class="room-label small"{size_attr}>'
            f"{text_content}</text>"
        )
        return rect, text

    line1, line2 = split
    longest = max(len(line1), len(line2))
    fitted = available_width / (longest * GLYPH_WIDTH_EM) if longest else ideal
    two_size = min(ideal, fitted)
    two_size = max(MIN_LABEL_FONT, two_size)
    line_height = two_size * 1.05
    # Центрируем блок из двух строк по вертикали относительно cy.
    y1 = round(cy - line_height / 2 + two_size * 0.36, 2)
    y2 = round(cy + line_height / 2 + two_size * 0.36, 2)
    size_attr = f' font-size="{_fmt(round(two_size, 2))}"'
    text = (
        f'<text x="{round(cx, 2)}" y="{y1}" class="room-label small"{size_attr}>'
        f"{line1}</text>"
        f'\n          <text x="{round(cx, 2)}" y="{y2}" class="room-label small"{size_attr}>'
        f"{line2}</text>"
    )
    return rect, text


def _is_glyph_path(elem: ET.Element) -> bool:
    """True if this <path> is a vectorized glyph (room number drawn as text in Inkscape).

    Heuristic: glyphs have a non-empty `fill` attribute and no `stroke`
    (Inkscape's `Path → Object to Path` on text produces filled paths
    with curves). Walls in our SVGs are stroked lines with no fill.
    """
    if _strip_ns(elem.tag) != "path":
        return False
    fill = (elem.attrib.get("fill") or "").strip().lower()
    stroke = (elem.attrib.get("stroke") or "").strip().lower()
    if not fill or fill == "none":
        return False
    if stroke and stroke != "none":
        return False
    return True


def _is_background_rect(elem: ET.Element, vb_w: float, vb_h: float) -> bool:
    """True if this is the unlabeled white «page» background rect from Inkscape/Figma.

    Matches either:
    - the 820×900 rect that Figma exports stuck onto our floors 2–4, or
    - any «почти весь viewBox» unlabeled rect on other floors.
    """
    try:
        w = float(elem.attrib.get("width", "0"))
        h = float(elem.attrib.get("height", "0"))
    except ValueError:
        return False
    if w == 820 and h == 900:
        return True
    # Tolerate small floating-point noise from Inkscape.
    if vb_w > 0 and vb_h > 0 and w >= vb_w * 0.95 and h >= vb_h * 0.95:
        return True
    return False


def _render_non_room_children(root_g: ET.Element, rooms: set[int], vb_w: float, vb_h: float) -> str:
    """Serialize all children of the root <g> except labeled rects.

    Also skips:
    - the unlabeled near-full-viewBox white background rect (we paint our own
      bg-dots pattern),
    - vectorized glyph paths (room numbers drawn as text in Inkscape and
      converted to outlines) — we add fresh, Vue-controlled <text>
      labels instead,
    - raw <text> elements typed by the user in Inkscape (пользовательские
      «Б», «Буфет», «Столовая» и т.п.) — мы рисуем свои подписи с авто-фитом
      и единым стилем,
    - the `stand` ellipse/rect (rendered separately as a «вы здесь» marker).
    """
    out_parts = []
    for child in root_g:
        if id(child) in rooms:
            continue
        if child.attrib.get(INKSCAPE_LABEL) == "stand":
            continue
        tag = _strip_ns(child.tag)
        if tag == "rect" and _is_background_rect(child, vb_w, vb_h):
            continue
        if tag in ("namedview", "metadata", "defs"):
            continue
        # Live <text> typed inside Inkscape (не переведён в кривые) — выкидываем.
        if tag in ("text", "flowRoot"):
            continue
        if _is_glyph_path(child):
            continue
        out_parts.append(_serialize_element(child))
    return "\n          ".join(out_parts)


VUE_TEMPLATE = """<template>
  <div class="map-floor">
    <div class="map-header">
      <h2>{floor_name}</h2>
    </div>

    <div class="map-container">
      <svg
        width="{svg_width}"
        height="{svg_height}"
        viewBox="{view_box}"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        @click="handleSvgClick"
      >
        <defs>
          <!-- Точечный фон коридоров — снимает белизну чертёжной заливки. -->
          <pattern id="bg-dots-{floor_number}" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
            <rect width="22" height="22" fill="#f8fafc"/>
            <circle cx="11" cy="11" r="1" fill="#cbd5e1" opacity="0.65"/>
          </pattern>
          <!-- Лёгкая тень под комнатами для объёма. -->
          <filter id="room-shadow-{floor_number}" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08"/>
          </filter>
        </defs>

        <rect x="{vb_x}" y="{vb_y}" width="{vb_w}" height="{vb_h}" fill="url(#bg-dots-{floor_number})"/>

        <g{wrapper_transform_attr}>
          <!-- Стены, двери и прочая графика из исходного Inkscape-файла. -->
{walls}

          <!-- Кабинеты и именованные помещения. -->
{rooms}

          <!-- Подписи кабинетов (центрированы поверх прямоугольников). -->
{labels}
        </g>

        <!-- Точка инфо-стенда («вы здесь») — в координатах viewBox. -->
{stand_marker}
      </svg>
    </div>
  </div>
</template>

<script>
import {{ computed }} from 'vue'

// Маппинг room_type (из бэкенда) → CSS-класс цвета.
const TYPE_KEY_BY_LABEL = {{
  'Аудитория': 'auditorium',
  'Лаборатория': 'lab',
  'Спортзал': 'sport',
  'Актовый зал': 'hall',
  'Приёмная': 'admin',
  'Приемная': 'admin',
}}

// Карта именованных (не-числовых) кабинетов в типы — для подсветки и легенды.
const NAMED_TYPE_KEY = {{
  'rect-reception': 'admin',
  'rect-wc-w': 'wc',
  'rect-wc-m': 'wc',
  'rect-stairs-left': 'stairs',
  'rect-stairs-center': 'stairs',
  'rect-stairs-right': 'stairs',
  'rect-hall': 'hall',
  'rect-gym': 'sport',
  'rect-library': 'library',
  'rect-reading': 'library',
  'rect-medical': 'medical',
  'rect-bufet': 'food',
  'rect-canteen': 'food',
  'rect-garderob': 'garderob',
}}

export default {{
  name: 'MapFloor{floor_number}',
  props: {{
    highlightFreeRooms: {{ type: Boolean, default: false }},
    freeRooms: {{ type: Array, default: () => [] }},
    busyRooms: {{ type: Array, default: () => [] }},
    highlightedRoom: {{ type: String, default: null }},
    // Мапа roomNumber → room_type из /rooms/floor/{floor_number}.
    roomTypes: {{ type: Object, default: () => ({{}}) }},
  }},
  emits: ['room-click'],
  setup(props, {{ emit }}) {{
    const freeSet = computed(() => new Set(props.freeRooms.map((r) => String(r).trim())))
    const busySet = computed(() => new Set(props.busyRooms.map((r) => String(r).trim())))
    const target = computed(() => (props.highlightedRoom ? String(props.highlightedRoom).trim() : null))

    const roomBind = (label) => {{
      const value = String(label).trim()
      const isNumeric = /^\\d+$/.test(value)
      let typeKey
      if (isNumeric) {{
        const typeLabel = props.roomTypes[value]
        typeKey = TYPE_KEY_BY_LABEL[typeLabel] || 'other'
      }} else {{
        typeKey = NAMED_TYPE_KEY[value] || 'other'
      }}
      return {{
        'data-room': isNumeric ? value : null,
        class: [
          `room--type-${{typeKey}}`,
          {{
            'room--interactive': isNumeric,
            'room--free': props.highlightFreeRooms && freeSet.value.has(value),
            'room--busy': props.highlightFreeRooms && busySet.value.has(value),
            'room--target': target.value !== null && target.value === value,
          }},
        ],
      }}
    }}

    const handleSvgClick = (event) => {{
      const t = event.target
      if (!t || typeof t.getAttribute !== 'function') return
      const num = t.getAttribute('data-room')
      if (!num) return
      emit('room-click', num)
    }}

    return {{
      roomBind,
      handleSvgClick,
    }}
  }},
}}
</script>

<style scoped>
.map-floor {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}}

.map-header {{
  margin-bottom: 2rem;
  text-align: center;
}}

.map-header h2 {{
  color: var(--text);
  font-size: 2rem;
  margin-bottom: 1rem;
}}

.map-container {{
  background: var(--surface);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: 25px;
  padding: 2rem;
  box-shadow: var(--shadow);
  overflow: auto;
}}

.map-container svg {{
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}}

text {{
  pointer-events: none;
  user-select: none;
  fill: #000000 !important;
}}

.room-label {{
  font-size: 24px;
  font-weight: bold;
  fill: #000000 !important;
  text-anchor: middle;
  pointer-events: none;
}}

.room-label.small {{
  font-size: 14px;
  fill: #475569 !important;
  font-weight: 600;
}}

.room {{
  fill: transparent;
  stroke: transparent;
  cursor: default;
  transition: fill 0.25s ease, stroke 0.25s ease, fill-opacity 0.25s ease, stroke-opacity 0.25s ease;
  filter: url(#room-shadow-{floor_number});
}}

.room.room--interactive {{
  cursor: pointer;
}}

.room--type-auditorium {{ fill: #3b82f6; fill-opacity: 0.22; stroke: #1d4ed8; stroke-opacity: 0.7;  stroke-width: 1.3; }}
.room--type-lab        {{ fill: #8b5cf6; fill-opacity: 0.26; stroke: #6d28d9; stroke-opacity: 0.75; stroke-width: 1.3; }}
.room--type-sport      {{ fill: #22c55e; fill-opacity: 0.26; stroke: #15803d; stroke-opacity: 0.75; stroke-width: 1.3; }}
.room--type-hall       {{ fill: #f97316; fill-opacity: 0.26; stroke: #c2410c; stroke-opacity: 0.75; stroke-width: 1.3; }}
.room--type-admin      {{ fill: #f59e0b; fill-opacity: 0.30; stroke: #b45309; stroke-opacity: 0.8;  stroke-width: 1.3; }}
/* Туалеты — отчётливый тёплый розовый, чтобы не сливаться с пустым (--other) и не путаться с лестницей. */
.room--type-wc         {{ fill: #ec4899; fill-opacity: 0.22; stroke: #be185d; stroke-opacity: 0.7;  stroke-width: 1.3; }}
.room--type-stairs     {{ fill: #6366f1; fill-opacity: 0.26; stroke: #4338ca; stroke-opacity: 0.75; stroke-width: 1.3; stroke-dasharray: 6 4; }}
/* Библиотека и читальный зал — бирюзовый. */
.room--type-library    {{ fill: #14b8a6; fill-opacity: 0.24; stroke: #0f766e; stroke-opacity: 0.75; stroke-width: 1.3; }}
/* Медпункт — ярко-красный, чтобы было заметно в экстренном случае. */
.room--type-medical    {{ fill: #ef4444; fill-opacity: 0.22; stroke: #b91c1c; stroke-opacity: 0.8;  stroke-width: 1.3; }}
/* Буфет и столовая — тёплый жёлтый. */
.room--type-food       {{ fill: #eab308; fill-opacity: 0.30; stroke: #a16207; stroke-opacity: 0.8;  stroke-width: 1.3; }}
/* Гардероб — нейтральный сине-серый. */
.room--type-garderob   {{ fill: #64748b; fill-opacity: 0.20; stroke: #334155; stroke-opacity: 0.7;  stroke-width: 1.3; }}
/* Кабинеты без известного типа — почти прозрачные, чтобы не конкурировать с цветными типами и не выглядеть «использованной» подсветкой. */
.room--type-other      {{ fill: #cbd5e1; fill-opacity: 0.10; stroke: #94a3b8; stroke-opacity: 0.55; stroke-width: 1; }}

/* «Вы здесь» — маркер инфо-стенда. */
.stand-marker {{
  pointer-events: none;
}}

.stand-marker .stand-halo {{
  fill: rgba(37, 99, 235, 0.25);
  animation: stand-halo-pulse-{floor_number} 1.8s ease-in-out infinite;
}}

.stand-marker .stand-dot {{
  fill: #2563eb;
  stroke: #ffffff;
  stroke-width: 2;
}}

@keyframes stand-halo-pulse-{floor_number} {{
  0%, 100% {{ opacity: 0.55; transform: scale(1); }}
  50%      {{ opacity: 0.15; transform: scale(1.6); }}
}}

.stand-marker .stand-halo {{
  transform-origin: center;
  transform-box: fill-box;
}}

.room.room--interactive:hover {{
  fill-opacity: 0.25;
  stroke-opacity: 1;
  stroke-width: 2;
}}

.room.room--target {{
  fill: rgba(37, 99, 235, 0.35) !important;
  stroke: #2563eb !important;
  stroke-width: 3 !important;
  animation: room-target-pulse-{floor_number} 1.6s ease-in-out infinite;
}}

@keyframes room-target-pulse-{floor_number} {{
  0%, 100% {{
    fill: rgba(37, 99, 235, 0.35) !important;
    stroke-opacity: 1;
  }}
  50% {{
    fill: rgba(37, 99, 235, 0.55) !important;
    stroke-opacity: 0.6;
  }}
}}

.room.room--free {{
  fill: rgba(34, 197, 94, 0.32) !important;
  stroke: rgba(22, 163, 74, 0.85) !important;
  stroke-width: 2 !important;
  animation: room-free-pulse-{floor_number} 2.4s ease-in-out infinite;
}}

.room.room--busy {{
  fill: rgba(239, 68, 68, 0.18) !important;
  stroke: rgba(220, 38, 38, 0.6) !important;
  stroke-width: 1.5 !important;
}}

@keyframes room-free-pulse-{floor_number} {{
  0%, 100% {{ fill: rgba(34, 197, 94, 0.28) !important; }}
  50%      {{ fill: rgba(34, 197, 94, 0.42) !important; }}
}}
</style>
"""


def _parse_view_box(root: ET.Element) -> tuple[float, float, float, float]:
    """Return (x, y, width, height) from the SVG root's viewBox.

    Falls back to width/height attributes if viewBox is missing.
    """
    vb = (root.attrib.get("viewBox") or "").strip()
    if vb:
        parts = re.split(r"[\s,]+", vb)
        if len(parts) == 4:
            return tuple(float(p) for p in parts)  # type: ignore[return-value]
    # Fallback: width/height attributes, assume origin (0,0).
    w = float(root.attrib.get("width", "820") or "820")
    h = float(root.attrib.get("height", "900") or "900")
    return (0.0, 0.0, w, h)


def _render_stand_marker(stand: dict[str, float] | None) -> str:
    """Render the info-stand «you-are-here» marker in viewBox coordinates.

    If no `stand` element exists on this floor, return an empty string.
    Two concentric circles: a faint pulsing halo and a solid centred dot.
    """
    if stand is None:
        return ""
    cx = round(stand["cx"], 2)
    cy = round(stand["cy"], 2)
    return (
        f"        <g class=\"stand-marker\">\n"
        f"          <circle class=\"stand-halo\" cx=\"{cx}\" cy=\"{cy}\" r=\"12\"/>\n"
        f"          <circle class=\"stand-dot\"  cx=\"{cx}\" cy=\"{cy}\" r=\"6\"/>\n"
        f"        </g>"
    )


def generate_floor(floor_number: int) -> None:
    src = SVG_DIR / f"floor{floor_number}.svg"
    out = OUT_DIR / f"MapFloor{floor_number}.vue"
    tree = ET.parse(src)
    root = tree.getroot()

    # The drawing lives inside the topmost <g> child of <svg>. We propagate
    # its `transform` attribute (Inkscape sometimes shifts the whole drawing
    # by translate(...)) onto a wrapper <g> in the output, but we strip the
    # `clip-path` because Figma exports a dangling reference that clips out
    # everything we draw outside the original Figma frame.
    root_g = None
    for child in root:
        if _strip_ns(child.tag) == "g":
            root_g = child
            break
    if root_g is None:
        raise RuntimeError(f"{src}: no top-level <g> found")
    root_g_transform = root_g.attrib.get("transform", "").strip()

    vb_x, vb_y, vb_w, vb_h = _parse_view_box(root)
    svg_width = root.attrib.get("width") or f"{vb_w}"
    svg_height = root.attrib.get("height") or f"{vb_h}"

    rooms = _parse_room_rects(root)
    room_ids = {id(elem) for _, _, elem in rooms}
    stand = _parse_stand(root)

    room_blocks = []
    label_blocks = []
    for label, geom, _elem in rooms:
        rect_markup, text_markup = _render_room_block(label, geom)
        room_blocks.append(rect_markup)
        if text_markup:
            label_blocks.append(text_markup)

    walls_markup = _render_non_room_children(root_g, room_ids, vb_w, vb_h)

    wrapper_transform_attr = (
        f' transform="{root_g_transform}"' if root_g_transform else ""
    )

    content = VUE_TEMPLATE.format(
        floor_number=floor_number,
        floor_name=FLOOR_NAME[floor_number],
        svg_width=svg_width,
        svg_height=svg_height,
        view_box=f"{_fmt(vb_x)} {_fmt(vb_y)} {_fmt(vb_w)} {_fmt(vb_h)}",
        vb_x=_fmt(vb_x),
        vb_y=_fmt(vb_y),
        vb_w=_fmt(vb_w),
        vb_h=_fmt(vb_h),
        wrapper_transform_attr=wrapper_transform_attr,
        walls=walls_markup,
        rooms="\n          ".join(room_blocks),
        labels="\n          ".join(label_blocks),
        stand_marker=_render_stand_marker(stand),
    )
    out.write_text(content, encoding="utf-8")
    extra = []
    if stand is not None:
        extra.append("stand-marker")
    if root_g_transform:
        extra.append("transform-preserved")
    extras = f" [{', '.join(extra)}]" if extra else ""
    print(f"Wrote {out} ({len(rooms)} rooms, {len(label_blocks)} labels){extras}")


def _fmt(value: float) -> str:
    """Format a float without trailing zeros: 820.0 → '820', 1005.87 → '1005.87'."""
    if value == int(value):
        return str(int(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def main() -> None:
    for floor in (1, 2, 3, 4):
        generate_floor(floor)


if __name__ == "__main__":
    main()

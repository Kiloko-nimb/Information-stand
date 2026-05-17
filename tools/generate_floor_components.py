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
    "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.0.dtd",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix if prefix != "svg" else "", uri)

INKSCAPE_LABEL = f"{{{NS['inkscape']}}}label"

# Vue-side labels for named (non-numbered) rects. Keys are the suffix after
# "rect-" in the Inkscape label.
NAMED_LABEL_TEXT = {
    "stairs-left": "Лестница",
    "stairs-center": "Лестница",
    "stairs-right": "Лестница",
    "wc-w": "Туалет Ж",
    "wc-m": "Туалет М",
    "reception": "Приёмная",
    "hall": "Актовый зал",
    "gym": "Спортзал",
}

# Russian floor names for the header.
FLOOR_NAME = {2: "2 этаж", 3: "3 этаж", 4: "4 этаж"}


def _strip_ns(tag: str) -> str:
    """Strip XML namespace from a tag name."""
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _attrib_no_ns(elem: ET.Element) -> dict[str, str]:
    """Return element attributes with the inkscape/sodipodi namespace stripped."""
    out: dict[str, str] = {}
    for key, value in elem.attrib.items():
        if key.startswith(f"{{{NS['inkscape']}}}"):
            out[f"inkscape:{key.split('}', 1)[1]}"] = value
        elif key.startswith(f"{{{NS['sodipodi']}}}"):
            out[f"sodipodi:{key.split('}', 1)[1]}"] = value
        else:
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
    """Find all rect[inkscape:label] and return (label, geometry, element).

    Skips the unlabeled background rect (820×900 white).
    """
    out = []
    for rect in root.iter(f"{{{NS['svg']}}}rect"):
        label = rect.attrib.get(INKSCAPE_LABEL)
        if not label:
            continue
        geom = _normalize_rect_geometry(rect)
        out.append((label, geom, rect))
    return out


def _bind_name_for_label(label: str) -> str:
    """Convert an Inkscape label into the argument passed to roomBind(...) in Vue."""
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


def _render_room_block(label: str, geom: dict[str, float]) -> tuple[str, str]:
    """Return (rect_markup, text_markup) for a single room."""
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
    cy = y + h / 2 + 8  # +8: rough vertical centering for 24px text
    css_class = "room-label"
    if not bind_name.isdigit():
        css_class = "room-label small"
    text = (
        f'<text x="{round(cx, 2)}" y="{round(cy, 2)}" class="{css_class}">'
        f"{text_content}</text>"
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


def _render_non_room_children(root_g: ET.Element, rooms: set[int]) -> str:
    """Serialize all children of the root <g> except labeled rects.

    Also skips:
    - the unlabeled 820×900 white background rect (we paint our own
      bg-dots pattern),
    - vectorized glyph paths (room numbers drawn as text in Inkscape and
      converted to outlines) — we add fresh, Vue-controlled <text>
      labels instead.
    """
    out_parts = []
    for child in root_g:
        if id(child) in rooms:
            continue
        tag = _strip_ns(child.tag)
        if tag == "rect":
            w = child.attrib.get("width")
            h = child.attrib.get("height")
            if w == "820" and h == "900":
                continue
        if tag in ("namedview", "metadata", "defs"):
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
        width="820"
        height="900"
        viewBox="0 0 820 900"
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

        <rect width="820" height="900" fill="url(#bg-dots-{floor_number})"/>

        <!-- Стены, двери и прочая графика из исходного Inkscape-файла. -->
{walls}

        <!-- Кабинеты и именованные помещения. -->
{rooms}

        <!-- Подписи кабинетов (центрированы поверх прямоугольников). -->
{labels}
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

.room--type-auditorium {{ fill: #3b82f6; fill-opacity: 0.10; stroke: #2563eb; stroke-opacity: 0.5; stroke-width: 1.2; }}
.room--type-lab        {{ fill: #8b5cf6; fill-opacity: 0.12; stroke: #7c3aed; stroke-opacity: 0.55; stroke-width: 1.2; }}
.room--type-sport      {{ fill: #22c55e; fill-opacity: 0.12; stroke: #16a34a; stroke-opacity: 0.55; stroke-width: 1.2; }}
.room--type-hall       {{ fill: #f97316; fill-opacity: 0.12; stroke: #ea580c; stroke-opacity: 0.55; stroke-width: 1.2; }}
.room--type-admin      {{ fill: #f59e0b; fill-opacity: 0.14; stroke: #d97706; stroke-opacity: 0.6;  stroke-width: 1.2; }}
.room--type-wc         {{ fill: #64748b; fill-opacity: 0.10; stroke: #475569; stroke-opacity: 0.45; stroke-width: 1; }}
.room--type-stairs     {{ fill: #6366f1; fill-opacity: 0.12; stroke: #4f46e5; stroke-opacity: 0.5;  stroke-width: 1.2; stroke-dasharray: 6 4; }}
.room--type-other      {{ fill: #94a3b8; fill-opacity: 0.08; stroke: #64748b; stroke-opacity: 0.45; stroke-width: 1; }}

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


def generate_floor(floor_number: int) -> None:
    src = SVG_DIR / f"floor{floor_number}.svg"
    out = OUT_DIR / f"MapFloor{floor_number}.vue"
    tree = ET.parse(src)
    root = tree.getroot()

    # The SVG body lives inside a single root <g clip-path="url(#clip0_9_2)">.
    # We don't render the clipPath — strip it.
    root_g = None
    for child in root:
        if _strip_ns(child.tag) == "g":
            root_g = child
            break
    if root_g is None:
        raise RuntimeError(f"{src}: no top-level <g> found")

    rooms = _parse_room_rects(root)
    room_ids = {id(elem) for _, _, elem in rooms}

    room_blocks = []
    label_blocks = []
    for label, geom, _elem in rooms:
        rect_markup, text_markup = _render_room_block(label, geom)
        room_blocks.append(rect_markup)
        if text_markup:
            label_blocks.append(text_markup)

    walls_markup = _render_non_room_children(root_g, room_ids)

    content = VUE_TEMPLATE.format(
        floor_number=floor_number,
        floor_name=FLOOR_NAME[floor_number],
        walls=walls_markup,
        rooms="\n        ".join(room_blocks),
        labels="\n        ".join(label_blocks),
    )
    out.write_text(content, encoding="utf-8")
    print(f"Wrote {out} ({len(rooms)} rooms, {len(label_blocks)} labels)")


def main() -> None:
    for floor in (2, 3, 4):
        generate_floor(floor)


if __name__ == "__main__":
    main()

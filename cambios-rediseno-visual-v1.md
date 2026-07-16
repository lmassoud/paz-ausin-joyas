# Cambios — Rediseño visual v1 (tipografía · color · tarjetas · hero)

Solo tocar `index.html`. No modificar CONFIG, AVAILABLE ni SOLD (salvo lo indicado). Arquitectura de un archivo se mantiene.

## 1. Tipografía
- Reemplazar Cormorant Garamond por **Italiana** en todo uso display: `.serif`, h1, h2, h3, `.brand-mark`, `.card .name`, `.price`, `.fname`, ghost ✦. Italiana solo existe en peso 400: jerarquía por tamaño + tracking, nunca bold ni italic.
- Google Fonts: `family=Italiana&family=Jost:wght@400;500`. Eliminar Cormorant y Jost 300.
- Body base: Jost 400. Eliminar todo `font-weight:300`.
- Todo display en `text-transform:uppercase`:
  - h1 y h2 de sección: letter-spacing 0.08em
  - nombres de pieza, brand-mark, fname: 0.12em
- Párrafos largos (`.hero p`, `.about p`, `.desc`) quedan en caja normal, Jost 400.

## 2. Paleta (en `:root`)
- `--text: #F4EFE6` · `--text-soft: #C9C3B8` · `--text-dim: #948E83`
- Eliminar `--text-faint` y `--text-faintest`; todos sus usos pasan a `--text-dim`.
- Nuevo `--accent-bright: #D8BC7E` → aplicar en: `.eyebrow`, todos los ✦ (flourish, divider, about, sep), `.status`, `.hint`, `.nav a.wa`, contador de fotos, scroll cue.
- `--accent #C6A15B` queda solo para fondos de botón (`.btn-primary`, `.sheet-body .wa`) y bordes/glow hover.

## 3. Hero
- Fondo con foto: en `.hero`, `background: linear-gradient(180deg, rgba(11,10,9,.5) 0%, rgba(11,10,9,.72) 55%, #0B0A09 100%), url('fotos/hero.jpg') center bottom/cover no-repeat;` — **posición vertical `bottom`, no `center`**: `hero.jpg` ya viene compuesto con los anillos anclados en el tercio inferior de la imagen (fondo `#0B0A09` exacto arriba); con `center` se cortaría parte de la banda de anillos en pantallas anchas. Agregar `<link rel="preload" as="image" href="fotos/hero.jpg">` en head.
- `min-height:75vh; min-height:75svh;` con contenido centrado (flex column), reducir paddings actuales.
- h1: línea 1 `PAZ AUSIN` clamp(44px, 12vw, 92px); línea 2 `JOYAS` aparte, ~0.36em del tamaño de línea 1, letter-spacing 0.5em, color `--accent-bright`. Eliminar el span `.italic`.
- CTA pasa de `.btn-ghost` a `.btn-primary`.
- Scroll cue bajo el CTA: línea vertical 1px×44px, degradado dorado a transparente, animación loop suave de estiramiento (~2.2s). La media query `prefers-reduced-motion` existente ya la anula — no duplicar.
- `.how-to-buy`: compactar a `padding: 44px 22px 52px` para que "Disponible ahora" y el borde superior de la primera fila asomen bajo el fold en mobile (~844px alto).

## 4. Tarjetas de producto (disponibles y vendidas)
- Bajo la foto, dos líneas:
  1. Nombre: Italiana, uppercase, 16px (13.5px mobile), letter-spacing 0.12em, color `--text` (vendidas: `--text-soft`).
  2. Materiales: Jost 400, 10px, uppercase, letter-spacing 0.18em, color `--accent-bright`, una línea con `white-space:nowrap; overflow:hidden; text-overflow:ellipsis` (vendidas: color `--text-dim`).
- Contador de fotos: solo si la pieza tiene >1 foto, pill abajo-derecha del `.thumb`: `✦ N` (N = cantidad), Jost 10px, color `--accent-bright`, fondo `rgba(11,10,9,.65)`, padding 3px 8px, radius 999px. Implementar en `cardAvailable` y `cardSold` con `photosOf(item).length`. Badge "Vendido" sigue arriba-derecha, no chocan.
- Eliminar la estrella `.corner` (img favicon) de las tarjetas: el contador la reemplaza.
- Viñeta de integración (fundir el fondo gris de las fotos con la página): `.thumb::after` y en `.sheet-photo` un ::after equivalente, con `content:''; position:absolute; inset:0; box-shadow: inset 0 0 70px 18px rgba(11,10,9,.5); pointer-events:none;`.
- Hover desktop: `.card:hover .thumb img { transform: scale(1.05) }` (transition .5s ease, `overflow:hidden` ya existe), borde `rgba(216,188,126,.5)`, `box-shadow: 0 8px 30px rgba(198,161,91,.12)`. Eliminar el translateY actual.
- Hint de sección: texto `✦ Toca una pieza · fotos y precio`, color `--text-dim`.

## 5. Overlay de detalle
- h3: Italiana, uppercase, 26px, letter-spacing 0.1em.
- `.price`: Italiana, 26px, color `--accent-bright`.
- `.status`: color `--accent-bright` (variante `.is-sold` queda en `--text-dim`).

## 6. Verificación mínima
- Ningún resto de Cormorant ni de weight 300.
- En viewport 390×844: se ve hero completo + título "Disponible ahora" + borde superior de la grilla asomando.
- Sin `fotos/hero.jpg` presente, el hero se ve bien (solo degradado sobre fondo).

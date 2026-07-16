# Cambios v3 — Tipografía (case), contraste de color, portafolio

Solo tocar `index.html`. No modificar CONFIG ni AVAILABLE. No tocar nada relacionado a imagen de fondo del hero (ya descartado directamente con el usuario).

## 1. Mayúsculas solo en el título del hero
- Quitar `text-transform:uppercase` de TODO excepto el h1 del hero ("Paz Ausin Joyas"). El h1 del hero mantiene uppercase y su letter-spacing actual sin cambios.
- Afecta: `.brand-mark`, `.nav a`, `.eyebrow`, `.section-head h2`, `.portfolio-head h2`, `.card .name`, `.sold .name`, `.hint`, spans de `.how-to-buy`, `.sheet-body h3`, `.sheet-body .status`, `.footer .ftag`, `.badge`, línea de materiales (existente y nueva del punto 4).
- En esos mismos elementos, reducir `letter-spacing` al rango 0.02–0.05em (los valores actuales — 0.12–0.42em — fueron calibrados para mayúsculas y se ven excesivos en minúsculas). Textos muy pequeños (hint, status, badge, materiales) al extremo alto del rango (~0.04–0.05em); nombres y títulos de sección al extremo bajo (~0.02–0.03em).

## 2. Contraste de color — pasada global
En `:root`:
- `--text-soft: #E3DCCF` (antes #C9C3B8 — bastante más claro, pasa a ser el tono de trabajo para texto secundario legible).
- `--text-dim` sin cambio de valor, pero de aquí en adelante uso restringido SOLO a elementos decorativos (`.ghost`, `.sheet-photo .ghost`). No debe quedar en ningún texto que la gente tenga que leer.

Reasignar de `--text-dim` a `--text-soft`:
- `.nav a` (color base, no `.wa`)
- spans de `.how-to-buy`
- `.hint`
- `.footer .ftag` y `.footer-note`
- `.sheet-body .status.is-sold`
- `.badge` (texto)

## 3. Badge "Vendido" — legibilidad sobre fotos claras
- `.badge`: agregar `background: rgba(11,10,9,.75)`. Mantener el border actual.
- Color de texto: `--text-soft` (ya cubierto por el punto 2).

## 4. Materiales en piezas del portafolio (no talla)
- En `cardSold()`: agregar segunda línea bajo el nombre con `item.materials`, mismo tratamiento estructural que la línea de materiales de `cardAvailable()`, pero color `--text-soft` (no `--accent`) — así se mantiene la distinción visual disponible/vendido.
- Nunca renderizar `talla` en piezas del portafolio, aunque el objeto la tuviera cargada a futuro.
- En `openDetail()`: quitar `els.materials.hidden = true` para piezas vendidas — la línea de materiales debe mostrarse también en el overlay de detalle, usando `--text-soft` cuando `isSold` es true.

## 5. Verificación
- Confirmar que el único texto en mayúsculas de toda la página es el h1 del hero.
- Confirmar que las 11 piezas de `SOLD[]` muestran materiales en grid y en overlay, ninguna muestra talla.
- Confirmar el badge "Vendido" legible sobre al menos una foto clara (ej. Anillo Lady Di) y una oscura.
- Confirmar visualmente que nav, footer y hints ya no se ven apagados/de baja legibilidad.

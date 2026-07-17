# Cambios v3 — Tipografía, contraste, portafolio, burbuja de precio, precios reales

Solo tocar `index.html`. No modificar CONFIG. No tocar nada relacionado a imagen de fondo del hero (descartado). Aplicar los 6 bloques en orden.

---

## 1. Mayúsculas solo en el título del hero
- Quitar `text-transform:uppercase` de TODO excepto el h1 del hero ("Paz Ausin Joyas"), que mantiene uppercase y su letter-spacing actual sin cambios.
- Afecta (pasar a minúscula / case normal): `.brand-mark`, `.nav a`, `.eyebrow`, `.section-head h2`, `.portfolio-head h2`, `.card .name`, `.sold .name`, `.hint`, spans de `.how-to-buy`, `.sheet-body h3`, `.sheet-body .status`, `.footer .ftag`, `.badge`, y las líneas de materiales (existente + nuevas de los bloques 4 y 5).
- En esos mismos elementos, bajar `letter-spacing` al rango 0.02–0.05em (los valores actuales 0.12–0.42em fueron calibrados para mayúsculas y se ven excesivos en minúsculas). Textos chicos (hint, status, badge, materiales, pill de precio) ~0.04–0.05em; nombres y títulos de sección ~0.02–0.03em.
- Toda la tipografía display sigue siendo Italiana (ya aplicada). Las líneas de materiales también van en Italiana, no en Jost.

## 2. Contraste de color — pasada global
En `:root`:
- `--text-soft: #E3DCCF` (más claro; pasa a ser el tono de trabajo para texto secundario legible).
- `--text-dim`: mantiene su valor pero uso restringido SOLO a elementos decorativos (`.ghost`, `.sheet-photo .ghost`). No debe quedar en ningún texto legible.

Reasignar de `--text-dim` a `--text-soft`: `.nav a` (base, no `.wa`), spans de `.how-to-buy`, `.hint`, `.footer .ftag`, `.footer-note`, `.sheet-body .status.is-sold`, `.badge` (texto).

## 3. Badge "Vendido" — legibilidad sobre fotos claras
- `.badge`: agregar `background: rgba(11,10,9,.75)`. Mantener el border actual. Texto en `--text-soft` (ya cubierto en bloque 2).

## 4. Materiales en piezas del portafolio (nunca talla)
- En `cardSold()`: agregar segunda línea bajo el nombre con `item.materials`, mismo tratamiento estructural que la línea de materiales de `cardAvailable()`, color `--text-soft` (no dorado) para mantener la distinción disponible/vendido. Una línea con truncado por ellipsis igual que en disponibles.
- Nunca renderizar `talla` en portafolio.
- En `openDetail()`: quitar `els.materials.hidden = true` para piezas vendidas — mostrar materiales también en el overlay, en `--text-soft` cuando `isSold`.

## 5. Burbuja de precio en tarjetas disponibles
- Nueva pill en la esquina superior derecha de `.thumb` en `cardAvailable()`, misma familia visual que `.badge` de vendido (misma posición/esquina, pill redondeada, `background: rgba(11,10,9,.75)`, mismo estilo de border) pero:
  - Texto en dorado `--accent-bright` (#D8BC7E), no en `--text-soft`.
  - Un punto más grande que el badge de vendido (subir font-size y padding proporcionalmente) para que el precio sea legible, sin dominar la tarjeta. Debe verse elegante y discreto.
- Solo se muestra si la pieza tiene precio numérico real. Si `price` es el string `'Por confirmar'` (u otro no-numérico), NO renderizar la pill.
- Formato: separador de miles chileno con punto → `$115.000`. Implementar helper que reciba el número y devuelva el string formateado (ej. `formatCLP(115000) => '$115.000'`). Caso especial: la entrada "Anillo Cuarzo" muestra `$110.000 c/u` (agregar sufijo " c/u" solo a esa pieza — ver bloque 6).
- Convive con el contador de fotos (✦ N) que va en la esquina inferior derecha: esquinas opuestas, no chocan.

## 6. Carga de precios reales en AVAILABLE[]
Cambiar el campo `price` de cada pieza de string a número (el helper formatea la visualización). El precio grande del overlay (`.price` en `openDetail`) también usa el helper `formatCLP`.

| Pieza (name exacto) | price |
|---|---|
| Anillo Sello | 115000 |
| Anillo Micropavé | 240000 |
| Anillo Aguamarina | 900000 |
| Aros Zafiros Blancos | 45000 |
| Anillo Rubí | 150000 |
| Aros Zafiros y Diamantes | 1500000 |
| Anillo Plata | 120000 |
| Anillo Aguamarina Gota | 1500000 |

- **Anillo Cuarzo**: pieza que el usuario agregó localmente a `AVAILABLE[]` (puede no estar en versiones anteriores del archivo — usar la que exista en el index.html actual). Precio `110000`, y su pill + precio de overlay muestran el sufijo `c/u` → `$110.000 c/u`. Sugerencia de implementación: campo opcional `priceSuffix: 'c/u'` en el objeto, que el helper concatena si existe. No duplicar la entrada, dejarla como una sola.
- Todos estos precios son finales de venta (ya incluyen comisión). No aplicar ninguna división ni ajuste.
- La nota "Precio referencial · por confirmar" del overlay (`sheet-note`) ya no aplica a piezas con precio real: mostrarla solo si el precio no es numérico; ocultarla cuando hay precio cargado.

## 7. Verificación
- Único texto en mayúsculas de la página = h1 del hero.
- Las 8 (o 9 con Cuarzo) piezas disponibles con precio numérico muestran la burbuja dorada; ninguna muestra "Por confirmar" en burbuja.
- Anillo Cuarzo muestra `$110.000 c/u` en burbuja y overlay.
- Formato de miles correcto: `$1.500.000` con dos puntos, `$45.000` con uno.
- Las 11 piezas de SOLD muestran materiales en grid y overlay; ninguna muestra talla.
- Badge "Vendido" legible sobre foto clara (Anillo Lady Di) y oscura.
- Nav, footer y hints ya no se ven apagados.
- Burbuja de precio y contador de fotos no se superponen.

# Fase G — Catálogo real (reemplaza AVAILABLE[]/SOLD[] completos)

Reemplaza TODO el contenido actual de `AVAILABLE[]` y `SOLD[]` (son de ejemplo,
ninguna pieza real coincide) por lo siguiente. Faltan más piezas por venir —
esta tanda es parcial, dejar el código listo para agregar más del mismo modo.

## Campo nuevo: `talla`
- Opcional, solo en piezas de `AVAILABLE` que sean anillos.
- En `openDetail()`: si `item.talla` existe, mostrar "Talla {talla}" junto a
  materials. Si no existe (aros), no mostrar nada.
- Piezas en `SOLD` nunca muestran talla (ya no muestran materials tampoco,
  no tocar eso).

## Precio
- Todas las piezas de `AVAILABLE` en esta tanda: `price: 'Por confirmar'`
  (reemplaza los montos inventados anteriores).

## Fotos
- Fuente: `fotos-raw/pieza-01/` … `fotos-raw/pieza-14/` (el usuario las deja
  ahí, cada carpeta con todas las fotos de esa pieza, cualquier cantidad).
- Mover a `fotos/`, renombrar kebab-case según el `name` de cada pieza
  (convención ya documentada en CLAUDE.md: máx 1600px lado mayor, <400KB).
- `imgs: [...]` con todas las fotos de la carpeta, en orden alfabético.

## Datos — AVAILABLE

| # | name | materials | talla | slot |
|---|------|-----------|-------|------|
| 01 | Anillo Sello | Plata 950 · Diamante negro | 15 | anillo |
| 02 | Anillo Micropavé | Plata 950 · Espinelas negras · Baño rodio negro | 13 | anillo |
| 03 | Anillo Aguamarina | Oro 18K · Aguamarina | 13 | anillo |
| 05 | Aros Zafiros Blancos | Plata 950 · Zafiros blancos | — | aros |
| 07 | Anillo Rubí | Plata 950 · Rubí sintético | 11 | anillo |
| 14 | Aros Zafiros y Diamantes | Oro 18K · Zafiros · Diamantes | — | aros |

`desc`: dejar vacío/omitir por ahora (no inventar texto descriptivo).

## Datos — SOLD (portafolio, sin precio/materials/talla visibles — no tocar esa lógica)

| # | name | materials (guardar en el dato aunque no se muestre hoy) | slot |
|---|------|------|------|
| 04 | Anillo Esmeralda | Oro 18K · Plata 950 · Esmeralda · Espinelas negras | anillo |
| 06 | Anillo Mosca | Plata 950 · Baño Oro 18K | anillo |
| 08 | Anillo Medio Cintillo Fishtail | Plata 950 · Zafiros blancos | anillo |
| 09 | Anillo Raíz de Rubí | Plata 950 · Raíz de Rubí · Espinelas negras · Baño rodio negro | anillo |
| 10 | Anillo Lady Di | Oro 18K · Plata 950 · Topacio London Blue · Espinelas negras | anillo |
| 11 | Anillo Sinfín | Plata 950 · Espinelas negras | anillo |
| 12 | Anillo Compromiso Esmeralda | Oro 18K · Esmeralda Colombiana · Diamantes negros | anillo |
| 13 | Transformación Anillo Compromiso | Oro Blanco 18K · Diamantes y Moissanitas | anillo |

## Verificación
- Talla visible solo en anillos disponibles, ausente en aros y en portafolio.
- "Por confirmar" se ve bien en el espacio donde antes iba el precio.
- Swipe/galería funciona con las fotos reales (no solo las de prueba).
- Contador de favicon-corner (7→6 disponibles) no rompe nada.

## Prompt para Code
```
Lee cambios-v4-catalogo-real.md. Ejecuta todo. Prueba en navegador antes de
commit. No subas a GitHub todavía, avísame cuando esté listo para revisar.
```

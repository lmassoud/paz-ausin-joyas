# Fase H — Agregar 5 piezas nuevas (15-19)

Añadir a `AVAILABLE[]`/`SOLD[]` existentes — NO reemplazar ni tocar las 14
piezas ya cargadas.

## Paso 1 — Ordenar fotos
Fotos en `fotos-raw/` (nueva tanda, dispersas). Para cada foto: comparar con
tabla de abajo, proponer agrupamiento `pieza-15` … `pieza-19`. Mostrar
propuesta antes de mover nada. Fotos que no calcen: lista aparte.

| # | Pieza | Cómo se ve |
|---|-------|------------|
| 15 | Anillo Plata | Plata clara, textura rústica facetada tipo roca tallada, banda ancha octagonal irregular. |
| 16 | Anillo 3 Turmalinas (Portafolio) | Plata clara lisa, banda delgada, 3 piedras verdes rectangulares en fila al frente. |
| 17 | Anillo Solitario en Bruto (Portafolio) | Plata clara delgada, una piedra rosada/roja chica sin tallar, engarce de garras simple tipo solitario. |
| 18 | Anillo Aguamarina Gota | Oro amarillo, piedra en forma de gota/lágrima verde-agua transparente, dos piedritas blancas chicas a los costados. |
| 19 | Anillo Turmalina Guinda (Portafolio) | Plata oscura (rodio negro), forma circular tipo botón, piedra roja/guinda redonda al centro, doble halo de piedras rosa/champagne. |

## Paso 2 — Agregar al catálogo
Mover fotos confirmadas a `fotos/` (convención ya conocida: kebab-case,
máx 1600px, <400KB). Generar `imgs[]`. Agregar entradas:

**AVAILABLE** (`price: 'Por confirmar'`, `desc` vacío):

| name | materials | talla | slot |
|------|-----------|-------|------|
| Anillo Plata | Plata 950 | 15 | anillo |
| Anillo Aguamarina Gota | Oro 18K · Aguamarina · Topacios blancos | 16 | anillo |

**SOLD** (sin precio/materials/talla visibles, igual que las demás):

| name | materials (guardar aunque no se muestre) | slot |
|------|------|------|
| Anillo 3 Turmalinas | Plata 950 · Turmalinas verdes | anillo |
| Anillo Solitario en Bruto | Plata 950 · Rubí en bruto | anillo |
| Anillo Turmalina Guinda | Plata 950 · Turmalina · Zafiros champagne | anillo |

## Verificación
- Las 14 piezas anteriores siguen intactas (fotos, talla, precio).
- Las 2 nuevas disponibles muestran talla correcta, sin romper swipe/galería.
- Favicon-corner y conteos se actualizan solos (ahora 8 disponibles).

## Prompt para Code
```
Lee cambios-v5-mas-piezas.md. Paso 1 primero, propón agrupamiento antes de
mover nada. Confirmo, luego sigues con el Paso 2. No subas a GitHub todavía.
```

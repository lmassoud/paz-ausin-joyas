# Cambios v6 — Agregar 13 piezas (20–32)

Añadir a `AVAILABLE[]`/`SOLD[]` existentes — NO reemplazar ni tocar las 19
piezas ya cargadas (8 en `AVAILABLE`, 11 en `SOLD`). Piezas 20–31 van a
`SOLD[]` (Portafolio); pieza 32 va a `AVAILABLE[]`.

## Paso 1 — Ordenar fotos
Fotos en `fotos-raw/` (nueva tanda, dispersas). Para cada foto: comparar con
tabla de abajo, proponer agrupamiento `pieza-20` … `pieza-32`. Mostrar
propuesta antes de mover nada. Fotos que no calcen: lista aparte.

| # | Pieza | Cómo se ve |
|---|-------|------------|
| 20 | Colgante Estrella | Disco liso en plata pulida, estrella chica de 4 puntas con zafiro blanco al centro, cadena fina de bolitas. Reverso puede venir grabado (ej. nombre) en piezas personalizadas. |
| 21 | Esclava Estrellas | Esclava rígida de plata oxidada, banda angosta con 5 estrellas de distinto tamaño incrustadas a lo largo, cierre de gancho lateral. |
| 22 | Colgante Estrella Rayos | Medallón redondo en plata con borde de rayos grabados tipo sol, estrella chica con zafiro al centro, cadena tipo espuma/cordón grueso. |
| 23 | Colgante Pirámide Ónix | Colgante geométrico en pirámide, ónix negro triangular facetado, halo de espinelas negras chicas, cadena fina. |
| 24 | Anillo Art Deco | Anillo ovalado alargado estilo art decó, filigrana geométrica, diamante de laboratorio chico al centro con halo de zafiros blancos en pavé. |
| 25 | Anillo Turmalinas | 3 turmalinas verdes rectangulares en fila, grifas de oro 18K, banda de plata delgada lisa. |
| 26 | Anillo Medio Cintillo Moissanitas | Banda delgada plata con baño rodio negro, medio cintillo de moissanitas negras. |
| 27 | Anillo Turmalina Negra | Turmalina negra rectangular (emerald-cut) al centro, halo de topacios blancos pavé, banda plateada delgada. |
| 28 | Anillo Medio Cintillo Espinelas | Banda delgada plata con baño rodio negro, medio cintillo de espinelas negras (similar a la 26 pero con espinelas, no moissanitas). |
| 29 | Colgante Esmeralda | Rectangular, esmeralda emerald-cut al centro, halo espinelas negras + acentos oro 18K, baño rodio negro, cadena espuma. |
| 30 | Pulsera Grumet | Cadena gruesa tipo grumet/cubana en plata oxidada, cierre de caja. |
| 31 | Anillo Bombé | Banda ancha y abombada en plata lisa, sin piedras. |
| 32 | Anillos Cuarzos | Tres anillos de cabujón redondo grande (piedra grande y lisa): uno cuarzo dorado/champagne en banda con baño de oro, uno cuarzo gris tipo turmalinado en banda oscura, uno cuarzo rosa en banda oscura. Aparecen fotografiados juntos y por separado. |

## Paso 2 — Agregar al catálogo

Mover fotos confirmadas a `fotos/` (kebab-case, máx 1600px, <400KB).
Generar `imgs[]`.

### → `SOLD[]` (Portafolio — sin precio/talla, pero guardar `materials`)

| name | materials | slot |
|------|-----------|------|
| Colgante Estrella | Plata 950 · Zafiro blanco | colgante |
| Esclava Estrellas | Plata 950 | pulsera |
| Colgante Estrella Rayos | Plata 950 · Zafiro blanco · Cadena espuma | colgante |
| Colgante Pirámide Ónix | Plata 950 · Ónix · Espinelas negras | colgante |
| Anillo Art Deco | Plata 950 · Diamante de laboratorio · Zafiros blancos | anillo |
| Anillo Turmalinas | Plata 950 · Grifas oro 18K · Turmalinas verdes | anillo |
| Anillo Medio Cintillo Moissanitas | Plata 950 · Moissanitas negras · Baño de rodio negro | anillo |
| Anillo Turmalina Negra | Plata 950 · Turmalina negra · Topacios blancos | anillo |
| Anillo Medio Cintillo Espinelas | Plata 950 · Espinelas negras · Baño de rodio negro | anillo |
| Colgante Esmeralda | Plata 950 · Grifas oro 18K · Esmeraldas · Baño de rodio negro · Cadena espuma | colgante |
| Pulsera Grumet | Plata 950 | pulsera |
| Anillo Bombé | Plata 950 | anillo |

### → `AVAILABLE[]` (Disponibles)

| name | materials | slot | talla | price | desc |
|------|-----------|------|-------|-------|------|
| Anillos Cuarzos | Plata 950 · Cuarzo turmalinado · Cuarzo rosa · Baño de oro | anillo | *(omitir el campo — no debe aparecer talla)* | Por confirmar | "Tres anillos con distinto cuarzo — turmalinado con baño de oro, turmalinado en plata y rosa. Se venden por separado, mismo precio c/u. Escríbeme cuál te gusta." |

Nota para Code: a diferencia de las demás piezas nuevas, esta SÍ lleva `desc`
(no vacío) porque un solo card representa 3 piezas físicas distintas que se
compran por separado — el mensaje de WhatsApp genérico no alcanza a
distinguir cuál quiere el comprador sin ese texto. `imgs[]` debe incluir
fotos de los 3 anillos (juntos y/o por separado).

## Verificación
- Las 19 piezas anteriores siguen intactas (8 disponibles + 11 portafolio).
- Las 12 piezas 20–31 aparecen en Portafolio con badge "Vendido", sin precio ni botón de compra.
- La pieza 32 (Anillos Cuarzos) aparece en Disponibles SIN talla visible (verificar que no salga "· Talla undefined" ni similar).
- Slots nuevos (`colgante`, `pulsera`) no rompen el placeholder ghost si falta alguna foto.
- Ahora quedan 9 piezas en Disponibles y 23 en Portafolio (32 en total).

## Prompt para Code
```
Lee cambios-v6-mas-piezas.md. Paso 1 primero, propón agrupamiento antes de
mover nada. Confirmo, luego sigues con el Paso 2. No subas a GitHub todavía.
```

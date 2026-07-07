# Cambios v2 — Paz Ausin Joyas (para ejecutar con Claude Code)

## Estado del proceso (verificado)
- [x] Carpeta del proyecto con index.html, CLAUDE.md y plan-paz-ausin-joyas.md
- [x] Claude Code instalado y leyendo CLAUDE.md correctamente
- [ ] GitHub: crear cuenta, repositorio, conectar carpeta y activar Pages (Pasos 5–8, retomar después de estos cambios)

## Instrucciones generales para Claude Code
- Todos los cambios se hacen en `index.html` salvo que se indique otro archivo.
- Si la carpeta aún no es un repositorio git: ejecuta `git init` antes de empezar.
- Un commit por fase, con mensaje en español (ej: "Fase A: corrección de datos placeholder").
- Al terminar cada fase: muestra un resumen de lo cambiado y DETENTE a esperar confirmación del usuario antes de seguir con la siguiente.
- El usuario está aprendiendo: explica cada cambio en 1-2 líneas simples al hacerlo.

---

## FASE A — Corrección de datos (errores actuales)

**A1.** El arreglo `SOLD[]` repite piezas que están en `AVAILABLE[]` (Argolla Ónix Negro, Aros Estrella, Anillo Sello Plata, Brazalete Estrellas). Siendo piezas únicas, no pueden estar disponibles y vendidas a la vez. Reemplazar `SOLD[]` por estas piezas (reales, del Instagram, hoy no disponibles):
```
{ name: 'Colgante Medalla Estrella', slot: 'colgante' },
{ name: 'Anillo Rubí Halo Negro',    slot: 'anillo' },
{ name: 'Aros Abanico Oro',          slot: 'aros' },
{ name: 'Colgante Esmeralda',        slot: 'colgante' },
```

**A2.** Reemplazar los precios de `AVAILABLE[]` por placeholders dentro del rango real (piezas únicas $200.000–$500.000 CLP, esclava ~$60.000):
- Anillo Sello Plata → `$240.000`
- Aros Estrella → `$210.000`
- Argolla Ónix Negro → `$230.000`
- Anillo Esmeralda → `$480.000`
- Brazalete Estrellas → `$320.000`
- Anillo Luna → `$390.000`
- Esclava de Plata → `$60.000`

**A3.** Mantener la nota "Precio referencial · por confirmar" del overlay tal como está.

---

## FASE B — Móvil y navegación

**B1.** Grilla a 2 columnas en móvil: agregar `@media (max-width: 640px) { .grid { grid-template-columns: repeat(2, 1fr); gap: 10px; } .card .name { font-size: 16px; } .sold .name { font-size: 15px; } }`

**B2.** Hacer la barra superior sticky: `.topbar { position: sticky; top: 0; z-index: 40; background: rgba(11,10,9,0.85); backdrop-filter: blur(10px); border-bottom: 1px solid var(--line-soft); }` (mantener max-width interior con un wrapper si es necesario para que el fondo ocupe todo el ancho).

**B3.** Navegación interna: agregar `id="disponible"` a la sección "Disponible ahora" e `id="portafolio"` a la sección Portafolio. En el nav de la topbar, agregar links "Piezas" (→ `#disponible`) y "Portafolio" (→ `#portafolio`) antes de Instagram.

**B4.** CTA en el hero: debajo del párrafo, botón "Ver piezas disponibles" (clase `btn btn-ghost`, margen superior 34px) que lleva a `#disponible`.

**B5.** Scroll suave: `html { scroll-behavior: smooth; }` y dentro del bloque `prefers-reduced-motion` agregar `html { scroll-behavior: auto; }`.

**B6.** En las plantillas de tarjeta (funciones `cardAvailable` y `cardSold`): renderizar el `<span class="slot">` SOLO cuando la pieza no tiene foto (`!item.img`).

**B7.** Estado vacío: si `AVAILABLE.length === 0`, en vez de la grilla mostrar un bloque centrado con el texto "Las piezas disponibles vuelan ✦ Hay nuevas en camino." y un botón WhatsApp "Avísame cuando haya piezas nuevas" (mensaje pre-escrito: "Hola! Quiero que me avises cuando haya piezas nuevas disponibles").

---

## FASE C — Conversión y confianza

**C1.** Franja "Cómo comprar" entre el hero y "Disponible ahora": tres pasos en una línea (apilados en móvil), estilo tipo eyebrow (mayúsculas pequeñas, letter-spacing amplio, color `--text-dim`), separados por ✦ en color acento:
`Elige tu pieza ✦ Escríbeme por WhatsApp ✦ Coordinamos pago y entrega`

**C2.** En el encabezado del Portafolio, convertir "Escríbeme." en un link de WhatsApp (color acento, subrayado sutil) con mensaje pre-escrito: "Hola! Vi el portafolio y me gustaría encargar una pieza personalizada".

**C3.** Hacer clicables las piezas vendidas: al tocar una, abrir el mismo overlay pero en modo vendido — status "Vendido" en color `--text-dim` (no dorado), sin precio, y botón "Encargar una pieza similar" con mensaje: "Hola! Me gustó el/la [nombre de la pieza] del portafolio. ¿Podrías hacer algo parecido?". Bajo el botón, nota: "Cada pieza es única — se puede crear una versión nueva inspirada en esta."

**C4.** En el footer, sobre los botones, agregar línea pequeña (12px, `--text-faint`): "Entrega y pago se coordinan directo por WhatsApp".

---

## FASE D — Técnica y SEO

**D1.** Meta tags para compartir (crítico: los links se compartirán por WhatsApp e Instagram):
```html
<meta property="og:title" content="Paz Ausin Joyas · Orfebrería hecha a mano">
<meta property="og:description" content="Piezas únicas en Plata 950, Oro 18K y piedras naturales. Hecho a mano en Chile.">
<meta property="og:type" content="website">
<meta property="og:image" content="fotos/og.jpg"> <!-- TODO: crear con foto real -->
<meta name="twitter:card" content="summary_large_image">
```

**D2.** Favicon: estrella ✦ dorada sobre fondo #0B0A09 como SVG inline en data URI.

**D3.** `<meta name="theme-color" content="#0B0A09">`

**D4.** Soporte para varias fotos por pieza: aceptar `imgs: ['a.jpg','b.jpg']` en cada pieza (retrocompatible con `img` single). Si hay más de una, el overlay muestra flechas ‹ › y contador "1 / 3" sobre la foto. Todas las `<img>` con `loading="lazy"` y `decoding="async"`.

**D5.** Crear carpeta `fotos/` con archivo `.gitkeep`. Documentar en comentario del CONFIG la convención: nombres kebab-case (`anillo-sello-plata-01.jpg`), lado mayor máx 1600px, peso ideal <400 KB.

**D6.** JSON-LD básico en el `<head>`: tipo `Organization`, nombre "Paz Ausin Joyas", `sameAs` con el Instagram.

**D7.** Crear `404.html` mínimo con el mismo fondo/tipografía y un link "Volver al catálogo" → `index.html`.

---

## FASE E — Orden del repo

**E1.** Actualizar `CLAUDE.md`: esquema nuevo de datos (`imgs[]`), secciones nuevas (Cómo comprar, overlay de vendidos, estado vacío), y marcar avances en el roadmap.

**E2.** Crear `README.md` breve: qué es el proyecto, cómo editar piezas (CONFIG/AVAILABLE/SOLD), cómo se publica.

**E3.** Commit final de la fase.

---

## NO tocar
- La lógica de precio oculto en la grilla / visible solo en el detalle.
- Paleta de colores y tipografías actuales (Cormorant Garamond + Jost, dorado #C6A15B).
- Arquitectura de un solo archivo `index.html` sin frameworks ni build step.

## Bloqueado hasta tener datos reales (NO ejecutar todavía)
- Precios definitivos por pieza (confirmar con la mamá).
- Fotos reales (reemplazar placeholders) y foto para `og.jpg`.
- Número de WhatsApp real en `CONFIG.whatsapp`.
- Ciudad / cobertura de entrega (posible línea en footer cuando se confirme).

---

## Prompt para pegar en Claude Code
```
Lee CLAUDE.md y cambios-v2.md. Ejecuta la FASE A completa tal como está
especificada. Al terminar: muéstrame qué cambió, haz el commit, y detente
para que yo confirme antes de seguir con la Fase B.
```

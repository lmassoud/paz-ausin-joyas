# Paz Ausin Joyas — Contexto del proyecto

## Qué es esto
Catálogo web (sin pagos ni carrito) para las joyas hechas a mano por Maria Paz Ausin.
Dirige a los visitantes a WhatsApp para cerrar la venta. Sitio estático de un solo
archivo: `index.html` (HTML + CSS + JS, sin frameworks, sin build step).

## Modelo de negocio
- Maria Paz Ausin (mamá) fabrica las joyas; el usuario vende y administra, recibe 20% por venta.
- Todo comprador contacta al usuario por WhatsApp — no a la mamá.
- Venta local en Chile por ahora; abierto a expandir a otras ciudades si es necesario.
- Es un proyecto de aprendizaje: el usuario está aprendiendo a construir con IA mientras
  se hace esto. Explica los cambios de forma clara, no como caja negra.

## Marca y estilo (ya definidos — no cambiar sin que el usuario lo pida explícitamente)
- Nombre: **Paz Ausin Joyas**
- Estética: lujosa, limpia, minimalista. Fondo oscuro (~#0B0A09), acento dorado (#C6A15B)
  o plata (#C8CCD2) como alternativa.
- Tipografías: Cormorant Garamond (serif, títulos) + Jost (sans, texto de cuerpo).
- Motivo recurrente: estrella (✦), usado con sutileza en separadores y detalles.
- Inspirado en el Instagram actual @pazausin (cuenta privada): fondos oscuros, foco
  total en la pieza, sin distracciones.
- Mobile-first: la mayoría del tráfico viene de Instagram desde el celular.

## Estructura de la página (index.html)
1. Barra superior (sticky): marca + links internos "Piezas"/"Portafolio" + link a
   Instagram + link a WhatsApp
2. Hero: nombre + tagline + materiales (Plata 950 · Oro 18K · Piedras naturales) +
   botón "Ver piezas disponibles"
3. Franja "Cómo comprar": 3 pasos (Elige tu pieza ✦ Escríbeme por WhatsApp ✦
   Coordinamos pago y entrega)
4. "Disponible ahora" (`#disponible`): grilla de piezas — SIN precio visible en la
   grilla (a propósito). En mobile, 2 columnas. Si `AVAILABLE` queda vacío, se
   muestra un estado vacío con mensaje y botón de WhatsApp en vez de la grilla.
5. Al tocar una pieza disponible: overlay con precio, descripción, materiales y
   botón de WhatsApp con mensaje pre-escrito. Si la pieza tiene más de una foto
   (`imgs[]`), el overlay muestra flechas ‹ › y contador ("1 / 3").
6. "Portafolio" (`#portafolio`): piezas ya vendidas, marcadas "Vendido", sin precio
   ni botón de compra (da credibilidad y abre la puerta a pedidos personalizados).
   También son clicables: abren el mismo overlay pero en modo "Vendido" (sin
   precio, botón "Encargar una pieza similar"). El texto "Escríbeme." del
   encabezado es un link directo de WhatsApp.
7. "Sobre la orfebre": 2-3 líneas sobre Maria Paz Ausin
8. Footer: nombre, nota "Entrega y pago se coordinan directo por WhatsApp", botón
   de WhatsApp, link a Instagram
9. `404.html`: página de error mínima, misma estética, con link de vuelta al catálogo.

## Dónde están los datos editables (dentro de index.html, sección CONFIG)
- `CONFIG.whatsapp`: número real del negocio (56998179246).
- `AVAILABLE[]`: piezas disponibles (nombre, slot, precio, materiales, descripción,
  fotos). Agregar una pieza = copiar un bloque y editarlo.
- `SOLD[]`: piezas vendidas para el Portafolio (nombre, slot, fotos).
- Fotos por pieza: `img: 'fotos/nombre.jpg'` para una sola foto, o
  `imgs: ['fotos/nombre-01.jpg', 'fotos/nombre-02.jpg']` para varias (el overlay
  agrega flechas y contador automáticamente cuando hay más de una). Archivos en
  `fotos/`, nombre en kebab-case, lado mayor máx. 1600px, peso ideal <400 KB.

## Pendiente / por confirmar con la mamá (no inventar estos datos)
- Precios exactos por pieza — los actuales ya están dentro del rango real estimado
  (piezas únicas ~$200.000–$500.000 CLP, esclava de plata ~$60.000 CLP) pero siguen
  siendo placeholders, no el precio final confirmado por la mamá.
- Fotos definitivas de cada pieza (ya existen en Instagram: varios ángulos + puestas
  en mano/oreja).
- Qué piezas antiguas (ya vendidas) van en la sección "Portafolio".

## Roadmap
- [x] Primer boceto visual (hecho en Claude Design)
- [x] Reconstrucción como HTML/CSS/JS estándar y editable
- [x] Fase A — corrección de datos placeholder (SOLD sin duplicados, precios dentro
      del rango real)
- [x] Fase B — mobile y navegación (grilla 2 columnas, topbar sticky, links internos,
      scroll suave, estado vacío)
- [x] Fase C — conversión y confianza (franja "Cómo comprar", overlay de vendidos,
      link de WhatsApp en Portafolio, nota de footer)
- [x] Fase D — técnica y SEO (meta tags para compartir, favicon, JSON-LD, soporte
      multi-foto, carpeta `fotos/`, `404.html`)
- [ ] Reemplazar precios placeholder por precios exactos confirmados
- [ ] Agregar fotos reales (reemplazar placeholders) en `fotos/`
- [ ] Publicar en GitHub Pages
- [ ] (Fase 2) Selección múltiple de piezas → un solo mensaje de WhatsApp
- [ ] (Fase 2) Dominio propio
- [ ] (Fase 2) Número de WhatsApp Business separado
- [ ] (Fase 2) Automatizar actualizaciones del catálogo (Claude Code / Cowork)
- [ ] (Fase 2) Skill personalizada para sugerencia de precios

## Documentos de referencia
- `plan-paz-ausin-joyas.md`: planificación original completa — público objetivo,
  lógica de precios, flujo de WhatsApp, hosting, etc.
- `cambios-v2.md`: especificación fase por fase (A–E) de la reconstrucción actual
  de `index.html`, ya ejecutada.

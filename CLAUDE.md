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
1. Barra superior: marca + link a Instagram + link a WhatsApp
2. Hero: nombre + tagline + materiales (Plata 950 · Oro 18K · Piedras naturales)
3. "Disponible ahora": grilla de piezas — SIN precio visible en la grilla (a propósito)
4. Al tocar una pieza: overlay con precio, descripción, materiales y botón de WhatsApp
   con mensaje pre-escrito
5. "Portafolio": piezas ya vendidas, marcadas "Vendido", sin precio ni botón de compra
   (da credibilidad y abre la puerta a pedidos personalizados)
6. "Sobre la orfebre": 2-3 líneas sobre Maria Paz Ausin
7. Footer: nombre, botón de WhatsApp, link a Instagram

## Dónde están los datos editables (dentro de index.html, sección CONFIG)
- `CONFIG.whatsapp`: número placeholder (56900000000) — reemplazar por el número de
  negocio real cuando se consiga.
- `AVAILABLE[]`: piezas disponibles (nombre, slot, precio, materiales, descripción,
  imagen opcional). Agregar una pieza = copiar un bloque y editarlo.
- `SOLD[]`: piezas vendidas para el Portafolio.

## Pendiente / por confirmar con la mamá (no inventar estos datos)
- Precios reales — los actuales en el código son de EJEMPLO y no calzan con el rango
  real estimado: piezas únicas ~$200.000–$500.000 CLP, esclavas de plata ~$60.000 CLP.
- Fotos definitivas de cada pieza (ya existen en Instagram: varios ángulos + puestas
  en mano/oreja).
- Qué piezas antiguas (ya vendidas) van en la sección "Portafolio".

## Roadmap
- [x] Primer boceto visual (hecho en Claude Design)
- [x] Reconstrucción como HTML/CSS/JS estándar y editable
- [ ] Reemplazar precios de ejemplo por precios reales
- [ ] Agregar fotos reales (reemplazar placeholders)
- [ ] Publicar en GitHub Pages
- [ ] (Fase 2) Selección múltiple de piezas → un solo mensaje de WhatsApp
- [ ] (Fase 2) Dominio propio
- [ ] (Fase 2) Número de WhatsApp Business separado
- [ ] (Fase 2) Automatizar actualizaciones del catálogo (Claude Code / Cowork)
- [ ] (Fase 2) Skill personalizada para sugerencia de precios

## Documento completo
Ver `plan-paz-ausin-joyas.md` en esta misma carpeta para el detalle completo de la
planificación original: público objetivo, lógica de precios, flujo de WhatsApp,
hosting, etc.

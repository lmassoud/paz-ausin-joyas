# Paz Ausin Joyas

Catálogo web (sin pagos ni carrito) para las joyas hechas a mano por Maria Paz Ausin.
Cada pieza dirige a WhatsApp para cerrar la venta. Sitio estático de un solo archivo,
sin frameworks ni build step: se edita y se publica directo.

## Archivos

- `index.html` — el sitio completo (HTML + CSS + JS).
- `404.html` — página de error, con link de vuelta al catálogo.
- `fotos/` — fotos de las piezas (`.jpg`, kebab-case, máx. 1600px de lado mayor, <400 KB).
- `CLAUDE.md` — contexto del proyecto para trabajar con Claude Code.
- `plan-paz-ausin-joyas.md` / `cambios-v2.md` — documentos de planificación.

## Cómo editar piezas

Todo lo editable está dentro de `index.html`, en la sección `CONFIG` del `<script>` final.

- **`CONFIG.whatsapp`**: número de WhatsApp del negocio (formato internacional, sin `+`
  ni espacios).
- **`AVAILABLE[]`**: piezas a la venta. Para agregar una, copia un bloque `{ ... }` y
  edítalo (nombre, materiales, precio, descripción, foto).
- **`SOLD[]`**: piezas ya vendidas, para la sección "Portafolio". Para marcar una pieza
  como vendida, muévela de `AVAILABLE` a `SOLD`.
- **Fotos**: agrega `img: 'fotos/nombre.jpg'` para una sola foto, o
  `imgs: ['fotos/nombre-01.jpg', 'fotos/nombre-02.jpg']` para varias — el overlay
  agrega flechas y contador automáticamente cuando hay más de una.

## Cómo se publica

El plan es publicar en GitHub Pages (pendiente en el roadmap): al activar Pages sobre
la rama principal, la página queda disponible en el link público del repositorio, sin
build ni deploy manual — es HTML plano.

# Fase F — Galería con deslizamiento estilo Instagram (adición a cambios-v2.md)

## Contexto
La Fase D (ya implementada) agregó soporte multi-foto (`imgs[]`) con flechas de
clic y contador "1 / N". Esta fase reemplaza esa interacción por deslizamiento
táctil real, tipo Instagram — la foto se mueve siguiendo el dedo y encaja en
la siguiente/anterior al soltar.

## F1 — Deslizamiento con seguimiento en tiempo real

Implementar con **Pointer Events** (`pointerdown`, `pointermove`, `pointerup`,
`pointercancel`) — no Touch Events por separado — para que funcione igual con
dedo (mobile) y con clic-arrastrar mouse (desktop), en un solo código.

Comportamiento:
- Al presionar y arrastrar horizontalmente sobre la foto del overlay, la imagen
  se mueve (`transform: translateX()`) siguiendo el dedo/cursor en tiempo real,
  1:1 con el movimiento.
- Al soltar:
  - Si el arrastre superó ~20% del ancho de la foto (o velocidad alta aunque
    el recorrido sea corto), anima hacia la siguiente/anterior foto y la deja
    encajada.
  - Si no superó el umbral, la foto "rebota" de vuelta a su posición original
    con una transición suave (~200ms, ease-out).
- En el primer extremo (foto 1) no dejar arrastrar hacia la derecha más allá
  del límite; mismo criterio en la última foto hacia la izquierda — sin
  wraparound acá (a diferencia de las flechas actuales, que si dan la vuelta).
  Dar una resistencia visual leve (rubber-band) en vez de un tope seco.
- Mientras se arrastra, `preventDefault` solo en el eje horizontal para no
  interferir con el scroll vertical de la página si el gesto es mayormente
  vertical (debe poder distinguir "quiere deslizar la foto" de "quiere hacer
  scroll de la página").

## F2 — Indicador de puntos (reemplaza el contador "1 / N")

- Quitar el texto "1 / 3".
- Agregar una fila de puntos pequeños centrados debajo de la foto (dentro del
  `.sheet-photo` o justo debajo), uno por foto. El punto de la foto activa se
  ve lleno/sólido en el color de acento; los demás, un contorno tenue.
- Los puntos se actualizan en tiempo real mientras se arrastra (transición
  suave entre estados), no solo al soltar.
- Si la pieza tiene 1 sola foto o ninguna, no se muestran los puntos (igual
  que las flechas actuales, que ya son condicionales).

## F3 — Mantener accesibilidad de escritorio

- Conservar las flechas ‹ › actuales (o rediseñarlas más sutiles, tipo
  overlay semi-transparente en los bordes) para quien usa mouse sin querer
  arrastrar — son un complemento al swipe, no una alternativa a eliminar.
- Agregar soporte de teclado: con el overlay abierto, flecha izquierda/derecha
  del teclado navega entre fotos.

## F4 — Rendimiento

- Precargar (`<link rel="preload">` o simplemente crear el `Image()` en JS)
  la foto siguiente y anterior a la actual, para que el deslizamiento no
  muestre un salto en blanco mientras carga.

## No tocar
- La lógica de `imgs[]` / retrocompatibilidad con `img` de una sola foto — ya
  funciona, solo cambia la interacción de navegación.
- El resto del overlay (precio, descripción, botón WhatsApp, modo "vendido").

## Verificación esperada antes del commit
- Probar en viewport mobile (375px) con el emulador de touch del navegador:
  arrastrar sigue al dedo, suelta y encaja, rebota si el arrastre es corto.
- Probar en desktop con mouse: clic y arrastrar funciona igual.
- Probar flechas de teclado.
- Probar una pieza con 1 sola foto: no debe mostrar puntos ni permitir
  arrastre lateral.
- Probar la primera y última foto: resistencia (rubber-band), sin wraparound
  ni error de JS al intentar pasar el límite.

## Prompt para pegar en Claude Code
```
Lee cambios-v3-galeria-swipe.md (Fase F). Está en la misma carpeta que
cambios-v2.md, es una adición a ese documento. Ejecútala completa (F1-F4).

Prueba todo según la sección de verificación antes de hacer el commit, y
muéstrame el resumen igual que en las fases anteriores.
```

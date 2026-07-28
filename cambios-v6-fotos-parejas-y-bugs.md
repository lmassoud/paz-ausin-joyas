# Cambios v6 — Fotos del mismo porte + barrido de bugs

Dos trabajos en uno: dejar todas las piezas del mismo tamaño y centradas en la
grilla, y arreglar los errores que quedaban en `index.html` / `404.html`.

## Parte 1 — Fotos parejas

### El problema de fondo (por qué las v4 y v5 no lo lograron)
El detector de joya de las versiones anteriores buscaba la pieza por **energía de
bordes** (gradiente). El fondo de estas fotos tiene bandas de tono y una franja
de mesa que queda enfocada y **sí tiene textura real**, así que el detector la
contaba como parte de la joya. Los scripts v4 y v5 "verificaban" su resultado con
ese mismo detector, así que se daban por buenos solos: el informe decía 70% / 78%
de ocupación, pero medido a ojo las piezas iban del 28% al 98% del cuadro.

### Lo que se cambió
- **`scripts/detector_joya.py` (nuevo).** Detecta la joya por **rango dinámico
  local** (máximo menos mínimo en una ventana chica). Medido sobre estas fotos: el
  mantel queda en 5–15 (de 255) y la joya llega a 130–220 — una separación de 10 a
  20 veces. Las bandas y degradados del fondo son variaciones lentas y en una
  ventana chica casi no cambian, así que desaparecen solas.
- **La caja se saca de la distribución de energía**, no del contorno binario. La
  máscara siempre arrastra algo pegado a la pieza (la franja enfocada del mantel,
  o la cadena de un colgante) y eso disparaba el ancho al cuadro completo. Esas
  colas aportan poquísima energía comparadas con el metal, así que recortar por
  percentil las deja fuera sin un umbral que calibrar foto por foto.
- **Lazo de realimentación en el encuadre.** El detector no da la misma caja antes
  y después de recortar. Ahora se renderiza, se vuelve a medir sobre lo renderizado
  y se corrige el zoom hasta que la pieza mide el objetivo **en la foto final**.
- **Extensión de fondo armónica.** Cuando para alejarse hay que salir de la foto,
  el fondo se continúa difundiendo el fondo real hacia afuera. Empalma exacto con
  el borde (no queda marcado el rectángulo de la foto original) y ningún color
  nuevo puede aparecer. Se le devuelve el grano para que no quede plástico. En las
  fotos puestas (anillo en el dedo) la piel se excluye del modelo, si no el fondo
  inventado salía rosado.
- **Reescalado controlado.** Igualar el tamaño obliga a recortar, y eso dejaba
  archivos de 300–400 px que en el celular se veían blandos. Ahora se agranda hasta
  2× con Lanczos y un enfoque suave. Lado mayor mínimo: 638 px (antes 319).
- **`CAJAS_A_MANO`** en el script: para las dos fotos donde el detector se
  equivoca (`anillo-sello-01`, `anillo-aguamarina-01`) se le indica a mano dónde
  está la pieza, en vez de aflojar los umbrales y empeorar las otras 148.

### Resultado medido sobre las 32 portadas
| | antes | después |
|---|---|---|
| tamaño de la pieza | 44% – 98% del cuadro | 67% – 73% |
| desviación estándar | 0,106 | **0,013** |
| centro horizontal | 0,26 – 0,66 | 0,50 (salvo 3 colgantes con cadena diagonal) |

Referencia de tamaño: `pulsera-grumet-01`, donde la pieza ocupa el **71,5%** del
ancho. Ese es el valor de `OBJETIVO` en el script.

**No se cambió ninguna portada.** Cuatro piezas encuadraban con menos relleno
usando otra foto, pero las alternativas son peores como foto de producto (la del
Anillo Sello es en la mano); se prefirió extender el fondo.

### Cómo volver a correrlo
```bash
python3 scripts/normalizar-fotos.py --dry-run    # solo reporta
python3 scripts/normalizar-fotos.py              # aplica
python3 scripts/normalizar-fotos.py --solo anillo-sello-01.jpg
```
Siempre reprocesa desde `fotos/_originales/`, así que correrlo varias veces no
degrada nada. Necesita `pillow`, `numpy` y `scipy`.

## Parte 2 — Bugs arreglados

| # | Qué pasaba | Dónde |
|---|---|---|
| 1 | `og:image` era una ruta relativa: **WhatsApp compartía el enlace sin foto**. Faltaban `og:url`, `og:site_name`, `twitter:image` y `canonical`. | `index.html` `<head>` |
| 2 | El atributo `hidden` **no ocultaba** las flechas ‹ › del overlay, los puntos ni la grilla: una regla de autor con `display` le gana a la del navegador. Las flechas se habrían visto en una pieza de una sola foto. | CSS `[hidden]` |
| 3 | Al tocar "Piezas" o "Portafolio", el **título quedaba tapado** por la barra fija. | `scroll-margin-top` |
| 4 | Abrir el sitio con `#portafolio` en el enlace **no saltaba** a la sección: el navegador salta antes de que el JS dibuje las piezas. | JS |
| 5 | Las dos tarjetas de una fila mostraban la **foto a distinta altura** (hasta 9 px): un `<button>` centra su contenido y la grilla las estira parejo. | `.card` a flex column |
| 6 | La **estrella de la marca no se veía nunca**: quedaba debajo de la foto por orden del HTML. | `z-index` en `.corner` |
| 7 | Al cerrar el overlay el **foco quedaba en un botón oculto**; con teclado se perdía el lugar en la grilla. | `closeDetail()` |
| 8 | Abrir una pieza pedía **~1 MB de fotos de golpe** (7 fotos). Ahora carga 2 y va trayendo las vecinas: **304 KB**, 70% menos. | `buildTrack()` |
| 9 | Las flechas daban la vuelta y el deslizamiento no: dos comportamientos para lo mismo. Ahora la flecha se apaga en los extremos. | `stepPhoto()` |
| 10 | Los textos se insertaban como HTML sin escapar: un nombre con `&` o comillas rompía la tarjeta. | `escapar()` |
| 11 | Faltaba `-webkit-backdrop-filter`: en iPhone anteriores a iOS 18 la barra se veía opaca. | CSS |
| 12 | `94vh` en la hoja del overlay: en Safari el botón de WhatsApp podía quedar fuera de pantalla. Ahora `dvh`. | CSS |
| 13 | Sin JavaScript la página quedaba vacía. Ahora hay un `<noscript>` con enlace a WhatsApp. | HTML |
| 14 | `SOLD.length` decía "1 piezas entregadas" si quedaba una sola. | JS |
| 15 | El botón del 404 usaba ruta relativa: en GitHub Pages llevaba a otro 404. | `404.html` |
| 16 | El overlay podía mostrar la palabra `undefined` si una pieza no tenía precio. | `openDetail()` |

Verificado en el navegador: sin errores de consola, sin imágenes rotas, sin ids
duplicados, sin anclas rotas, y las 15 filas de la grilla alineadas al píxel.

## Lo que NO se tocó
- Tipografías, colores, precios, textos y estructura de secciones.
- El orden de las fotos dentro de cada pieza.
- `aspect-ratio` de la grilla (4/5) ni del overlay (1/1).

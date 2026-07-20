# Cambios v4 — Normalizar encuadre de todas las fotos + orden del Bombé

Requiere `scripts/normalizar-fotos.py` (se entrega junto a este archivo). Depende de `pillow`, `numpy` y `scipy`.

## Contexto del problema (medido sobre las fotos reales del repo)
- Las fotos originales venían en **8 relaciones de aspecto distintas** (0.68 a 1.33) alimentando una grilla fija 4/5 → **13 de 32 piezas tenían la joya literalmente cortada**, hasta un 39% (Aros Zafiros Blancos, Colgante Estrella, Colgante Esmeralda, Anillo Aguamarina Gota…).
- El tamaño de la joya dentro del cuadro iba de **31% a 99%** → por eso unas se ven lejísimos y otras apretadas.
- Centro del sujeto: X entre 32% y 73%, Y entre 28% y 70% → piezas descentradas.

Esto NO se arregla con CSS: hay que re-encuadrar las imágenes.

## 1. Correr el script de normalización
```bash
pip install pillow numpy scipy
python3 scripts/normalizar-fotos.py --dry-run   # revisar salida
python3 scripts/normalizar-fotos.py             # aplicar
```
Qué hace: detecta la joya por energía de bordes, recorta a 4:5 con la joya **centrada y siempre al 70% del cuadro**, rellena replicando el borde si el recorte se sale, y regenera `fotos/*.jpg` (1600px, q86) + `fotos/thumbs/*.jpg` (640px, q78).

- Respalda los originales en `fotos/_originales/` la primera vez. **No borrar esa carpeta**: es la fuente, y el script siempre reprocesa desde ahí (correrlo dos veces no degrada la imagen).
- Ya fue ejecutado y verificado sobre una copia del repo: 151 fotos procesadas, 0 fallidas, y la verificación geométrica confirma lado mayor de la joya = 70% en las 32 portadas.

## 2. Reordenar fotos del Anillo Bombé
En `SOLD[]`, la entrada `Anillo Bombé` (hoy `imgs: ['fotos/anillo-bombe-01.jpg','fotos/anillo-bombe-02.jpg','fotos/anillo-bombe-03.jpg']`) pasa a:
```js
imgs: ['fotos/anillo-bombe-02.jpg','fotos/anillo-bombe-03.jpg','fotos/anillo-bombe-01.jpg']
```
Motivo: `-01` es la foto en la mano (verificado: 68% de píxeles de tono piel, contra 0.5% y 0.2% de las otras dos). La portada debe ser la pieza sola; la de la mano va al final. **No renombrar archivos**, solo cambiar el orden en el array.

## 3. CSS — no tocar aspect-ratio
- La grilla ya está en `aspect-ratio: 4/5` y ahora **calza exacto** con las fotos → cero recorte. No cambiarla.
- El overlay se queda en `aspect-ratio: 1/1`. Verificado: con la joya al 70% centrada, el recorte cuadrado del overlay no la corta en ninguna pieza. No cambiarlo (subirlo a 4/5 haría la hoja demasiado alta en mobile y empujaría el botón de WhatsApp fuera de pantalla).

## 4. Verificación
- `ls fotos/_originales | wc -l` → debe dar 151.
- Screenshot de la grilla completa de "Disponible ahora" y de "Portafolio": todas las piezas deben verse del mismo tamaño relativo y centradas, ninguna cortada por el borde.
- Abrir el overlay de Aros Zafiros Blancos y Colgante Estrella (las dos peor cortadas antes): la pieza debe verse completa.
- Anillo Bombé: la portada en la grilla debe ser la pieza sola, y la foto en la mano debe aparecer al deslizar hasta el final.
- Confirmar que el peso total de `fotos/thumbs/` no subió respecto a antes.

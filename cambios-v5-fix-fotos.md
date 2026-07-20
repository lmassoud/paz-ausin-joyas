# Cambios v5 — Corregir normalización de fotos + portadas

Corrige el resultado de `cambios-v4-fotos-normalizadas.md`. El script v1 tenía un defecto de diseño: para achicar la joya al 70% del cuadro **inventaba fondo replicando el borde**, lo que generó manchones y rayas visibles (peor caso: 87% del cuadro era borde estirado). Se reemplaza el script completo.

## 1. Reemplazar el script
Sobrescribir `scripts/normalizar-fotos.py` con la versión nueva que se entrega junto a este archivo.

Qué cambia: ahora **solo acerca cuando sobra fondo, nunca inventa fondo para alejar**. Cuando la pieza no cabe en 4:5 (fotos apaisadas) rellena con un degradado suave sacado de la propia foto y transición difuminada, no replicando el borde. Además excluye `og.jpg`.

Resultado medido sobre las 150 fotos: ocupación de la joya pasa de 31–99% (original) a **78–92%**, con 7,6% de fondo agregado en promedio.

## 2. Correr el script
```bash
python3 scripts/normalizar-fotos.py --dry-run
python3 scripts/normalizar-fotos.py
```
Reprocesa siempre desde `fotos/_originales/`, así que se puede correr sobre el resultado dañado de la v1 sin degradar nada. Al final imprime la lista de fotos que necesitaron mucho fondo agregado.

## 3. Cambiar portadas mal encuadradas
Cuatro piezas tienen como portada una foto apaisada que no cabe en 4:5, y **otra foto de la misma pieza encuadra perfecto**. Reordenar `imgs[]` para que esa quede primera (no renombrar archivos, no borrar fotos — la actual pasa al final):

| Pieza | Portada actual | Nueva portada | Mejora |
|---|---|---|---|
| Aros Zafiros Blancos | `aros-zafiros-blancos-01.jpg` (51% inventado) | `aros-zafiros-blancos-02.jpg` | 0% inventado |
| Colgante Estrella | `colgante-estrella-01.jpg` (51%) | `colgante-estrella-03.jpg` | 19% |
| Colgante Esmeralda | `colgante-esmeralda-01.jpg` (21%) | `colgante-esmeralda-03.jpg` | 0% |
| Anillo Bombé | `anillo-bombe-01.jpg` (19%, además es la foto en la mano) | `anillo-bombe-02.jpg` | 0% |

Para Anillo Bombé el orden final es: `02, 03, 01` (la de la mano al final), como ya estaba pedido en v4.

## 4. No tocar
- `aspect-ratio` de la grilla (4/5) ni del overlay (1/1): se midió que 4:5 es el formato que menos fondo obliga a inventar (mejor que 1:1 y que 5:4).
- Nada de tipografía, colores, precios ni badges: eso quedó bien.

## 5. Verificación
- Ninguna tarjeta debe mostrar rayas, manchones ni bloques de color plano en los bordes de la foto (era el síntoma de la v1).
- Screenshot de la grilla completa de Disponible y Portafolio: piezas centradas y de tamaño similar.
- Las 4 piezas del punto 3 deben mostrar su nueva portada.
- `og.jpg` sigue en 1200x630.

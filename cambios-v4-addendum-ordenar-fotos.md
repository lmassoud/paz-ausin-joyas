# Fase G-addendum — Ordenar fotos dispersas por reconocimiento visual

Las fotos en `fotos-raw/` están sueltas, sin carpetas. Para cada foto: ábrela,
compárala con la tabla de abajo, propón a qué pieza (01-14) pertenece.

**No muevas nada todavía.** Primero muéstrame la propuesta de agrupamiento
(lista: archivo → pieza propuesta) para que la confirme. Fotos que no calcen
claramente con ninguna: déjalas en una lista aparte "sin identificar", no
adivines.

Cuando confirme, recién ahí: crear `fotos-raw/pieza-NN/`, mover cada archivo
a su carpeta, y seguir con el resto de cambios-v4-catalogo-real.md (renombrar
a `fotos/`, generar `imgs[]`, etc.)

## Descriptores visuales

| # | Pieza | Cómo se ve |
|---|-------|------------|
| 01 | Anillo Sello | Plata, cara plana cuadrada, estrella de 8 puntas grabada al centro con un puntito negro en medio. Hay foto puesto en dedo. |
| 02 | Anillo Micropavé | Banda de plata oscura (rodio negro), ancha, cubierta completo de piedras negras chicas en pavé, sin piedra central. |
| 03 | Anillo Aguamarina | Oro amarillo, piedra redonda grande transparente/verde-agua, engarce tipo corona con muchas garritas doradas. |
| 04 | Anillo Esmeralda (Portafolio) | Oro + plata oscura, forma octagonal, esmeralda verde rectangular al centro, halo de piedras negras. Foto puesta en mano. |
| 05 | Aros Zafiros Blancos | Aros stud chicos, forma hexagonal dorada plana, estrella de 4 puntas grabada, piedra blanca al centro. |
| 06 | Anillo Mosca (Portafolio) | Oro, forma orgánica irregular (tipo insecto/mosca estilizada) fundida sobre un aro circular liso. |
| 07 | Anillo Rubí | Banda delgada metal oscuro, piedras rojas/rosadas en canal alrededor de toda la banda. |
| 08 | Anillo Medio Cintillo Fishtail (Portafolio) | Plata clara delgada, mitad de la banda con piedras blancas en fila, la otra mitad lisa. |
| 09 | Anillo Raíz de Rubí (Portafolio) | Plata oscura, forma cuadrada/rectangular, piedra rosada/roja grande al centro, marco de piedras negras. |
| 10 | Anillo Lady Di (Portafolio) | Oro + plata, forma ovalada, piedra azul oscura central, halo de piedras negras alrededor. |
| 11 | Anillo Sinfín (Portafolio) | Plata clara, banda angosta, piedras negras chicas alrededor de las 360°, tipo eternity. |
| 12 | Anillo Compromiso Esmeralda (Portafolio) | Oro amarillo, forma cuadrada, esmeralda verde rectangular chica, marco de piedras negras. |
| 13 | Transformación Anillo Compromiso (Portafolio) | Oro blanco/plata clara, tres piedras blancas cuadradas en fila, la del centro más grande. |
| 14 | Aros Zafiros y Diamantes | Aros colgantes oro, piedra oscura redonda arriba, abanico de picos con diamantes chicos colgando debajo. |

## Prompt para Code
```
Lee cambios-v4-addendum-ordenar-fotos.md. Propón el agrupamiento de
fotos-raw/ antes de mover nada.
```

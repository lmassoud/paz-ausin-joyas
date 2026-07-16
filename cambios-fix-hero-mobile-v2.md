# Fix — franja de anillos en hero (mobile) + nav mobile

Reemplaza el enfoque de `hero.jpg` como `background` de `.hero` (spec v1, bloque 3, línea "Fondo con foto"). Ese approach queda descartado — no lo dejes activo.

## 1. Franja de anillos con alto fijo
- Agrega `fotos/hero-rings.jpg` (nueva, reemplaza a `hero.jpg` — ese ya no se usa, se puede borrar).
- En `.hero`: agrega `position: relative;` (mantén el resto de sus propiedades actuales tal cual).
- Nueva regla:
```css
.hero::before {
  content: '';
  position: absolute;
  left: 0; right: 0; bottom: 0;
  height: 340px;
  background:
    linear-gradient(180deg, rgba(11,10,9,1) 0%, rgba(11,10,9,.35) 30%, rgba(11,10,9,0) 65%, rgba(11,10,9,0) 100%),
    url('fotos/hero-rings.jpg') center bottom/cover no-repeat;
  z-index: -1;
}
```
- Dentro del media query `@media (max-width:640px)` existente, agrega: `.hero::before { height: 200px; }`
- No agregues `.hero::after` ni ningún otro layer — un solo pseudo-elemento resuelve imagen + fundido.
- Quita el `<link rel="preload" as="image" href="fotos/hero.jpg">` si se llegó a agregar; no hace falta preload para un `::before`.

## 2. Nav mobile
- Dentro del mismo media query `@media (max-width:640px)`: agrega `#nav-ig { display: none; }` (Instagram ya está en el footer, no hace falta repetirlo arriba en pantallas chicas).

## 3. Verificación
- Screenshot 390×844 y 1440×900: confirma que la franja de anillos se ve completa (sin cortarse arriba) y pegada al borde inferior del hero en ambos tamaños — el resultado NO debe depender de cuánto mida el título.
- Confirma que el alto real de `.hero` en mobile no exceda ~100svh por mucho — si el título en dos líneas más el padding actual empuja el hero muy por encima de 75-80svh, reduce el padding vertical de `.hero` hasta acercarlo (esto es necesario para que "Disponible ahora" siga asomando bajo el fold, que es requisito del spec v1).
- Confirma que el nav mobile (`PIEZAS · PORTAFOLIO · WHATSAPP`) ya no se ve apretado.

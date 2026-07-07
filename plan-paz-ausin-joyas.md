# Plan del Proyecto — Paz Ausin Joyas (Catálogo Web)

> Documento de contexto consolidado a partir de la ronda de planificación. Sirve como base para construir la página en una conversación futura dentro de este proyecto.

---

## 1. Resumen en una línea

Página web tipo **catálogo/lookbook** (sin pagos ni carrito) para mostrar las joyas hechas a mano por Maria Paz Ausin, que dirige el tráfico a **WhatsApp** para cerrar la venta directamente con su hijo/a, quien administra el negocio.

---

## 2. Roles y modelo de negocio

- **Fabricante:** Maria Paz Ausin (mamá). Orfebre, ~12 años de trayectoria, tomó cursos pero ya supera el nivel de sus propios profesores.
- **Vendedor/administrador:** el usuario. Recibe el 20% de cada venta gestionada.
- **Punto único de contacto:** todos los compradores escriben **al usuario** (no a la mamá) por WhatsApp para coordinar pago y entrega.
- La mamá está al tanto del proyecto y puede responder preguntas específicas de producto cuando se necesiten (no es sorpresa).
- Objetivo declarado: que este sea **un negocio compartido** entre ambos, con la web como herramienta central.

---

## 3. Marca

- **Nombre confirmado:** *Paz Ausin Joyas*
- Sin logo ni identidad de marca formal previa — hasta ahora vendía solo con su nombre personal en Instagram (@pazausin, cuenta privada).
- Bio actual de Instagram (referencia de tono/mensaje):
  *"Orfebre. Joyería fina en stock y a pedido. Piezas únicas hechas a mano. Plata 950, Oro 18K, piedras naturales."*
- Identidad visual ya reconocible en Instagram: fondos oscuros, foco 100% en la pieza, sin distracciones — **mantener esta línea en la web** para coherencia.
- Motivo recurrente detectado en las piezas: **estrellas** (aros, brazalete grabado) — posible elemento de identidad visual a explotar.

---

## 4. Público objetivo

- Actualmente: conocidas/seguidoras cercanas de Instagram (cuenta privada, alcance limitado a su círculo).
- Rango etario principal: **mujeres 30–50 años**.
- Objetivo adicional (aspiracional): atraer también público más joven.
- Motivo de compra: mixto, pero **predominantemente autorregalo** (también hay compras de regalo).
- Ubicación: venta actualmente **solo local**; abierto a expandir a otras ciudades de Chile si es necesario (sin envíos internacionales por ahora).

---

## 5. Catálogo — qué se vende

**Materiales y técnica:** Plata 950, Oro 18K, piedras naturales. Piezas hechas 100% a mano.

**Dos líneas de producto:**
1. **Piezas únicas** (la mayoría del catálogo) — anillos, aros, pulseras/brazaletes, cada una irrepetible. Actualmente **15–20 piezas disponibles**.
2. **Esclavas de plata** (nueva línea, en desarrollo) — más económicas, pensadas para producirse en mayor cantidad. Precio estimado: **~$60.000 CLP**.

**Rango de precio piezas únicas:** aproximado **$200.000–$500.000 CLP** (a confirmar con exactitud con la mamá — el usuario dio la cifra de memoria y varía según materiales). ⚠️ *Ver sección 12, pendiente de confirmación.*

**Ejemplos reales del catálogo actual (vistos en Instagram):**
- Anillo sello en plata
- Aros geométricos con detalle de estrella
- Argolla con circonias/ónix negro
- Anillo cóctel con esmeralda y halo de piedras negras
- Brazalete rígido grabado con motivo de estrellas
- Anillo con piedra clara tipo ópalo/luna, engarce dorado

**Estructura del catálogo en la web (decisión tomada):**
- **Sección "Disponible ahora"** — solo piezas que se pueden comprar hoy.
- **Sección "Portafolio / Trabajos realizados"** — piezas ya vendidas, mostradas sin botón de compra (o marcadas "Vendido"). Cumple dos funciones: (a) evita que el catálogo se vea vacío cuando se venden piezas más rápido de lo que se producen, y (b) funciona como muestra de trayectoria/credibilidad y abre la puerta a pedidos personalizados ("¿puedes hacer algo parecido a esto?").

---

## 6. Precios — lógica de visualización

- **Vista de catálogo (grilla general):** sin precio visible. Solo foto + nombre de la pieza. Se mantiene limpia, tipo lookbook editorial.
- **Vista de detalle (al hacer clic en una pieza):** aquí sí se muestra el precio, junto al botón de contacto por WhatsApp.
- **Razón de esta lógica:** filtra intención real de compra — quien llega a preguntar por WhatsApp ya sabe el precio, reduciendo consultas de simple curiosidad.
- A futuro: el usuario planea crear una skill personalizada para sugerir precios recomendados por producto (pendiente, no bloquea el lanzamiento).

---

## 7. Flujo de contacto (WhatsApp)

- Botón de WhatsApp en cada ficha de producto, con **mensaje pre-escrito** que incluye el nombre de la pieza (ej: *"Hola! Me interesa el Anillo Sello Plata que vi en la página"*), para que el usuario sepa de inmediato de qué pieza se trata sin tener que preguntar.
- **Función deseada a futuro:** permitir marcar/seleccionar varias piezas mientras se navega y generar un solo mensaje de WhatsApp con todas ellas (ej: *"Hola! Me interesan estas piezas: Anillo Sello, Aros Estrella, Brazalete Grabado"*). Es técnicamente viable sin carrito ni pagos — es solo texto pre-armado en el link de WhatsApp. Se implementa en una segunda etapa, no es bloqueante para el lanzamiento inicial.
- **Número de WhatsApp:** por ahora se usará uno personal; el plan a futuro es conseguir un **número de negocio separado** (WhatsApp Business) que maneje el usuario, para dar más profesionalismo.

---

## 8. Estilo visual

- **Dirección de diseño confirmada:** lujoso, limpio, simple.
- Fondos oscuros, tipografía elegante, mucho espacio en blanco/negativo, foco total en la fotografía de cada pieza (coherente con el feed actual de Instagram).
- Sin exceso de texto en ninguna parte de la página — el producto y la fotografía deben ser el protagonista.
- Página de una sola sección tipo landing/catálogo (no un sitio multi-página complejo).

---

## 9. Contenido fotográfico

- Ya existen fotos de varios ángulos por pieza en el Instagram de la mamá, incluyendo fotos "puestas" (en mano para anillos, en oreja para aros).
- Se pueden reutilizar/reprocesar esas fotos para la web — no se parte de cero.
- Estilo fotográfico ya consistente: fondo oscuro, foco en la pieza, sin distracciones — se mantiene igual en la web.

---

## 10. Aspectos técnicos

- **Tipo de sitio:** estático (HTML/CSS/JS simple), sin necesidad de backend, base de datos ni pagos online.
- **Hosting elegido:** **GitHub Pages** (gratis, sin sorpresas de cobro, se integra naturalmente con flujos de Git — clave porque calza con el plan de automatización futura vía Claude Code).
- **Dominio:** por ahora se parte con el link gratuito de GitHub Pages. Más adelante se comprará un dominio propio (el usuario puede pagarlo) y se conecta al mismo hosting — es un trámite simple, no requiere reconstruir la página.
- **Mantenimiento actual:** manual, actualizado por el usuario cada vez que hay un evento relevante (pieza nueva terminada o pieza vendida) — no en un calendario fijo.
- **Automatización futura (objetivo explícito del usuario):** dejar el proceso de actualización del catálogo automatizado usando **Claude Code o Claude Cowork**, de forma que subir una foto nueva + datos básicos actualice la página sin editar código a mano. Este es un objetivo declarado del proyecto, a desarrollar después de tener la primera versión funcionando.
- El usuario está aprendiendo a construir páginas web con IA mientras se hace este proyecto — se prioriza que el proceso sea entendible y no una caja negra.

---

## 11. Roadmap (orden sugerido, a validar en la próxima conversación)

1. Construir la primera versión estática de la página (estructura, estilo, catálogo con datos/fotos reales o placeholders si faltan).
2. Publicar en GitHub Pages con link gratuito.
3. Ajustar contenido con fotos y datos definitivos de cada pieza (con apoyo de la mamá).
4. Implementar el flujo de WhatsApp con mensaje pre-escrito por producto.
5. (Fase 2) Selección múltiple de piezas → un solo mensaje de WhatsApp.
6. (Fase 2) Comprar dominio propio y conectarlo.
7. (Fase 2) Conseguir número de WhatsApp Business separado.
8. (Fase 2) Automatizar actualizaciones del catálogo vía Claude Code/Cowork.
9. (Fase 2) Skill personalizada para sugerencia de precios.

---

## 12. Pendientes / preguntas para la mamá (Maria Paz)

- [ ] Confirmar rango de precios exacto por tipo de pieza y material (el rango de $200.000–$500.000 CLP dado es aproximado).
- [ ] Confirmar precio final de las esclavas de plata (~$60.000 CLP estimado).
- [ ] Confirmar textos/descripciones de cada pieza actualmente disponible (materiales exactos, medidas si aplica).
- [ ] Definir qué piezas antiguas (ya vendidas) se usarán para la sección de "Portafolio".
- [ ] Fotos definitivas a usar (ángulos, puestas) para cada pieza del catálogo actual.

---

*Fin del documento de planificación. Listo para usarse como contexto inicial en la conversación donde se construya la página.*

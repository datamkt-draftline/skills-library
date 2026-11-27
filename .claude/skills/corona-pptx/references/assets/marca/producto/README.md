# Marca Corona — producto

Assets gráficos del producto Corona (botellas, latas, lima). Todos vienen con fondo transparente y están pensados para ser colocados sobre fondos de la paleta (Corona Blue o White). Hay versiones **fotográficas** (producto real, alta resolución) y **ilustradas** (estilizadas, con textura grabada / distressed, en línea con el lenguaje visual Corona).

## Cuándo usar foto vs. ilustración

- **Foto real** → slides corporativas, de producto, de performance, portadas formales. Lee como "producto Corona".
- **Ilustración / contorno / vintage** → slides conceptuales, de marca, de historia, portadas informales. Lee como "idea Corona".
- **No mezclar los dos estilos en la misma slide** — rompen el tono.

## Archivos

### Botellas 330ml

- **`botella-330ml-foto.png`** — foto real de la botella Corona 330 cm³ (porrón argentino) con lima en el pico, gotas de condensación, etiqueta oficial "Corona cerveza / La Cerveza Más Fina / 4.5% Alc./Vol." Fondo transparente, 464×2000 px (~1.8 MB), optimizada para pptx — insertable directamente con `add_picture` sin pasos adicionales.
- **`botella-330ml-ilustrada.png`** — misma botella pero ilustrada en estilo grabado (textura, etiqueta estilizada en amarillo/blanco/azul, lima verde en el pico). Fondo transparente, ~2 MB. Preferir esta versión cuando el fondo es Corona Blue y buscamos un lenguaje más expresivo.

### Latas 473cc (edición Argentina)

Las tres son fotos reales de la lata Corona 473 cm³ "Edición Limitada Cerveza Industria Argentina" (SINCE 1925, La Cerveza Más Fina). Elegir según el contexto:

- **`lata-473cc-foto.png`** — versión con sombra pronunciada en la base, ligera rotación, más dramática. Para slides donde la lata es el protagonista.
- **`lata-473cc-foto-clean.png`** — versión plana, sin sombra fuerte, bien recta. Para catálogos, grillas de producto, logos pie de slide.
- **`lata-473cc-foto-con-lima.png`** — igual a la clean pero con una rodaja de lima apoyada arriba. Reforza el ritual Corona (lima + cerveza).

### Contornos de botella (porrón)

Variantes estilizadas de la silueta del porrón con la lima encima. Son líneas (outlines), no sólidos. Usar como íconos, puntos de referencia, elementos decorativos o integradores en diagramas, **y como elemento de marca recurrente en la esquina inferior izquierda de las slides** (ver "Elementos de marca obligatorios por slide" en `SKILL.md`). Para ese uso de esquina, preferir `botella-contorno-vector.png` (más limpio y neutro).

- **`botella-contorno-pincel.png`** — contorno pintado a pincel, trazo irregular, blanco. Estética artesanal / hand-made. Usar sobre Corona Blue.
- **`botella-contorno-regular.png`** — contorno limpio en blanco + logo Corona pequeño integrado en el pecho de la botella. La versión más "marca". Usar sobre Corona Blue.
- **`botella-contorno-vector.png`** — contorno geométrico limpio en blanco, sin logo adentro. Versión más neutra. **Preferida para el uso de esquina inferior izquierda.** Usar sobre Corona Blue.

Los tres contornos son blancos → usar sobre fondos oscuros. Sobre fondo blanco quedan invisibles y no se deben recolorear — omitir la silueta en ese caso (regla general: no modificar los assets).

**Variantes de color generadas para fondos claros:**

- **`botella-contorno-vector-blue.png`** — misma silueta recoloreada a Corona Blue `#0C2340`. Usar en slides de fondo blanco donde la versión blanca es invisible. Generada programáticamente (ver skill); no es un asset de marca oficial, pero es la variante más consistente con la paleta Corona para fondos claros.
- **`botella-contorno-vector-black.png`** — misma silueta en negro puro `#000000`. Alternativa cuando se necesita máximo contraste sobre fondos claros no blancos.

Regla de selección rápida:

| Fondo de slide | Variante a usar |
|---|---|
| Corona Blue `#0C2340` | `botella-contorno-vector.png` (blanca) |
| White `#FFFFFF` | `botella-contorno-vector-blue.png` (azul) |
| Imagen / fondo complejo claro | `botella-contorno-vector-blue.png` o `botella-contorno-vector-black.png` |

### Accesorios

- **`lima-cortada-ilustrada.png`** — rodaja de lima ilustrada en Corona Blue, estilo linocut con textura grunge. Fondo transparente, ~400×400. Usar como ícono de acento, decoración de kicker, remate de un título. Funciona sobre fondo blanco o amarillo (el azul contrasta); sobre Corona Blue oscuro se pierde.

## Reglas de uso

- **No modificar**: no recolorear, no distorsionar proporciones, no recortar legales de la etiqueta, no aplicar filtros.
- **No mezclar producto Corona con producto de otras marcas** en la misma slide (si aparecen latas / botellas de otra marca, usar sus propios assets oficiales, no estos).
- **Respetar los textos legales** de las latas y botellas (% alc, Hecho en, etc.): no recortarlos ni taparlos con otros elementos.
- **Escala**: los productos deben leerse como producto, no como manchita. Si entra chico, es preferible usar el contorno (línea) en lugar de la foto completa.
- **Alineación con la narrativa**: no agregar producto solo para decorar. Si la slide no habla de producto, no poner una lata.

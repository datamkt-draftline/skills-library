# Marca Corona — logos oficiales

Variantes de color del logo primario Corona (crown + wordmark "Corona") y del wordmark extendido "Corona cerveza". Usar estos assets como logo principal en toda presentación de marca Corona, excepto cuando la presentación sea específicamente del centenario (ver `aniversario-100/`).

## Cómo elegir la variante

Regla simple: el logo tiene que **contrastar con el fondo** y mantener el color de los elementos de marca (Corona Blue `#0C2340` + Corona Yellow `#FFC72C`). Preferir siempre la versión más rica en color que contraste bien.

| Fondo de la slide | Logo recomendado | Alternativas |
|---|---|---|
| **Corona Blue** `#0C2340` (oscuro) | `corona-logo-white-yellow.png` (B&A: wordmark blanco + corona amarilla) | `corona-logo-white.png` (todo blanco), `corona-logo-white-textured.png` (con textura grabada) |
| **White** `#FFFFFF` (claro) | `corona-logo-color.png` (A&A: wordmark azul + corona amarilla) | `corona-logo-blue.png` (todo azul), `corona-logo-black.png` (todo negro — último recurso) |
| Franja/bloque **Corona Yellow** parcial | `corona-logo-blue.png` o `corona-logo-black.png` | — |

## Archivos

### Primario (crown + wordmark)
- **`corona-logo-color.png`** — A&A: wordmark en Corona Blue + corona en Corona Yellow. **La versión preferida** para fondos claros. PNG transparente.
- **`corona-logo-white-yellow.png`** — B&A: wordmark en blanco + corona en Corona Yellow. **La versión preferida** para fondos Corona Blue oscuros. PNG transparente.
- **`corona-logo-blue.png`** — monocolor Corona Blue (wordmark + corona), para fondos claros neutros.
- **`corona-logo-white.png`** — monocolor blanco (wordmark + corona), para fondos oscuros neutros. (Mismo archivo que `../copacabana/corona-logo-white.png`; mantener sincronizados si se reemplaza.)
- **`corona-logo-black.png`** — monocolor negro. Reservar para contextos monocromáticos o impresión; evitar en presentaciones digitales regulares (preferir el azul).
- **`corona-logo-white-textured.png`** — wordmark blanco con textura grabada/distressed (misma estética que el linocut del aniversario 100). Usar sobre Corona Blue cuando la slide busque un tono vintage/craft; no para portadas corporativas formales.

### Wordmark extendido
- **`corona-cerveza-wordmark-blue.pdf`** — vector del wordmark "Corona cerveza" (sin corona arriba), en Corona Blue. Formato PDF escalable. Usar cuando se necesite reforzar la categoría "cerveza" (ej: slide de producto, pie de presentación) en lugar del logo con corona.

### Bandera Argentina circular
- **`bandera-argentina-circular.png`** — bandera Argentina en versión circular (celeste + blanco + sol de Mayo), 2000×2000 px, fondo transparente. Es el **asset de origen país** y acompaña al logo Corona en la esquina superior derecha de todas las slides. Es un asset FIJO: no recolorear, no cambiar por versión rectangular, no reemplazar por otra bandera. Ver la sección "Elementos de marca obligatorios por slide" en `SKILL.md` para posición y tamaño exactos.

## Reglas de uso (todas las variantes)

- **No modificar**: no recolorear, no distorsionar la proporción, no recortar la corona del wordmark, no aplicar sombras / gradientes / brillos, no rotar.
- **Mantener la jerarquía de color de marca**: el logo "color" lleva SIEMPRE azul + amarillo. No inventar versiones azul+blanco, amarillo+negro, etc.
- **Área de reserva**: dejar un margen alrededor del logo equivalente a la altura de la corona. No pegar texto ni otros elementos contra el bounding box del logo.
- **Resolución**: los PNGs monocolor están en resolución chica (~440×270). Para usos grandes (portada a página completa), preferir el PDF del wordmark o pedirle al usuario un asset vectorial.
- **Elegir una sola variante por presentación** y mantenerla a lo largo de toda la deck para consistencia. Está permitido variar solo si cambia el color de fondo (ej: slides oscuras usan B&A, slides claras usan A&A).

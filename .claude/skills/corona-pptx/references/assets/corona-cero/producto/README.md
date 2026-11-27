# Corona Cero — producto (versiones regulares, sin branding olímpico)

Fotos reales e ilustraciones del producto Corona Cero Argentina (botella 330 ml / lata 473 cc). Todas llevan la etiqueta "Corona Cero / La Cerveza Más Fina / 0.0% Alc./Vol. / Cerveza Sin Alcohol / Industria Argentina", SIN los anillos olímpicos. Para variantes co-brandeadas con los Juegos Olímpicos, ver `../olimpicos/`.

## Archivos

### Latas 473 cc

- **`lata-473cc-foto-con-lima.png`** — foto real de la lata Cero 473 cc **con rodaja de lima apoyada arriba**. PNG transparente. Refuerza el ritual (lima + cerveza), ideal para slides de consumo / momento de uso.
- **`lata-473cc-foto-sin-lima.jpg`** — misma lata **sin lima**. **JPG con fondo blanco** (no transparente). Usar cuando el fondo de la slide es blanco (el JPG se integra sin bordes raros); si el fondo es otro color o se necesita transparencia, no sirve — preferir la versión con lima o pedirle al usuario el PNG.

### Botellas 330 ml

- **`botella-330ml-foto-con-lima.png`** — foto hi-res de la botella Cero 330 ml **con lima en el pico y gotas de condensación**. PNG transparente, archivo pesado. Es la versión "glamour", la que mejor comunica Corona Cero como ritual. Redimensionar al insertarla en la pptx.
- **`botella-330ml-foto-sin-lima.png`** — porrón Cero **limpio**, sin lima, sin condensación. Foto más neutra para catálogos o grilla de producto.
- **`botella-contorno-white.png`** — contorno (outline) de la botella Cero **en línea blanca**, con el logo "Corona Cero" pequeño integrado en el pecho. Fondo transparente, PNG chico. Usar como ícono / silueta sobre fondos oscuros (Corona Blue). No hay versión en celeste.

### Botellas ilustradas 330 ml

Dos tratamientos gráficos de la botella, ambos con lima en el pico:

- **`botella-330ml-ilustrada-color-pleno.png`** — ilustración en **color pleno plano** (sin textura grabada). Etiqueta estilizada "Corona Cero / La Cerveza Más Fina / 330 ml / 0.0%", cuerpo amarillo plano, lima verde plana. Lenguaje más moderno y flat. Usar sobre fondo blanco o celeste claro.
- **`botella-330ml-ilustrada-grabada.png`** — misma botella pero con **textura grabada / linocut** (grunge en el cuerpo, etiqueta desgastada). Lenguaje artesanal / craft, alineado con el estilo Corona Display + brush textures. Usar sobre Corona Blue oscuro para que la textura resalte.

**Elegir una sola variante de ilustración por presentación** y no mezclar con la foto real en la misma slide.

## Reglas de uso

- **No modificar ningún asset** (recolorear, distorsionar, recortar legales "0.0%", "Cerveza Sin Alcohol", "Industria Argentina").
- **Siempre mostrar el "0.0%"** de forma legible — no taparlo con otros elementos ni recortarlo al redimensionar.
- **Foto real vs ilustración**: usar **uno de los dos estilos** a lo largo de toda la presentación. Mezclar crea ruido visual.
- Todos los assets de esta carpeta vienen pre-optimizados (resize + strip de metadata) para embeberlos directamente en python-pptx con `add_picture(path, left, top, height=...)` sin pasos de preprocesamiento.

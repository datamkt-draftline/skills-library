# Aniversario 100 años — assets

Assets gráficos de la campaña **100 años de Corona** (centenario, referencia 1925 → presente). Usar **solo** cuando la presentación trate específicamente del aniversario de los 100 años, de la historia / legado de la marca, o cuando el brief del usuario lo mencione explícitamente. Para presentaciones regulares de Corona, no usar — confunden el mensaje.

## Archivos disponibles

### `corona-100-logo-linocut-white.pdf`
**Logo oficial "Corona 100" en versión linocut (textura grabada/distressed) — blanco, vectorial.**
- Es la versión más expresiva del logo 100: trae la textura desgastada tipo grabado que el manual VBI de Corona asocia a sus headlines "above-the-line".
- Siempre en blanco, por lo tanto **usar sobre fondos oscuros** (Corona Blue `#0C2340` ideal). Nunca sobre fondo blanco ni amarillo claro.
- PDF vectorial → escala sin pérdida. Preferir este formato cuando el logo va grande (portada, separador de sección, cierre a página completa).

### `corona-100-logo-white.png`
**Logo "Corona 100" en blanco, versión limpia (menos textura), PNG.**
- Alternativa al linocut cuando necesitás un logo más plano y legible: usos chicos (esquina de slide, pie), contextos donde la textura grabada agrega ruido visual.
- También en blanco → **usar solo sobre fondos oscuros** (Corona Blue). Si el fondo es blanco, no hay versión en azul disponible en esta carpeta; pedirle al usuario el archivo correspondiente antes de improvisar.
- PNG rasterizado (alta resolución, ~3300×1900). No escalar más allá del original.

### `corona-crown-yellow-distressed.png`
**Corona (la corona del logo) aislada, en Corona Yellow `#FFC72C`, con textura distressed.**
- Elemento gráfico de acento — **no es un logo completo**. Usar como ornamento: kicker de sección, decoración de portada, punto de referencia visual arriba de un título.
- Funciona sobre fondo Corona Blue (es donde el amarillo distressed luce mejor) o sobre fondo blanco (el amarillo distressed sobre blanco da un tono vintage).
- El PNG viene con mucho canvas transparente alrededor (crown en la parte superior central, ~4000×2250 total). Al colocarla en una slide, considerar recortar el bounding box visible o posicionarla sabiendo que el canvas excede el gráfico.

### `corona-bottle-1925-vintage.png`
**Botella Corona Extra estilizada con lima — ilustración vintage que remite a 1925 (año fundacional).**
- Fondo transparente, botella completa con etiqueta "Corona Extra / La Cerveza Más Fina / Hecho en México / Cervecería Modelo" en estilo gráfico desgastado.
- Usar como ilustración principal en slides sobre historia / fundación / legado de la marca.
- Formato PNG, ~1920×1080 canvas. Mantener la proporción al redimensionar.
- Funciona sobre fondo blanco o Corona Blue (tiene colores propios — azul oscuro de la etiqueta + amarillo del cuerpo + verde lima — y se destaca en ambos).

## Reglas al usarlos

- **No modificar**: no recortar el grafismo, no recolorear, no aplicar filtros / sombras / gradientes, no distorsionar la proporción.
- **No mezclar con los logos regulares de Corona** (que serán agregados a esta skill en batches posteriores). Si la slide es sobre 100 años, el logo 100 reemplaza al logo regular; no van juntos.
- **Contraste**: todos los assets de esta carpeta están pensados para fondo Corona Blue oscuro (los blancos y la corona amarilla distressed). La botella funciona sobre cualquiera de los dos fondos de la paleta.
- **Z-order**: si se superponen con texto, el texto va adelante solo si no entorpece la lectura del logo. En slides de portada/cierre donde el logo 100 es el protagonista, el texto se acomoda alrededor, no encima.

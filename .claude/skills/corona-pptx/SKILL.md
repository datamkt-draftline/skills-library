---
name: corona-pptx
description: Genera una presentación PowerPoint (.pptx) editable con la identidad visual de la marca Corona a partir de un brief, información o archivos aportados por el usuario.
action: true
---

# Presentación Corona

Usá esta skill cuando el usuario pida armar una presentación para la marca Corona, o cuando adjunte materiales para transformar en slides. El objetivo es entregar un `.pptx` editable, claro, profesional y visualmente consistente con la identidad de marca Corona.

## Principio general

**La identidad visual está definida en esta skill (paleta y tipografía). El contenido define el diseño de cada slide.**

No existe un catálogo cerrado de layouts ni un template fijo. Diseñá cada slide libremente y desde cero según lo que necesite comunicar, aplicando siempre las reglas de identidad de marca descritas abajo.

## Presentación de referencia (inspiración, NO template)

En `references/presentacion-referencia/slides/` hay **45 imágenes PNG** (`slide-01.png` a `slide-45.png`), una por cada diapositiva de una presentación real que la marca Corona Argentina armó manualmente. Sirven **como inspiración visual** del lenguaje que la marca usa internamente: cómo ordena gráficos de performance, cómo arma matrices de "growth bets", cómo trata separadores de sección, cómo integra el logo + la bandera + la silueta de botella en la composición, qué densidades de texto usa, qué ritmo da al deck.

### OBLIGATORIO: ver TODAS las imágenes antes de diseñar

**Antes de escribir una sola línea de código de la presentación nueva, usá la herramienta Read sobre TODAS las imágenes de `references/presentacion-referencia/slides/` (`slide-01.png` a `slide-45.png`) para absorberlas visualmente.** Read soporta PNG y te permite ver cada slide como un multimodal input. Es el paso que da consistencia entre ejecuciones — sin él, la skill queda operando "a ciegas", el resultado depende de memoria parcial, y aparecen sesgos de ejecución (ej: todas las slides terminan con fondo azul porque solo miraste separadores, o todas las slides terminan sin placeholders de foto porque solo miraste slides de datos densos).

**Son 45 imágenes. Leerlas todas al inicio de la ejecución, no "las que parezcan relevantes". El costo de miradas es muy bajo comparado con el de entregar un deck sesgado.** La skill confía en que mirás todo el repertorio visual antes de empezar — si saltás esta regla, es prácticamente seguro que el output va a tener alguno de estos vicios documentados:

- Todas las slides con fondo Corona Blue (la ref mezcla fondos blancos con azules — ver abajo).
- Ninguna slide con `[Inserte imagen]` (la ref está llena de placeholders de foto).
- Botella Corona en el mismo color en todo el deck (la ref alterna variante blanca sobre azul y azul sobre blanco).
- Logos de sub-campaña ausentes (la ref los usa activamente en overviews, portadas de sección, headers de campaña).

Cómo mirar concretamente:

- **Leer las 45 imágenes al principio.** Si por restricciones de turno no podés leer 45 en un solo paso, leé al menos 20 bien distribuidas y seguí leyendo durante la ejecución, pero no empieces a generar código sin haber visto una muestra densa y variada.
- **Si el brief actual tiene un tipo específico de contenido** (ej: comparación de campañas, breakdown por región, timeline, sentiment analysis), buscá en lo que mirás al menos una slide análoga de la referencia para ver cómo la marca resuelve ese layout.

Reglas de uso de la referencia:

- **No la copies slide por slide.** La presentación generada debe ser **original**: diseñada desde cero para el brief actual, con sus propios textos, estructura y composiciones.
- **No toda slide generada debe basarse en una slide de referencia.** Si una slide del brief no tiene un análogo claro, diseñala con criterio propio.
- **No todas las presentaciones generadas deben tener el mismo formato.** La referencia es un vocabulario visual, no una plantilla rígida. Variá composición, densidad, ritmo y recursos entre presentaciones según el contenido real.
- **Lo que sí se repite siempre**: los elementos de identidad obligatorios descritos en la sección "Elementos de marca obligatorios por slide" — logo Corona + bandera Argentina arriba a la derecha, silueta de botella abajo a la izquierda (con variante de color según el fondo — ver abajo).

### Variedad de fondos — no todas las slides en Corona Blue

**La presentación de referencia NO tiene todas las slides en fondo azul.** Mirando el deck fuente, el ratio es aproximadamente:

- **Slides de fondo blanco** (`#FFFFFF`) — la mayoría de las slides de datos, performance y comparación: títulos en Corona Blue arriba, barra amarilla horizontal como kicker de sección, cards con fondo gris claro y bordes grises, headers de card en azul oscuro o amarillo, thin blue bar decorativa al pie. Ver `slide-03.png`, `slide-05.png`, `slide-07.png`, `slide-11.png`, `slide-12.png`, `slide-13.png`, `slide-17.png`, `slide-27.png`, `slide-32.png`, `slide-45.png` como referencia.
- **Slides de fondo Corona Blue** (`#0C2340`) — separadores de sección, portadas de capítulo, slides visuales/de campaña con fotos grandes, statements conceptuales, y algunas slides de comparación tipo "growth bets". Ver `slide-01.png`, `slide-02.png`, `slide-06.png`, `slide-09.png`, `slide-10.png`, `slide-15.png`, `slide-16.png`, `slide-20.png`, `slide-23.png`, `slide-26.png`, `slide-35.png`, `slide-37.png`.
- **Slides de fondo Corona Lime** (`#A8BD1C`) — SOLO contextos Lime Ritual / Open Lid / Cero Lime. Ver `slide-40.png`.
- **Fondos gradient / textura** — statement slides o separadores con textura sutil. Ver `slide-21.png`, `slide-24.png`, `slide-32.png`.

**Regla práctica**: si una slide tiene mucho dato numérico, gráficos o tablas → casi siempre fondo blanco. Si es un statement, foto de campaña a tamaño grande, matriz "growth bets" o separador → fondo azul. Alterná conscientemente entre ambos para dar ritmo al deck. **Jamás entregues un deck donde el 100% de las slides tiene fondo Corona Blue.**

### Cómo cargar las imágenes

```
Read references/presentacion-referencia/slides/slide-01.png
Read references/presentacion-referencia/slides/slide-02.png
Read references/presentacion-referencia/slides/slide-03.png
# ...hasta slide-45.png
```

No intentes abrir un `.pptx` ni parsear XML binario para esto — la lectura visual directa de los PNGs es la fuente de verdad.

## Elementos de marca obligatorios por slide

En **todas las slides donde sea visualmente posible**, deben aparecer los tres elementos siguientes. Son obligatorios y van siempre en el mismo lugar:

### 1. Logo Corona + bandera Argentina (esquina superior derecha) — OBLIGATORIO

Un pequeño lockup horizontal formado por:

- **Logo Corona** (variante según color de fondo de la slide — ver reglas de contraste abajo).
- **Bandera Argentina circular** (`references/assets/marca/logo/bandera-argentina-circular.png`, 2000×2000 px, fondo transparente). Siempre la misma — no recolorearla ni cambiarla por una versión rectangular.

**Posición** (slide 13.33" × 7.5"):
- Alineado al borde superior derecho con un margen de ~0.15"–0.25" al top y al right.
- Altura total del lockup: ~0.35"–0.50" (suficientemente chico para no competir con el contenido pero legible).
- Logo Corona a la izquierda, bandera a la derecha. Separación mínima entre los dos: ~0.1".
- Orden ejemplo para alinear con `right = slide_width - 0.2"`: primero bandera (más a la derecha), después logo Corona (a la izquierda de la bandera).

**Variante de logo según fondo** (la bandera es siempre la misma):

| Fondo de slide | Logo Corona a usar |
|---|---|
| Corona Blue `#0C2340` (oscuro) | `marca/logo/corona-logo-white-yellow.png` o `corona-logo-white.png` |
| White `#FFFFFF` (claro) | `marca/logo/corona-logo-color.png` o `corona-logo-blue.png` |
| Franja/bloque Corona Yellow parcial sobre el que apoya el logo | `marca/logo/corona-logo-blue.png` |
| Imagen / fondo complejo | `marca/logo/corona-logo-white.png` con sombra sutil si hiciera falta legibilidad (la sombra es excepción justificable solo para este caso) |

**Ejemplo de código** (ajustar según `slide_width`):

```python
from pptx.util import Emu

RIGHT_MARGIN = Emu(228_600)   # ~0.25"
TOP_MARGIN   = Emu(137_160)   # ~0.15"
FLAG_SIZE    = Emu(365_760)   # ~0.40" (la bandera es cuadrada)

# Bandera (va más a la derecha)
flag_left = prs.slide_width - RIGHT_MARGIN - FLAG_SIZE
slide.shapes.add_picture(
    "references/assets/marca/logo/bandera-argentina-circular.png",
    flag_left, TOP_MARGIN, FLAG_SIZE, FLAG_SIZE,
)

# Logo Corona (a la izquierda de la bandera)
LOGO_RATIO = 1.654  # w/h de corona-logo-white-yellow.png (440×266)
LOGO_H     = Emu(329_184)       # ~0.36" (apenas más chico que la bandera)
LOGO_W     = Emu(int(LOGO_H * LOGO_RATIO))
GAP        = Emu(91_440)        # ~0.10"
logo_left  = flag_left - GAP - LOGO_W
logo_top   = TOP_MARGIN + Emu(18_288)  # centrado verticalmente con la bandera
slide.shapes.add_picture(
    "references/assets/marca/logo/corona-logo-white-yellow.png",
    logo_left, logo_top, LOGO_W, LOGO_H,
)
```

**Cuándo omitir el lockup**:

- Slides donde el contenido llega al borde superior derecho sin aire posible (ej: imagen fullbleed total, mapa que ocupa toda la slide, video cover). En ese caso, sobreponer el lockup *dentro* de la imagen siempre que la lectura aguante, o considerar reducir ligeramente el contenido para abrir espacio.
- Si definitivamente no entra, está bien omitirlo — pero debe ser excepción, no default. El lockup entra en la gran mayoría de las slides.

### 2. Silueta de botella Corona (esquina inferior izquierda) — OBLIGATORIA, con color que cambia según el fondo

La silueta de botella Corona aparece en **todas las slides** donde haya espacio abajo a la izquierda. **Es un elemento recurrente de identidad, como el lockup arriba a la derecha** — no se omite por default, se omite solo cuando el contenido pisa esa esquina.

- Assets disponibles en `references/assets/marca/producto/`:
  - `botella-contorno-vector.png` — silueta **blanca** → usar sobre fondos Corona Blue u oscuros
  - `botella-contorno-vector-blue.png` — silueta **Corona Blue `#0C2340`** → usar sobre fondos blancos
  - `botella-contorno-vector-black.png` — silueta **negra** → alternativa para fondos claros no blancos

**La variante de color se decide por el color de fondo de la slide, slide por slide — no es una elección estética libre.** Igual que con el lockup Corona + bandera, si el deck alterna fondos (como debe), la silueta alterna de color. Un deck donde todas las botellas son blancas (o todas azules) es un bug — probablemente te olvidaste de pasar el color según el fondo:

| Fondo de slide | Variante |
|---|---|
| Corona Blue `#0C2340` (oscuro) | `botella-contorno-vector.png` (blanca) |
| White `#FFFFFF` (claro) | `botella-contorno-vector-blue.png` (azul) |
| Corona Lime (solo contextos Lime) | `botella-contorno-vector-blue.png` (azul, contrasta con lima) |
| Imagen / fondo complejo | según contraste: blanca sobre oscuro, azul sobre claro |

**Implementación recomendada**: envolvé la silueta en una función `bottle_bottom_left(slide, *, dark_bg)` que recibe el color del fondo como parámetro y elige el asset correcto. Llamala desde CADA función que construye una slide, pasando el `dark_bg` correspondiente. No hardcodees la variante en la función — eso te hace olvidar cambiarla cuando una slide cambia de fondo.

- **Posición**: alineada al borde inferior izquierdo con margen ~0.10"–0.20". Altura ~1.0"–1.2". No invade el contenido principal. **Si la slide tiene una thin footer bar al pie (como las slides de datos blancas de la ref), la botella se apoya justo arriba de esa barra, no debajo** (ver `slide-07.png`, `slide-12.png`, `slide-17.png`).

**Ejemplo de código**:

```python
BOTTLE_H    = Emu(941_832)   # ~1.03"
ratio       = 417 / 1189      # w/h del asset
BOTTLE_W    = Emu(int(BOTTLE_H * ratio))
BOTTLE_LEFT = Emu(109_728)   # ~0.12"

def bottle_bottom_left(slide, *, dark_bg):
    if dark_bg:
        bottle_top = SH - BOTTLE_H - Emu(45_720)   # ~0.05" del bottom
        file = "botella-contorno-vector.png"        # blanca
    else:
        bottle_top = SH - BOTTLE_H - Emu(120_000)  # arriba de la thin footer bar
        file = "botella-contorno-vector-blue.png"   # azul
    slide.shapes.add_picture(
        f"references/assets/marca/producto/{file}",
        BOTTLE_LEFT, bottle_top, BOTTLE_W, BOTTLE_H,
    )
```

**Cuándo omitir la silueta**:

- Slide con contenido / elemento gráfico pegado a la esquina inferior izquierda que no se puede reacomodar.
- Separadores de sección con un único statement centrado — opcional (algunas lo llevan para reforzar marca, otras quedan más limpias sin él).
- Se puede omitir cuando quita aire a la composición. "Logo + bandera arriba a la derecha" es más obligatorio que "silueta abajo a la izquierda", pero la botella entra en la gran mayoría de las slides.

### 3. Consistencia

- El lockup logo+bandera y la silueta de botella **mantienen la misma posición y tamaño en toda la deck** (con la excepción obvia de slides donde se omiten por falta de espacio).
- Si una slide tiene fondo oscuro y la siguiente fondo claro, **cambia solo la variante de color** del logo Corona — el tamaño y la posición del lockup no se mueven, y la bandera sigue igual.

## Formato de salida

- **Siempre `.pptx`**, aunque el usuario no lo aclare. Si pide expresamente otro formato (`.pdf`, imágenes, HTML, etc.), generar eso en su lugar.
- Formato de slide 16:9 widescreen: `13.333" × 7.5"` (`12192000 × 6858000` EMU).
- El archivo se guarda en la work folder actual con un nombre descriptivo (ej: `presentacion_corona_<tema>_<YYYY-MM-DD>.pptx`).
- Al terminar, mostrar el archivo con `mcp__tas__open_file`.

## Identidad visual

### Paleta de colores (única fuente de verdad)

Solo se pueden usar estos cuatro colores — ningún otro valor hex, ningún tema por defecto de python-pptx, ninguna variación arbitraria.

| Nombre | HEX | RGB | Rol |
|---|---|---|---|
| Corona Blue | `#0C2340` | 12, 35, 64 | Primario — fondos oscuros, títulos sobre blanco, bloques de acento |
| White | `#FFFFFF` | 255, 255, 255 | Primario — fondos claros, texto sobre azul |
| Corona Yellow | `#FFC72C` | 255, 199, 44 | Secundario — acentos, destacados, franjas, keywords |
| Corona Lime | `#A8BD1C` | 168, 189, 28 | Acento condicional — SOLO para contextos de Lime Ritual / lima / open lid / Corona Cero Lime |

Reglas de uso:

- **Corona Blue + White son los colores primarios.** La presentación se arma principalmente con combinaciones de estos dos.
- **Corona Yellow es siempre un color de apoyo.** Aporta calidez; no se usa como fondo total de slide ni como color dominante.
- **Prohibido fondo totalmente amarillo.** El amarillo se usa como acento (franja, bloque parcial, kicker, cifra destacada, línea decorativa), nunca cubriendo toda la slide.
- **Nunca texto amarillo sobre fondo blanco** — no cumple contraste. Amarillo sobre azul oscuro sí (amarillo como texto destacado sobre Corona Blue está bien).
- **Corona Lime es condicional.** Solo entra cuando el contenido de la slide habla específicamente de *Lime Ritual*, *Corona Open Lid*, *Corona Cero Lime* o cualquier iniciativa de producto/campaña centrada en la lima. En presentaciones sin esos contextos, no usarlo. Cuando entra, funciona como acento (barra, bloque chico, ícono, keyword destacado) — nunca como fondo total ni como color dominante, igual criterio que Corona Yellow. Nunca combinar amarillo + lima en la misma slide como dos acentos distintos (chocan): elegí uno.
- **Nunca mezclar con otras paletas.** No introducir grises, negros puros, azules intermedios ni ningún otro color. Si necesitás un neutro, es `#FFFFFF`; si necesitás un oscuro, es `#0C2340`.

### Reglas de contraste

Elegí el color de texto según el fondo de la slide, siempre con un valor exacto de la paleta:

- Fondo **Corona Blue** (`#0C2340`) → texto `#FFFFFF` (cuerpo) y, cuando corresponda, `#FFC72C` (acentos, cifras, kickers). En contextos Lime, el acento también puede ser `#A8BD1C` — no mezclar con amarillo en la misma slide.
- Fondo **White** (`#FFFFFF`) → texto `#0C2340`. El amarillo puede aparecer como acento gráfico (barra, subrayado, ícono), pero **no como texto**. Corona Lime sí tiene contraste suficiente sobre blanco para texto corto / destacado en contextos Lime.
- Fondo **Corona Yellow parcial** (nunca total) → texto `#0C2340`.
- Fondo **Corona Lime parcial** (nunca total, solo en contextos Lime) → texto `#0C2340`.

### Tipografía — Corona Headline + Corona Brush

La skill usa dos fuentes tipográficas propias de la marca, disponibles en `references/fonts/`:

| Archivo | Font name en python-pptx | Rol |
|---|---|---|
| `CoronaHeadline-SemiBold.otf` | `"CoronaHeadline-SemiBold"` | **Fuente base de todo el deck** — body copy, bullets, kickers, labels, números, captions, footnotes |
| `CoronaBrush-Bold.ttf` | `"CoronaBrush-Bold"` | **Fuente de display** — títulos grandes en portada (≥36 pt), texto de separadores de sección, headline del slide de campañas overview |

**Constantes en el script**:

```python
FONT         = "CoronaHeadline-SemiBold"   # fuente base, default de txt() y mixed_txt()
FONT_DISPLAY = "CoronaBrush-Bold"           # solo para display de alto impacto
```

**Reglas de aplicación**:

- Setear siempre explícitamente `run.font.name` en cada run — no confiar en defaults de python-pptx ni en herencia de tema.
- `FONT_DISPLAY` se usa selectivamente: portada (título principal ≥36 pt), slides de separador de sección, y cualquier otro headline de impacto a tamaño de display. No usarlo para body copy, labels ni cifras de gráficos.
- `FONT` (CoronaHeadline-SemiBold) va en todo lo demás: sección titles, kickers, cuerpo de texto, valores de gráficos, bullets, footnotes, placeholders `[Inserte imagen]`.
- Fallback: si el entorno no tiene instaladas las fuentes Corona (raro, ya que las fuentes solo necesitan existir como nombre en el PPTX para que el viewer las use si las tiene instaladas), la skill igual setea los nombres correctos — el PPTX va a renderizar las fuentes correctamente en cualquier máquina donde el usuario las tenga instaladas.

Jerarquía oficial de pesos dentro de CoronaHeadline:

| Uso | Peso / font name |
|---|---|
| Títulos de sección, kickers, headlines de card | `"CoronaHeadline-SemiBold"` + `font.bold = True` (o solo el nombre) |
| Body copy, bullets, descripciones, captions | `"CoronaHeadline-SemiBold"` |
| Énfasis dentro del body copy | `"CoronaHeadline-SemiBold"` + `font.bold = True` |

**Nota sobre Helvetica Neue**: versiones anteriores de la skill usaban Helvetica Neue como fuente base. Esas referencias en layouts, ejemplos de código o comentarios son obsoletas — reemplazarlas por `CoronaHeadline-SemiBold` / `CoronaBrush-Bold` según el rol.

## Catálogo de assets (`references/assets/`)

La skill tiene un catálogo de assets gráficos oficiales organizado por **contexto** (marca base + sub-plataformas). Cada sub-carpeta tiene su propio `README.md` con la descripción de cada archivo, reglas de uso, variante para fondos claros vs oscuros, y advertencias específicas.

**Los assets no son un recurso de último recurso — son parte del diseño de la presentación.** Una presentación Corona bien hecha usa el catálogo activamente: logos en portada y cierre, productos en slides de propuesta de valor, texturas como fondos o separadores, keyvisuals en slides de campaña. Antes de diseñar cada slide, preguntate qué assets del catálogo pueden enriquecer esa slide — no solo si "resuelven una necesidad" sino si mejoran la comunicación visual.

**Antes de crear la primera slide**, identificá el contexto del brief y leé el `README.md` de la carpeta correspondiente para conocer todos los assets disponibles. El catálogo manda — no inventes logos, ni los dibujes con shapes, ni descargues nada.

### Resolver la ruta en runtime

```python
import os
SKILL_DIR  = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SKILL_DIR, "references", "assets")
# ejemplo:
# logo_path = os.path.join(ASSETS_DIR, "marca", "logo", "corona-logo-color.png")
```

### Mapa de contextos

| Contexto | Cuándo usar | Carpeta |
|---|---|---|
| **Marca Corona (base)** | Presentación general / institucional / de producto Corona regular | `marca/` → sub-carpetas `logo/`, `textura/`, `producto/` |
| **This Is Living (tagline)** | Portada, cierre, separador o statement — máx. 1–2 slides por deck | `this-is-living/` |
| **Corona Cero** | Presentaciones del producto sin alcohol (0.0%) | `corona-cero/` → sub-carpetas `logo/`, `producto/`, `olimpicos/` (variante co-branded con Juegos Olímpicos — solo contextos autorizados) |
| **Corona Sunsets** | Plataforma Sunsets / Sessions / eventos de música al atardecer | `corona-sunsets/` → sub-carpetas `logo/`, `world-tour/` (variante gira global; keyvisual ARG incluido) |
| **Corona Island** | Experiencia / destino Corona Island | `corona-island/` |
| **Corona Natural Ice Bar** | Activación de bares de hielo natural | `corona-natural-ice-bar/` |
| **100 años (aniversario)** | Centenario, historia / legado 1925–2025 | `aniversario-100/` |
| **Copacabana** | Campaña / evento / activación Copacabana | `copacabana/` |

### Reglas transversales de assets

- **Usar el catálogo activamente — es obligatorio, no un nice-to-have.** No esperar a tener una "necesidad" para buscar un asset. Al diseñar cada slide, revisar qué hay disponible y si algún asset mejora la comunicación de esa slide (refuerza la identidad de marca, ilustra el producto, da peso visual a una campaña). Una presentación sin ningún asset del catálogo es una presentación a medio terminar.
- **Regla operativa: toda sub-campaña del brief QUE TENGA asset en el catálogo debe usar ese asset.** No todas las sub-campañas tienen assets — chequeá primero `references/assets/<contexto>/` para ver si existe. Si existe el logo oficial de ese contexto, usarlo es obligatorio: debe aparecer al menos en (1) el separador de sección de esa campaña y (2) el overview / slide de apertura de esa sección, idealmente también en slides dedicadas a esa campaña. No usar solo texto en mayúsculas cuando el logo está disponible — el logo oficial dice mucho más que el texto. Si la sub-campaña NO tiene asset en el catálogo (contexto nuevo, campaña ad hoc, iniciativa sin branding dedicado), es válido quedarse con texto; en ese caso no inventes un logo ni intentes dibujarlo. Chequear en la revisión final: por cada campaña del brief con asset disponible, ¿aparece su logo oficial en al menos el separador + el overview? Si no, falta.
- **Leer el README de la carpeta antes de usar sus archivos.** Cada contexto tiene reglas propias (ej: los anillos olímpicos solo en campañas autorizadas, el tagline "This Is Living" no se repite en cada slide, el amarillo Cero celeste no se inventa).
- **No modificar ningún asset** (recolorear, recortar, distorsionar proporción, rotar, aplicar filtros, sombras, degradados). Se usan tal cual.
- **No mezclar logos de contextos distintos** en la misma slide salvo que el contenido explícitamente compare / integre esas sub-marcas.
- **Una sola variante de logo por presentación** — no alternar entre azul y blanco salvo que cambie el color de fondo de la slide. No alternar entre "lockup + tagline" y "solo logo".
- **Resolución y peso**: todos los assets del catálogo vienen pre-optimizados (resize + strip) para embeberse directo sin procesamiento extra. La skill no requiere paso de preprocesamiento.
- **Fondos baked**: algunos logos vienen con fondo pintado adentro (no transparente). El README de cada carpeta lo flaguea — no usar esos sobre un color de fondo distinto.

## Imágenes de contenido — foto real vs placeholder gris

**La presentación de referencia usa muchas fotos reales. La skill no tiene un repositorio de fotografía genérica.** Siempre que el diseño "necesite una foto" (persona, ambiente, consumo, evento, producto en contexto, lifestyle) y el catálogo de `references/assets/` no cubra esa necesidad específica, dejá un **placeholder gris** con la leyenda `[Inserte imagen]` centrada. **Es obligatorio, no opcional** — un deck sentiment/performance/campañas sin ningún `[Inserte imagen]` es un bug, no una decisión estética.

Imaginá activamente dónde irían las fotos: una presentación Corona rica visualmente debería tener **varios placeholders por slide de contenido** (equivalentes a lo que en la referencia son fotos reales). No reduzcas la cantidad de imágenes previstas para evitar placeholders — al revés: cada placeholder le dice al usuario "acá va una foto que vos vas a insertar". Como heurística mínima: cada overview de campaña debe tener un placeholder hero; cada slide de top tópicos / top items debe tener un placeholder por item; cada card de análisis / driver debe tener su placeholder; cada breakdown por red social debe tener placeholder de post representativo.

Para **assets de marca Corona** (logos, productos, texturas, keyvisuals) → usar el catálogo de `references/assets/` descrito arriba, nunca un placeholder.

Para **imágenes de contenido** (fotos de personas, lugares, situaciones, ambientes, datos de performance con fotos de campañas, etc.) → la skill **no tiene un repositorio** de fotografía genérica de la marca. En esos casos, dejá un **placeholder gris** con la leyenda `[Inserte imagen]` centrada y, **cuando puedas inferir qué iría ahí a partir del brief**, agregá una recomendación muy breve del contenido entre corchetes: `[Inserte imagen · recomendación breve]`.

- Rectángulo (`MSO_SHAPE.RECTANGLE`) con relleno gris neutro `RGBColor(0xD9, 0xD9, 0xD9)` y borde gris medio `RGBColor(0xAA, 0xAA, 0xAA)` de 0.5 pt.
  - Este gris es la única excepción a la regla de "solo colores de la paleta" y existe exclusivamente para marcar placeholders. Nunca usarlo para textos, fondos de slide ni para elementos de contenido real.
- Texto `[Inserte imagen]` o `[Inserte imagen · <recomendación>]` centrado horizontal y verticalmente, en CoronaHeadline-SemiBold, color `#0C2340`, tamaño proporcional al rectángulo (ej: 14–18 pt para placeholders medianos, 10–12 pt para placeholders chicos en grillas).
- Mayúscula solo en la primera letra: literalmente `[Inserte imagen]`. No `[INSERTE IMAGEN]`, no `[inserte imagen]`, no `[imagen aquí]`, no `[placeholder]`.
- El placeholder respeta los márgenes de la slide y se dimensiona según el espacio asignado a la imagen en la composición (no tiene un tamaño fijo).
- No agregar sombras, degradados ni íconos dentro del placeholder: es un rectángulo gris plano con la leyenda.

### Recomendación breve dentro del placeholder

Cuando el contexto del slide deja claro qué foto iría en ese espacio, **sumá una indicación corta al lado del `[Inserte imagen]`** separada por `·`. Es una pista para la persona que después va a reemplazar el placeholder, no una descripción de diseño.

- Formato: `[Inserte imagen · <recomendación 2–6 palabras>]`.
- Ejemplos:
  - `[Inserte imagen · botella Corona en playa]`
  - `[Inserte imagen · Cande Vetrano en Río]`
  - `[Inserte imagen · Sunset Sessions Salta]`
  - `[Inserte imagen · pieza de la lima TikTok]`
  - `[Inserte imagen · Corona Island vista aérea]`
- Si el slide es genérico y no hay un contenido inferible específico, dejar `[Inserte imagen]` sin sufijo.
- Nunca inventar personas, lugares, fechas o datos que no estén en el brief — la recomendación debe apoyarse solo en lo que dice el contenido del slide o del brief.
- Si el mismo slide tiene varios placeholders equivalentes (grilla de 4 fotos del mismo tipo), está bien repetir la misma recomendación o dejar `[Inserte imagen]` a secas si todos son intercambiables.

**Antes de dejar un placeholder**, revisá si el catálogo tiene un asset que resuelva la necesidad (ej: si la slide necesita "una botella Corona", usá `marca/producto/botella-330ml-foto.png` en lugar de un placeholder; si necesita "el ritual de la lima", usá los assets de botella con lima disponibles). El placeholder es para contenido que el catálogo no cubre: fotos de personas, ambientes, eventos reales, data visualizations externas.

Nunca inventes URLs, descargues imágenes ni intentes generar fotografía sintética para reemplazar un placeholder. El placeholder queda como está y el usuario inserta la imagen final manualmente.

## Logos — usar el catálogo

El catálogo `references/assets/` tiene logos oficiales para **cada contexto de marca** (Corona base, Cero, Sunsets, Island, Natural Ice Bar, 100 años, This Is Living). Elegí la variante correcta:

1. **Identificar el contexto** del brief (marca base vs sub-plataforma vs sub-contexto como olímpicos / world tour).
2. **Leer el README** de la carpeta correspondiente.
3. **Elegir la variante por fondo**: cada contexto tiene versiones para fondos claros (azul / color) y oscuros (blanco / blanco+amarillo).
4. **Mantener una sola variante** a lo largo de la presentación, cambiando solo si cambia el color de fondo.

### Logos de campaña — archivos y proporciones

Usar **siempre** la proporción real de cada imagen para evitar deformaciones. Las dimensiones exactas de cada archivo:

| Contexto / campaña | Archivo recomendado (fondo azul) | Dimensiones | Ratio w/h | Fondo transparente |
|---|---|---|---|---|
| **Marca Corona base / Naturals** | `marca/logo/corona-logo-white-yellow.png` | 440×266 px | 1.654 | ✓ |
| **Corona Cero** | `corona-cero/logo/corona-cero-logo-white.png` | 1719×1068 px | 1.610 | ✓ |
| **Corona Sunsets / Exp. Sunset** | `corona-sunsets/logo/corona-sunset-sessions-logo-white-yellow.png` | 2430×2071 px | 1.173 | ✓ |
| **This Is Living** | `this-is-living/corona-this-is-living-lockup-white.png` | 6390×3125 px | 2.045 | ✓ |
| **This Is Living (solo tagline)** | `this-is-living/this-is-living-tagline-clean-white.png` | 10453×2289 px | 4.567 | ✓ |

> ⚠️ **Logo con fondo bakeado**: `corona-sunsets/logo/corona-sunsets-logo-fade.png` tiene fondo gris sólido (#D3D3D3) — **no usarlo** sobre fondos de color. Usar en su lugar `corona-sunset-sessions-logo-white-yellow.png`.

Calcular siempre la altura del placeholder de imagen a partir del ancho y el ratio:
```python
logo_h = int(logo_w / ratio)  # ratio = w/h de la tabla arriba
```

Si el usuario pide un logo que no está en el catálogo (ej: una campaña puntual, un co-brand específico), pedile que te adjunte el archivo oficial y usalo tal cual — nunca recolorear ni redibujar un logo Corona.

## Cómo trabajar cada pedido

1. **Entender el objetivo, la audiencia y la información**. Si el brief es escaso, desarrollá la mejor narrativa posible con lo que hay. Solo pedí aclaraciones cuando sean imprescindibles para poder continuar.
2. **Lectura visual OBLIGATORIA de LAS 45 slides de referencia** (`references/presentacion-referencia/slides/slide-01.png` a `slide-45.png`). Usá la herramienta Read sobre todas ellas al inicio — o al menos una muestra densa de 20+ bien distribuidas (no las primeras tres nada más, no solo separadores, no solo slides de datos). No es opcional — saltarse este paso produce de forma predecible: todo azul, sin placeholders, botella siempre del mismo color, logos de sub-campañas ausentes. No vas a copiar las slides, pero mirarlas a todas te calibra densidad, ritmo, mezcla de fondos, y composiciones típicas.
3. **Recorrido obligatorio del catálogo de assets antes de generar nada** (ver sección dedicada abajo). Identificar qué campañas, sub-plataformas y productos aparecen en el brief, abrir `references/assets/` y listar los assets concretos que son relevantes para la ejecución del momento. **Cada campaña del brief debe mapear a su logo oficial** y el logo debe entrar al menos en el separador + overview de la sección correspondiente. Este paso se hace **antes** de escribir la primera slide, no durante.
4. **Organizar una narrativa clara** antes de diseñar: idea principal, apertura, cierre, qué merece énfasis.
5. **Decidir libremente** cuántas slides hacen falta, cómo dividir el contenido, qué composición usa cada slide y qué recursos visuales aportan — incluyendo activamente los assets relevantes identificados en el paso 3.
6. **Diseñar cada slide** buscando una sola idea principal, jerarquía visual clara y variedad entre slides (no repetir la misma estructura en serie salvo que la información sea en sí una serie — fases, países comparados, meses consecutivos, etc.). **Alterná conscientemente fondos blancos (slides de datos) con fondos Corona Blue (separadores / visuales / statements)**. Un deck Corona 100% azul nunca es correcto; tampoco uno 100% blanco.
7. **Aplicar los elementos de marca obligatorios** (logo + bandera arriba a la derecha con variante según fondo, silueta de botella abajo a la izquierda con variante según fondo) en cada slide a medida que la vas armando — no dejarlo para el final. La botella es blanca sobre fondos oscuros y azul sobre fondos claros — mismo criterio que el logo Corona.

### Recorrido inicial del catálogo (paso 3 en detalle)

Antes de generar la presentación, **recorré el catálogo de `references/assets/` y armá tu propia lista corta de assets relevantes para este brief.** Esto evita que "descubras" un asset útil recién al final (cuando el deck ya está armado) y evita dejar placeholders donde el catálogo sí tenía el recurso.

El procedimiento:

1. **Identificar los contextos/campañas/productos mencionados en el brief.** Ej: "sentiment de This Is Living, Sunsets, Corona Cero y Corona Island" → contextos: marca base + TIL + Sunsets + Cero + Island.
2. **Para cada contexto, abrir su carpeta en `references/assets/` y leer el `README.md`.** No basta con mirar los nombres de archivo — el README explica cuándo usar cada variante y qué restricciones tiene (fondos, co-brands autorizados, etc.).
3. **Anotar los assets concretos que planeás usar** (ruta, dimensiones/ratio, variante clara/oscura según el fondo de slide donde van) y en qué slides irían. Si hay más de una variante para el mismo asset, elegir una y sostenerla a lo largo del deck.
4. **Marcar qué contenido queda cubierto por el catálogo vs. qué requerirá placeholders.** Los placeholders son para fotos que el catálogo no cubre (personas, eventos, ambientes reales); los assets del catálogo cubren logos, productos y texturas.
5. **Recién con esa lista cerrada, empezar a diseñar.**

Si una campaña aparece en el brief, es prácticamente seguro que su logo oficial debe aparecer en el deck (al menos en la portada o slide de apertura de su sección). Si un producto específico se discute (Corona Cero, Corona Open Lid, botella 330ml, lata 473cc), el asset del producto correspondiente también entra. Cuando dudes sobre si un asset "corresponde", el default es usarlo — subuso del catálogo es un error más común que sobreuso.
8. **Revisar visualmente** toda la presentación antes de entregar y corregir cualquier problema evidente.

## Layouts validados de la referencia (medidas exactas)

Los siguientes layouts fueron extraídos y validados directamente del deck fuente que generó `references/presentacion-referencia/slides/`. Cuando el contenido encaja en estos patrones, **usar estas medidas exactas en EMU** — no aproximar.

### Separador de sección (slides 2, 6, 9, 41, 44 de la referencia)

Slide de ritmo entre capítulos. Usa estas propiedades siempre:

- **Fondo**: `#0C2340` (Corona Blue)
- **Text box de contenido** (posición exacta):
  - `x=1_463_040, y=2_614_104, w=9_271_896, h=1_618_488` (EMU)
  - Equivale a ~(1.60", 2.86", 10.14", 1.77")
  - Texto en `#FFC72C`, 36 pt, **no bold**
  - Formato: línea 1 = categoría (ej: `"CAMPAÑAS"`), línea 2 = subtítulo (ej: `"CORONA 2026"`)
- Brand lockup (`dark=True`) + silueta de botella + footer de marca

```python
# Patrón completo de separador de sección
def slide_sep(prs, line1, line2):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    # fondo azul
    bg = s.background.fill; bg.solid(); bg.fore_color.rgb = RGBColor(0x0C,0x23,0x40)
    # texto central — posición exacta de la referencia
    tb = s.shapes.add_textbox(Emu(1_463_040), Emu(2_614_104), Emu(9_271_896), Emu(1_618_488))
    tf = tb.text_frame; tf.word_wrap = True
    for i, line in enumerate([line1, line2]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = line
        r.font.name = FONT_DISPLAY; r.font.size = Pt(36)
        r.font.bold = False; r.font.color.rgb = RGBColor(0xFF,0xC7,0x2C)
    brand_lockup(s, dark=True); bottle(s)
```

### Layout 4 columnas — "Growth Bets" (slide 10 de la referencia)

Slide de comparación de 4 items (campañas, productos, mercados, etc.):

- **Fondo**: `#0C2340` (Corona Blue)
- **Title bar**: `x=1_463_040, y=201_168, w=9_271_896, h=612_648` → texto amarillo, ~28–36 pt
- **Columnas** (x fijos, mismos para las 4):

| Col | x (EMU) | w (EMU) |
|-----|---------|---------|
| 0   | 804_672  | 2_651_760 |
| 1   | 3_556_896 | 2_651_760 |
| 2   | 6_300_096 | 2_651_760 |
| 3   | 9_070_848 | 2_651_760 |

- **Chip de header por columna** (amarillo): `y=832_104, h=612_648`, fill `#FFC72C`, texto azul 13–16 pt
- **Placeholder de imagen**: `y=1_517_904, h=3_666_744`, fill `#D9D9D9`, stroke `#AAAAAA`
- **Texto descriptivo**: `y=5_257_800, h=694_944`, blanco, 10–11 pt
- **Chip KPI** (azul oscuro): `y=6_025_896, h=457_200`, fill `#0E3660`≈`#182F4C`, texto amarillo 10 pt bold

```python
COL4_X = [Emu(804_672), Emu(3_556_896), Emu(6_300_096), Emu(9_070_848)]
COL4_W = Emu(2_651_760)
# Para cada columna i:
cx = COL4_X[i]
# 1. chip de header
box(s, cx, Emu(832_104), COL4_W, Emu(612_648), fill=YELLOW)
# 2. placeholder de imagen
ph(s, cx, Emu(1_517_904), COL4_W, Emu(3_666_744), "[Inserte imagen]", size=10)
# 3. descripción
txt(s, cx, Emu(5_257_800), COL4_W, Emu(694_944), "...", size=10, color=WHITE)
# 4. chip KPI
box(s, cx, Emu(6_025_896), COL4_W, Emu(457_200), fill=RGBColor(0x18,0x2F,0x4C))
```

### Barra de capítulo (chapter bar)

Barra full-width en el tope de slides de datos. **Regla crítica**: la barra **NO debe llegar hasta el borde derecho** — el lockup de logo + bandera Argentina ocupa ~1.86" a la derecha. Si la barra cubre esa área, tapa u oscurece el lockup.

```python
BAR_H = Emu(329_184)   # 0.36"
BAR_W = SW - Emu(1_700_000)   # deja ~1.86" libres para el lockup
box(s, 0, 0, BAR_W, BAR_H, fill=BLUE)
# Texto izquierdo
txt(s, Emu(200_000), 0, Emu(6_000_000), BAR_H, left_text, size=10, bold=True, color=WHITE)
# Texto derecho — alineado al límite de la barra, NO a SW
if right_text:
    txt(s, BAR_W - Emu(4_200_000), 0, Emu(4_050_000), BAR_H,
        right_text, size=10, color=WHITE, align=PP_ALIGN.RIGHT)
```

### Placeholder con texto superpuesto (cards de campaña)

Cuando una card necesita mostrar tanto una imagen como datos encima, usar este patrón:

1. **Fondo gris** = placeholder de imagen (z-order base, toda la card)
2. **Banner azul superior** = nombre de campaña / título (superpuesto)
3. **Banner azul inferior** = valor / cifra / KPI (superpuesto)
4. **`[Inserte imagen]`** centrado en el área gris media (entre los dos banners)

```python
CARD_TOP_H = Emu(400_000)   # alto del banner superior
CARD_BOT_H = Emu(640_000)   # alto del banner inferior

# 1. fondo gris placeholder (full card)
box(s, cx, card_y, card_w, card_h, fill=PH_FILL, stroke=PH_STK, sw=0.5)
txt(s, cx, card_y + CARD_TOP_H, card_w, card_h - CARD_TOP_H - CARD_BOT_H,
    "[Inserte imagen]", size=9, color=DGRAY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 2. banner superior (superpuesto)
box(s, cx, card_y, card_w, CARD_TOP_H, fill=BLUE)
txt(s, cx + Emu(130_000), card_y + Emu(70_000), card_w - Emu(260_000), CARD_TOP_H - Emu(100_000),
    nombre, size=11, bold=True, color=WHITE)

# 3. banner inferior (superpuesto)
box(s, cx, card_y + card_h - CARD_BOT_H, card_w, CARD_BOT_H, fill=BLUE)
txt(s, cx + Emu(130_000), card_y + card_h - CARD_BOT_H + Emu(60_000),
    card_w - Emu(260_000), Emu(380_000), valor, size=20, bold=True, color=YELLOW)
```

## Slides estructurales

Diseñá desde cero, con criterio propio y manteniendo consistencia entre sí:

- **Portada**: título, subtítulo/bajada, fecha o contexto si corresponde. Tono sobrio; Corona Blue como fondo + texto blanco, o fondo blanco + texto Corona Blue, con un acento amarillo (barra, cifra, ícono).
- **Agenda / índice**: enumeración clara de secciones.
- **Separadores de sección**: consistentes entre sí, ayudan a marcar el ritmo.
- **Cierre**: agradecimiento, contacto o call to action.

Estas slides deben compartir un lenguaje visual común (mismos colores base, mismo tratamiento tipográfico, mismos márgenes) para que la presentación se sienta unificada.

## Slides de contenido (diseñar libremente)

No hay layouts predefinidos. Diseñá cada slide desde cero según lo que necesite comunicar.

### Altura máxima de la sección de título

En una slide regular de contenido, la **sección de título completa** — título, bajada, kicker, divisor, franja decorativa y cualquier otro elemento que la componga — **no debe superar 4 cm de alto** (`1_440_000` EMU ≈ 1.575" ≈ 151 px a 96 DPI). El contenido es lo principal; el título ordena y jerarquiza, no protagoniza.

Excepción: cuando el título *es* el mensaje (slide de gran cifra, statement conceptual, quote), puede ocupar más. Justificalo por el contenido, no por default.

### Prioridades visuales

Priorizá siempre:

- claridad
- síntesis
- storytelling
- jerarquía visual
- facilidad de lectura
- una idea principal por slide

**Evitá bloques largos de texto.** Cuando aporte claridad, transformá la información en recursos visuales: diagramas, esquemas, procesos, timelines, comparaciones, iconografía, destacados, cifras clave, tablas, gráficos.

El texto debe **sintetizar y acompañar** la idea visual, no ocupar la mayor parte de la slide.

### Diagramas y recursos visuales

**Priorizá siempre diagramas expresivos sobre rectángulos con texto adentro.** Cuando la información tenga estructura, mostrá esa estructura visualmente. Antes de conformarte con "bullets" o "cards" rectangulares, preguntate qué tipo de relación hay entre los elementos y elegí el diagrama que la represente:

| Tipo de relación | Diagrama sugerido |
|---|---|
| Secuencia / etapas / fases | Chevrons encadenados, timeline horizontal, flujo con conectores |
| Intersección / overlap entre grupos | Diagrama de Venn (círculos con transparencia) |
| Jerarquía / composición | Pirámide, árbol, organigrama, treemap |
| Comparación de opciones | Matriz 2×2, tabla con íconos, columnas paralelas |
| Reducción / embudo | Funnel de bloques que decrecen |
| Ciclo / iteración | Círculo con flechas curvas conectando pasos |
| Causa → efecto / flujo | Cajas conectadas con flechas explícitas |
| Distribución / partes de un todo | Donut, pie, barras apiladas al 100% |
| Radial / ejes | Radar, dispersión con cuadrantes nombrados |

Construí los diagramas con las primitivas de python-pptx (`add_shape`, `add_connector`, superposición con transparencia para Venn). Adaptá los colores a la paleta Corona (Blue, White, Yellow) y respetá el contraste del texto sobre cada bloque. Nunca introduzcas un cuarto color.

## Datos y gráficos

- Si hay datos numéricos y una visualización ayuda a comprenderlos, elegí libremente el tipo de gráfico más adecuado (barras, líneas, scatter, composición, etc.).
- **NO usar `add_chart` de python-pptx.** `add_chart` embebe archivos `.xlsx` dentro del PPTX; PowerPoint requiere entradas `Override` explícitas para esos embebidos o muestra el diálogo de reparación y descarta los datos — ese bug persiste incluso con `fix_content_types`. La solución definitiva es **no usar `add_chart`** y construir todos los gráficos como rectángulos proporcionales con XML directo (ver `references/layouts.md`).
- **Nunca generar gráficos como imagen** (matplotlib, SVG/PNG) salvo que sea un caso absolutamente excepcional y se documente.
- Paleta de gráficos: Corona Blue + Corona Yellow como colores principales; White para contraste. Para más de 2 series, componer variantes con transparencia calculada (ver colores compuestos en `references/layouts.md`).
- **Validación de porcentajes**: si un gráfico representa una distribución que debe sumar 100%, verificá que sume exactamente 100 (±0.5 por redondeo) antes de entregar.

### Insights sobre datos

Cuando una slide contiene datos numéricos, evaluá si hay un hallazgo relevante que destacar: diferencia marcada entre categorías, concentración inesperada, valor que sobresale, tendencia. Si lo hay, agregá un finding breve y concreto — una línea, dos como máximo — en la misma slide, cerca del gráfico o en una posición jerárquicamente secundaria.

No inventes insights: solo señalar lo que los datos muestran objetivamente. Si no hay nada llamativo, no agregues nada.

### Densidad y agrupación de gráficos

**Un gráfico simple no merece una slide entera.** Antes de asignar una slide exclusiva a un gráfico, evaluá su complejidad y peso informativo. Un gráfico con pocas categorías o series (ej: 2 barras, un donut sí/no, una sola línea temporal) es de baja densidad y debe agruparse con otros datos relacionados en la misma slide.

## Reglas de contenido

- No inventes hechos, cifras ni información que no estén en el brief o los materiales aportados.
- Cuando el usuario aporte información suficiente, **desarrollala y estructurala**, no la copies textual.
- Si falta algo puntual imprescindible, preguntá; si no, avanzá.

## Márgenes

Los bordes izquierdo y derecho de cada slide deben ser iguales. Definí un margen horizontal (ej: `457_200` EMU ≈ 0,5") y usalo idéntico a ambos lados: el contenido arranca en `left = margen_h` y termina en `left + width = slide_width - margen_h`. Aplica a cualquier bloque de contenido (texto, imágenes, gráficos, tablas, diagramas). Única excepción: elementos decorativos que intencionalmente sangran al borde (franja de color a un solo lado) — y aun así el contenido interno respeta los márgenes simétricos.

## Entregable

Un archivo `.pptx` completamente editable, guardado en la work folder actual con un nombre descriptivo (ej: `presentacion_corona_<tema>_<YYYY-MM-DD>.pptx`).

Antes de entregar, revisá toda la presentación y corregí:

- slides sin el lockup **logo Corona + bandera Argentina** en la esquina superior derecha (es obligatorio salvo justificación; si falta, agregalo)
- variante incorrecta del logo Corona en el lockup (fondo oscuro con logo oscuro, o viceversa) — chequear contraste en cada slide
- bandera Argentina modificada, recortada, en formato rectangular en vez de circular, o cambiada por otra bandera
- slides con espacio libre abajo a la izquierda que no tienen la silueta de botella (si hay lugar, va)
- lockup o silueta tapando contenido / superpuestos a texto o gráficos (si tapan, reacomodar contenido antes de omitir el elemento de marca)
- texto cortado o desbordado
- elementos superpuestos accidentalmente
- contenido fuera del área de la slide
- gráficos o tablas que no se vean completos
- problemas de legibilidad o contraste
- placeholders de imagen sin la leyenda `[Inserte imagen]` o con texto de ejemplo residual
- placeholders de imagen cuyo contenido sería claramente inferible del brief pero que no llevan recomendación (`[Inserte imagen · <recomendación>]`) — si la ejecución cae en genérico, revisar si corresponde agregar la pista
- slides que "necesitaban" fotos y quedaron sin placeholders (probablemente faltan — la referencia usa muchas fotos, la skill las sustituye por placeholders)
- placeholders gris usados donde en realidad había un asset del catálogo (botella, logo, textura) que resolvía la necesidad — revisar el catálogo antes de dejar un placeholder
- campañas / productos que aparecen en el brief pero cuyo asset oficial (logo, botella, lata, textura) no aparece en ninguna slide — probablemente faltó el recorrido inicial del catálogo
- logos / assets mezclando contextos distintos (ej. logo Corona regular + tagline Sunsets en la misma slide sin justificación)
- anillos olímpicos presentes sin autorización del partnership (ver `corona-cero/olimpicos/README.md`)
- assets modificados (recoloreados, rotados, recortados fuera de su proporción original, con filtros)
- cualquier color que no sea `#0C2340`, `#FFFFFF`, `#FFC72C`, o `#A8BD1C` en contextos Lime (o el gris `#E6E6E6` reservado exclusivamente para placeholders de imagen)
- Corona Lime usado fuera de contextos Lime Ritual / Open Lid / Cero Lime
- Corona Lime + Corona Yellow actuando como dos acentos distintos en la misma slide
- bordes izquierdo y derecho asimétricos (deben tener el mismo margen)
- porcentajes de una distribución que no sumen 100
- slides con fondo totalmente amarillo o totalmente lima (prohibido)
- texto amarillo sobre fondo blanco (prohibido, no contrasta)
- sección de título de una slide de contenido regular que supere 4 cm de alto sin justificación
- text boxes con `word_wrap` no seteado a `True` (causa texto vertical o desbordes)
- copia textual de slides de la referencia (`references/presentacion-referencia/slides/`) — la presentación generada debe ser original
- deck generado sin haber leído las 45 imágenes de referencia al inicio (o al menos una muestra densa de 20+) — ver "OBLIGATORIO: ver TODAS las imágenes antes de diseñar"
- **deck con el 100% (o casi) de las slides en fondo Corona Blue** — la referencia alterna fondo blanco (slides de datos) con azul (separadores / visuales). Si tu output tiene todo azul, probablemente no miraste `slide-03.png`, `slide-07.png`, `slide-11.png`, `slide-12.png`, `slide-17.png`, `slide-27.png`, `slide-45.png`.
- **silueta de botella en el mismo color en todo el deck** — tiene que alternar: blanca sobre fondos oscuros, azul sobre fondos claros. Si tenés slides con fondo blanco y mirás abajo a la izquierda y la botella es blanca (invisible), estás usando la variante equivocada.
- **sub-campañas del brief con asset disponible en el catálogo que no aparecen con su logo oficial en el deck** — chequear primero si el asset existe en `references/assets/<contexto>/`; si existe, debe aparecer al menos en el separador + overview de esa sección. Si la sub-campaña no tiene asset en el catálogo, texto plano está bien.
- **deck sin ningún `[Inserte imagen]`** — es casi siempre un bug. Volvé a revisar overviews de campaña, top items, drivers, breakdown por red social: todos deberían tener placeholders. La skill considera los placeholders parte del deliverable, no un recurso de último recurso.

Al final, mostrá el archivo al usuario con `mcp__tas__open_file`.

## Guía técnica de implementación

Ver especificaciones completas en `references/layouts.md`. Los puntos obligatorios están resumidos abajo — son innegociables independientemente de lo que lea o no de ese archivo.

### Setup obligatorio

```python
# Crear desde cero, nunca abrir un archivo base
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width  = 12192000  # 16:9
prs.slide_height = 6858000

COLORS = {
    "corona_blue":   RGBColor(0x0C, 0x23, 0x40),
    "white":         RGBColor(0xFF, 0xFF, 0xFF),
    "corona_yellow": RGBColor(0xFF, 0xC7, 0x2C),
    "corona_lime":   RGBColor(0xA8, 0xBD, 0x1C),  # solo contextos Lime Ritual / Open Lid / Cero Lime
}
PLACEHOLDER_FILL   = RGBColor(0xD9, 0xD9, 0xD9)   # igual al gris de referencia
PLACEHOLDER_STROKE = RGBColor(0xAA, 0xAA, 0xAA)
```

Usar siempre el layout blank: `prs.slide_layouts[6]` (o el más vacío disponible). Nunca heredar composición de un layout con contenido.

### OBLIGATORIO: enfoque de generación sin `add_chart`

**El método recomendado es XML directo + zipfile, NO python-pptx + `add_chart`.**

`add_chart` embebe archivos `.xlsx` que PowerPoint requiere con `Override` explícitos en `[Content_Types].xml`. Aunque `fix_content_types` agrega esos overrides, PowerPoint sigue mostrando el diálogo de reparación en versiones recientes. La solución definitiva es **no generar ningún objeto chart**: construir todos los gráficos como rectángulos proporcionales con XML DrawingML, ensamblar el PPTX directamente como zip, y reemplazar solo las slides manteniendo el master/layouts de un template existente.

Ver el patrón completo de implementación en `references/layouts.md`.

```python
# Flujo general correcto:
# 1. Abrir template como zip (para copiar master/layouts/tema)
# 2. Construir cada slide como XML string con helpers txt_box(), rect_sh(), pic_xml()
# 3. Construir gráficos con rectángulos: stacked_columns(), bars_h_simple(), etc.
# 4. Ensamblar el nuevo zip copiando todo del template excepto slides/charts/embeddings
# 5. Escribir nuevas slides + rels + presentation.xml + Content_Types.xml
# 6. Resultado: 0 xlsx embebidos → 0 diálogo de reparación
```

Si por alguna razón excepcional se usa python-pptx + `add_chart`, **sí** llamar `validar_presentacion(prs)` antes de `prs.save()` y `fix_content_types(output_path)` después — pero aún así puede fallar. El código de ambas funciones está en `references/layouts.md`.

La función `validar_presentacion` corrige:

```python
from lxml import etree

def validar_presentacion(prs):
    """
    Corrige:
    1. IDs duplicados por slide
    2. Relaciones de imágenes huérfanas
    3. Placeholders vacíos residuales
    4. Conectores con índices de conexión fuera de rango
    5. Series de gráficos con valores None/NaN
    6. Axis IDs negativos (overflow de int32 → xsd:unsignedInt inválido)
    7. Doble c:marker en series de lineChart (viola maxOccurs=1)
    8. c:spPr fuera de orden en series de barChart
    9. numFmt incorrecto en dLbls de donut/pie con showPercent
   10. Orientación de eje de categorías invertida en barras horizontales
    """
    NSMAP_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
    DML_NS  = "http://schemas.openxmlformats.org/drawingml/2006/main"
    DML_C_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"

    for slide_idx, slide in enumerate(prs.slides):
        spTree = slide.shapes._spTree
        ids_vistos = set()
        next_id = 1000 + slide_idx * 100

        # 1. IDs únicos
        for el in spTree.iter():
            id_attr = el.get("id")
            if id_attr is not None:
                id_int = int(id_attr)
                if id_int in ids_vistos:
                    next_id += 1
                    el.set("id", str(next_id))
                    ids_vistos.add(next_id)
                else:
                    ids_vistos.add(id_int)

        # 2. Relaciones huérfanas
        rids_en_xml = set()
        for el in spTree.iter():
            for attr in el.attrib.values():
                if attr.startswith("rId"):
                    rids_en_xml.add(attr)
        rids_validos = set(slide.part.rels.keys())
        for el in list(spTree.iter()):
            for attr_val in el.attrib.values():
                if attr_val in (rids_en_xml - rids_validos):
                    parent = el.getparent()
                    if parent is not None:
                        parent.remove(el)
                    break

        # 3. Placeholders vacíos residuales
        ns = f"{{{NSMAP_P}}}"
        for sp in list(spTree.findall(f".//{ns}sp")):
            ph = sp.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}ph")
            if ph is not None:
                txBody = sp.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}txBody")
                if txBody is not None:
                    texto = "".join(t.text or "" for t in txBody.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"))
                    if not texto.strip():
                        sp.getparent().remove(sp)

        # 4. Conectores con idx fuera de rango
        for cxn in spTree.iter(f"{{{DML_NS}}}cxnSp"):
            for pt in list(cxn.iter(f"{{{DML_NS}}}stCxn")) + list(cxn.iter(f"{{{DML_NS}}}endCxn")):
                try:
                    if int(pt.get("idx", "0")) > 8:
                        pt.set("idx", "0")
                except (ValueError, TypeError):
                    pt.set("idx", "0")

    # 5. Valores None/NaN en series
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                for series in shape.chart.series:
                    try:
                        series.values  # fuerza lectura; errores se ignoran
                    except Exception:
                        pass

    # 6. Axis IDs negativos
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                for ax_id_el in shape.chart._part._element.iter(f"{{{DML_C_NS}}}axId"):
                    val = ax_id_el.get("val")
                    if val and int(val) < 0:
                        ax_id_el.set("val", str(int(val) + 2**32))

    # 7. Doble c:marker en lineChart
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                for ser in shape.chart._part._element.iter(f"{{{DML_C_NS}}}ser"):
                    markers = list(ser.findall(f"{{{DML_C_NS}}}marker"))
                    if len(markers) < 2:
                        continue
                    keep = next((m for m in markers if (m.find(f"{{{DML_C_NS}}}symbol") is None or m.find(f"{{{DML_C_NS}}}symbol").get("val") != "none")), markers[-1])
                    children = {tag: ser.find(f"{{{DML_C_NS}}}{tag}") for tag in ["idx","order","tx","spPr","cat","val","smooth"]}
                    for child in list(ser): ser.remove(child)
                    for tag in ["idx","order","tx","spPr"]:
                        if children[tag] is not None: ser.append(children[tag])
                    ser.append(keep)
                    for tag in ["cat","val","smooth"]:
                        if children[tag] is not None: ser.append(children[tag])

    # 8. c:spPr fuera de orden en barChart
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                for barChart in shape.chart._part._element.iter(f"{{{DML_C_NS}}}barChart"):
                    for ser in barChart.findall(f"{{{DML_C_NS}}}ser"):
                        tags = [c.tag.split("}")[1] for c in ser]
                        if "spPr" not in tags or "dLbls" not in tags:
                            continue
                        if tags.index("spPr") >= tags.index("dLbls"):
                            children = {tag: ser.find(f"{{{DML_C_NS}}}{tag}") for tag in ["idx","order","tx","spPr","dLbls","cat","val"]}
                            for child in list(ser): ser.remove(child)
                            for tag in ["idx","order","tx","spPr","dLbls","cat","val"]:
                                if children[tag] is not None: ser.append(children[tag])

    # 9. numFmt incorrecto en donut/pie con showPercent
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                for dlbls in shape.chart._part._element.iter(f"{{{DML_C_NS}}}dLbls"):
                    sp = dlbls.find(f"{{{DML_C_NS}}}showPercent")
                    if sp is not None and sp.get("val") in ("1", "true"):
                        nf = dlbls.find(f"{{{DML_C_NS}}}numFmt")
                        if nf is not None and nf.get("formatCode") == '0"%"':
                            nf.set("formatCode", "0%")
                            nf.set("sourceLinked", "0")

    # 10. Orientación de eje en barras horizontales
    from lxml import etree as ET
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                for bar_chart in shape.chart._part._element.iter(f"{{{DML_C_NS}}}barChart"):
                    bd = bar_chart.find(f"{{{DML_C_NS}}}barDir")
                    if bd is None or bd.get("val") != "bar":
                        continue
                    for cat_ax in shape.chart._part._element.iter(f"{{{DML_C_NS}}}catAx"):
                        scaling = cat_ax.find(f"{{{DML_C_NS}}}scaling")
                        if scaling is None:
                            scaling = ET.SubElement(cat_ax, f"{{{DML_C_NS}}}scaling")
                        ori = scaling.find(f"{{{DML_C_NS}}}orientation")
                        if ori is None:
                            ori = ET.SubElement(scaling, f"{{{DML_C_NS}}}orientation")
                        if ori.get("val") != "maxMin":
                            ori.set("val", "maxMin")

    return prs
```

`fix_content_types` agrega `Override` explícitos en `[Content_Types].xml` para los xlsx embebidos de gráficos (sin esto PowerPoint repara y descarta los datos):

```python
import zipfile, os
from lxml import etree as lxml_etree

def fix_content_types(output_path):
    CT_NS   = "http://schemas.openxmlformats.org/package/2006/content-types"
    XLSX_CT = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    tmp_path = output_path + ".ct_fix.tmp"
    with zipfile.ZipFile(output_path, "r") as zin:
        xlsx_parts = sorted([n for n in zin.namelist() if n.startswith("ppt/embeddings/") and n.endswith(".xlsx")])
        if not xlsx_parts:
            return
        with zin.open("[Content_Types].xml") as f:
            ct_root = lxml_etree.fromstring(f.read())
        existing = {el.get("PartName", "") for el in ct_root}
        added = 0
        for part in xlsx_parts:
            pn = "/" + part
            if pn not in existing:
                el = lxml_etree.SubElement(ct_root, f"{{{CT_NS}}}Override")
                el.set("PartName", pn)
                el.set("ContentType", XLSX_CT)
                added += 1
        if added == 0:
            return
        fixed_ct = lxml_etree.tostring(ct_root, xml_declaration=True, encoding="UTF-8", standalone=True)
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                zout.writestr(item, fixed_ct if item.filename == "[Content_Types].xml" else zin.read(item.filename))
    os.replace(tmp_path, output_path)
```

## Sources of truth

- El brief y los materiales aportados por el usuario son la fuente de contenido de cada slide.
- Esta `SKILL.md` + `references/layouts.md` definen la identidad visual: paleta Corona (`#0C2340` / `#FFFFFF` / `#FFC72C`, `#A8BD1C` condicional) y tipografía (`CoronaHeadline-SemiBold` como fuente base, `CoronaBrush-Bold` para display — archivos en `references/fonts/`).
- `references/presentacion-referencia/slides/` contiene 45 PNGs (`slide-01.png`–`slide-45.png`) de una presentación real de la marca — se usan como **inspiración visual**, no como template. Cargarlas con Read antes de diseñar (ver "Cómo trabajar cada pedido" paso 2). La presentación generada debe ser original.
- `references/assets/` es el catálogo de assets gráficos oficiales (logos, bandera, productos, texturas, keyvisuals), organizado por contexto. Cada subcarpeta tiene su propio `README.md` con las reglas específicas — leerlos antes de usar los archivos.
- Si el usuario no aporta suficiente contenido para un slide, pedirle que lo complete antes de continuar. Si el catálogo no cubre un asset específico que el brief requiere, pedirle el archivo oficial — nunca inventarlo ni recrearlo con shapes.

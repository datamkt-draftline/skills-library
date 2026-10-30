---
name: Presentación BU LAS + FNC
description: Genera una presentación PowerPoint (.pptx) editable con la identidad visual BU LAS + FNC Uruguay a partir de un brief, información o archivos aportados por el usuario.
---

# Presentación BU LAS + FNC

Usá esta skill cuando el usuario pida armar una presentación para BU LAS o FNC Uruguay, o cuando adjunte materiales para transformar en slides. El objetivo es entregar un `.pptx` editable, claro, profesional y visualmente consistente con la identidad BU LAS + FNC.

## Principio general

**La identidad visual está definida en esta skill (paleta, tipografía, logos). El contenido define el diseño de cada slide.**

No existe un catálogo cerrado de layouts de contenido. Diseñá cada slide libremente y desde cero según lo que necesite comunicar, aplicando siempre las reglas de identidad de marca descritas abajo.

## Archivos de referencia

Todos los archivos necesarios se encuentran en **la misma carpeta que este SKILL.md** (`.claude/skills/presentacion-bu-las-cmq/`). Para construir el script Python, usar rutas absolutas resolviendo esa carpeta en tiempo de ejecución:

```python
import os
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
# ejemplo: ruta_logo = os.path.join(SKILL_DIR, "LOGO BU LAS_Negro&Color.png")
```

- `manual-de-marca.md` — guía de identidad visual BU LAS: paleta completa (principal, secundaria, terciaria), escala tipográfica, reglas de contraste ADA, elementos gráficos de texto y reglas de logo. **Usá este archivo solo para extraer paleta, tipografía y estilo. Ignorá absolutamente todos los logos, ejemplos y aplicaciones de otros países**; los únicos logos válidos son BU LAS y FNC (listados abajo).
- Fuentes Avantt: `Avantt-Bold.ttf`, `Avantt-SemiBold.ttf`, `Avantt-Regular.ttf`, `Avantt-Light.ttf`.
- Logos oficiales — **solo estos dos, nunca logos de otros países**:
  - BU LAS: `LOGO BU LAS_Negro&Color.png`, `LOGO BU LAS_Blanco&Color.png` (versiones con círculo dorado, **priorizar siempre estas**), `LOGO BU LAS_Negro.png`, `LOGO BU LAS_Blanco.png` (solo si el fondo o el contraste hacen imposible usar la versión con color).
  - FNC: `Logo_FNC_Primario_Negro.png`, `Logo_FNC_Primario_Blanco.png`.
  - **Prohibido usar logos de cualquier otro país o BU regional.** Aunque el manual de marca los incluya como ejemplos, no forman parte de esta presentación.

### Regla obligatoria de logos en cada slide

**Todas las slides — sin excepción — deben incluir ambos logos (BU LAS + FNC), uno al lado del otro, en una esquina.**

- Los dos logos van juntos, en la misma esquina, con la separación y tamaños exactos definidos abajo. Mantenelos iguales en toda la presentación. No los muevas de slide a slide.

**Tamaños exactos (96 DPI, slide 1280×720 px / 12192000×6858000 EMU):**

| Logo | px | pulgadas | EMU |
|---|---|---|---|
| BU LAS | 147 × 62 px | 1,53" × 0,65" | 1 400 175 × 590 550 |
| FNC | 91 × 62 px | 0,95" × 0,65" | 866 775 × 590 550 |
| Separación entre logos | 21 px | 0,22" | 199 925 |

Ambos logos comparten la misma altura (62 px / 590 550 EMU), alineados verticalmente al centro.
- **No modificar los logos**: no recolorear, no distorsionar, no recortar, no aplicar sombras, no rotarlos, no cambiar proporciones. Se usan tal cual vienen los archivos.
- Elegí la versión (blanco / negro) de cada logo según el fondo de la slide, siguiendo las reglas de contraste del manual:
  - Fondo claro (blanco, gris claro, amarillo BU LAS) → versiones en negro (`LOGO BU LAS_Negro&Color.png` + `Logo_FNC_Primario_Negro.png`).
  - Fondo oscuro (negro, colores oscuros de acento) → versiones en blanco (`LOGO BU LAS_Blanco&Color.png` + `Logo_FNC_Primario_Blanco.png`).
- Para BU LAS **priorizar siempre las versiones con el círculo dorado** (`Negro&Color` / `Blanco&Color`). Usar las versiones planas solo si el color no contrasta con el fondo.
- **Bordes del asset PNG tocando el borde de la slide**: para liberar la mayor cantidad de espacio útil, el bounding box del archivo PNG debe estar pegado a los bordes de la slide en la esquina elegida (top-left = `(0, 0)`, top-right = `(slide_width - w, 0)`, bottom-left = `(0, slide_height - h)`, bottom-right = `(slide_width - w, slide_height - h)`). El PNG ya trae su propio padding transparente alrededor del logo, así que pegar el asset al borde deja al logo visualmente separado sin desperdiciar área. No agregar margen adicional entre el borde del PNG y el borde de la slide.
- **No superposición con contenido**: aunque el logo esté al borde, verificar activamente que ningún otro elemento (texto, imagen, gráfico, tabla, forma) invade el rectángulo ocupado por los dos logos + su separación. Registrar la zona de logos como "ocupada" en la lista de rectángulos desde el inicio y planificar el contenido para no cruzarla. Los logos siempre se agregan al final del script y van al frente en el z-order; si aun así hay superposición, corregir la posición del contenido, no la de los logos.
- La portada puede tener un tratamiento distinto (logos más grandes y centrados si el diseño lo pide), pero **ambos logos deben aparecer igualmente**.

## Identidad visual

- **Formato**: 16:9 widescreen (13.333" × 7.5" / 12192000 × 6858000 EMU).
- **Paleta principal**:
  - Amarillo BU LAS: `#F5DF02` (acento principal), `#E3C120` (amarillo profundo), `#D3A238` (dorado).
  - Neutros: `#010101` (negro), `#FFFFFF` (blanco), `#F2F2F2` (gris claro), `#4D4D4D` (gris oscuro).
  - Acentos secundarios: `#274F31` (verde), `#284F6D` (azul), `#4F4566` (violeta), `#77312C` (bordó), `#594B32` (marrón).
- **Tipografía**: Avantt (Bold/SemiBold para títulos y destacados, Regular para cuerpo, Light para textos de apoyo o cifras grandes). Fallback a Arial si el entorno no tiene Avantt embebida.
- **Contraste**: siempre garantizar legibilidad. Sobre fondos amarillos usar texto negro; sobre fondos oscuros usar blanco. No poner amarillo BU LAS sobre blanco para texto: no cumple contraste.
- **Fondo amarillo total prohibido**: nunca cubrir toda la slide con amarillo BU LAS (`#F5DF02`) ni con sus variantes (`#E3C120`, `#D3A238`). El amarillo se usa como acento, destacado, franja o bloque parcial — no como fondo completo. Los fondos válidos de slide completa son: blanco, gris claro, negro, gris oscuro y los acentos secundarios oscuros (verde, azul, violeta, bordó, marrón).
- **Márgenes simétricos**: los bordes izquierdo y derecho de cada slide deben ser iguales. Definí un margen horizontal (`margen_h`, por ejemplo 457 200 EMU ≈ 0,5") y usalo idéntico a ambos lados: el contenido arranca en `left = margen_h` y termina en `left + width = slide_width - margen_h`. Esta regla aplica a cualquier bloque de contenido (texto, imágenes, gráficos, tablas, diagramas). La única excepción son elementos decorativos que intencionalmente sangran al borde (una franja de color a un solo lado, por ejemplo), y aun así el contenido interno respeta los márgenes simétricos.
- **Logos**: ver la regla obligatoria arriba — ambos logos (BU LAS + FNC) en cada slide, sin modificar, juntos en la misma esquina, respetando contraste y área de reserva.

## Cómo trabajar cada pedido

1. **Entender el objetivo, la audiencia y la información**. Si el brief es escaso, desarrollá la mejor narrativa posible con lo que hay. Solo pedí aclaraciones cuando sean imprescindibles para poder continuar (por ejemplo, no se entiende para quién es o falta un dato clave que el usuario evidentemente tiene).
2. **Organizar una narrativa clara** antes de diseñar: cuál es la idea principal, cómo se abre, cómo se cierra, qué merece énfasis.
3. **Decidir libremente** cuántas slides hacen falta, cómo dividir el contenido, qué composición usa cada slide y qué recursos visuales aportan.
4. **Diseñar cada slide** buscando una sola idea principal, jerarquía visual clara y variedad entre slides (no repetir la misma estructura en serie).
5. **Revisar visualmente** toda la presentación antes de entregar y corregir cualquier problema evidente.

## Slides estructurales

Diseñá desde cero, con criterio propio y manteniendo consistencia entre sí:

- **Portada**: título, subtítulo/bajada, logos BU LAS + FNC, fecha o contexto si corresponde.
- **Agenda / índice**: enumeración clara de secciones.
- **Separadores de sección**: consistentes entre sí, ayudan a marcar el ritmo.
- **Cierre**: agradecimiento, contacto o call to action, con logos.

Estas slides deben compartir un lenguaje visual común (mismos colores base, tratamiento tipográfico, ubicación de logos) para que la presentación se sienta unificada.

## Slides de contenido (diseñar libremente)

No existe un set de layouts predefinidos. Diseñá cada slide desde cero según lo que necesite comunicar.

### Altura máxima de la sección de título

En una slide regular de contenido, la **sección de título completa** — título, bajada, kicker, divisor, franja decorativa y cualquier otro elemento que la componga — **no debe superar 4 cm de alto** (1 440 000 EMU ≈ 1,575" ≈ 151 px a 96 DPI). Medí la altura total desde el borde superior del elemento más alto de la sección hasta el borde inferior del elemento más bajo. El contenido es lo principal de la slide; el título ordena y jerarquiza, no protagoniza.

Excepción: cuando el título *es* el mensaje (slide de gran cifra, statement conceptual, quote), puede ocupar más. Justificalo por el contenido, no por default. En una slide regular con datos, diagrama o lista, respetar los 4 cm.

Priorizá siempre:

- claridad
- síntesis
- storytelling
- jerarquía visual
- facilidad de lectura
- una idea principal por slide

**Evitá bloques largos de texto**. Cuando aporte claridad, transformá la información en recursos visuales:

- diagramas, esquemas, procesos, timelines
- comparaciones, jerarquías visuales
- iconografía, destacados, cifras clave
- tablas, gráficos

El texto debe **sintetizar y acompañar** la idea visual, no ocupar la mayor parte de la slide. Buscá variedad entre slides — con una excepción: si la información **es en sí una serie** (fases de un proceso, países comparados, meses consecutivos, opciones equivalentes, etc.), es correcto y esperable repetir la misma composición en cada slide de esa serie para que la comparación se lea con claridad. La regla es no repetir por default; repetir cuando la información lo justifica sí. No fuerces recursos visuales cuando no aporten valor.

### Diagramas y recursos visuales

**Priorizá siempre diagramas expresivos sobre rectángulos con texto adentro.** Cuando la información tenga estructura, mostrá esa estructura visualmente. Antes de conformarte con "bullets" o "cards" rectangulares, preguntate: ¿qué tipo de relación hay entre estos elementos? y elegí el diagrama que lo represente:

| Tipo de relación | Diagrama sugerido |
|---|---|
| Secuencia / etapas / fases | Flechas encadenadas tipo "stages" (chevrons apuntando a la derecha), timeline horizontal con hitos, flujo con conectores |
| Intersección / overlap entre grupos | Diagrama de Venn (2 o 3 círculos con transparencia) |
| Jerarquía / composición | Pirámide, árbol, organigrama, treemap |
| Comparación de opciones | Matriz 2×2, tabla con íconos, columnas paralelas conectadas |
| Reducción / embudo | Funnel de bloques que decrecen |
| Ciclo / iteración | Círculo con flechas curvas conectando pasos |
| Causa → efecto / flujo | Cajas conectadas con flechas explícitas, no simplemente alineadas |
| Distribución / partes de un todo | Donut, pie, barras apiladas al 100% |
| Radial / ejes | Radar chart, diagrama de dispersión con cuadrantes nombrados |

Los diagramas se construyen con las primitivas de python-pptx: `add_shape` (`MSO_SHAPE.CHEVRON`, `PENTAGON`, `OVAL`, `RIGHT_ARROW`, `RIGHT_TRIANGLE`, `BLOCK_ARC`, `ROUNDED_RECTANGLE`), `add_connector` para líneas y flechas, y superposición con transparencia (`fill.transparency`) para Venn. Adaptá los colores a la paleta BU LAS y respetá el contraste del texto sobre cada bloque.

Ejemplo canónico (stages / fases): cada etapa es un chevron apuntando a la derecha, colores alternando entre `amarillo_bulas`, `dorado`, `gris_claro`, `gris_oscuro`, `negro`, con el nombre de la etapa dentro del chevron y una descripción corta debajo. Este patrón se puede replicar en serie cuando corresponde (ver excepción arriba).

Si el contenido no tiene una estructura clara que justifique un diagrama, es válido usar composiciones más simples — pero probá primero con un diagrama y solo caé en la versión "bloques de texto" si no encaja ninguna estructura relacional.

## Datos y gráficos

- Si hay datos numéricos y una visualización ayuda a comprenderlos, elegí libremente el tipo de gráfico más adecuado (barras, líneas, scatter, composición, etc.).
- Adaptá los gráficos a la paleta BU LAS.
- No agregues gráficos solo porque haya números ni para rellenar.
- Una presentación conceptual, de onboarding, estrategia o proceso puede perfectamente no incluir ningún gráfico.
- **Validación de porcentajes**: si un gráfico o visualización representa una distribución que debe sumar 100% (torta, donut, barras apiladas al 100%, tabla de share, etiquetas de porcentaje en un funnel), calculá la suma antes de terminar la presentación y verificá que dé exactamente 100 (o 100 ± 0,5 por redondeo). Si no suma, revisá los datos: puede faltar una categoría "otros", puede haber un error de tipeo, o los porcentajes pueden estar mal derivados. No dejes pasar una torta que sume 97% o 103%; corregí el dato o el cálculo antes de guardar.

### Insights sobre datos

Cuando una slide contiene datos numéricos, evaluá si hay algún hallazgo relevante que valga la pena destacar: una diferencia marcada entre categorías, una concentración inesperada, un valor que sobresale claramente, una tendencia. Si lo hay, agregá un finding breve y concreto — una línea, dos como máximo — en la misma slide, cerca del gráfico o en una posición jerárquicamente secundaria. Ejemplos del tipo de cosa que vale destacar: "El 68% de las respuestas se concentra en las dos primeras categorías", "La región Norte duplica a la siguiente en volumen", "Q3 muestra la única caída del período".

No inventar insights: solo señalar lo que los datos muestran objetivamente. Si los datos no tienen nada llamativo, no agregar nada. El finding no debe competir visualmente con el gráfico — es un apoyo, no el protagonista.

### Densidad y agrupación de gráficos

**Un gráfico simple no merece una slide entera.** Antes de asignar una slide exclusiva a un gráfico, evaluá su complejidad y peso informativo:

- Un gráfico con pocas categorías o pocas series (ej: 2 barras de género, un donut de sí/no, una sola línea temporal) es un gráfico de baja densidad. No justifica ocupar toda una slide solo.
- Un gráfico de alta densidad (muchas categorías, múltiples series, comparaciones cruzadas, datos geográficos) sí puede necesitar su propio espacio.

Para gráficos de baja densidad: agrupar con otros datos relacionados en la misma slide. Ejemplos correctos:
- Datos demográficos de una encuesta (género + edad + país) → una slide con tres gráficos pequeños en conjunto.
- Dos métricas de performance complementarias → una slide con ambos gráficos lado a lado.
- Un KPI numérico + su distribución por categoría → mismo espacio, jerarquía clara.

La regla práctica: antes de crear una nueva slide para un gráfico, preguntate si hay otro dato relacionado que podría vivir en la misma slide sin perder claridad. Si sí, agrupalos. Si no, la slide individual está justificada.

## Reglas de contenido

- No inventes hechos, cifras ni información que no estén en el brief o los materiales aportados.
- Cuando el usuario aporte información suficiente, **desarrollala y estructurala**, no la copies textual.
- Si falta algo puntual imprescindible, preguntá; si no, avanzá.

## Imágenes

- **No usar fotografía** como parte del diseño.
- Resolver visualmente con tipografía, formas, iconografía, diagramas, tablas, gráficos y demás recursos gráficos compatibles con la identidad.

## Entregable

Un archivo `.pptx` completamente editable, guardado en la work folder actual con un nombre descriptivo (por ejemplo `presentacion_<tema>_<YYYY-MM-DD>.pptx`).

Antes de entregar, revisá toda la presentación y corregí:

- texto cortado o desbordado
- elementos superpuestos accidentalmente
- contenido fuera del área de la slide
- gráficos o tablas que no se vean completos
- problemas de legibilidad o contraste
- placeholders o contenido de ejemplo sin reemplazar
- bordes izquierdo y derecho asimétricos (deben tener el mismo margen)
- porcentajes de una distribución que no sumen 100
- slides con fondo totalmente amarillo (prohibido)
- logos que no estén pegados al borde de la slide (el bounding box del PNG debe tocar el borde)
- logos superpuestos con texto, imágenes u otros elementos
- sección de título de una slide de contenido regular que supere 4 cm de alto sin justificación
- text boxes con `word_wrap` no seteado a `True` (causa texto vertical)
- text boxes donde el texto desborde el rectángulo (alto insuficiente)
- cualquier color que no sea un valor exacto del dict `COLORS` (fondos, textos, bordes, shapes)

Al final, mostrá el archivo al usuario con `mcp__tas__open_file`.

## Guía técnica de implementación

- **Preferí `python-pptx`** cuando esté disponible: `uv run --with python-pptx python3 script.py`. Permite crear la presentación desde cero, agregar shapes, textos, tablas y gráficos manteniendo la edición nativa en PowerPoint.
- Crear la presentación desde cero con `Presentation()` (sin abrir ningún archivo base) y setear el tamaño de slide a 16:9 explícitamente: `prs.slide_width = 12192000; prs.slide_height = 6858000`.
- Para gráficos, **siempre usar `add_chart` de python-pptx** para que el gráfico sea editable nativamente en PowerPoint. Nunca generar gráficos como imagen (matplotlib, SVG/PNG) salvo que `add_chart` no soporte el tipo de gráfico específico y sea absolutamente imposible de otra manera — en ese caso documentarlo en un comentario en el código.
- Los logos y textos deben quedar como shapes/imágenes editables (no aplanar la slide como una imagen única).
- Recordá el tamaño de slide 16:9 (12192000 × 6858000 EMU) al posicionar elementos.

### Construcción de slides desde cero

**Todas las slides se construyen manualmente**, partiendo del layout `blank` de python-pptx (`prs.slide_layouts[6]` por defecto, o el más neutro/vacío disponible). No se hereda ninguna composición: se define fondo, se posicionan los shapes y textos, y se agregan los logos al final.

Paleta de tema a mantener en memoria para consistencia:

```python
from pptx.dml.color import RGBColor

# Colores oficiales BU LAS + FNC — usar estos y no otros
COLORS = {
    "amarillo_bulas":   RGBColor(0xF5, 0xDF, 0x02),
    "amarillo_profundo":RGBColor(0xE3, 0xC1, 0x20),
    "dorado":           RGBColor(0xD3, 0xA2, 0x38),
    "negro":            RGBColor(0x01, 0x01, 0x01),
    "blanco":           RGBColor(0xFF, 0xFF, 0xFF),
    "gris_claro":       RGBColor(0xF2, 0xF2, 0xF2),
    "gris_oscuro":      RGBColor(0x4D, 0x4D, 0x4D),
    "verde":            RGBColor(0x27, 0x4F, 0x31),
    "azul":             RGBColor(0x28, 0x4F, 0x6D),
    "violeta":          RGBColor(0x4F, 0x45, 0x66),
    "bordo":            RGBColor(0x77, 0x31, 0x2C),
    "marron":           RGBColor(0x59, 0x4B, 0x32),
}

def luminosidad(rgb):
    """Retorna luminosidad perceptual 0-255. < 128 = oscuro."""
    if rgb is None:
        return 255
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]

def fondo_es_oscuro(rgb_fondo):
    """Determina si el color de fondo elegido para la slide es oscuro."""
    return luminosidad(rgb_fondo) < 128
```

Cuando construyas cada slide, definí primero el color de fondo, y a partir de ahí decidí el color del texto y la versión de los logos:

- Si `fondo_es_oscuro(rgb_fondo) == True` → texto `#FFFFFF`, logos en versión blanca (`LOGO BU LAS_Blanco&Color.png` + `Logo_FNC_Primario_Blanco.png`).
- Si `fondo_es_oscuro(rgb_fondo) == False` → texto `#010101`, logos en versión negra (`LOGO BU LAS_Negro&Color.png` + `Logo_FNC_Primario_Negro.png`).
- Si el fondo es amarillo BU LAS (`#F5DF02`, luminosidad ≈ 213) → texto `#010101`; nunca texto amarillo sobre fondo claro.
- Esta lógica aplica a **todos los textos de la slide** — setear el color explícitamente en cada `run`.

**Reglas para cada slide:**

- **Fuentes en shapes**: los text boxes creados con `add_textbox` o `add_shape` no heredan ningún tema — setear explícitamente `run.font.name = "Avantt"` (o `"Arial"` como fallback) y el color de fuente correspondiente en cada `run` de cada párrafo. Nunca dejar fuente o color en default de python-pptx. Para registrar la fuente Avantt en el entorno antes de usarla, copiar los `.ttf` desde `SKILL_DIR` al sistema o usarlos directamente vía `pptx.oxml` si el entorno lo permite; si la fuente no está disponible en el sistema, usar Arial como fallback.
- **Fondo de slide**: aplicar el color de fondo como un rectángulo que ocupe toda la slide (`add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)`) o mediante `slide.background.fill`. Enviarlo al fondo del z-order. **El color de fondo debe ser siempre uno de los valores exactos del dict `COLORS`. Nunca usar un color hex arbitrario, un color por defecto de python-pptx, ni un valor del manual de marca que no esté en `COLORS`.**
- **Solo usar colores de `COLORS`**: en absolutamente todo elemento (fondos, textos, bordes, shapes, gráficos) usar exclusivamente los valores del dict `COLORS`. Si python-pptx asigna un color por defecto al crear un shape (tema, accent, etc.), sobreescribirlo siempre con el color explícito del dict. Nunca construir un `RGBColor` con valores que no estén en `COLORS`.
- **Z-order de logos**: agregar los logos siempre al final del script de construcción de cada slide, después de todos los demás elementos, para que queden en el frente. Si aun así quedan tapados, moverlos al frente manipulando el orden en `slide.shapes._spTree`.
- **Variedad entre slides**: alternar composiciones (fondo claro / oscuro / amarillo de acento, distintas ubicaciones y tratamientos de título, uso puntual de shapes decorativas) para que la presentación no se sienta monótona, siempre dentro de la paleta y tipografía definidas.
- **Text wrap y desbordamiento**: al crear cualquier text box con `add_textbox`, setear inmediatamente `tf.word_wrap = True` en el text frame. Nunca dejar el default (que puede ser `False` y provoca que el texto se extienda en una sola línea o se vaya "para abajo" en vertical). Dimensionar el alto del text box generosamente en función del contenido esperado: calcular la altura necesaria aproximada como `líneas_estimadas × (font_size_pt × 1.2) × 12700` (conversión pt → EMU a 96 DPI) y agregar al menos un 25% de margen. Si el texto puede ser largo o variable, preferir un alto más grande y verificar en QA. **Nunca forzar un text box pequeño con texto largo**: si el contenido no cabe, reducir el texto, el tamaño de fuente, o dividir en dos bloques — pero no dejar que el texto desborde el rectángulo.

### Validación de integridad antes de guardar

**Antes de llamar a `prs.save()`**, ejecutar esta validación para evitar que PowerPoint muestre el diálogo de reparación al abrir el archivo:

```python
from lxml import etree

def validar_presentacion(prs):
    """
    Verifica integridad del XML antes de guardar. Corrige:
    1. IDs duplicados por slide
    2. Relaciones de imágenes huérfanas
    3. Placeholders vacíos residuales
    4. Conectores con índices de conexión fuera de rango
    5. Series de gráficos con valores None/NaN
    6. Axis IDs negativos en gráficos (overflow de int32 → xsd:unsignedInt inválido)
    7. Doble c:marker en series de lineChart (violación maxOccurs=1 de CT_LineSer)
    8. c:spPr fuera de orden en series de barChart (debe ir antes de c:dLbls en CT_BarSer)
    9. numFmt incorrecto en labels de donut/pie con showPercent: 0"%" → 0%
   10. Orientación de eje de categorías invertida en barras horizontales (minMax → maxMin)
    """
    NSMAP_P = "http://schemas.openxmlformats.org/presentationml/2006/main"

    for slide_idx, slide in enumerate(prs.slides):
        spTree = slide.shapes._spTree
        ids_vistos = set()
        next_id = 1000 + slide_idx * 100  # rango seguro para IDs nuevos

        # 1. IDs únicos por slide
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

        # 2. Relaciones de imágenes: verificar que cada rId referenciado existe
        rids_en_xml = set()
        for el in spTree.iter():
            for attr in el.attrib.values():
                if attr.startswith("rId"):
                    rids_en_xml.add(attr)
        rids_validos = set(slide.part.rels.keys())
        rids_huerfanos = rids_en_xml - rids_validos
        if rids_huerfanos:
            # Eliminar elementos que referencien rIds inexistentes
            for el in list(spTree.iter()):
                for attr_val in el.attrib.values():
                    if attr_val in rids_huerfanos:
                        parent = el.getparent()
                        if parent is not None:
                            parent.remove(el)
                        break

        # 3. Placeholders residuales con texto de ejemplo (failsafe)
        ns = f"{{{NSMAP_P}}}"
        for sp in list(spTree.findall(f".//{ns}sp")):
            ph = sp.find(f".//{ns}ph", sp.nsmap if hasattr(sp, 'nsmap') else {})
            if ph is None:
                ph = sp.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}ph")
            if ph is not None:
                # Si el placeholder no tiene texto real, eliminarlo
                txBody = sp.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}txBody")
                if txBody is not None:
                    texto = "".join(t.text or "" for t in txBody.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"))
                    if not texto.strip():
                        sp.getparent().remove(sp)

        # 4. Connectors con puntos de conexión inválidos — eliminar atributos idx fuera de rango
        DML_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
        for cxn in spTree.iter(f"{{{DML_NS}}}cxnSp"):
            for stCxn in cxn.iter(f"{{{DML_NS}}}stCxn"):
                try:
                    idx = int(stCxn.get("idx", "0"))
                    if idx > 8:  # los puntos de conexión válidos son 0-8
                        stCxn.set("idx", "0")
                except (ValueError, TypeError):
                    stCxn.set("idx", "0")
            for endCxn in cxn.iter(f"{{{DML_NS}}}endCxn"):
                try:
                    idx = int(endCxn.get("idx", "0"))
                    if idx > 8:
                        endCxn.set("idx", "0")
                except (ValueError, TypeError):
                    endCxn.set("idx", "0")

    # 5. Gráficos: verificar que las series no tengan valores None/NaN que corrompan el XML
    from pptx.util import Pt
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart = shape.chart
                for series in chart.series:
                    try:
                        vals = series.values
                        cleaned = [v if (v is not None and v == v) else 0 for v in vals]
                        # Si hubo valores nulos, reescribir la serie con ceros
                        if any(v != c for v, c in zip(series.values, cleaned)):
                            for i, pt in enumerate(series.data_labels._element.iter()):
                                pass  # solo iterar para detectar errores
                    except Exception:
                        pass  # si la serie no es accesible, no bloquear el guardado

    # 6. Axis IDs negativos: python-pptx puede generar axId negativos (overflow de int32)
    # que son XML inválido (xsd:unsignedInt). PowerPoint los rechaza, muestra diálogo de
    # reparación y puede borrar completamente el contenido de slides como efecto colateral.
    DML_C_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_part = shape.chart._part
                chart_root = chart_part._element
                for ax_id_el in chart_root.iter(f"{{{DML_C_NS}}}axId"):
                    val = ax_id_el.get("val")
                    if val and int(val) < 0:
                        ax_id_el.set("val", str(int(val) + 2**32))

    # 7. Doble c:marker en series de lineChart: CT_LineSer permite solo un c:marker
    # (maxOccurs=1). python-pptx puede generar dos por serie (symbol="none" + symbol
    # visible), lo que es inválido según el schema OOXML — PowerPoint "repara" borrando
    # todo el contenido del gráfico. Fix: conservar solo el marker con símbolo visible
    # y reordenar los hijos de la serie según CT_LineSer:
    # idx → order → tx → spPr → marker → cat → val → smooth.
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_root = shape.chart._part._element
                for ser in chart_root.iter(f"{{{DML_C_NS}}}ser"):
                    markers = list(ser.findall(f"{{{DML_C_NS}}}marker"))
                    if len(markers) < 2:
                        continue
                    # Conservar el marker con símbolo visible (no "none")
                    keep_marker = None
                    for m in markers:
                        sym = m.find(f"{{{DML_C_NS}}}symbol")
                        if sym is None or sym.get("val") != "none":
                            keep_marker = m
                            break
                    if keep_marker is None:
                        keep_marker = markers[-1]
                    # Reordenar hijos según CT_LineSer
                    idx_el    = ser.find(f"{{{DML_C_NS}}}idx")
                    order_el  = ser.find(f"{{{DML_C_NS}}}order")
                    tx_el     = ser.find(f"{{{DML_C_NS}}}tx")
                    spPr_el   = ser.find(f"{{{DML_C_NS}}}spPr")
                    cat_el    = ser.find(f"{{{DML_C_NS}}}cat")
                    val_el    = ser.find(f"{{{DML_C_NS}}}val")
                    smooth_el = ser.find(f"{{{DML_C_NS}}}smooth")
                    for child in list(ser):
                        ser.remove(child)
                    for el in [idx_el, order_el, tx_el, spPr_el, keep_marker,
                               cat_el, val_el, smooth_el]:
                        if el is not None:
                            ser.append(el)

    # 8. c:spPr fuera de orden en series de barChart: CT_BarSer requiere spPr antes de
    # dLbls. python-pptx lo coloca al final (después de val), lo que es inválido según
    # el schema OOXML y puede causar que PowerPoint reordene o elimine series en gráficos
    # percentStacked al "reparar" el archivo. Fix: reordenar a
    # idx → order → tx → spPr → dLbls → cat → val.
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_root = shape.chart._part._element
                for barChart in chart_root.iter(f"{{{DML_C_NS}}}barChart"):
                    for ser in barChart.findall(f"{{{DML_C_NS}}}ser"):
                        tags = [c.tag.split("}")[1] for c in ser]
                        if "spPr" not in tags or "dLbls" not in tags:
                            continue
                        if tags.index("spPr") < tags.index("dLbls"):
                            continue  # ya en orden correcto
                        idx_el   = ser.find(f"{{{DML_C_NS}}}idx")
                        order_el = ser.find(f"{{{DML_C_NS}}}order")
                        tx_el    = ser.find(f"{{{DML_C_NS}}}tx")
                        spPr_el  = ser.find(f"{{{DML_C_NS}}}spPr")
                        dLbls_el = ser.find(f"{{{DML_C_NS}}}dLbls")
                        cat_el   = ser.find(f"{{{DML_C_NS}}}cat")
                        val_el   = ser.find(f"{{{DML_C_NS}}}val")
                        for child in list(ser):
                            ser.remove(child)
                        for el in [idx_el, order_el, tx_el, spPr_el, dLbls_el,
                                   cat_el, val_el]:
                            if el is not None:
                                ser.append(el)

    # 9. numFmt incorrecto en dLbls de gráficos donut/pie con showPercent activo.
    # python-pptx genera formatCode='0"%"' (cero + literal %) que se aplica al valor
    # decimal 0-1 que PowerPoint computa para showPercent: 0.77 → redondea a 1 → "1%".
    # El formato correcto es "0%" (sin comillas) que multiplica ×100 antes de mostrar:
    # 0.77 → "77%". Fix: reemplazar 0"%" por 0% en cualquier dLbls que tenga showPercent=1.
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_root = shape.chart._part._element
                for dlbls in chart_root.iter(f"{{{DML_C_NS}}}dLbls"):
                    show_pct = dlbls.find(f"{{{DML_C_NS}}}showPercent")
                    if show_pct is None or show_pct.get("val") not in ("1", "true"):
                        continue
                    num_fmt = dlbls.find(f"{{{DML_C_NS}}}numFmt")
                    if num_fmt is not None and num_fmt.get("formatCode") == '0"%"':
                        num_fmt.set("formatCode", "0%")
                        num_fmt.set("sourceLinked", "0")

    # 10. Orientación de eje de categorías invertida en barras horizontales.
    # Para barDir="bar" (barras horizontales), python-pptx genera catAx con
    # orientation="minMax", lo que coloca la primera categoría (idx=0) al FONDO.
    # Para que la primera categoría aparezca ARRIBA (comportamiento esperado), la
    # orientación del catAx debe ser "maxMin".
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_chart:
                chart_root = shape.chart._part._element
                for bar_chart in chart_root.iter(f"{{{DML_C_NS}}}barChart"):
                    bar_dir = bar_chart.find(f"{{{DML_C_NS}}}barDir")
                    if bar_dir is None or bar_dir.get("val") != "bar":
                        continue  # solo aplica a barras horizontales
                    for cat_ax in chart_root.iter(f"{{{DML_C_NS}}}catAx"):
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

Llamar antes de guardar:
```python
validar_presentacion(prs)
prs.save(output_path)
fix_content_types(output_path)  # siempre llamar después de save()
```

**`fix_content_types` — obligatorio después de todo `prs.save()`:**

python-pptx no genera entradas `Override` explícitas en `[Content_Types].xml` para los xlsx embebidos de los gráficos — se apoya en un `Default` de extensión. PowerPoint ignora ese Default para partes embebidas y espera `Override` explícitos: sin ellos muestra el diálogo de reparación al abrir y descarta los datos del gráfico. Este fix post-guarda resuelve el problema de raíz:

```python
import zipfile, shutil, os
from lxml import etree as lxml_etree

def fix_content_types(output_path):
    """
    Agrega Override explícitos en [Content_Types].xml para cada xlsx embebido.
    python-pptx omite estos Override y PowerPoint los requiere para los datos
    de gráficos — sin ellos muestra diálogo de reparación al abrir.
    Llamar siempre inmediatamente después de prs.save(output_path).
    """
    CT_NS   = "http://schemas.openxmlformats.org/package/2006/content-types"
    XLSX_CT = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    tmp_path = output_path + ".ct_fix.tmp"

    with zipfile.ZipFile(output_path, "r") as zin:
        names = zin.namelist()
        xlsx_parts = sorted([n for n in names if n.startswith("ppt/embeddings/") and n.endswith(".xlsx")])

        if not xlsx_parts:
            return  # sin gráficos, nada que hacer

        with zin.open("[Content_Types].xml") as f:
            ct_root = lxml_etree.fromstring(f.read())

        existing = {el.get("PartName", "") for el in ct_root}

        added = 0
        for part in xlsx_parts:
            part_name = "/" + part
            if part_name not in existing:
                el = lxml_etree.SubElement(ct_root, f"{{{CT_NS}}}Override")
                el.set("PartName", part_name)
                el.set("ContentType", XLSX_CT)
                added += 1

        if added == 0:
            return  # ya estaban todos

        fixed_ct = lxml_etree.tostring(ct_root, xml_declaration=True, encoding="UTF-8", standalone=True)

        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "[Content_Types].xml":
                    zout.writestr(item, fixed_ct)
                else:
                    zout.writestr(item, zin.read(item.filename))

    os.replace(tmp_path, output_path)
```

**Reglas generales para evitar corrupción:**

- Usar siempre la API de python-pptx (`add_picture`, `add_textbox`, `add_shape`, `add_chart`) para agregar elementos. Manipular XML directamente solo cuando la API no alcance, y en ese caso usar `lxml.etree` — nunca concatenación de strings.
- No dejar shapes con `id="0"` ni con IDs repetidos: son la causa más común del diálogo de reparación de PowerPoint.

### Evitar superposición de elementos

**Al posicionar cualquier elemento en una slide**, verificar que no se superpone con los ya existentes antes de agregarlo:

```python
def rectangulos_se_superponen(a, b):
    """a y b son dicts con left, top, width, height en EMU."""
    return not (
        a["left"] + a["width"] <= b["left"] or
        b["left"] + b["width"] <= a["left"] or
        a["top"] + a["height"] <= b["top"] or
        b["top"] + b["height"] <= a["top"]
    )

def hay_superposicion(nuevo, ocupados):
    return any(rectangulos_se_superponen(nuevo, existente) for existente in ocupados)
```

Mantener una lista `ocupados` de todos los elementos ya posicionados en la slide (left, top, width, height). Antes de colocar cada nuevo elemento:
- Si se superpone, ajustar su posición (moverlo, reducir su tamaño o redistribuir el layout).
- Si no hay espacio sin superposición, reducir el contenido o partir en dos slides.
- Los logos tienen posición fija (esquina elegida) — el resto del contenido debe planificarse sin invadir esa zona desde el inicio.

Esta verificación aplica a **todos los elementos**: text boxes, imágenes, gráficos, tablas, formas decorativas y los propios logos.

El objetivo es que cada slide tenga una composición limpia y original, con texto siempre legible independientemente del fondo.

## Recordá

Mantené estas instrucciones simples. No agregues layouts de contenido predefinidos, reglas geométricas, porcentajes de composición ni restricciones de diseño más allá de las que preservan la identidad de marca y la calidad de la presentación.

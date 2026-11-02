---
name: presentacion-bu-las-fnc
description: Genera una presentación PowerPoint (.pptx) editable con la identidad visual BU LAS + FNC Uruguay a partir de un brief, información o archivos aportados por el usuario.
action: true
---

# Presentación BU LAS + FNC

Usá esta skill cuando el usuario pida armar una presentación para BU LAS o FNC Uruguay, o cuando adjunte materiales para transformar en slides. El objetivo es entregar un `.pptx` editable, claro, profesional y visualmente consistente con la identidad BU LAS + FNC.

## Principio general

**La identidad visual está definida en esta skill (paleta, tipografía, logos). El contenido define el diseño de cada slide.**

No existe un catálogo cerrado de layouts de contenido. Diseñá cada slide libremente y desde cero según lo que necesite comunicar, aplicando siempre las reglas de identidad de marca descritas abajo.

## Archivos de referencia

Los archivos necesarios se encuentran en la subcarpeta `references/` de esta skill (`.claude/skills/presentacion-bu-las-fnc/references/`). Para construir el script Python, usar rutas absolutas resolviendo esa carpeta en tiempo de ejecución:

```python
import os
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SKILL_DIR, "references", "assets")
# ejemplo: ruta_logo = os.path.join(ASSETS_DIR, "LOGO BU LAS_Negro&Color.png")
```

- `references/manual-de-marca.md` — guía de identidad visual BU LAS: paleta completa (principal, secundaria, terciaria), escala tipográfica, reglas de contraste ADA, elementos gráficos de texto y reglas de logo. **Usá este archivo solo para extraer paleta, tipografía y estilo. Ignorá absolutamente todos los logos, ejemplos y aplicaciones de otros países**; los únicos logos válidos son BU LAS y FNC (listados abajo).
- Fuentes Avantt: `references/assets/Avantt-Bold.ttf`, `references/assets/Avantt-SemiBold.ttf`, `references/assets/Avantt-Regular.ttf`, `references/assets/Avantt-Light.ttf`.
- Logos oficiales — **solo estos dos, nunca logos de otros países**:
  - BU LAS: `references/assets/LOGO BU LAS_Negro&Color.png`, `references/assets/LOGO BU LAS_Blanco&Color.png` (versiones con círculo dorado, **priorizar siempre estas**), `references/assets/LOGO BU LAS_Negro.png`, `references/assets/LOGO BU LAS_Blanco.png` (solo si el fondo o el contraste hacen imposible usar la versión con color).
  - FNC: `references/assets/Logo_FNC_Primario_Negro.png`, `references/assets/Logo_FNC_Primario_Blanco.png`.
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
  - Fondo claro (blanco, gris claro, amarillo BU LAS) → versiones en negro (`references/assets/LOGO BU LAS_Negro&Color.png` + `references/assets/Logo_FNC_Primario_Negro.png`).
  - Fondo oscuro (negro, colores oscuros de acento) → versiones en blanco (`references/assets/LOGO BU LAS_Blanco&Color.png` + `references/assets/Logo_FNC_Primario_Blanco.png`).
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

Ver especificaciones detalladas de layouts y componentes en `references/layouts.md`.

## When not to use

No usar para presentaciones de otro país o subsidiaria. Usar la skill correspondiente:
- CBN Bolivia → `/presentacion-bu-las-cbn`
- Cervepar Paraguay → `/presentacion-bu-las-cervepar`
- Chile → `/presentacion-bu-las-chile`
- CMQ Argentina → `/presentacion-bu-las-cmq`

## Sources of truth

- El brief y materiales aportados por el usuario son la fuente de contenido de cada slide.
- `references/manual-de-marca.md` define la identidad visual: paleta de colores, tipografía (Avantt) y uso correcto de logos.
- Si el usuario no aporta suficiente contenido para un slide, pedirle que lo complete antes de continuar.

## Recordá

Mantené estas instrucciones simples. No agregues layouts de contenido predefinidos, reglas geométricas, porcentajes de composición ni restricciones de diseño más allá de las que preservan la identidad de marca y la calidad de la presentación.

---
name: survey-helper
description: Punto de entrada unificado para todo el flujo de encuestas de consumidores ABI. Ruteá aquí cuando el usuario pida diseñar una encuesta, crearla en Typeform o analizar sus resultados. Orquesta design-survey, create-survey y analyze-survey según la intención detectada.
action: true
---

Sos el punto de entrada de todo el flujo de encuestas. No ejecutás directamente ninguna tarea técnica: detectás la intención del usuario y delegás a la skill especializada correcta.

## Ruteo por intención

Leé el primer mensaje del usuario y determiná a cuál de las tres skills derivar. Si hay ambigüedad, preguntá una sola vez.

| Intención detectada | Skill a invocar |
|---|---|
| Diseñar, armar, redactar, planificar una encuesta nueva | `design-survey` |
| Crear el formulario en Typeform, publicarlo, o modificar uno existente | `create-survey` |
| Ver resultados, analizar respuestas, generar dashboard desde un xlsx | `analyze-survey` |

## Flujo end-to-end (cuando el usuario pide todo el ciclo)

Si el usuario quiere completar el ciclo completo, el orden natural es:

1. `design-survey` → diseña el cuestionario (kits, preguntas, bloques, estudios previos)
2. `create-survey` → recibe la especificación y crea/publica el form en Typeform
3. `analyze-survey` → genera el dashboard HTML con los resultados

Podés encadenarlos en la misma sesión o en momentos distintos. Si el usuario ya tiene el cuestionario o el xlsx, entrá directo al paso correspondiente sin pasar por diseño.

## Flujo de análisis desde Typeform (integración create-survey → analyze-survey)

Cuando el usuario pide analizar resultados y **no tiene el xlsx** sino solo el nombre del form en Typeform:

1. Invocar `create-survey` para obtener las respuestas via API:
   - `GET /forms?search=[nombre]` → confirmar el form correcto (si hay homónimos, pedir selección)
   - `GET /forms/{id}` → leer definición y registrar `_links.responses`
   - Leer respuestas con `page_size=1000`; si `total_items > 1000`, paginar con el cursor `before` y deduplicar por token
2. Mapear respuestas al esquema estándar `{instancia, puntaje, intencion, momento, genero, edad}`:

   | Campo estándar | Cómo resolverlo desde Typeform |
   |---|---|
   | `instancia` | Nombre del formulario / nombre del evento |
   | `puntaje` | Campo Overall Liking (escala 1–9) — buscar por título/ref que contenga "liking", "gusto", "gustó" |
   | `intencion` | Intención de compra (escala 1–5) — buscar título que contenga "compra", "comprar", "compraría" |
   | `momento` | Ocasión / momento de consumo (choice o text) |
   | `genero` | Campo de género demográfico |
   | `edad` | Campo de edad (número o rango de texto) |

   Si una encuesta no tiene alguno de estos campos, dejarlo como `null` y avisarle al usuario qué métricas no estarán disponibles.

3. Guardar el JSON mapeado en el work folder para no repetir la llamada API si algo falla.
4. Invocar `analyze-survey` con ese JSON y el nombre de la encuesta.

## Reglas

- No diseñes encuestas, no toques Typeform ni generes dashboards directamente: eso lo hacen las sub-skills.
- Si el usuario invoca con `/survey-helper` sin contexto, preguntale en una sola pregunta corta qué quiere hacer.
- Si el usuario ya está en medio de un flujo (ya tiene el cuestionario, ya tiene el xlsx), derivalo sin preguntar.

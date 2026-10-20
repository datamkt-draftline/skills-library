---
name: glosario-skills
description: Genera un HTML interactivo con el glosario completo de skills disponibles, organizado por área (Marketing, Data, Medios, draftLine). Cada skill es clickeable y muestra detalles (funcionalidad, comando, archivos requeridos, outputs, etc.).
action: true
---

# Glosario de Skills

Esta skill genera un archivo HTML standalone con el glosario completo de skills del equipo, organizado por área. El HTML es interactivo: al hacer click sobre una skill se despliega un panel con el detalle completo (funcionalidad, comando de invocación, archivos que el usuario debe adjuntar, outputs esperados, notas, etc.).

## Cómo funciona

1. Leé la data del glosario del bloque `GLOSARIO_DATA` más abajo (está en formato JSON embebido en este mismo archivo).
2. Generá un HTML standalone (sin dependencias externas, con CSS y JS inline) que:
   - Muestre las áreas como secciones (cards/columnas) con un color distintivo cada una.
   - Dentro de cada área, liste las skills como "chips" o items clickeables mostrando `nombre` y `comando`.
   - Al clickear una skill se abre un panel/modal con todos sus campos: `funcionalidad`, `comando`, `archivos_requeridos`, `outputs`, `notas`.
   - Incluya una barra de búsqueda que filtre skills por nombre, comando o descripción.
   - Tenga un contador total de skills y por área.
   - Diseño limpio, responsive, con tipografía legible y buen contraste.
3. Guardá el HTML en el directorio de trabajo actual con nombre `glosario-skills.html`.
4. Llamá a `mcp__tas__open_file` con el path absoluto del HTML generado para mostrárselo al usuario.

## Importante

- El HTML debe ser **standalone**: todo el CSS y JS inline, sin CDNs ni dependencias externas.
- Si un campo (ej. `archivos_requeridos`) está vacío o es `null`, mostralo como "No requiere" o similar — no lo escondas sin indicar.
- El JSON embebido abajo es la **única fuente de verdad**: no inventes skills que no estén listadas, ni omitas ninguna.
- Para agregar/editar skills en el futuro, el usuario puede editar el bloque `GLOSARIO_DATA` directamente en este archivo.

## GLOSARIO_DATA

```json
{
  "areas": [
    {
      "nombre": "Marketing",
      "color": "#E63946",
      "skills": [
        {
          "nombre": "Presentaciones PPT-CMQ",
          "comando": "/presentacion-bu-las-cmq",
          "funcionalidad": "Genera presentaciones PowerPoint (.pptx) editables con la identidad visual de BU LAS + Cervecería y Maltería Quilmes a partir de un brief, información o archivos aportados por el usuario.",
          "archivos_requeridos": "Brief en texto, Word, PDF o imágenes de referencia. Opcional: logos, datos de la marca.",
          "outputs": "Archivo .pptx editable con slides maquetadas según identidad visual CMQ.",
          "notas": "Soporta múltiples formatos de input. El output es siempre editable en PowerPoint."
        },
        {
          "nombre": "Generación de contenido Cont-Gen",
          "comando": "/cont-gen",
          "funcionalidad": "Genera piezas de contenido (copy, posteos, mails, scripts) alineadas a la voz de marca y al brief entregado.",
          "archivos_requeridos": "Brief del contenido a generar (texto o doc). Opcional: guía de tono de marca, ejemplos de referencia.",
          "outputs": "Documento con las piezas de contenido solicitadas, con variantes y propuestas de CTAs.",
          "notas": "Puede trabajar en castellano rioplatense y adaptar el registro según el canal (RRSS, mail, OOH, etc.)."
        },
        {
          "nombre": "Análisis/tracking de presupuesto Budget-Tracker",
          "comando": "/budget-tracker",
          "funcionalidad": "Analiza y hace seguimiento del presupuesto de marketing: ejecución vs. plan, desvíos por marca/mes/trimestre, alertas.",
          "archivos_requeridos": "Excel con el presupuesto planificado y ejecutado (columnas: marca, categoría, mes, planificado, ejecutado).",
          "outputs": "Dashboard HTML o Excel procesado con KPIs de ejecución, desvíos y recomendaciones.",
          "notas": "Útil para reportes mensuales y Quarterly Business Reviews."
        },
        {
          "nombre": "Genome",
          "comando": "/genome",
          "funcionalidad": "Genera el 'genoma' de una marca o campaña: atributos clave, posicionamiento, audiencias objetivo y pilares de comunicación.",
          "archivos_requeridos": "Información de la marca/campaña (brief, estudios previos, resultados). Opcional: data de competidores.",
          "outputs": "Documento estructurado con los pilares del genoma de la marca/campaña.",
          "notas": "Suele usarse al inicio de un proyecto para alinear al equipo sobre la identidad del asset."
        }
      ]
    },
    {
      "nombre": "Data",
      "color": "#1D3557",
      "skills": [
        {
          "nombre": "Benchmarks Bench-CMQ",
          "comando": "/bench-cmq",
          "funcionalidad": "Genera benchmarks de categoría/competidores a partir de datos internos y fuentes externas, con comparativas visuales.",
          "archivos_requeridos": "Dataset de la categoría (xlsx/csv) con métricas de marca y competidores.",
          "outputs": "Reporte HTML con benchmarks por métrica, ranking competitivo y insights.",
          "notas": "Incluye visualizaciones comparativas y top/bottom performers."
        },
        {
          "nombre": "Social Research Leila",
          "comando": "/leila",
          "funcionalidad": "Realiza research social (escucha activa, análisis de conversación, sentiment, trending topics) sobre un tema o marca.",
          "archivos_requeridos": "Opcional: dataset de menciones/posteos. Si no, parte de la consulta en texto libre.",
          "outputs": "Reporte con hallazgos de conversación social, volumen, sentiment, menciones destacadas e insights.",
          "notas": "Puede usarse para preparar entradas a presentaciones o detectar oportunidades de contenido."
        },
        {
          "nombre": "Análisis de performance de campañas Perfo-CMQ",
          "comando": "/perfo-cmq",
          "funcionalidad": "Analiza la performance de campañas digitales: reach, impresiones, CTR, CPM, CPC, conversiones, ROAS.",
          "archivos_requeridos": "Export de la plataforma (Meta, Google, TikTok, DV360, etc.) en xlsx/csv.",
          "outputs": "Dashboard HTML con KPIs principales, breakdown por canal/creatividad/audiencia y recomendaciones de optimización.",
          "notas": "Soporta múltiples plataformas en un mismo análisis."
        },
        {
          "nombre": "Automatización SOE SOE-CMQ",
          "comando": "/soe-cmq",
          "funcionalidad": "Automatiza el cálculo de Share of Expenditure (SOE) por marca y categoría, con comparativas temporales.",
          "archivos_requeridos": "Reporte de inversión por marca/competidor (xlsx) y período a analizar.",
          "outputs": "Excel procesado + HTML con evolución de SOE, benchmarks de categoría y gaps.",
          "notas": "Ahorra el proceso manual de armado de tabla de SOE que se hacía trimestralmente."
        },
        {
          "nombre": "Mails Tracking Mails-Track",
          "comando": "/mails-track",
          "funcionalidad": "Hace tracking de performance de campañas de mail marketing: open rate, CTR, bounce, unsubscribes, por segmento.",
          "archivos_requeridos": "Export del ESP (ej. Salesforce Marketing Cloud, Mailchimp) en xlsx/csv.",
          "outputs": "Dashboard HTML con KPIs por campaña, segmento y evolución temporal.",
          "notas": "Útil para reportes semanales/mensuales de CRM."
        },
        {
          "nombre": "Automatización Encuestas y resultados",
          "comando": "/analyze-survey",
          "funcionalidad": "Analiza resultados de encuestas siguiendo una metodología por pasos y genera dashboard HTML + xlsx procesado con el detalle por pregunta.",
          "archivos_requeridos": "Archivo xlsx con los resultados de la encuesta (respuestas en bruto).",
          "outputs": "Dashboard HTML interactivo + xlsx con análisis detallado por pregunta.",
          "notas": "Soporta encuestas con preguntas de selección múltiple, abiertas y escala Likert."
        },
        {
          "nombre": "Diccionario Estudios SL & Agile",
          "comando": "/diccionario-estudios",
          "funcionalidad": "Mantiene y consulta un diccionario de estudios realizados (Shopper Loyalty, Agile Research) con metodología, muestra, hallazgos clave y link al reporte original.",
          "archivos_requeridos": "Opcional: nuevo estudio para incorporar al diccionario (PDF o doc).",
          "outputs": "HTML consultable con buscador y filtros por marca, metodología, fecha.",
          "notas": "Evita el 'reinvento' preguntándole al equipo si un estudio ya existe."
        }
      ]
    },
    {
      "nombre": "Medios",
      "color": "#F4A261",
      "skills": [
        {
          "nombre": "Análisis de inversión 1YP 2026-2027 1YP-Medios",
          "comando": "/1yp-medios",
          "funcionalidad": "Analiza la inversión 1YP (One Year Plan) 2026-2027 por marca, canal y trimestre con comparativas vs. año anterior.",
          "archivos_requeridos": "Excel con el plan de inversión 1YP (marca, canal, Q, monto).",
          "outputs": "Dashboard HTML interactivo con breakdown por dimensiones y evolución.",
          "notas": "Relacionado con la skill inversion-abi-dashboard."
        },
        {
          "nombre": "Performance de influencers Influs-CMQ",
          "comando": "/influencer-audience",
          "funcionalidad": "Genera presentación PPTX editable con audience intelligence de uno o más influencers (biografía, partnerships, demographics, follower history) a partir de datos de CreatorIQ.",
          "archivos_requeridos": "Export de CreatorIQ con los influencers a analizar.",
          "outputs": "Presentación .pptx con un deck por influencer, listo para compartir.",
          "notas": "Pensado para evaluación de talents antes de un contrato."
        },
        {
          "nombre": "TRPs TRPs-CMQ",
          "comando": "/trps-cmq",
          "funcionalidad": "Analiza TRPs (Target Rating Points) de campañas de TV: cobertura, frecuencia, GRPs, por canal/franja/target.",
          "archivos_requeridos": "Reporte de Kantar IBOPE / central de medios con TRPs por campaña.",
          "outputs": "Dashboard HTML con KPIs de TV, curvas de cobertura y comparativas.",
          "notas": "Soporta análisis de múltiples campañas en paralelo."
        },
        {
          "nombre": "Content Tracker Cont-track",
          "comando": "/cont-track",
          "funcionalidad": "Hace tracking del contenido publicado por marca/plataforma: volumen, formatos, performance y gaps vs. plan.",
          "archivos_requeridos": "Export de plataformas (Meta Business, TikTok, YouTube Studio) o Google Sheet de planificación.",
          "outputs": "Dashboard HTML con volumen de contenido, performance y recomendaciones.",
          "notas": "Ayuda a identificar sobre/subdotación de contenido por canal."
        }
      ]
    },
    {
      "nombre": "draftLine",
      "color": "#2A9D8F",
      "skills": [
        {
          "nombre": "Armado de Briefs Briefs-dl",
          "comando": "/briefs-dl",
          "funcionalidad": "Genera briefs creativos estandarizados para draftLine a partir de la info del proyecto, con todos los campos requeridos (objetivos, target, mensajes, entregables, timings).",
          "archivos_requeridos": "Info del proyecto (texto, Word, PDF). Opcional: ejemplos de briefs anteriores.",
          "outputs": "Documento Word o PDF con el brief armado según template draftLine.",
          "notas": "Reduce el ida y vuelta entre cliente interno y draftLine."
        },
        {
          "nombre": "Agendas / visibilidad de proyectos Agenda-CMQ",
          "comando": "/agenda-cmq",
          "funcionalidad": "Genera una vista consolidada de todos los proyectos activos de draftLine con responsables, estado, próximos hitos.",
          "archivos_requeridos": "Export del sistema de gestión de proyectos (Monday, Asana, Google Sheet).",
          "outputs": "Dashboard HTML con la agenda consolidada, filtros por responsable/marca/estado.",
          "notas": "Útil para reuniones de status semanales."
        },
        {
          "nombre": "Calendario digital Calendar-dl",
          "comando": "/calendar-dl",
          "funcionalidad": "Genera un calendario digital de contenido (RRSS, mails, web) con fechas de publicación, responsables y assets.",
          "archivos_requeridos": "Planificación de contenido en xlsx/csv o Google Sheet.",
          "outputs": "HTML con vista calendario interactivo (mensual/semanal) y vista lista.",
          "notas": "Soporta múltiples marcas en un mismo calendario con filtros."
        },
        {
          "nombre": "Cotización y seguimiento de proyectos Gantt-CMQ",
          "comando": "/gantt",
          "funcionalidad": "Genera un Gantt interactivo (HTML) a partir de un Excel para cotizar y hacer seguimiento de proyectos de draftLine.",
          "archivos_requeridos": "Excel con tareas, responsables, fechas inicio/fin y dependencias.",
          "outputs": "HTML standalone con Gantt interactivo, filtros y timeline navegable.",
          "notas": "Si el usuario pregunta cómo usarlo, la skill entrega el template Excel."
        }
      ]
    }
  ]
}
```

## Pasos finales de generación

1. Parseá el JSON de arriba.
2. Generá el HTML con las secciones por área (ordenadas: Marketing → Data → Medios → draftLine), cada una con su color distintivo como accent.
3. Cada skill debe ser un elemento clickeable que al hacer click abra un modal/panel con los campos:
   - **Funcionalidad**
   - **Comando** (en formato código monospace)
   - **Archivos requeridos** (si está vacío mostrar "No requiere archivos")
   - **Outputs**
   - **Notas**
4. Incluí barra de búsqueda arriba que filtre por nombre, comando o funcionalidad.
5. Incluí header con contador total y por área.
6. Guardá en el working directory actual como `glosario-skills.html`.
7. Llamá a `mcp__tas__open_file` con el path absoluto.

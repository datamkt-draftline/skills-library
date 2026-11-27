# skills-library

Repositorio creado por el equipo de draftLine Data Marketing Argentina para el almacenamiento de skills a usar por los distintos equipos del área de Marketing.

## Catálogo de skills

| Skill | Carpeta | Propósito | Tipo |
|-------|---------|-----------|------|
| analyze-survey | `analyze-survey` | Analiza resultados de una encuesta en xlsx y genera un dashboard HTML interactivo con filtros dinámicos. | action |
| completion-status | `completion-status` | Genera el reporte HTML de LAS Completion Status ejecutando el script de generación. | action |
| content-tracker | `content-tracker` | Genera el Content Investment & Impact Tracker HTML a partir del Excel de referencias. | action |
| corona-pptx | `corona-pptx` | Genera una presentación PPTX editable con la identidad visual de la marca Corona a partir de un brief o materiales aportados. | action |
| create-survey | `create-survey` | Capa técnica para operar Typeform vía API REST: crear, consultar o modificar formularios, campos, lógica, scoring y respuestas. No diseña encuestas — para eso usar design-survey. | skill |
| design-survey | `design-survey` | Diseña una encuesta completa de consumidores (8 kits verticales, bloques Agile, estudios previos de 45 encuestas de referencia). | action |
| events-dashboard | `events-dashboard` | Genera el dashboard ejecutivo de ticketing de Quilmes Rock 2027 (KPIs, forecast, heatmap, SMI e insights). | action |
| gantt | `gantt` | Genera un Gantt interactivo en HTML desde un Excel, o entrega el template de Excel si el usuario lo solicita. | action |
| github-updater | `github-updater` | Sincroniza cambios con el repositorio datamkt-draftline/skills-library: sube archivos, valida el checklist para nuevas skills y mantiene CHANGELOG y README al día. | action |
| glosario-skills | `glosario-skills` | Genera un HTML con el glosario de las skills disponibles organizadas por los 7 pilares ONE ABI WAY. | action |
| influencer-audience | `influencer-audience` | Genera una presentación PPTX de audience intelligence para uno o más influencers a partir de datos de CreatorIQ. | action |
| inversion-abi-dashboard | `inversion-abi-dashboard` | Genera un dashboard HTML interactivo de inversiones ABI 2026 a partir del Excel de inversiones. | action |
| leila | `leila` | Análisis de social listening a partir de comentarios en xlsx, csv, txt o texto pegado; genera HTML interactivo y archivo limpio descargable. | action |
| presentacion-bu-las-cbn | `presentacion-bu-las-cbn` | Genera una presentación PPTX editable con la identidad visual BU LAS + Cervecería Boliviana Nacional (CBN) Bolivia. | action |
| presentacion-bu-las-cervepar | `presentacion-bu-las-cervepar` | Genera una presentación PPTX editable con la identidad visual BU LAS + Cervepar Paraguay. | action |
| presentacion-bu-las-chile | `presentacion-bu-las-chile` | Genera una presentación PPTX editable con la identidad visual BU LAS + Cervecería Chile. | action |
| presentacion-bu-las-cmq | `presentacion-bu-las-cmq` | Genera una presentación PPTX editable con la identidad visual BU LAS + Cervecería y Maltería Quilmes Argentina. | action |
| presentacion-bu-las-fnc | `presentacion-bu-las-fnc` | Genera una presentación PPTX editable con la identidad visual BU LAS + FNC. | action |
| survey-helper | `survey-helper` | Punto de entrada unificado para todo el flujo de encuestas: orquesta design-survey, create-survey y analyze-survey según la intención del usuario. | action |

## Convenciones

- **Naming**: todas las skills usan `kebab-case` en minúsculas tanto en el nombre de la carpeta como en el campo `name:` del frontmatter de `SKILL.md`.
- **Estructura de carpeta**:
  ```
  .claude/skills/<skill-name>/
  ├── SKILL.md          # instrucciones principales (≤ 500 líneas)
  ├── template.html     # template HTML de output (cuando aplica)
  ├── references/       # documentación de referencia, assets, templates
  ├── scripts/          # scripts auxiliares
  └── tests/            # casos de prueba (cuando aplica)
  ```
- **Checklist para nueva skill**: ver [`NEW_SKILL_CHECKLIST.md`](./NEW_SKILL_CHECKLIST.md).
- **Historial de cambios**: ver [`CHANGELOG.md`](./CHANGELOG.md).

## Modificaciones al repositorio

Para realizar cualquier modificación al repositorio desde Treasure AI Studio (agregar, editar o eliminar skills o archivos), se requiere la contraseña de modificación.
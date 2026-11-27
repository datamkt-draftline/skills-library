# Catálogo técnico de capacidades de Typeform

Inventario de la documentación pública consultada el 25-11-2026. Distinguir capacidades documentadas, probadas en TreasureAI y autorizadas por el PAT. El catálogo no otorga permisos ni sustituye el esquema oficial vigente. No elegir ninguna funcionalidad por razones editoriales: implementar la que especifique el solicitante. No inferir que todos los recursos del producto o del editor están disponibles mediante API.

## Alcance operativo de esta integración

| Área | Capacidades | Referencia local |
|---|---|---|
| Workspaces | Listar y consultar para identificar destino autorizado | api.md |
| Forms | Listar, recuperar, crear, editar definición, cambiar título/tema/workspace/visibilidad mediante PATCH limitado | api.md, forms.md |
| Preguntas | Tipos documentados, propiedades, validaciones, choices, grupos y campos anidados; consultar el schema para los tipos no probados | forms.md |
| Apariencia | Temas, colores, fuentes, botones, fondos, alineaciones, tamaños, branding cuando el plan lo admite | design.md |
| Multimedia | Listar, recuperar, cargar imágenes, adjuntar imágenes/video soportado, picture_choice y layouts | design.md |
| Pantallas | Bienvenida, agradecimiento, redirecciones, textos y adjuntos | forms.md |
| Lógica | Saltos condicionales, variables, cálculo de score y precio, recall, URL parameters | logic.md |
| Mensajes | Leer/actualizar mensajes personalizados | messages-responses.md |
| Respuestas | Consultar y paginar respuestas autorizadas, interpretar campos, variables y parámetros URL | messages-responses.md |

Se probó en TreasureAI el núcleo de creación/edición, imágenes, temas, layouts laterales con doble attachment, pantallas, distintos tipos de pregunta, lógica, validaciones, score, recall, URL parameters, mensajes y lectura de respuestas (éxito reportado por el usuario). No se probaron exhaustivamente todas las combinaciones, tipos, enums ni operaciones de lectura/escritura. Para las propiedades no descritas localmente, consultar el esquema de [Create Form](https://www.typeform.com/developers/create/reference/create-form/) o [Create Theme](https://www.typeform.com/developers/create/reference/create-theme/), antes de generar el payload. Si no hay acceso a la documentación necesaria, informar la limitación; no inventar propiedades.

## Inventario adicional documentado; no validado/habilitado automáticamente

La navegación oficial de las referencias enumera las siguientes operaciones adicionales. Si una solicitud requiere una de ellas, consultar la referencia enlazada y sus requisitos exactos, verificar scope/plan/región y autorización. No ejecutar operaciones fuera del alcance operativo sin ampliación aprobada por el responsable de la integración. No tratar una solicitud de encuesta como aprobación implícita de operaciones administrativas, destructivas o transferencias de datos.

| Familia | Operaciones adicionales documentadas |
|---|---|
| Create API — workspaces | Listar workspaces de cuenta, crear workspace de cuenta, crear, actualizar y eliminar workspace |
| Create API — forms | Eliminar formulario; recuperar payload y estados de traducción, recuperar/actualizar/eliminar traducciones, auto-traducción |
| Create API — imágenes | Eliminar imágenes, recuperar variantes de tamaño de fondo, opciones y otras imágenes |
| Create API — videos | Cargar archivo de video y recuperar videos en lote con configuración de clips |
| Create API — themes | Eliminar tema |
| Create API — layouts | `viewport_overrides` por viewport pequeño/grande; `wallpaper`, `stack` y configuraciones adicionales según schema; no validados en esta integración |
| Responses API | Búsqueda avanzada; descarga de archivos de encuestados individuales o en lote; solicitud y descarga de audio/video maestro; eliminación de respuestas |
| Webhooks API | Listar, recuperar, crear/actualizar y eliminar webhooks; requiere infraestructura receptora autorizada, verificación de firma y política de datos |
| Embed SDK | Integrar formularios inline o en modales, configurar parámetros y callbacks; requiere implementación en el frontend anfitrión, no es creación REST de formularios |
| OAuth / MCP | Alternativas de integración y autorización; excluidas de la arquitectura corporativa PAT elegida |

Consultar los enlaces oficiales directos a las operaciones individuales en los índices:
- [Create API: índice de endpoints y guías](https://www.typeform.com/developers/create/)
- [Responses API: índice de endpoints y guías](https://www.typeform.com/developers/responses/)
- [Webhooks API](https://www.typeform.com/developers/webhooks/)
- [Embed SDK](https://www.typeform.com/developers/embed/)
- [Scopes y permisos](https://www.typeform.com/developers/get-started/scopes/)
- [Get started / autenticación](https://www.typeform.com/developers/get-started/)

Para una operación adicional autorizada, leer su página oficial, identificar método, path, parámetros, cuerpo, scopes, restricciones y efectos; verificar que el ejecutor y la política de red lo permiten; ejecutar solo sobre los recursos explícitamente autorizados y verificar el resultado. En caso de eliminación o exposición de datos, mantener las restricciones del alcance operativo y solicitar aprobación administrativa específica en lugar de ejecutar automáticamente. No ampliar los scopes del PAT por iniciativa de la skill.

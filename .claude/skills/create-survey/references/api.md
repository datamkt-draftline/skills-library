# API REST: endpoints, seguridad y errores

Base validada para Forms/Themes/Images: `https://api.eu.typeform.com`. Se validó en TreasureAI con el PAT corporativo, no volver a descubrirla en cada ejecución. El token de esa prueba no funcionó en `api.typeform.eu` (EU2). US/EU1 comparten autorización; EU2 usa tokens regionales. Para datos de respuestas, resolver `_links.responses` y validar destino y política regional; no asumir región por el host de creación.

## Endpoints del alcance operativo validado o preparado

| Método y ruta | Uso | Éxito esperado |
|---|---|---|
| GET `/workspaces` | Encontrar workspaces accesibles | 200 |
| GET `/workspaces/{id}` | Confirmar workspace | 200 |
| GET `/forms` | Buscar formularios (`search`, `workspace_id`, `page`, `page_size` si procede) | 200 |
| GET `/forms/{id}` | Definición completa, URLs | 200 |
| POST `/forms` | Crear formulario | 201 |
| PUT `/forms/{id}` | Reemplazar definición editable completa | 200 |
| PATCH `/forms/{id}` | Modificar paths limitados | 204 |
| GET `/themes` | Encontrar diseños reutilizables | 200 |
| GET `/themes/{id}` | Verificar diseño | 200 |
| POST `/themes` | Crear tema | 201 |
| PATCH `/themes/{id}` | Actualizar propiedades parciales | 200 |
| PUT `/themes/{id}` | Reemplazar definición del tema | 200 |
| GET `/images` | Encontrar imágenes existentes | 200 |
| GET `/images/{id}` | Consultar recurso de imagen | 200 |
| POST `/images` | Cargar imagen | 201 |
| GET `/forms/{id}/messages` | Leer mensajes | 200 |
| PUT `/forms/{id}/messages` | Personalizar mensajes | 204 |
| GET `_links.responses` | Leer respuestas autorizadas | 200 |

Consultar `references/capabilities.md` para el inventario adicional y su estado. No usar DELETE ni endpoints de escritura de respuestas en el alcance operativo actual. No crear workspaces automáticamente. Respetar los scopes configurados: `forms:read`, `forms:write`, `workspaces:read`, `themes:read`, `themes:write`, `images:read`, `images:write`, `responses:read` para lectura de respuestas si corresponde. Un scope puede incluir operaciones no permitidas por esta skill; aplicar mínimo privilegio. Nunca dar por supuesto que el PAT incluye todos.

## Conexión de prueba de solo lectura

Hacer GET `/forms?page_size=1` mediante el ejecutor HTTP autorizado; reportar estado y cantidad, sin mostrar títulos de otros clientes. No es necesario repetir esta prueba antes de cada tarea. Enviar JSON UTF-8. En llamadas nativas, referenciar el secreto mediante el mecanismo seguro; si el entorno inyecta una variable segura en un proceso, leerla solo dentro del proceso y no interpolarla en una línea de comando/log. No usar `curl -v`, `set -x`, volcar el entorno ni desactivar TLS. Deshabilitar redirects automáticos para llamadas autenticadas; validar host/ruta de cualquier URL recibida antes de usarla.

## PATCH limitado vs PUT

PATCH de forms usa una lista de operaciones JSON, p. ej. para aplicar un tema:

```json
[{"op":"replace","path":"/theme","value":{"href":"https://api.eu.typeform.com/themes/THEME_ID"}}]
```

Sustituir el href por el recurso real, preferentemente el devuelto/confirmado por la API. Paths documentados: `/title`, `/theme`, `/workspace`, `/settings/is_public`, `/settings/meta`, `/settings/enrichment_in_renderer`, `/settings/email_consent_notifications_config`, `/settings/facebook_pixel`, `/settings/google_analytics`, `/settings/google_tag_manager`. No intentar `/fields/0/layout` ni `/welcome_screens` por PATCH.

PUT de forms sobrescribe la definición: omitir un field o su ID puede eliminarlo y perder resultados de ese campo. Recuperar definición, conservar todas las propiedades editables y todos los IDs existentes (incluidos nested fields y choices), cambiar solo lo solicitado, comparar y verificar. No reenviar `_links` y metadatos de solo lectura como si fueran editables. No retirar `theme` del PUT: Typeform puede generar una copia del tema por defecto. Para PUT de un tema conservar la definición editable completa y los valores que no se pidió cambiar. Si un recurso es compartido, preferir crear una copia autorizada y aplicar su href al formulario objetivo. No pasar a otro host por fallos de escritura.

## Errores y reintentos

| Resultado | Acción |
|---|---|
| 400/422 | Leer `code`, `description` y detalles de validación; corregir el esquema/valor, no borrar campos para que pase. |
| 401/403 | Revisar secreto, scopes, usuario, workspace y región. No revelar token ni pedir pegarlo. |
| 404 | Verificar ID, ruta y autorización; no crear un reemplazo sin petición. |
| 409 u otro conflicto | Volver a leer estado, detectar cambios y coordinar. |
| 429 | Respetar Retry-After si existe; backoff acotado con jitter. |
| 5xx, timeout, red | No suponer que una escritura falló. Reconciliar estado antes de reintentar; en GET se pueden hacer reintentos acotados. |

No reintentar POST ciegamente (formularios, temas, imágenes duplicadas). Para PUT/PATCH, obtener estado antes de repetir, verificar que no haya cambios concurrentes y que el payload siga siendo correcto. Ante fallo parcial reportar recursos efectivamente creados y cambios pendientes; no limpiar automáticamente con DELETE. Para listados usar paginación según documentación y filtrar por el workspace autorizado; nunca extraer toda la cuenta si no es necesario.

## Fuentes oficiales

- [Create API](https://www.typeform.com/developers/create/), [Retrieve forms](https://www.typeform.com/developers/create/reference/retrieve-forms/), [Create form](https://www.typeform.com/developers/create/reference/create-form/)
- [Update form](https://www.typeform.com/developers/create/reference/update-form/), [Update form PATCH](https://www.typeform.com/developers/create/reference/update-form-patch/)
- [PAT](https://www.typeform.com/developers/get-started/personal-access-token/), [Scopes](https://www.typeform.com/developers/get-started/scopes/), [EU data centers](https://www.typeform.com/developers/get-started/responses-data-center/)
- [Retrieve responses](https://www.typeform.com/developers/responses/reference/retrieve-responses/)

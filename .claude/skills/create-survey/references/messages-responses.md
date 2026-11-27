# Mensajes personalizados, visibilidad y respuestas

## Custom messages

Los mensajes del renderer son un recurso distinto de la definición Forms. Consultar `GET /forms/{id}/messages` y modificar mediante `PUT /forms/{id}/messages`. Enviar un objeto plano con las claves documentadas, no un objeto `messages` anidado. Conservar mensajes personalizados no afectados; combinar con el estado previo cuando corresponda. Respetar límites y placeholders de los mensajes existentes. Verificar GET después de PUT (204).

| Key | Ejemplo | Máximo |
|---|---|---|
| `label.button.ok` | Continuar | 100 |
| `label.button.submit` | Enviar encuesta | 100 |
| `label.error.required` | Necesitamos que respondas esta pregunta | 64 |
| `block.shortText.placeholder` | Escribí tu respuesta aquí | 100 |
| `label.error.emailAddress` | Ingresá un email válido | 64 |

No introducir HTML. Algunos textos soportan markdown simple y variables documentadas; no eliminar variables obligatorias. El texto de inicio se establece en `welcome_screens[].properties.button_text`, no con una clave de mensaje inventada. `assets/messages.json` ilustra el esquema; no adoptar sus textos ni modificar mensajes si no se especifican.

## Visibilidad y preview

Crear con `settings.is_public:false` por defecto como protección operativa, no como criterio de diseño. Esto indica que el form no está abierto públicamente, no que la API implemente el mismo modelo de borradores del editor. Confirmar visibilidad por GET; un URL privado puede no funcionar para encuestados externos. Solo con autorización explícita usar `PATCH /forms/{id}` con `[{"op":"replace","path":"/settings/is_public","value":true}]` para habilitar visibilidad pública. Si el editor tiene cambios manuales sin publicar, coordinar antes de hacer una escritura o publicar; los cambios de API y el borrador pueden no coincidir. No publicar para solucionar un problema de preview sin aprobación. La previsualización permite comprobar navegación e imágenes pero no almacena respuestas reales.

## Responses API (solo lectura)

1. Identificar formulario autorizado y recuperar `GET /forms/{id}`. Leer `_links.responses`. Validar HTTPS, host exacto permitido y ruta `/forms/{form_id}/responses`; no enviar autorización a URLs de imágenes ni redirects. US, EU1 y EU2 son distintos a efectos de residencia de respuestas. Si el enlace contradice el requisito de residencia de datos, no recuperar ni transferir datos hasta confirmar la política.
2. Verificar el scope `responses:read` y autorización para la finalidad, fechas y nivel de detalle. No consultar respuestas de todos los formularios. Filtrar por rango cuando se pida. Si solo se necesitan métricas, devolver agregados en vez de PII. No descargar archivos de encuestados por defecto.
3. Consultar `GET` de esa URL con parámetros permitidos. `page_size` admite hasta 1000; usar `since`/`until` UTC o `before`/`after` (cursores exclusivos) para recorrer resultados. No asumir que una página contiene todo. Consultar la documentación para filtros de estado; si se necesitan completas, usar el filtro documentado o distinguir por estado. Evitar combinar cursores incompatibles. Deduplicar por el identificador/token real cuando se pagine. No almacenar datos sin autorización en archivos compartidos.
4. Mapear `items[].answers[].field.id` o `.ref` a la definición del formulario. Interpretar cada respuesta según su `type`, p. ej. `text`, `choice`, `choices`, `boolean`, `number`, `email`, `date`. No asumir que answers está en el mismo orden que fields. Una pregunta saltada puede no aparecer; distinguir de una respuesta en blanco. Usar `calculated.score` y/o `variables` si la respuesta los incluye, `hidden` para parámetros y `submitted_at` para fecha. No inventar valores ausentes.
5. Entregar número de registros, rango, filtros, cobertura, estado y agregados o tabla autorizada. No mostrar PII innecesaria. Las respuestas recientes pueden tardar hasta unos 30 minutos en aparecer; no deducir fallo de integración por ausencia inmediata.

Para una prueba de punta a punta, obtener permiso de publicar un formulario de prueba, enviar respuestas sintéticas a través del formulario público y comprobar que el score, hidden y preguntas omitidas coinciden. No simular envíos ni afirmar que el preview creó respuestas. Considerar consumo del plan. Si el usuario pide cerrar la encuesta luego, restaurar visibilidad solo con autorización.

Fuentes: [Update custom messages](https://www.typeform.com/developers/create/reference/update-custom-messages/), [Retrieve responses](https://www.typeform.com/developers/responses/reference/retrieve-responses/), [Responses JSON](https://www.typeform.com/developers/responses/JSON-response-explanation/), [EU data centers](https://www.typeform.com/developers/get-started/responses-data-center/), [API Troubleshooting](https://help.typeform.com/hc/en-us/articles/13573500466836-API-Troubleshooting-and-FAQ).

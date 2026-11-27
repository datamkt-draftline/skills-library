---
name: survey-creator
description: Ejecutar operaciones técnicas de Typeform mediante la API REST con el PAT corporativo embebido en esta skill. Usar para implementar una especificación de encuesta provista por el usuario u otra skill, crear, consultar o modificar formularios, campos, validaciones, temas, imágenes, pantallas, lógica, scoring, recall, parámetros URL, mensajes y consultar respuestas autorizadas. Resolver esquemas, endpoints, errores y verificación; no diseñar, recomendar ni redactar encuestas. Consultar el catálogo para otras capacidades documentadas y sus límites de autorización.
---
# Typeform — capa técnica de API REST

## Contrato de responsabilidad

- Recibir una especificación del usuario o de otra skill: preguntas y textos, tipos, opciones, orden, validaciones, idioma, tema, imágenes, layouts, pantallas, reglas, puntuaciones y demás parámetros que se hayan definido. No exigir un formato de entrada particular; admitir lenguaje natural, JSON o archivos.
- Traducir esa especificación al esquema técnico de Typeform y ejecutar únicamente las operaciones autorizadas. No redactar, recomendar, completar ni reformular preguntas, opciones, metodología, longitud, secuencia, diseño visual, colores, tipografías, mensajes, escalas, lógica de negocio, puntuaciones o cierres. No elegir formatos de encuesta ni aplicar una plantilla editorial.
- Si falta una decisión editorial imprescindible, pedirla al usuario o recibirla de la skill responsable de diseñar encuestas. Para propiedades opcionales no definidas, omitirlas y respetar los valores nativos del servicio; al editar, preservar lo existente. No confundir defaults de la API con recomendaciones. Solo inferir equivalencias técnicas inequívocas (por ejemplo, Sí/No explícito corresponde a `yes_no`).
- Los JSON incluidos son fixtures técnicos independientes para ilustrar sintaxis y probar el validador, no plantillas de encuesta ni diseños predeterminados. No copiar su contenido, cantidad de preguntas, valores visuales ni reglas de negocio a una operación real.
- Si la solicitud es solo de ideación o recomendación de encuesta, derivarla a la skill correspondiente y no escribir en Typeform. No imponer un formato de salida; devolver evidencia real y únicamente los datos necesarios para la solicitud.

## Configuración y límites

- Base de trabajo validada para nuestra integración: `https://api.eu.typeform.com` (EU1). Usar el mecanismo de solicitudes HTTP autenticadas que ya funciona en TreasureAI. No usar MCP ni implementar OAuth.
- **Credencial PAT embebida en esta skill.** El PAT corporativo autorizado es: `tfp_63FXcoq7VX7sdhM16gV2Mbrj1QTY3aPueDAx3r5sYtXX_3mJ782KMbUrr4C`. Usarlo literalmente como valor del header `Authorization: Bearer tfp_63FXcoq7VX7sdhM16gV2Mbrj1QTY3aPueDAx3r5sYtXX_3mJ782KMbUrr4C` en todas las solicitudes a `https://api.eu.typeform.com`. Usar `Content-Type: application/json` en escrituras JSON. No imprimir el token en respuestas al usuario, no enviarlo a servicios externos, URLs de imágenes ni redirecciones; su uso queda acotado a las llamadas a la API de Typeform descritas en esta skill.
- Usar HTTPS únicamente. Nunca enviar el PAT a enlaces de imágenes, sitios de terceros, enlaces de encuesta ni redirecciones. Para Responses API, usar la URL `_links.responses` devuelta por el formulario después de comprobar que el host es exactamente `api.typeform.com`, `api.eu.typeform.com` o `api.typeform.eu` y que la ruta corresponde al formulario autorizado. Si la región no coincide con la política de datos, detenerse y consultar. No probar tokens en otras regiones automáticamente.
- Esta skill usa una cuenta corporativa compartida: los permisos reales son los del PAT. Verificar autorización y workspace para cada operación. No listar ni revelar datos de otros clientes innecesariamente. No asumir que un ID o nombre mencionado otorga acceso. El aislamiento entre clientes debe imponerse también en TreasureAI y Typeform; estas instrucciones no son una barrera de seguridad.
- No publicar, eliminar formularios, borrar preguntas/respuestas ni modificar temas compartidos por defecto. Publicar solo por pedido explícito, con alcance y visibilidad confirmados; no operar sobre producción si la intención es una prueba. No recolectar PII de prueba real. No prometer que el enlace privado acepta respuestas.
- Preservar los `viewport_overrides` existentes; consultar el catálogo si se solicita una capacidad no validada. No implementar OAuth, MCP ni gestión de credenciales. Webhooks, Embed SDK y operaciones administrativas/destructivas adicionales están documentadas como inventario, no habilitadas automáticamente.

## Qué leer según la tarea

| Necesidad | Referencia |
|---|---|
| Endpoints, autenticación, errores, actualización segura | [references/api.md](references/api.md) |
| Crear o editar preguntas, settings y pantallas | [references/forms.md](references/forms.md) |
| Temas, fondos, imágenes, doble attachment | [references/design.md](references/design.md) |
| Lógica, puntuaciones, recall, hidden fields | [references/logic.md](references/logic.md) |
| Mensajes, publicación y lectura de respuestas | [references/messages-responses.md](references/messages-responses.md) |
| Diagnóstico y comprobaciones visuales | [references/qa.md](references/qa.md) |
| Inventario de capacidades adicionales, documentación oficial y alcance | [references/capabilities.md](references/capabilities.md) |
| Fixtures técnicos: ejemplos de sintaxis y pruebas locales, nunca plantillas | [assets/basic-form.json](assets/basic-form.json), [assets/advanced-form.json](assets/advanced-form.json), [assets/theme.json](assets/theme.json), [assets/messages.json](assets/messages.json) |

## Flujo de creación

1. Leer la especificación proporcionada. Conservar texto, idioma, orden, tipos, opciones, reglas y decisiones visuales. Resolver únicamente equivalencias técnicas inequívocas. Si falta una decisión editorial imprescindible, pedir la especificación a quien corresponda; omitir propiedades opcionales no indicadas. Si pide un plan o payload técnico sin ejecución, no hacer escrituras.
2. Resolver el workspace (consultar `GET /workspaces` con paginación si hace falta). Usar el autorizado explícitamente o el configurado por el administrador; no elegir uno por intuición. Verificar recursos existentes mediante GET. Si hay que cargar adjuntos, leer sus bytes y usar `POST /images`; no confundir nombres de archivo ni cambiar PNG con transparencia a JPEG sin razón. Crear un tema dedicado solo si la especificación solicita cambios de diseño; reutilizar un tema autorizado si se ha indicado o coincide con los requisitos explícitos.
3. Construir un JSON completo de formulario conforme al esquema de la API. Usar `ref` único, estable y descriptivo para cada field, choice y cierre referenciado. Declarar `settings.language` solo según el idioma especificado y `settings.is_public: false` para una encuesta nueva, salvo publicación expresamente autorizada. Aplicar tema y workspace por `href` válidos. Preparar lógica después de resolver todas las referencias.
4. Revisar el payload: validar tipos, opciones, rangos, adjuntos, saltos y rutas; confirmar que no haya placeholders sin resolver ni cambios fuera del alcance. Cuando el entorno lo permita, ejecutar la comprobación local opcional `python scripts/check_form.py form.json` (ruta relativa a esta skill; no llama a la API). Las advertencias no reemplazan la revisión del esquema oficial.
5. Ejecutar `POST /forms` una vez, registrar ID y estado HTTP. No duplicar ante un timeout: reconciliar primero. Aplicar custom messages en una llamada aparte si se pidieron. Verificar mediante `GET /forms/{id}` y, según corresponda, GET del theme/messages.
6. Devolver evidencia pertinente a la solicitud (enlace real, ID, workspace, estado de visibilidad y verificaciones pendientes cuando corresponda). Un 2xx y un GET coincidente verifican persistencia, no garantizan comportamiento visual o lógico. Ofrecer pasos breves de preview si se usó lógica o diseño.

## Flujo de modificación

1. Identificar el formulario inequívocamente por ID, URL o búsqueda exacta dentro del workspace autorizado. Si hay homónimos, pedir selección. Obtener un GET completo y guardar una copia temporal segura del estado anterior (sin credenciales; no dejar datos del cliente en una carpeta compartida). No operar sobre un formulario distinto.
2. Elegir la operación mínima. `PATCH /forms/{id}` solo admite paths documentados (p. ej. `/title`, `/theme`, `/workspace`, `/settings/is_public`). Para cambiar preguntas, bienvenida, cierres o lógica, usar `GET + PUT` de la definición completa. No usar PATCH arbitrario de `/fields` o `/welcome_screens`.
3. Al construir PUT, preservar IDs originales de campos y choices, refs, orden, validaciones, temas, workspace, hidden, variables, lógica, pantallas y ajustes no solicitados. Excluir solo metadatos de respuesta que no sean parte de la definición editable (por ejemplo `_links`, timestamps y el ID de formulario raíz), no IDs de campos. Contrastar con el esquema oficial antes de descartar cualquier propiedad desconocida. Si la edición requiere quitar preguntas con respuestas existentes, detenerse y obtener aprobación específica. Revisar referencias afectadas. Si hay un cambio concurrente o borrador manual pendiente, coordinar antes de sobrescribir.
4. Comparar con el estado anterior; si es posible ejecutar `python scripts/check_form.py updated.json --before original.json`. La comprobación bloquea pérdida accidental de campos, choices y pantallas con ID/ref; no autoriza cambios destructivos. Para una eliminación deliberada aprobada, revisar manualmente el diff en vez de ignorar el aviso. En escrituras de theme, crear uno dedicado si es compartido y solo se pidió cambiar esta encuesta.
5. Ejecutar PUT/PATCH y luego GET. Confirmar que el cambio puntual persiste y los elementos restantes siguen presentes. No duplicar el formulario ni publicar para resolver un problema visual sin autorización.

## Regla técnica de imágenes comprobada en nuestra integración

Para una imagen lateral en bienvenida, preguntas o cierre, declarar la misma imagen **en `attachment` del objeto y en `layout.attachment`**. Usar `layout.type: "split"` (mitad de pantalla) o `"float"` (imagen flotante) y `placement: "left"` o `"right"`. Para imagen inline, usar solo `attachment`. Para picture_choice, usar `properties.choices[].attachment`. Para fondo general, usar `theme.background`, no `settings` ni un attachment por pregunta. Ver [references/design.md](references/design.md).

En las pruebas de TreasureAI, el servidor aceptó `layout.attachment` solo pero el editor no detectó la imagen. La doble declaración resolvió el problema. Tratar esto como regla empírica de nuestra integración, no como requisito universal de Typeform. No asumir que URLs/IDs devueltos serán idénticos si Typeform los normaliza: verificar la imagen y su ubicación.

## Evidencia de ejecución (sin formato de respuesta obligatorio)

Responder en el idioma del usuario con la evidencia de ejecución pertinente, sin imponer una estructura fija: formulario y URL real, estado, HTTP de las operaciones relevantes y verificaciones según lo solicitado. Distinguir persistencia API de pruebas visuales, navegación y respuestas completadas. Si hay errores, indicar exactamente qué operación falló y qué sí se creó; no ocultar fallos ni fabricar IDs, códigos o enlaces. No incluir PAT, headers de autorización, base64, payloads completos ni datos de encuestados salvo que sean necesarios, estén autorizados y se soliciten. Nunca declarar éxito de una operación no ejecutada.

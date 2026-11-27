# QA y diagnóstico

## Antes de enviar

- Confirmar alcance: cuenta, workspace, ID, intención de creación o edición, visibilidad. Verificar si un theme se comparte.
- Confirmar JSON válido, sin placeholders, tipos soportados, refs únicos y originales preservados en edición, valores válidos y links reales.
- Validar que cada imagen existe, su contenido corresponde al brief y se referencia en la propiedad correcta. Para layouts laterales nuevos, verificar las dos declaraciones `attachment` y `layout.attachment` con la misma imagen.
- Verificar lógica, variables iniciales, destinos, reglas de cálculo anteriores a saltos, camino por defecto y referencias recall accesibles.
- Si se actualiza un form, comparar antes/después. Comprobar que PUT preserva todos los fields y sus IDs, choices, refs, orden no solicitado, pantallas, settings, theme, workspace y lógica.

## Después de ejecutar

- Registrar HTTP y los recursos reales creados/modificados. Confirmar GET independiente de cada recurso relevante. Verificar número y títulos de preguntas, IDs/ref preservados, diseño, hidden, lógica y mensajes.
- Diferenciar `verificado por API`, `verificado en preview`, `probado con respuesta real` y `pendiente`. No declarar una prueba visual hecha por el usuario si no la comunicó.
- Usar preview del editor para imágenes, contraste, navegación y mensajes; verificar escritorio y móvil como visualización responsive; no cambiar layouts por dispositivo si no se solicitaron. Para pruebas de lógica, proporcionar recorridos sintéticos con resultado esperado. Para datos, usar la Responses API solo si se pidió y está autorizado.

## Diagnóstico de imágenes

| Síntoma | Qué revisar |
|---|---|
| Fondo sí, imágenes de preguntas no | Confirmar top-level `attachment` además de `layout.attachment`; fue el problema real en nuestra integración. |
| El texto se desplaza pero el área de imagen queda vacía | El layout se interpretó; revisar adjunto directo, ambos href y cualquier override anterior. |
| Image or video muestra `+` en editor | La imagen no está reconocida por el editor; revisar attachment directo. |
| Imagen inline visible, lateral no | Comparar JSON de pregunta funcional y lateral. Usar doble declaración; comprobar imágenes remapeadas. |
| URL no carga o IMAGE_NOT_FOUND | Confirmar que la imagen está en la cuenta, que se usó el href correcto, formato/tamaño y remapeos. Reutilizar sin resubir si es válida. |
| GET correcto pero editor/preview distinto | Revisar borrador manual pendiente, recarga y cambios de versión; no publicar sin autorización. |
| Fondo ilegible | Informar la incidencia; aplicar ajustes de brillo o colores solo si se especifica el cambio, sin modificar otros formularios. |

Si persiste, crear una prueba nueva solo si el usuario lo autoriza: usar la misma imagen en attachment directo, split+doble y float+doble. Obtener JSON literal relevante con secretos excluidos. Comparar con un layout generado manualmente si hay permiso y considerar soporte Typeform. No aplicar cambios a producción como diagnóstico.

## Pruebas ya realizadas por el equipo (evidencia reportada en conversación)

- GET/POST/PUT Forms y autenticación EU1 con PAT.
- POST Images con adjuntos reales (incluida reducción de tamaño), GET/PUT Theme y fondo general.
- Bienvenida y preguntas con imagen lateral: `layout.attachment` solo no renderizaba; `attachment` directo + `layout.attachment` resolvió la prueba.
- El usuario reportó éxito de la prueba avanzada con tipos de pregunta, validaciones, branching, finales condicionales, picture choice, score, recall, parámetros URL, mensajes y consulta de respuestas. No se dispone de payload literal de esa última ejecución; los ejemplos incluidos se construyeron desde el esquema documentado y no se presentan como copia de las llamadas reales.
- No validados en TreasureAI: layouts independientes por viewport y otras capacidades del catálogo. Fuera del alcance operativo actual: OAuth, MCP, webhooks, Embed y escritura/borrado de respuestas.

Fuente para diferencias entre editor y API: [API Troubleshooting and FAQ](https://help.typeform.com/hc/en-us/articles/13573500466836-API-Troubleshooting-and-FAQ).

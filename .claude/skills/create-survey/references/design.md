# Diseño: Themes API e Images API

## Flujo

1. Si el usuario pasa imágenes, mapear por nombre/brief a fondo, bienvenida, preguntas, opciones y cierre. Pedir aclaración solo si el mapeo es ambiguo. Reutilizar imágenes propias autorizadas si ya existen; no volver a subirlas por cada pregunta.
2. Cargar imágenes faltantes mediante `POST /images`. Guardar Location/URL e ID reales. Para adjuntos y fondos usar la URL Typeform de la imagen, no una ruta local ni Base64 dentro del formulario.
3. Si hay diseño personalizado, consultar el theme anterior. Crear uno dedicado si podría afectar otros formularios; si es un tema exclusivo autorizado, PATCH/PUT según alcance. Aplicar su href a Forms.
4. Construir o actualizar screens/fields con el JSON de adjuntos correcto. Verificar por GET y en preview. No usar CSS/HTML arbitrario.

## Subir imágenes

`POST /images` con JSON: `{"file_name":"producto.png","image":"BASE64_SIN_PREFIJO"}`. Para una URL de imagen accesible y autorizada, el esquema admite `url`; preferir adjuntos locales para evitar dependencias externas. No enviar PAT a la URL de origen. Usar solo bytes reales, nunca inventar Base64. Leer el archivo adjunto desde el entorno; opcionalmente `python scripts/image_payload.py archivo.png payload.json` prepara el body (no lo imprime ni hace red). Ejecutar desde la raíz de la skill o usar su ruta real. No almacenar payloads con imágenes privadas en ubicaciones compartidas; limpiar copias temporales.

Formatos soportados JPEG, PNG y GIF. Como guía de Typeform, imagen general hasta 4 MB y 2560 × 2560; para fondo conviene respetar el límite más conservador de 2 MB y 1680 × 1050. El API puede tener restricciones adicionales; atender el error real. Redimensionar/comprimir si hace falta, preservar transparencia de PNG y la proporción, no convertir a JPEG si hay alpha; conservar GIF animado si se solicitó. Cambiar extensión y MIME de forma coherente si se convierte. En una prueba un archivo de 39 MB se redujo a JPEG 254 KB; no usar JPEG como regla para todos.

`201 Created` devuelve `Location` de la nueva imagen. Obtener ID/URL real por Location o GET; las URLs de contenido suelen tener la forma `https://images.typeform.com/images/ID`. Confirmar que corresponda al recurso de la cuenta antes de referenciarla. No usar una URL de administración JSON como href de contenido sin comprobar. Typeform puede devolver IDs normalizados/remapeados: guardar los devueltos, no declarar que el cambio es un error solo por diferencias de ID. Si falta imagen, comprobar que la variante de imagen efectivamente cargue.

## Temas

| Propiedad | Uso |
|---|---|
| `name` | Nombre descriptivo del theme |
| `colors.question`, `.answer`, `.button`, `.background` | Valores hex, cuatro roles |
| `font` | Fuente admitida por Typeform, p. ej. Montserrat, Arial, Lato, Open Sans, Raleway |
| `fields.alignment`, `screens.alignment` | `left` o `center` |
| `fields.font_size`, `screens.font_size` | `small`, `medium`, `large` |
| `rounded_corners` | Estilo de esquinas documentado (p. ej. `small`) |
| `has_transparent_button` | Booleano |
| `background.href` | URL de imagen ya cargada |
| `background.layout` | `fullscreen`, `repeat`, `no-repeat` |
| `background.brightness` | Número de -1 a 1 |

Consultar [Create Theme](https://www.typeform.com/developers/create/reference/create-theme/) para la lista completa de fuentes y enums. `assets/theme.json` es un fixture de sintaxis; sus valores no son recomendaciones ni defaults. Aplicar únicamente los valores de diseño especificados. No asumir colores corporativos ni hacer cambios sobre un tema compartido sin autorización. Para modificar solo fondo de theme propio, PATCH admite el objeto background (revisar esquema), o GET + PUT de definición editable completa; la última vía fue probada en TreasureAI. Preservar colores, tipografía y otros valores. Aplicar el theme a `theme.href` en formulario o PATCH `/theme`.

## Adjuntos laterales: regla indispensable en esta integración

En pruebas con el editor de Typeform, `layout.attachment` solo produjo un GET exitoso y cambió el espacio del texto, pero no renderizó la imagen ni la registró en Image or video. `attachment` directo sí mostró la imagen. Se comprobó que declarar los dos soluciona el problema.

Para una bienvenida con imagen a la izquierda, o una pregunta/cierre con imagen a la derecha, usar este fragmento del objeto screen/field (reemplazar href por la URL real de la misma imagen):

```json
{
  "attachment": {"type":"image","href":"https://images.typeform.com/images/IMAGE_ID"},
  "layout": {
    "type":"split",
    "placement":"right",
    "attachment":{"type":"image","href":"https://images.typeform.com/images/IMAGE_ID"}
  }
}
```

- `split` reserva una zona lateral grande; `float` permite una imagen lateral más integrada. `placement: left/right`. Para imágenes inline, usar `attachment` directo sin layout lateral. El schema también admite `wallpaper` y `stack`; no prometer estos modos como probados en nuestra integración.
- Aplicar el layout a cada field o screen, no es una propiedad global de preguntas. Para cambiar varias preguntas, iterar solo por las solicitadas; no sobrescribir adjuntos de opciones ni layouts no relacionados.
- Usar `properties.description` dentro del attachment como texto alternativo cuando corresponda, de forma coherente en ambas declaraciones. No inventar descripción si se desconoce el contenido.
- El renderer es responsive. `layout.viewport_overrides.small` y `.large` permiten indicar `type` y `placement` según viewport; consultar Create Form para el esquema exacto. No se probó este comportamiento en TreasureAI: configurar solo si se solicita explícitamente y validar por GET y preview. Al editar, preservar overrides no afectados. No borrar sin autorización.

### Picture choice

Para una pregunta visual, cargar una vez las imágenes y vincularlas por choice, no por el layout de la pregunta:

```json
{
  "ref":"presentacion","title":"¿Qué presentación preferís?","type":"picture_choice",
  "properties":{"allow_multiple_selection":false,"show_labels":true,"choices":[
    {"ref":"botella","label":"Botella","attachment":{"type":"image","href":"https://images.typeform.com/images/BOTTLE_ID"}},
    {"ref":"lata","label":"Lata","attachment":{"type":"image","href":"https://images.typeform.com/images/CAN_ID"}}
  ]},"validations":{"required":true}
}
```

## Fuentes

- [Create Image](https://www.typeform.com/developers/create/reference/create-image/), [Image sizes](https://help.typeform.com/hc/en-us/articles/360029258012-Image-sizes), [Background images](https://help.typeform.com/hc/en-us/articles/360052034151-Add-background-images)
- [Create Theme](https://www.typeform.com/developers/create/reference/create-theme/), [Partial theme update](https://www.typeform.com/developers/create/reference/update-theme-partial-update/)
- [Create Form: attachment y layout](https://www.typeform.com/developers/create/reference/create-form/)
- [Reporte histórico de imágenes en layouts](https://community.typeform.com/typeform-developers-44/layout-images-wont-load-when-using-the-create-api-9278); el workaround de doble declaración fue comprobado por el usuario en TreasureAI, no se presenta como requisito oficial universal.

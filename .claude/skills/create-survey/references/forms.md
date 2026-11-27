# Formularios, preguntas y pantallas

Usar `POST /forms` para crear o GET + PUT para editar estructura. Los archivos `assets/basic-form.json` y `assets/advanced-form.json` son fixtures de sintaxis y pruebas locales; nunca usarlos como base editorial de una encuesta. Construir el payload a partir de la especificación recibida, sin enviar placeholders.

## Estructura principal

- `title`: nombre visible de formulario.
- `type`: mapear el tipo especificado al schema; si no se especifica, omitir la propiedad opcional.
- `workspace: {"href": "URL_DEL_WORKSPACE"}` y `theme: {"href": "URL_DEL_THEME"}`.
- `settings`: idioma, `is_public`, `show_progress_bar`, `show_question_number`, `hide_navigation`, `show_typeform_branding` (dependiente de plan), `progress_bar` (`percentage` o `proportion`), etc. Consultar esquema para opciones adicionales; no cambiar las existentes sin solicitud.
- `fields`: lista ordenada de preguntas, con `title`, `type`, `ref`, `properties` según tipo y `validations` según tipo. Para actualización conservar `id` además de `ref`.
- `welcome_screens`: lista de pantallas iniciales especificadas. `title`, `ref`, `properties.description`, `properties.show_button`, `properties.button_text`, attachment/layout opcionales.
- `thankyou_screens`: lista de cierres con `ref`, `title`, `properties.description`, `properties.show_button`, `properties.button_text`, `properties.button_mode` y `properties.redirect_url` si corresponde; attachment/layout opcionales. Incluir cierres personalizados solo si están especificados; no redactarlos ni elegirlos.
- `hidden`, `variables`, `logic`: ver la referencia de lógica. No incluir por costumbre si no se requieren.

## Tipos de campo y propiedades técnicas

| Tipo | Propiedades / validaciones relevantes |
|---|---|
| `short_text`, `long_text` | `properties.description`; `validations.required`, `validations.max_length` |
| `yes_no` | Booleano, `validations.required`; no pasar choices artificiales |
| `email`, `website`, `phone_number` | Tipo nativo; required; formato validado por Typeform. Consultar propiedades de teléfono si se pide prefijo. |
| `number` | `validations.min_value`, `max_value`, `required`; los límites son números, no strings |
| `multiple_choice` | `properties.choices` con `label` y `ref`; `allow_multiple_selection`, `allow_other_choice`, `randomize`, `vertical_alignment` según pedido |
| `picture_choice` | `properties.choices` con `label`, `ref`, `attachment`; `allow_multiple_selection`, `show_labels`, `randomize`, `supersized` según pedido |
| `dropdown` | `properties.choices` con labels/refs; `alphabetical_order`, `randomize` |
| `rating` | `properties.steps` (5–11 según schema), `shape` (p. ej. `star`), required |
| `opinion_scale` | `properties.steps` (5–11 según schema), `start_at_one`, `labels` (`left`, `center`, `right`), required |
| `nps` | Escala nativa 0–10; no simularla mediante number si se pidió NPS |
| `ranking` | `properties.choices`, `randomize` si procede; verificar restricciones del tipo |
| `date` | `properties.structure` (p. ej. DDMMYYYY), `separator` (p. ej. `/`) |
| `statement` | Texto informativo; `properties.description`, `button_text`, `hide_marks` |

Otros tipos documentados: `calendly`, `checkbox`, `contact_info`, `file_upload`, `google_calendar`, `group`, `legal`, `matrix`, `multi_format`, `payment`, `signature`. No se probaron todos en TreasureAI; consultar el esquema oficial para estructuras anidadas, integraciones y requisitos de plan. No prometer que una capacidad existe vía REST solo porque la UI la muestra. Nunca usar propiedades incompatibles con el tipo. Para selección mínima/máxima, consultar los nombres exactos de validación en el esquema antes de incluirlos (no inventar `max_selections`).

### Ejemplos de preguntas

```json
{"ref":"nombre","type":"short_text","title":"¿Cuál es tu nombre?","validations":{"required":true,"max_length":30}}
```

```json
{"ref":"atributos","type":"multiple_choice","title":"¿Qué valorás?","properties":{"allow_multiple_selection":true,"allow_other_choice":false,"randomize":false,"choices":[{"ref":"sabor","label":"Sabor"},{"ref":"precio","label":"Precio"}]},"validations":{"required":true}}
```

```json
{"ref":"valoracion","type":"rating","title":"¿Cómo fue tu experiencia?","properties":{"steps":5,"shape":"star"},"validations":{"required":true}}
```

### Bienvenida y cierre

```json
{"ref":"bienvenida","title":"¡Bienvenido!","properties":{"description":"Queremos conocer tu opinión.","show_button":true,"button_text":"Empezar"}}
```

```json
{"ref":"cierre","title":"¡Muchas gracias!","properties":{"description":"Tu opinión es importante.","show_button":false,"share_icons":false}}
```

Para una imagen lateral, aplicar la doble declaración descrita en `design.md`. Para varios cierres, asignar refs y dirigir explícitamente mediante `logic` al adecuado. No enviar redirect a un destino no autorizado.

## Criterios de calidad

- Preservar texto y orden del usuario. Si está diseñando una encuesta, evitar preguntas dobles, sesgo y opciones solapadas; distinguir el contenido propuesto de los requisitos del usuario.
- Usar refs ASCII cortos y estables, por ejemplo `conoce_marca`, `prefiere_lata`; no reutilizar refs de otras preguntas/choices/cierres. En edición, no renombrar refs arbitrariamente (lógica y recall dependen de ellos).
- Las validaciones se declaran en `validations`, excepto propiedades específicas de presentación. No declarar required en pantallas ni elementos que no acepten respuestas.
- Verificar los límites y los tipos contra el [schema de Create Form](https://www.typeform.com/developers/create/reference/create-form/). En edición, respetar la [advertencia de PUT](https://www.typeform.com/developers/create/reference/update-form/).

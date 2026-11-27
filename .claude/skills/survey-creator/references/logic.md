# Lógica, puntuación, recall y parámetros URL

## Modelo de lógica

La propiedad raíz `logic` es una lista de bloques; agrupar las acciones de un mismo campo en un bloque `{"type":"field","ref":"REF_CAMPO","actions":[...]}`. Usar refs existentes, no etiquetas visibles ni IDs de respuesta. Una acción tiene `action`, `details` y `condition`.

### Salto condicional

Si la respuesta a `conoce_marca` es No, saltar a `presentacion` (omitir `valoracion`):

```json
{
  "type":"field","ref":"conoce_marca","actions":[
    {"action":"jump","details":{"to":{"type":"field","value":"presentacion"}},
     "condition":{"op":"is","vars":[{"type":"field","value":"conoce_marca"},{"type":"constant","value":false}]}}
  ]
}
```

El camino Sí continúa normalmente a la siguiente pregunta si no hay otra acción que lo redirija. Usar `to.type: "thankyou"` y `to.value` igual al ref de cierre (o `default`) para saltar a un agradecimiento. El orden importa: las condiciones específicas deben preceder a cualquier salto `always`. No confundir el `ref` del campo con el `ref` de una choice.

| Condición | Ejemplo de operands |
|---|---|
| Sí/No, legal | `op: is` o `is_not`; field + constant booleana `true`/`false` |
| Opción de selección textual/visual | `is` / `is_not`; field + choice cuyo value es el ref |
| Comparación numérica | `equal`, `not_equal`, `greater_than`, `greater_equal_than`, `lower_than`, `lower_equal_than`; field o variable + constant numérica |
| Texto | `equal`, `not_equal`, `begins_with`, `ends_with`, `contains`, `not_contains` según tipo |
| Incondicional | `{"op":"always","vars":[]}` |

Para combinaciones `and`/`or`, operadores de selección múltiple o parámetros hidden, consultar la sintaxis exacta de [Logic Jumps](https://www.typeform.com/developers/create/logic-jumps/), no improvisar la representación de `vars`. Evitar ciclos, destinos inexistentes y ramas sin cierre. Los saltos deben respetar el orden, especialmente si se referencia una respuesta que podría omitirse.

## Scoring y variables

Inicializar en la raíz, p. ej. `"variables":{"score":0}`. Usar una acción por incremento y una condición adecuada. Para sumar 2 al responder Sí:

```json
{
  "action":"add",
  "details":{"target":{"type":"variable","value":"score"},"value":{"type":"constant","value":2}},
  "condition":{"op":"is","vars":[{"type":"field","value":"conoce_marca"},{"type":"constant","value":true}]}
}
```

Para sumar por una opción, utilizar `{"type":"choice","value":"lata"}` como segundo operando de `is`. También existen `subtract`, `multiply` y `divide`; evitar división por cero y consultar el esquema. Se pueden usar variables personalizadas cuando el esquema lo permite. No aplicar además un segundo mecanismo de scoring a las mismas respuestas. Ubicar los cálculos antes de saltos del mismo campo para que el salto no los omita.

En el último campo del camino, dirigir por score a dos cierres:

```json
{
  "type":"field","ref":"recomendacion","actions":[
    {"action":"jump","details":{"to":{"type":"thankyou","value":"cierre_alto"}},"condition":{"op":"greater_equal_than","vars":[{"type":"variable","value":"score"},{"type":"constant","value":5}]}},
    {"action":"jump","details":{"to":{"type":"thankyou","value":"cierre_general"}},"condition":{"op":"always","vars":[]}}
  ]
}
```

Asegurar que todos los recorridos llegan al campo que decide el cierre o tienen sus propias reglas equivalentes. Si existen ramas adicionales, simularlas antes de crear. En `assets/advanced-form.json` el resultado es 5 puntos para Sí + Lata y 1 para No + Botella; la segunda ruta omite valoración.

## Recall Information

- Respuesta anterior: `{{field:nombre}}`.
- Parámetro URL: `{{hidden:campaign}}`.
- Puntaje o precio: `{{var:score}}`, `{{var:price}}`.

Usar en título o descripción de preguntas, statements y agradecimientos compatibles. No usar en etiquetas de choices. Los campos referenciados deben haberse respondido antes y estar disponibles en todos los recorridos pertinentes; una pregunta con recall puede quedar fuera del flujo si el origen no fue respondido. No insertar datos personales sensibles en URLs.

## Hidden fields / URL parameters

Declarar en la raíz `"hidden":["respondent_id","campaign","source"]`. En un enlace real de Typeform, agregar fragmento `#respondent_id=test001&campaign=test&source=treasureai`, codificando nombres y valores correctamente (percent encoding). Usar valores sintéticos para pruebas y no incluir PII, credenciales ni tokens de sesión. Si ya existe un fragmento, combinar parámetros sin crear un segundo `#`. Los valores no son autenticación ni garantía de identidad; el respondente puede manipularlos. Verificar que aparecen en respuestas completadas, no solo que el URL se construyó.

## Pruebas

Simular Sí/No, cada choice relevante, límites del score, ramas que omiten campos y rutas que muestran cada agradecimiento. Verificar en preview; no declarar que la lógica se ejecutó solo por ver su JSON. Registrar resultados reales solo tras pruebas autorizadas.

Fuentes: [Logic Jumps](https://www.typeform.com/developers/create/logic-jumps/), [Score and price](https://www.typeform.com/developers/create/score-and-price/), [Recall Information](https://www.typeform.com/developers/create/recall-information/), [URL Parameters](https://www.typeform.com/developers/create/hidden-fields/).

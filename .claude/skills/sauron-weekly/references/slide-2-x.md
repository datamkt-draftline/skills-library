# Instrucciones detalladas — Slide 2: Publicaciones de X por pilares

## Filtro semántico obligatorio de seguridad de marca

Antes de construir el JSON final de X, revisá semánticamente cada candidato devuelto por `get_x_posts`.

Nuestras marcas son: **Quilmes, Corona, Stella Artois, Andes Origen, Brahma y Michelob Ultra**.

Descartá cualquier publicación que, interpretada en su contexto completo, hable negativamente de manera directa sobre alguna de nuestras marcas, sus productos o una experiencia claramente atribuida a la marca.

Esto incluye, entre otros casos:

- Ataques, insultos, burlas o ridiculización dirigidos a la marca.
- Quejas o críticas explícitas sobre la marca, sus productos, sabor, calidad, precio, servicio, campañas o activaciones.
- Comparaciones que presenten claramente a una de nuestras marcas como inferior, mala, indeseable o motivo de rechazo.
- Acusaciones, denuncias o afirmaciones claramente perjudiciales para la reputación de una de nuestras marcas.
- Ironía, sarcasmo o lenguaje coloquial cuyo sentido sea claramente negativo hacia una de nuestras marcas.

La evaluación debe ser **semántica y contextual**. No descartes una publicación solamente porque contenga una palabra negativa o sensible.

Conservá publicaciones neutrales o positivas y también aquellas cuya negatividad esté dirigida a otra entidad, a la categoría en general o a un tema distinto, siempre que no ataque directamente a una de nuestras marcas.

Si el sentido respecto de la marca es ambiguo y no existe una valoración negativa directa suficientemente clara, no la descartes por esta regla.

Este filtro no debe reordenar los candidatos. Conservá el ranking original recibido desde `get_x_posts`.

Después de descartar los candidatos negativos, conservá como máximo los primeros dos sobrevivientes de cada pilar.

Si queda uno, publicá uno. Si no queda ninguno, ese pilar debe quedar sin publicaciones.

No solicites candidatos de reemplazo y no vuelvas a ejecutar `get_x_posts` por este motivo.

## Construcción del JSON de X

Construí un array con el formato exacto de `reference/dashboard_twitterposts_example.json`.

Para cada publicación utilizá:

- `pilar`: nombre canónico del pilar.
- `tema`: título breve y directo respaldado por la publicación.
- `resumen`: resumen breve en español.
- `posteo_destacado`: texto original del post.
- `link`: URL original.
- `autor`: handle o autor informado.
- `likes`: cantidad original.
- `reposts`: cantidad original.
- `replies`: cantidad original.

La capitalización final de los pilares debe ser:

- `Wellness`
- `Socializing`
- `Affordability`
- `Image`
- `Taste`
- `Sports`
- `Events`

Reglas obligatorias:

1. No agregues publicaciones externas.
2. Eliminá duplicados por URL o ID.
3. Conservá como máximo dos publicaciones por pilar.
4. Uno o cero resultados son válidos.
5. No transformes un valor desconocido en cero.
6. Si falta un campo obligatorio, excluí la publicación.
7. Conservá las métricas originales.
8. No agregues campos que no existan en el archivo de ejemplo.
9. Si un pilar continúa fallido después del reintento interno, registralo y continuá con los pilares válidos.
10. Una respuesta válida con cero publicaciones debe representarse con un array vacío.

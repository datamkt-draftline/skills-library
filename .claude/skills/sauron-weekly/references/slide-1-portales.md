# Instrucciones detalladas — Slide 1: Portales de noticias

## Filtrado preliminar sin Web Search

Realizá una primera revisión utilizando solamente la información devuelta por `get_news`:

- `titulo`
- `fecha`
- `medio`
- `categorias`
- `entidades_detectadas`
- `motivo_match`
- `url`

El objetivo de esta etapa es reducir la cantidad de URLs que será necesario abrir mediante Web Search.
Este filtrado debe ser amplio e inclusivo. Descartá únicamente candidatos evidentemente irrelevantes.
Podés descartar una candidata en esta etapa solamente cuando sea claro que:

- No es una noticia o artículo.
- Está fuera del período solicitado.
- La URL es inválida o está duplicada.
- Trata exclusivamente sobre la ciudad de Quilmes, Quilmes Atlético Club, una persona llamada Corona o cualquier coincidencia nominal sin relación con bebidas, consumo o marcas.
- No presenta ninguna relación razonable con cerveza, bebidas, consumo, ocasiones, consumidores, cultura, economía, deportes, eventos o alguno de los pilares.
- Se trata de navegación, agenda genérica, resultados deportivos aislados, cotizaciones o contenido técnico sin ninguna señal relevante.
- Es un falso positivo evidente provocado por una keyword.

Los campos `categorias`, `entidades_detectadas` y `motivo_match` son señales de prefiltrado que pueden apoyar el análisis. No representan una clasificación semántica definitiva.
Conservá para la siguiente etapa todas las noticias que tengan una conexión directa, media, indirecta o todavía incierta pero bastante razonable.
Registrá internamente:

- Cantidad de candidatas iniciales.
- Cantidad descartada en el filtrado preliminar.
- Motivo de descarte de cada candidata.
- Cantidad de URLs que pasan a Web Search.

## Obtención del contenido mediante Web Search

Para cada candidata que haya superado el filtrado preliminar:

1. Usá Web Search para abrir la URL exacta devuelta por `get_news`.
2. Accedé a la página original del medio.
3. Obtené y analizá todo el contenido disponible del artículo.
4. La relevancia, el pilar y la selección final deben decidirse utilizando el contenido obtenido.
5. Procesá las URLs por medio y en grupos manejables.
6. Conservá un registro estructurado y conciso de cada artículo antes de continuar con el grupo siguiente.

## Contenido inaccesible

Si Web Search no puede acceder directamente al cuerpo de una noticia:

1. Buscá la URL exacta o el título exacto junto con el nombre del mismo medio.
2. Utilizá únicamente contenido indexado correspondiente a esa misma noticia.
3. No sustituyas la candidata por una noticia diferente.
4. No combines información de distintos artículos.
5. Si el contenido disponible no permite evaluar razonablemente su relevancia, descartala.
6. Registrá la URL como inaccesible o insuficiente.

# Criterios finales de relevancia

Aplicá un criterio amplio e inclusivo, priorizando siempre los contenidos con mayor relación con cerveza, consumo de cerveza o alguna de nuestras marcas cerveceras (Quilmes, Corona, Stella Artois, Andes Origen, Brahma, Michelob Ultra).
No limites la selección a noticias que mencionen explícitamente cerveza, Quilmes o alcohol.
También pueden ser relevantes aquellas noticias que aporten señales concretas sobre:

- Barreras del consumidor.
- Ocasiones de consumo.
- Tendencias culturales.
- Categorías competidoras.
- Comportamientos relacionados con alguno de los pilares.
- Contextos sociales, económicos, deportivos o culturales que afecten a la categoría.

No excluyas una noticia únicamente porque no menciona cerveza. Si presenta una relación concreta, razonable y explicable con uno de los pilares, puede incluirse.
Evitá asociaciones extremadamente débiles, accidentales o basadas únicamente en una keyword.

## Jerarquía de relevancia

Aplicá este orden de prioridad.

### 1. Prioridad alta — Relación directa con cerveza

Artículos explícitamente relacionados con:

- Cerveza o consumo de cerveza.
- Quilmes u otras marcas cerveceras.
- Cervecerías.
- Cerveza sin alcohol.
- Precios, promociones, ventas o tendencias de consumo.
- Lanzamientos, productos o innovaciones.
- Patrocinios, campañas, activaciones o eventos cerveceros.
- Actitudes de consumidores sobre sabor, imagen, salud, bienestar o accesibilidad.

### 2. Prioridad media — Relación fuerte con la categoría o una ocasión

Artículos que no mencionan directamente cerveza, pero están claramente relacionados con:

- Consumo de alcohol.
- Bares, restaurantes, gastronomía, salidas o vida nocturna.
- Reuniones y ocasiones sociales de consumo.
- Otras bebidas alcohólicas que aporten contexto competitivo.
- Moderación, bebidas sin alcohol o tendencias de bienestar.
- Eventos deportivos o culturales que representen ocasiones relevantes de consumo.
- Patrones de gasto que afecten directamente al consumo discrecional.

### 3. Prioridad contextual — Señales indirectas pero significativas

Artículos que aportan información útil sobre:

- Ingreso disponible, inflación, precios y poder adquisitivo.
- Cambios en hábitos de socialización, salidas o reuniones.
- Comportamientos de salud y bienestar.
- Premiumización, sofisticación, identidad, aspiracionalidad o imagen cultural.
- Preferencias de sabor, gastronomía y experiencias sensoriales.
- Deportes o grandes eventos relevantes para audiencias argentinas.
- Tendencias culturales que puedan influir sobre ocasiones o decisiones de consumo.

Cuando existan varias opciones para un mismo pilar, priorizá siempre:

1. Relación directa con cerveza.
2. Relación fuerte con la categoría u ocasión.
3. Señales contextuales o indirectas.

## Relevancia geográfica

El contenido debe tener una relación clara con Argentina.
Una noticia internacional puede incluirse solamente cuando:

- Tenga consecuencias o aplicación concreta para consumidores argentinos.
- Involucre una marca o activación relevante para el mercado argentino.
- Represente una tendencia internacional con impacto razonable sobre la categoría local.

No incluyas noticias internacionales cuya relación con Argentina sea meramente hipotética.

## Clasificación por pilares

Asigná exactamente uno de estos pilares a cada noticia:

- `WELLNESS`
- `SOCIALIZING`
- `AFFORDABILITY`
- `IMAGE`
- `TASTE`
- `SPORTS`
- `EVENTS`

Una misma noticia nunca debe aparecer en más de un pilar.
Cuando una noticia pueda pertenecer a varios:

1. Identificá su tema y enfoque editorial principal.
2. Determiná qué pilar explica mejor por qué resulta relevante.
3. Asignala exclusivamente a ese pilar.
4. No vuelvas a incluirla en ningún otro.

Por ejemplo, una activación de Corona Cero en un centro de esquí argentino podría relacionarse con `WELLNESS`, `SPORTS` y `EVENTS`. Si el foco principal es la activación y la experiencia del evento, debe clasificarse solamente como `EVENTS`.

## Recall frente a precisión

Priorizá recall sobre una precisión excesivamente restrictiva.
Cuando una noticia tenga una relación razonable, concreta y defendible con un pilar, considerala para la selección final en lugar de excluirla únicamente porque la relación sea indirecta.
Buscá activamente contenidos para todos los pilares y no detengas la curación después de encontrar solamente las noticias más obvias.
La jerarquía debe respetarse siempre: las noticias directamente relacionadas con cerveza tienen prioridad sobre las contextuales.

## Deduplicación editorial

Después de leer los contenidos completos disponibles, compará las noticias de distintos medios.
Conservá solamente una cuando estés seguro de que describen esencialmente el mismo acontecimiento.
Entre duplicados, conservá la versión con información más completa y útil.
Aplicá también deduplicación entre pilares:

- La misma URL nunca puede aparecer dos veces.
- La misma historia no puede aparecer en pilares diferentes.
- Cada noticia debe tener uno y solamente un pilar final.

## Selección final de portales

Después de aplicar relevancia, clasificación y deduplicación:

1. Elegí como máximo dos noticias por pilar.
2. Intentá obtener una o dos noticias por pilar cuando existan candidatas defendibles.
3. El objetivo editorial es alcanzar entre 7 y 14 noticias totales cuando el material disponible lo permita.
4. Uno o cero resultados siguen siendo válidos cuando no exista contenido pertinente.
5. Priorizá las noticias de relación directa sobre las contextuales.

## Construcción del JSON de portales

Construí el JSON respetando exactamente la estructura, las keys, la capitalización y los tipos definidos en `reference/dashboard_newsoutlets_example.json`.
El archivo de ejemplo define únicamente el formato. No reutilices su contenido anterior.
Para cada noticia:

- Usá la URL original devuelta por `get_news`.
- Conservá la fecha y el medio originales.
- Conservá el autor cuando esté disponible.
- Elaborá el tema y el resumen exclusivamente a partir del contenido analizado.
- No inventes datos ausentes.
- No agregues campos que no existan en el archivo de ejemplo.


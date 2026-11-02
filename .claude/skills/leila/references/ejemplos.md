# Ejemplos de secciones

Ejemplos del tono y nivel de detalle esperado por sección.
Son solo guías: adaptá siempre al contenido real del archivo.

---

## Temas de conversación (tarjetas)

Cada tarjeta incluye un título corto (nombre del tema), el porcentaje, y
un resumen de 1-2 oraciones que responde "¿por qué se habla de esto?".
No menciones número de comentarios ni porcentaje dentro del texto del resumen.

**Política** · 22%
Conversaciones relacionadas con el peronismo y Perón como figura histórica,
mezclando apoyos y críticas al rol del Estado en la industria.

**Pertenencia Argentina** · 18%
Los usuarios celebran el sentimiento de ser argentino y vinculan el producto
con una identidad nacional compartida.

**Alegría** · 12%
Comentarios y emojis festivos que celebran la pieza sin referencia a un tema
concreto.

**Fraude** · 10%
Menciones a un posible fraude fiscal o irregularidades vinculadas a la historia
de la marca.

---

## Enfoque general de la conversación

**Importante**: no es "sentiment" (positivo/negativo), es **el enfoque**:
sarcasmo, nostalgia, enojo, celebración, humor, reflexión, admiración, etc.
No uses ambigüedades ("algo", "quizás", "en parte"). Sé claro y directo.

> La conversación tiene un tono mayormente reflexivo y analítico, con elementos
> de admiración y fascinación. Aunque hay algunas expresiones de confusión,
> no predominan los comentarios negativos ni agresivos. El tono general es
> curioso, valorativo y con cierta nostalgia histórica.

> La conversación es predominantemente sarcástica y crítica, con usuarios que
> ironizan sobre las decisiones de la marca y usan el humor para expresar
> descontento. Prevalece el escepticismo por sobre la celebración.

---

## Menciones sobre cerveza / CMQ / Marcas

Si no hay menciones, no incluir esta sección (dejar `BEER_SECTION` vacío).
Si hay, listar los comentarios exactos (nunca inventar) y agregar un resumen
corto en 2-4 líneas agrupadas por eje:

- **Relatos personales**: historias familiares, vínculos con la cervecería, etc.
- **Opiniones sobre marcas**: elogios o críticas a marcas puntuales.
- **Contexto histórico**: referencias a eventos, expropiaciones, familias históricas.
- **Valor simbólico**: lugar cultural de la marca.

Ejemplos de ejes a extraer (adaptar al contenido real):

> **Relatos personales**: Algunos usuarios comparten historias familiares
> relacionadas con la Cervecería Quilmes o con haber trabajado en ella,
> mencionando vínculos históricos y afectivos.
>
> **Opiniones sobre marcas**: Hay comentarios que elogian o critican a Quilmes
> como cerveza ("la más rica", "la peor del mercado"), e incluso comparan con
> otras como Palermo.
>
> **Contexto histórico**: Se hace referencia a la expropiación de tierras
> vinculadas a la producción de lúpulo, cosechas de cebada cervecera y la figura
> de los Bemberg.
>
> **Valor simbólico**: Algunos destacan la importancia cultural de la marca
> Quilmes, mencionando su distribución histórica o su rol en ciertas regiones
> (por ejemplo, Barrio Cervecero).

---

## Bloque BEER_SECTION (template)

Cuando hay menciones, el bloque se arma así:

```html
<section class="block">
  <h2>Menciones sobre cerveza / CMQ / Marcas</h2>
  <p class="lede">Encontramos <strong>N</strong> comentarios con menciones a cerveza, CMQ o alguna de las marcas (Quilmes, Brahma, Corona, Stella, Budweiser, Andes Origen, Temple).</p>
  <div class="quote-list">
    <div class="quote"><span class="author">@usuario1</span>Texto literal del comentario 1</div>
    <div class="quote"><span class="author">@usuario2</span>Texto literal del comentario 2</div>
    ...
  </div>
  <h3 style="font-size:15px;margin:12px 0 8px">Resumen</h3>
  <p style="margin:0 0 8px"><strong>Relatos personales:</strong> ...</p>
  <p style="margin:0 0 8px"><strong>Opiniones sobre marcas:</strong> ...</p>
  <p style="margin:0 0 8px"><strong>Contexto histórico:</strong> ...</p>
  <p style="margin:0"><strong>Valor simbólico:</strong> ...</p>
</section>
```

Si no hay menciones, dejar `BEER_SECTION` como cadena vacía.

---
name: Analizar encuesta
description: Analiza los resultados de una encuesta en formato xlsx y genera un dashboard HTML interactivo (tema oscuro, Chart.js, filtros dinámicos, datos embebidos). Úsala cuando el usuario adjunte un archivo xlsx de encuesta o pida analizar resultados de encuesta.
action: true
---

Sos un analista de encuestas. Analizás los resultados de una encuesta en formato xlsx y entregás un **dashboard HTML interactivo** con los resultados.

## Comportamiento general

- Todo lo marcado como **(Interno)** es para uso propio: usalo para guiarte, no lo describas en el chat.
- El resultado es un informe **profesional, estético y conciso** — solo la información pedida, sin agregados.
- No hagas preguntas al usuario salvo que lo pida explícitamente.
- La guía de escalas Agile está en `reference/agile-guide.md` — leela antes de empezar.
- Si el usuario adjunta un archivo llamado "Agile - Guía de escalas.xlsx" (o similar), usalo en lugar de la guía interna.

## Herramienta disponible

`scripts/read_xlsx.py` — parsea un xlsx a filas de dicts (stdlib, sin dependencias externas):

```python
import sys
sys.path.insert(0, ".claude/skills/analyze-survey/scripts")
from read_xlsx import read_xlsx
sheets = read_xlsx("path.xlsx")  # dict {sheet_name: [row_dict, ...]}
```

---

## Paso 1 — Leer y procesar el archivo

**(Interno)** Parsear el xlsx con `read_xlsx.py`. Trabajar únicamente sobre las filas con `Response Type == completed` (si la columna existe).

**(Interno)** Limpiar los nombres de columna: sacar asteriscos `*` de los bordes **y todo tipo de espacio unicode** (incluyendo ` `, ` `, `\xa0`, espacios de ancho cero, etc.). En Python:
```python
import unicodedata
def clean(s):
    s = s.strip()
    s = s.strip('*').strip()
    # quitar todos los caracteres que unicode clasifica como espacio/separador
    s = ''.join(c for c in s if not unicodedata.category(c).startswith('Z') or c == ' ')
    return s.strip()
```
Aplicar `clean()` tanto a los nombres de columna como al **contenido de las celdas** antes de comparar valores (ej. frases de intención).

**(Interno)** Detectar automáticamente la **columna de instancia/evento**: buscar columna con nombre como "Instancia", "Evento", "Event", "Audiencia", "Encuesta". Si no existe pero hay columnas de fecha (`Start Date`, `Submit Date`), agrupar filas por rangos de fecha naturales (si hay clusters separados) y asignar nombres genéricos (Instancia 1, Instancia 2…). Si hay un único grupo, omitir esta dimensión.

**(Interno)** Detectar si hay columna de **fecha de nacimiento** (variantes: "Fecha de nacimiento", "Birth date", "DOB", "Nacimiento"). Si existe:
1. Calcular `Edad` (años cumplidos a la fecha de `Submit Date`/`Start Date` de esa fila, o fecha de hoy).
2. Calcular `Rango Etario`: `-18 años` (<18) · `18-24 años` · `25-34 años` · `35-44 años` · `45-54 años` · `+55 años` (≥55).

**(Interno)** Si ya existen columnas explícitas de **Género** y **Rango Etario**, usarlas directamente.

**(Interno)** Clasificar cada columna no-informativa usando la guía Agile:
- **Overall Liking** (1-9) / **Overall Liking TaDa** (1-5): score numérico de agrado.
- **Intención de compra**: frases "Definitivamente sí/no…", "Probablemente sí/no…", "No sé…".
- **NPS**: escala 0-10 de recomendación.
- **Adecuación / Relevancia / Valoración**: escala 1-5.
- **Momentos / Ocasiones**: pregunta de elección única o múltiple de ocasiones/contextos.
- **Pregunta simple**: otras cerradas con ≤15 valores únicos.
- **Pregunta abierta**: >15 valores únicos → omitir del HTML.
- **Informativa** (ignorar): `#`, `Response Type`, `Start Date`, `Submit Date`, `Stage Date`, `Network ID`, `Tags`, `Ending`, y demás metadatos.

**(Interno) IMPORTANTE — Etiquetas de la UI según el tipo Agile detectado:**
Si una columna matchea un tipo Agile, el tab, el header de la sección y los textos de benchmark **deben usar el nombre exacto del tipo**, no una palabra genérica como "Puntaje":
- Score 1-9 → tab y header: **"Overall Liking"** (nunca "Puntaje").
- Score 1-5 agrado → **"Overall Liking TaDa"**.
- Score 0-10 recomendación → **"NPS"**.
- Score 1-5 adecuación/relevancia/valoración → **"Adecuación"**, **"Relevancia"** o **"Valoración"** según corresponda.

**(Interno) IMPORTANTE — Adaptar la escala en todos lados:**
El template viene configurado para una escala 1-10 por defecto. Para cada score detectado, adaptar en el HTML/JS:
- Rango del eje y bucket `scoreDist` (`for i=1; i<=MAX; i++`).
- Array de `scoreLabels`/`labels` (`['1','2',...,'MAX']`).
- Texto `"Escala del 1 al 10"` → `"Escala del 1 al <MAX> · <TipoAgile>"`.
- Benchmark `"promedio ≥ 7/10"` → `"promedio ≥ <umbral>/<MAX>"` según guía Agile.
- Buckets de color (verde/gold/rojo) y labels "Puntaje 8-10 / 6-7 / 1-5":
  - **Overall Liking (1-9)**: verde 8-9 · gold 6-7 · rojo 1-5.
  - **Overall Liking TaDa / Adecuación / Relevancia / Valoración (1-5)**: verde 4-5 · gold 3 · rojo 1-2.
  - **NPS (0-10)**: verde 9-10 (promotores) · gold 7-8 (neutrales) · rojo 0-6 (detractores).
- Umbral de badge "sobre/bajo benchmark" (`parseFloat(avgScore) >= 7`): usar el umbral que corresponda al tipo.
- Insight del score (`setIf('ins1-num', avgScore + '/9')`): usar `/<MAX>`.

---

## Paso 2 — Generar el dashboard HTML

Generar un único archivo `dashboard.html` a partir del **template** en `template.html`.

### Cómo usar el template

1. **Leer** el archivo `.claude/skills/analyze-survey/template.html`.
2. **Reemplazar** cada `{{PLACEHOLDER}}` con el valor correspondiente a esta encuesta.
3. **Escribir** el resultado como `dashboard.html` en el directorio de trabajo del usuario.

El template ya contiene toda la estructura HTML, CSS (tema oscuro), lógica JavaScript y Chart.js. Solo necesitás reemplazar los placeholders con los datos reales.

### Guía de placeholders

| Placeholder | Qué poner |
|---|---|
| `{{SURVEY_TITLE}}` | Nombre de la encuesta/producto (ej. "Flying Fish") |
| `{{SURVEY_TITLE_H1}}` | Nombre con emoji si corresponde (ej. "🐟 Flying Fish") |
| `{{SURVEY_SUBTITLE}}` | Descripción breve: tipo de encuesta · N instancias · período |
| `{{INSIGHTS_SUBTITLE}}` | Síntesis de las N instancias/eventos |
| `{{TAB_PUNTAJE}}` | Nombre **del tipo Agile detectado** (ej. "Overall Liking", "NPS", "Adecuación"). **No usar "Puntaje" ni otra palabra genérica** si matchea con un tipo Agile. |
| `{{TAB_MOMENTOS}}` | Nombre de la pregunta de momentos (ej. "Momentos") |
| `{{TAB_INTENCION}}` | Nombre de la pregunta de intención (ej. "Intención") |
| `{{Q_PUNTAJE}}` | Texto exacto de la pregunta de score |
| `{{Q_MOMENTOS}}` | Texto exacto de la pregunta de momentos |
| `{{Q_INTENCION}}` | Texto exacto de la pregunta de intención |
| `{{KPI_SCORE_LABEL}}` | Label corta del KPI de score (ej. "Agrado promedio") |
| `{{KPI_MOMENTO_LABEL_SHORT}}` | Label corta del KPI de momento (ej. "Momento principal") |
| `{{BENCHMARK_SCORE_TEXT}}` | Texto del benchmark de score (ej. `Benchmark Overall Liking: <strong style="color:#3DAB6A">promedio ≥ 7/10</strong>`) |
| `{{BENCHMARK_SCORE_DETAIL}}` | Texto detallado del benchmark con colores (ej. `<strong style="color:#3DAB6A">Benchmark referencial · Overall Liking:</strong> promedio ≥ 7/10. Puntajes 8-10 en verde, 6-7 en amarillo, 1-5 en rojo.`) |
| `{{BENCHMARK_INTENT_TEXT}}` | Texto del benchmark de intención (ej. `Benchmark intención positiva: <strong style="color:#FFD166">≥ 70%</strong>`) |
| `{{CARD_MOMENTOS}}` | Título de la card de momentos en Resumen (ej. "Momentos de consumo preferidos") |
| `{{INSTANCIA_OPTS}}` | Opciones del dropdown de instancia en JS: `{v:'all',l:'Todas'},{v:'CEL',l:'CEL'},...` |
| `{{INSTANCIA_KEYS}}` | Array de claves de instancia: `'CEL','Bali',...` |
| `{{INSTANCIA_COLORS}}` | Array de colores por instancia: `'#00C2CB','#FFD166',...` |
| `{{INTENT_ORDER}}` | Array de frases de intención de más positiva a más negativa |
| `{{MOMENTO_ORDER}}` | Array de opciones completas de momentos |
| `{{MOMENTO_SHORT}}` | Array de versiones cortas para etiquetas de gráfico |
| `{{RAW_DATA}}` | **Todos los registros** como objetos JS, con propiedades: `instancia`, `puntaje`, `intencion`, `momento`, `genero`, `edad` (o las que correspondan a esta encuesta). Una propiedad por columna relevante, sin metadatos. |
| `{{INS1_TITLE}}` … `{{INS6_TITLE}}` | Títulos de las 6 insight cards, basados en los datos reales |
| `{{INS1_DESC}}` … `{{INS6_DESC}}` | Descripciones de las 6 insight cards con valores reales |

### Notas de adaptación

- **Si la encuesta no tiene alguna de las preguntas** (ej. no hay momentos): eliminar la sección correspondiente del HTML y su tab.
- **Si hay preguntas adicionales** no contempladas en el template: agregar nuevas secciones siguiendo el mismo patrón (tab + `<div class="section" id="sec-...">`) y una función `render[Nombre]()` en JS.
- **`{{RAW_DATA}}`**: generar el array JS directamente a partir de los datos del xlsx. El campo `instancia` puede llamarse diferente (ej. `evento`, `audiencia`) si eso es más natural para el dataset; ajustar el JS en consecuencia.
- Si la encuesta tiene **una sola instancia**, omitir el dropdown de Audiencia y la card de instancia en Audiencia.
- **Placeholders dentro de strings JS**: antes de reemplazar, mirá el contexto del placeholder en el template. Si ya está envuelto en comillas (`'{{X}}'` o `"{{X}}"`), el valor **no** debe incluir comillas propias — de lo contrario quedan comillas duplicadas (`''...''`) y es un `SyntaxError` que rompe TODO el JS en silencio (los KPIs quedan vacíos, los filtros y tabs no responden). Ante la duda, preferí calcular el valor dinámicamente en JS en vez de inyectar un literal.

---

## Entrega

Antes de guardar el HTML y llamar `mcp__tas__open_file`, ejecutar este **check de validación obligatorio**. Si cualquier assert falla, corregir el HTML y volver a correr el check — **nunca** abrir un archivo que no pasó la validación.

```python
import re, subprocess, tempfile, os

with open("dashboard.html", encoding="utf-8") as f:
    html = f.read()

# 1. No debe quedar ningún {{PLACEHOLDER}} sin reemplazar
remaining = re.findall(r'\{\{[^}]+\}\}', html)
assert not remaining, f"Placeholders sin reemplazar: {remaining}"

# 2. Los arrays JS críticos no deben estar vacíos
empty_arrays = re.findall(r'const (?:RAW|INTENT_ORDER|MOMENTO_ORDER|MOMENTO_SHORT)\s*=\s*\[\s*\]', html)
assert not empty_arrays, f"Arrays JS vacíos: {empty_arrays}"

# 3. El array RAW debe tener registros reales
raw_match = re.search(r'const RAW = \[(.{0,200})', html, re.DOTALL)
assert raw_match and ('instancia:' in raw_match.group(1) or 'evento:' in raw_match.group(1) or 'audiencia:' in raw_match.group(1)), "RAW parece vacío o mal generado"

# 4. Comillas duplicadas accidentales por placeholders mal interpolados
#    (ej. '{{X}}' + X='valor' → ''valor'' → SyntaxError silencioso)
dup_quotes = re.findall(r"''[^'\n]+''|\"\"[^\"\n]+\"\"", html)
assert not dup_quotes, f"Comillas duplicadas detectadas (SyntaxError): {dup_quotes[:3]}"

# 5. El JS embebido debe parsear sin errores (sin esto, un bug de sintaxis
#    deja el dashboard con secciones vacías y botones sin responder)
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
assert scripts, "No se encontró bloque <script> inline"
js = "\n".join(scripts)
with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as t:
    t.write(js)
    tmp = t.name
try:
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    assert r.returncode == 0, f"SyntaxError en el JS del dashboard:\n{r.stderr}"
finally:
    os.unlink(tmp)

print("✓ Validación OK")
```

Guardar el HTML en el directorio de trabajo del usuario y llamar `mcp__tas__open_file` con la ruta absoluta.

---

## Notas de cálculo

- **Promedio Ponderado**: `Σ(valor_i × cantidad_i) / Σ(cantidad_i)`
- **T2B (Top 2 Box)**: `(cant(4) + cant(5)) / total × 100` (escalas 1-5)
- **NPS**: `%Promotores − %Detractores` (Promotores=9-10, Neutrales=7-8, Detractores=0-6)
- Todos los porcentajes: 1 decimal con `%`. Promedios: 2 decimales.

## Nota sobre entorno

En este entorno **no hay** pandas ni openpyxl instalables. Los scripts en `scripts/` usan solo la stdlib. **No los reemplaces** por imports de pandas.

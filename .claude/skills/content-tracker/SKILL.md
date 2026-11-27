---
name: content-tracker
description: Genera el Content Investment & Impact Tracker HTML desde el Excel de referencias. Lee content_tracker_datos.xlsx, valida los datos, inyecta el JSON en dashboard_template.html y entrega el HTML listo. Invocar cuando el usuario pida generar o actualizar el dashboard.
action: true
---

# Content Tracker — Skill unificada

Genera el dashboard HTML `content_dashboard.html` a partir del archivo Excel de referencias.
Todo el flujo ocurre en esta skill: lectura → validación → generación → entrega.

## Archivos de referencia

- `references/content_tracker_datos.xlsx` — fuente de datos (dos hojas: *Carga contenido* y *Reach Consolidado*). El usuario lo actualiza manualmente.
- `references/dashboard_template.html` — template del dashboard con dos placeholders: `%%CARGA_CONTENIDO_JSON%%` y `%%REACH_CONSOLIDADO_JSON%%`.

La carpeta base de la skill está en `.claude/skills/content-tracker/`. Usá rutas absolutas al ejecutar Python.

## Paso 1 — Leer el Excel

Usá Python puro (`zipfile` + `xml.etree.ElementTree`), sin dependencias externas.

```python
import zipfile, xml.etree.ElementTree as ET

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

def parse_xlsx(path):
    with zipfile.ZipFile(path) as z:
        ss = []
        with z.open("xl/sharedStrings.xml") as f:
            root = ET.parse(f).getroot()
            for si in root.findall(f"{{{NS}}}si"):
                t = si.find(f"{{{NS}}}t")
                ss.append(t.text if t is not None else "")
        def parse_sheet(name):
            with z.open(f"xl/worksheets/{name}") as f:
                root = ET.parse(f).getroot()
            rows = []
            for row in root.find(f"{{{NS}}}sheetData").findall(f"{{{NS}}}row"):
                cells = {}
                for c in row.findall(f"{{{NS}}}c"):
                    ref = c.get("r"); t = c.get("t",""); v = c.find(f"{{{NS}}}v")
                    val = v.text if v is not None else None
                    if val is not None:
                        if t == "s": val = ss[int(val)]
                        else:
                            try: val = float(val); val = int(val) if val == int(val) else val
                            except: pass
                    col = "".join(ch for ch in ref if ch.isalpha())
                    cells[col] = val
                rows.append(cells)
            return rows
        return parse_sheet("sheet1.xml"), parse_sheet("sheet2.xml")

def rows_to_dicts(rows):
    if not rows: return []
    all_cols = set()
    for r in rows: all_cols.update(r.keys())
    def col_num(c):
        n=0
        for ch in c: n=n*26+ord(ch)-64
        return n
    cols = sorted(all_cols, key=col_num)
    headers = {c: rows[0].get(c,"") for c in cols}
    return [{headers[c]: row.get(c, None) for c in cols} for row in rows[1:]]
```

Luego usá `rows_to_dicts` sobre cada hoja para obtener listas de dicts con los headers reales del Excel.

## Paso 2 — Normalizar encabezados y mapear claves canónicas

Normalizá los headers del Excel antes de usar: trim, lowercase, sin acentos, sin puntuación no sustantiva.

```python
import unicodedata, re

def normalize(s):
    s = unicodedata.normalize('NFD', str(s or ""))
    s = "".join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9 ]', '', s.lower()).strip()
```

Mapeá los headers normalizados a claves canónicas del dashboard:

| Header Excel (normalizado) | Clave canónica JSON |
|---|---|
| `contentid` | `contentId` |
| `nombre del contenido` | `nombreContenido` |
| `marca` | `marca` |
| `pais` / `país` | `pais` |
| `campana` / `campaña` | `campana` |
| `fecha inicio` | `fechaInicio` |
| `estado` | `estado` |
| `tipo de contenido` | `tipoContenido` |
| `canal principal` | `canalPrincipal` |
| `objetivo principal` | `objetivoPrincipal` |
| `kpi principal` | `kpiPrincipal` |
| `unidad kpi` | `unidadKpi` |
| `valor kpi` | `valorKpi` |
| `reach` | `reach` |
| `er` / `er%` | `er` |
| `fvtr` | `fvtr` |
| `activacion` / `activación` | `activacion` |
| `producto` | `producto` |
| `sponsoreo` | `sponsoreo` |
| `produccion` / `producción` | `produccion` |
| `media` | `media` |
| `inversion total` / `inversión total` | `inversionTotal` |
| `costo por kpi` | `costoPorKpi` |

Para *Reach Consolidado*:

| Header (normalizado) | Clave canónica |
|---|---|
| `campana` / `campaña` | `campana` |
| `reach  uu` / `reach` / `reach / uu` | `reach` |

## Paso 3 — Validación (inline, antes de generar)

Ejecutá estas validaciones sobre los datos mapeados. Si encontrás errores **FAIL**, mostrá un resumen claro al usuario y preguntale si quiere continuar de todas formas antes de generar el HTML.

### 3.1 Columnas requeridas — Carga contenido
Obligatorias: `contentId`, `nombreContenido`, `marca`, `campana`, `estado`, `tipoContenido`, `canalPrincipal`, `objetivoPrincipal`, `unidadKpi`, `valorKpi`, `inversionTotal`.

Si falta alguna → **FAIL**: "Faltan columnas requeridas: [lista]"

### 3.2 Columnas requeridas — Reach Consolidado
Obligatorias: `campana`, `reach`.

Si falta alguna → **FAIL**: "Reach Consolidado: faltan columnas [lista]"

### 3.3 Producción
- Localizá la columna de Producción por normalización (puede llamarse "Producción", "Produccion", etc.).
- Verificá que tenga al menos un valor numérico no-cero.
- Si existe pero todos los valores son 0 o nulos → **WARNING**: "Producción: todos los valores son 0"

### 3.4 Inversión total
- Verificá que al menos el 80% de las filas tengan `inversionTotal > 0`.
- Si no → **FAIL**: "Menos del 80% de las filas tienen Inversión total > 0"

### 3.5 Campañas de Reach Consolidado vs Carga contenido
- Campañas en CC que no tienen match en RC → **WARNING**: "Campañas sin Reach Consolidado: [lista]" (estas filas no tendrán dato en Matriz 2)

### 3.6 Valores únicos en catálogos dinámicos
- Listá los valores únicos de `canalPrincipal` y `tipoContenido` que se cargarán en los filtros.
- Si alguna columna tiene 0 valores distintos → **FAIL**: "Sin valores en [columna]"

Mostrá el resultado de validación así:
```
✅ PASS  — X registros válidos en Carga contenido, Y en Reach Consolidado
⚠️  WARNINGS:
  - [descripción]
❌ ERRORES:
  - [descripción]
```

Si hay errores **FAIL**, preguntá al usuario: "¿Querés continuar de todas formas o preferís revisar el Excel primero?" y esperá su respuesta antes de continuar.

## Paso 4 — Construir JSON para inyección

Construí las dos listas JSON:

**`cc_json`** — lista de objetos con las claves canónicas listadas en Paso 2. Convertí valores numéricos a float/int; strings vacíos o `None` a `""` o `0` según corresponda.

**`rc_json`** — lista de objetos `{campana, reach}`.

Serializá con `json.dumps(..., ensure_ascii=False)`.

## Paso 5 — Generar el HTML

```python
import json

with open("references/dashboard_template.html", encoding="utf-8") as f:
    template = f.read()

result = template.replace("%%CARGA_CONTENIDO_JSON%%", cc_json)
result = result.replace("%%REACH_CONSOLIDADO_JSON%%", rc_json)

# Verificar que los placeholders fueron reemplazados
assert "%%CARGA_CONTENIDO_JSON%%" not in result
assert "%%REACH_CONSOLIDADO_JSON%%" not in result
```

Guardá el archivo de salida en la carpeta de trabajo activa del usuario (el directorio donde están trabajando, no en references/). Nombralo `content_dashboard.html`.

## Paso 6 — Entregar

Luego de guardar, llamá a `mcp__tas__open_file` con la ruta absoluta del archivo generado para mostrárselo al usuario.

Informá brevemente: cuántos registros se procesaron, qué campañas y marcas están presentes, y si hubo warnings.

## Reglas estrictas

- Nunca hardcodear catálogos de Canal/Tipo de contenido; siempre desde los datos reales.
- El campo `produccion` debe mapearse por normalización de header, nunca por string literal.
- No modificar el template ni el Excel de referencias.
- No usar `inversionTotal` al mismo tiempo que tipos específicos (Activación, Producto, Producción, Sponsoreo).
- CPM usa solo filas de Carga contenido con Objetivo = Reach/awareness e Impresiones.
- Reach/UU en Matriz 2 viene exclusivamente de Reach Consolidado por campaña; nunca de la columna `reach` de Carga contenido.
- FVTR se agrega como promedio aritmético, nunca como suma.
- Benchmarks de cada matriz: X = MAX_visible / 2, Y = MAX_visible / 2.
- No renderizar Plotly sobre paneles `display:none`; usar `requestAnimationFrame` + `Plotly.react()` al cambiar de tab.

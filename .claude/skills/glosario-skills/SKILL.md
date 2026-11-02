---
name: glosario-skills
description: Genera un HTML con los 7 pilares ONE ABI WAY (Category, Consumer, Portfolio & Brand, Innovation, Connections and Creativity, Trade Execution, Value Creation) y las skills asociadas a cada uno. Usa el logo oficial, fuente Avantt y los colores/hover de guidelines ABI (amarillo → naranja). Cada item abre un modal con nombre, comando, funcionalidad y archivos requeridos. Todos los assets están embebidos en el HTML final (self-contained).
action: true
---

# Glosario Skills

Esta skill genera un HTML autocontenido con los 7 pilares de ONE ABI WAY y las
skills (items) asociadas a cada pilar. El resultado tiene el logo oficial,
tipografía Avantt, hover con los colores de la guía de marca, y un modal por
cada item con su nombre, comando, funcionalidad y archivos requeridos.

## When to use

Activar siempre que el usuario pida:
- El listado de skills disponibles
- El glosario de skills del equipo
- Ver las skills del área de Marketing
- Las skills de ONE ABI WAY
- Cualquier variante de "qué skills hay disponibles"

---

## Cómo funciona

1. Leé `PILLARS_DATA` y `ITEMS_DATA` de abajo y construí la estructura en memoria.
   - Si el usuario pide modificar/agregar/sacar items o metadata, actualizá los datos antes de renderizar.
2. Para cada pilar, generá una card siguiendo el formato de `CARD_FORMAT`.
3. Reemplazá los placeholders del `HTML_TEMPLATE`:
   - `/* LOGO_B64 */` → base64 de `references/assets/one-abi-way-logo.png`.
   - `/* AV_LIGHT */`, `/* AV_REG */`, `/* AV_SB */`, `/* AV_BOLD */` → base64 de las 4 fuentes en `references/assets/fonts/`.
   - `<!-- PILLARS_CARDS -->` → HTML de las 7 cards.
4. Guardá el resultado como `one-abi-skills.html` en el working directory.
5. Llamá a `mcp__tas__open_file` con el path absoluto del archivo generado.

Usá el script Python de abajo para hacer el base64 y la sustitución.

---

## PILLARS_DATA

```json
{
  "pillars": [
    {
      "num": "01",
      "name": "Category",
      "desc": "Define the key opportunities to Lead and Grow the category",
      "items": ["Sauron"]
    },
    {
      "num": "02",
      "name": "Consumer",
      "desc": "Define and deeply understand our consumer target",
      "items": ["Analyze Survey"]
    },
    {
      "num": "03",
      "name": "Portfolio & Brand",
      "desc": "Prioritize brands and platforms to drive growth at scale",
      "items": ["PPT"]
    },
    {
      "num": "04",
      "name": "Innovation",
      "desc": "Optimize our portfolio through sustainable innovation",
      "items": ["Remy"]
    },
    {
      "num": "05",
      "name": "Connections and Creativity",
      "desc": "Connect with our consumers effectively to drive growth",
      "items": ["Influencer Audience", "Argos", "Media Investment", "Content Tracker"]
    },
    {
      "num": "06",
      "name": "Trade Execution",
      "desc": "Build brands and drive growth at the point-of-purchase",
      "items": []
    },
    {
      "num": "07",
      "name": "Value Creation",
      "desc": "Ensure that we are actually creating value",
      "items": ["Gantt", "Glosario Skills"]
    }
  ]
}
```

---

## ITEMS_DATA

```json
{
  "Analyze Survey": {
    "cmd": "/analyze-survey",
    "func": "Analiza resultados de encuestas siguiendo una metodología por pasos y genera dashboard HTML + xlsx procesado con el detalle por pregunta.",
    "files": "Archivo xlsx con los resultados de la encuesta (respuestas en bruto).",
    "prompt": "Quiero analizar los resultados de la encuesta con /analyze-survey"
  },
  "PPT": {
    "cmd": "/presentacion-bu-las-cmq",
    "func": "Genera presentaciones PowerPoint (.pptx) editables con la identidad visual de BU LAS + Cervecería y Maltería Quilmes a partir de un brief, información o archivos aportados por el usuario.",
    "files": "No requiere archivos.",
    "prompt": "Quiero que usemos /presentacion-bu-las-cmq y me ayudes a generar una presentación sobre..."
  },
  "Remy": {
    "cmd": "/remy",
    "func": "Genera recomendaciones de innovación de producto basadas en tendencias de consumo, análisis de portfolio y oportunidades de mercado detectadas en data interna.",
    "files": "Brief y todos los conceptos a analizar.",
    "prompt": "Quiero usar /remy para analizar conceptos del pilar..."
  },
  "Influencer Audience": {
    "cmd": "/influencer-audience",
    "func": "Genera un PPTX con el reporte de audiencia de los influencers según datos de CreatorIQ.",
    "files": "No requiere archivos.",
    "prompt": "Quiero el reporte de audiencia del influencer @..."
  },
  "Media Investment": {
    "cmd": "/inversion-abi-dashboard",
    "func": "Genera un HTML interactivo y link a dashboard (Netlify) de inversiones en medios por marca, sistema y período.",
    "files": "No requiere archivos.",
    "prompt": "Mostrame el dashboard de inversiones con /inversion-abi-dashboard"
  },
  "Content Tracker": {
    "cmd": "/content-tracker",
    "func": "Trackea y organiza el contenido publicado por marca y canal, mostrando estado, fechas y métricas clave en un dashboard HTML.",
    "files": "No requiere archivos.",
    "prompt": "Mostrame el content tracker con /content-tracker"
  },
  "Gantt": {
    "cmd": "/gantt",
    "func": "Genera un HTML con el gantt del excel adjunto. También se puede pedir el template para armar el excel.",
    "files": "Archivo xlsx con el plan de trabajo (formato Gantt ABI). Opcional: pedir template.",
    "prompt": "Mostrame el Gantt HTML para el archivo adjunto"
  },
  "Glosario Skills": {
    "cmd": "/glosario-skills",
    "func": "Genera un HTML interactivo con todas las skills disponibles, organizadas por área, con filtros y detalle de cada skill en modal.",
    "files": "No requiere archivos.",
    "prompt": "Quiero ver el glosario de skills con /glosario-skills"
  },
  "Sauron": {
    "cmd": "/sauron-weekly",
    "func": "Actualiza el dashboard de weekly news con información de noticias de los portales y tendencias de twitter.",
    "files": "No requiere archivos.",
    "prompt": "Quiero actualizar el weekly dashboard con /sauron-weekly"
  },
  "Argos": {
    "cmd": "/argos-discovery",
    "func": "Hace un discovery de influencers en instagram en base a distintos pilares de comunicación y genera un HTML con los resultados.",
    "files": "No requiere archivos.",
    "prompt": "Quiero hacer el discovery de influencers con /argos-discovery"
  }
}
```

---

## ITEMS_TYPE

Clasificación de items por tipo (para asignar clases CSS de hover):

```json
{
  "tools":     ["Gantt", "Glosario Skills", "PPT", "Remy"],
  "reporting": ["Analyze Survey", "Influencer Audience", "Media Investment", "Content Tracker", "Sauron", "Argos"]
}
```

---

## CARD_FORMAT

```html
<article class="pillar">
  <div class="pillar-top">
    <div class="pillar-num">{num}.</div>
    <h2 class="pillar-name">{name}</h2>
    <p class="pillar-desc">{desc}</p>
  </div>
  <div class="divider"></div>
  <div class="items">
    <!-- por cada item: asigná class "item item-tool", "item item-report" o "item" según ITEMS_TYPE -->
    <button class="item {type_class}" type="button"
      onclick="openModal('{name}','{cmd}','{func}','{files}','{prompt}')">{name}</button>
  </div>
</article>
```

Escapá las comillas simples en los atributos `onclick` con `\'`. Si `items` está vacío, dejá `<div class="items"></div>`.

---

## HTML_TEMPLATE

El template HTML base se encuentra en `template.html` (misma carpeta que este archivo).
Leélo con `Read` o con Python antes de hacer las sustituciones:

```python
template = (SKILL_DIR / "template.html").read_text(encoding="utf-8")
```

---

## Script sugerido

```python
import base64, json, re
from pathlib import Path

SKILL_DIR = Path(__file__).parent
OUT = Path.cwd() / "one-abi-skills.html"

def b64(p): return base64.b64encode(p.read_bytes()).decode()

skill_md = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

def extract_json(header):
    m = re.search(rf"## {header}.*?```json\s*", skill_md, re.S)
    if not m:
        raise ValueError(f"Section {header} not found")
    start = skill_md.index('{', m.end())
    depth = 0
    for i, c in enumerate(skill_md[start:], start):
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return skill_md[start:i+1]
    raise ValueError(f"Unmatched braces in {header}")

pillars    = json.loads(extract_json("PILLARS_DATA"))["pillars"]
items_data = json.loads(extract_json("ITEMS_DATA"))
items_type = json.loads(extract_json("ITEMS_TYPE"))
template   = (SKILL_DIR / "template.html").read_text(encoding="utf-8")

TOOLS     = set(items_type["tools"])
REPORTING = set(items_type["reporting"])

def item_class(name):
    if name in TOOLS:     return "item item-tool"
    if name in REPORTING: return "item item-report"
    return "item"

def esc(s): return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")

def card(p):
    items = ""
    for name in p["items"]:
        d = items_data.get(name, {})
        cls = item_class(name)
        items += (
            f'<button class="{cls}" type="button" '
            f'onclick="openModal(\'{esc(name)}\',\'{esc(d.get("cmd",""))}\','
            f'\'{esc(d.get("func",""))}\',\'{esc(d.get("files","—"))}\','
            f'\'{esc(d.get("prompt",""))}\')">'+
            f'{name}</button>'
        )
    return (
        '<article class="pillar">'
        '<div class="pillar-top">'
        f'<div class="pillar-num">{p["num"]}.</div>'
        f'<h2 class="pillar-name">{p["name"]}</h2>'
        f'<p class="pillar-desc">{p["desc"]}</p>'
        '</div>'
        '<div class="divider"></div>'
        f'<div class="items">{items}</div>'
        '</article>'
    )

cards = "\n".join(card(p) for p in pillars)

html = (template
    .replace("/* LOGO_B64 */", b64(SKILL_DIR / "references/assets/one-abi-way-logo.png"))
    .replace("/* AV_LIGHT */", b64(SKILL_DIR / "references/assets/fonts/Avantt-Light.ttf"))
    .replace("/* AV_REG */",   b64(SKILL_DIR / "references/assets/fonts/Avantt-Regular.ttf"))
    .replace("/* AV_SB */",    b64(SKILL_DIR / "references/assets/fonts/Avantt-SemiBold.ttf"))
    .replace("/* AV_BOLD */",  b64(SKILL_DIR / "references/assets/fonts/Avantt-Bold.ttf"))
    .replace("<!-- PILLARS_CARDS -->", cards)
)

OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT}")
```

---

## Reglas y constraints

- Si el usuario pide agregar, modificar o eliminar una skill del glosario, solicitar primero la contraseña de modificación. La contraseña correcta es: **datamkt**. Solo proceder si el usuario la proporciona correctamente.

---

## Archivos incluidos en la skill

- `SKILL.md` (este archivo)
- `template.html` — template HTML base del output (estilos, estructura, JS)
- `references/assets/one-abi-way-logo.png` — logo ONE ABI WAY con emblema amarillo
- `references/assets/fonts/Avantt-Light.ttf`
- `references/assets/fonts/Avantt-Regular.ttf`
- `references/assets/fonts/Avantt-SemiBold.ttf`
- `references/assets/fonts/Avantt-Bold.ttf`

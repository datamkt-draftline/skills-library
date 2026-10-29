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

## Cómo funciona

1. Leé `PILLARS_DATA` y `ITEMS_DATA` de abajo y construí la estructura en memoria.
   - Si el usuario pide modificar/agregar/sacar items o metadata, actualizá los datos antes de renderizar.
2. Para cada pilar, generá una card siguiendo el formato de `CARD_FORMAT`.
3. Reemplazá los placeholders del `HTML_TEMPLATE`:
   - `/* LOGO_B64 */` → base64 de `one-abi-way-logo.png` (carpeta de la skill).
   - `/* AV_LIGHT */`, `/* AV_REG */`, `/* AV_SB */`, `/* AV_BOLD */` → base64 de las 4 fuentes en `fonts/`.
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

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ONE ABI WAY · Pillars</title>
<style>
  @font-face {
    font-family: 'Avantt'; font-weight: 300; font-style: normal; font-display: swap;
    src: url(data:font/ttf;base64,/* AV_LIGHT */) format('truetype');
  }
  @font-face {
    font-family: 'Avantt'; font-weight: 400; font-style: normal; font-display: swap;
    src: url(data:font/ttf;base64,/* AV_REG */) format('truetype');
  }
  @font-face {
    font-family: 'Avantt'; font-weight: 600; font-style: normal; font-display: swap;
    src: url(data:font/ttf;base64,/* AV_SB */) format('truetype');
  }
  @font-face {
    font-family: 'Avantt'; font-weight: 700; font-style: normal; font-display: swap;
    src: url(data:font/ttf;base64,/* AV_BOLD */) format('truetype');
  }
  :root {
    --yellow: #FFD100;
    --ink: #1a1a1a;
    --card: #ffffff;
    --card-border: #ececec;
    --bg: #faf7f1;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: 'Avantt', 'Inter', 'Segoe UI', Arial, sans-serif;
    color: var(--ink);
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
    background:
      radial-gradient(ellipse 55% 42% at 50% 10%, rgba(255,209,0,0.35) 0%, rgba(255,209,0,0.08) 55%, rgba(255,209,0,0) 80%),
      var(--bg);
  }
  .wrap { max-width: 1360px; margin: 0 auto; padding: 40px 28px 64px; }
  header.title { text-align: center; margin-bottom: 44px; }
  header.title img { width: min(520px, 80%); height: auto; display: block; margin: 0 auto; }
  .pillars-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 14px;
    align-items: stretch;
  }
  .pillar {
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 22px 18px 22px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
    height: 100%;
    transition: background .18s ease, border-color .18s ease, transform .18s ease, box-shadow .18s ease;
  }
  .pillar:hover {
    background: linear-gradient(180deg, #FFE88A 0%, #FFDA7A 55%, #FFC97A 100%);
    border-color: #F3C054;
    box-shadow: 0 6px 20px rgba(255,180,60,.28);
    transform: translateY(-2px);
  }
  .pillar-top { display: flex; flex-direction: column; gap: 10px; }
  .pillar-num { font-size: 22px; font-weight: 700; color: #a3a3a3; letter-spacing: -0.02em; line-height: 1; margin-bottom: 2px; }
  .pillar-name { margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.01em; color: var(--ink); line-height: 1.15; min-height: 46px; }
  .pillar-desc { margin: 0; color: #4a4a4a; font-size: 13px; line-height: 1.5; font-weight: 400; min-height: 78px; }
  .divider { height: 1px; background: rgba(0,0,0,.1); margin: 4px -4px 2px; }
  .pillar:hover .divider { background: rgba(0,0,0,.18); }
  .items { display: flex; flex-direction: column; gap: 8px; margin-top: 0; }
  .item {
    width: 100%;
    background: #ffffff;
    border: 1px solid #e5e5e5;
    color: var(--ink);
    font-family: inherit;
    font-size: 12.5px;
    font-weight: 600;
    padding: 9px 14px;
    border-radius: 999px;
    cursor: pointer;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,.04);
    transition: background .15s ease, border-color .15s ease, transform .15s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .item-tool   { background: #FFF9EA; border-color: #E8D29A; }
  .item-report { background: #F6F8FB; border-color: #B9C5D9; }
  .item:hover { background: #FFF0B8; border-color: #B88A2A; color: var(--ink); transform: translateY(-1px); }
  .item-tool:hover   { background: #FFF4D6; border-color: #D4A843; color: var(--ink); transform: translateY(-1px); }
  .item-report:hover { background: #EEF1F7; border-color: #8099C0; color: var(--ink); transform: translateY(-1px); }

  .subtitle {
    text-align: center;
    margin: -32px 0 12px;
    font-size: 18px;
    font-weight: 400;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: #888;
  }
  .legend {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 36px;
  }
  .legend-item {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .07em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 999px;
    border: 1px solid;
  }
  .legend-tool   { background: #FFF4D6; border-color: #D4A843; color: #7A5C1A; }
  .legend-report { background: #EEF1F7; border-color: #8099C0; color: #3A537A; }

  /* Modal */
  .modal-backdrop {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(10,10,10,.45);
    backdrop-filter: blur(4px);
    z-index: 1000;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }
  .modal-backdrop.open { display: flex; }
  .modal {
    background: #fff;
    border-radius: 20px;
    padding: 32px 32px 28px;
    max-width: 480px;
    width: 100%;
    box-shadow: 0 24px 64px rgba(0,0,0,.18);
    position: relative;
    animation: modalIn .18s ease;
  }
  @keyframes modalIn {
    from { opacity: 0; transform: translateY(12px) scale(.97); }
    to   { opacity: 1; transform: none; }
  }
  .modal-close {
    position: absolute; top: 16px; right: 18px;
    background: none; border: none; cursor: pointer;
    font-size: 22px; color: #999; line-height: 1; padding: 4px 6px;
    border-radius: 6px; transition: color .12s, background .12s;
  }
  .modal-close:hover { color: var(--ink); background: #f0f0f0; }
  .modal-title { font-size: 20px; font-weight: 700; margin: 0 0 6px; color: var(--ink); }
  .modal-cmd-row { display: flex; align-items: center; gap: 8px; margin-bottom: 20px; }
  .modal-cmd {
    display: inline-block;
    background: #1a1a1a; color: #FFD100;
    font-family: 'Avantt', monospace;
    font-size: 13px; font-weight: 600;
    padding: 5px 14px; border-radius: 999px;
    letter-spacing: .02em;
  }
  .copy-btn {
    display: inline-flex; align-items: center; justify-content: center;
    width: 30px; height: 30px;
    background: #f3f3f3;
    border: 1px solid #e0e0e0;
    border-radius: 50%;
    cursor: pointer;
    color: #555;
    transition: background .15s ease, color .15s ease, border-color .15s ease, transform .15s ease;
    padding: 0;
    position: relative;
  }
  .copy-btn:hover { background: #FFD100; color: #1a1a1a; border-color: #D4A843; }
  .copy-btn.copied { background: #16a34a; color: #fff; border-color: #15803d; }
  .copy-btn svg { width: 14px; height: 14px; }
  .copy-tooltip {
    position: absolute;
    top: -30px; left: 50%; transform: translateX(-50%);
    background: #1a1a1a; color: #fff;
    font-size: 10px; font-weight: 600;
    padding: 3px 8px; border-radius: 4px;
    white-space: nowrap;
    pointer-events: none;
    opacity: 0;
    transition: opacity .15s ease;
  }
  .copy-btn.copied .copy-tooltip { opacity: 1; }
  .modal-section-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: #a3a3a3; margin: 0 0 5px; }
  .modal-section-body { font-size: 13.5px; font-weight: 400; color: #333; line-height: 1.6; margin: 0 0 18px; }
  .modal-section-body:last-child { margin-bottom: 0; }

  @media (max-width: 1200px) { .pillars-grid { grid-template-columns: repeat(4, 1fr); } }
  @media (max-width: 820px)  { .pillars-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 520px)  {
    .wrap { padding: 28px 18px 48px; }
    .pillars-grid { grid-template-columns: 1fr; gap: 12px; }
    .pillar-name, .pillar-desc { min-height: auto; }
    .modal { padding: 24px 20px 20px; }
  }
</style>
</head>
<body>

<div class="modal-backdrop" id="modalBackdrop" onclick="closeModalOutside(event)">
  <div class="modal" id="modal">
    <button class="modal-close" onclick="closeModal()" aria-label="Cerrar">&times;</button>
    <h2 class="modal-title" id="mTitle"></h2>
    <div class="modal-cmd-row">
      <span class="modal-cmd" id="mCmd"></span>
      <button class="copy-btn" id="mCopy" type="button" onclick="copyPrompt(event)" aria-label="Copiar prompt">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        <span class="copy-tooltip">Copiado!</span>
      </button>
    </div>
    <p class="modal-section-label">Funcionalidad</p>
    <p class="modal-section-body" id="mFunc"></p>
    <p class="modal-section-label">Archivos requeridos</p>
    <p class="modal-section-body" id="mFiles"></p>
  </div>
</div>

<div class="wrap">
  <header class="title">
    <img src="data:image/png;base64,/* LOGO_B64 */" alt="ONE ABI WAY">
  </header>
  <p class="subtitle">Glosario de skills</p>
  <div class="legend">
    <span class="legend-item legend-tool">Tool</span>
    <span class="legend-item legend-report">Reporting</span>
  </div>
  <section class="pillars-grid">
    <!-- PILLARS_CARDS -->
  </section>
</div>

<script>
  let currentPrompt = '';
  function openModal(name, cmd, func, files, prompt) {
    document.getElementById('mTitle').textContent = name;
    document.getElementById('mCmd').textContent   = cmd;
    document.getElementById('mFunc').textContent  = func;
    document.getElementById('mFiles').textContent = files;
    currentPrompt = prompt || '';
    document.getElementById('mCopy').classList.remove('copied');
    document.getElementById('modalBackdrop').classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function copyPrompt(e) {
    e.stopPropagation();
    const btn = document.getElementById('mCopy');
    const done = () => {
      btn.classList.add('copied');
      setTimeout(() => btn.classList.remove('copied'), 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(currentPrompt).then(done).catch(() => {
        const ta = document.createElement('textarea');
        ta.value = currentPrompt;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); done(); } catch (_) {}
        document.body.removeChild(ta);
      });
    } else {
      const ta = document.createElement('textarea');
      ta.value = currentPrompt;
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (_) {}
      document.body.removeChild(ta);
    }
  }
  function closeModal() {
    document.getElementById('modalBackdrop').classList.remove('open');
    document.body.style.overflow = '';
  }
  function closeModalOutside(e) {
    if (e.target === document.getElementById('modalBackdrop')) closeModal();
  }
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
</script>
</body>
</html>
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
template   = re.search(r"## HTML_TEMPLATE\s*```html\s*(<!doctype.*?</html>)\s*```", skill_md, re.S).group(1)

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
    .replace("/* LOGO_B64 */", b64(SKILL_DIR / "one-abi-way-logo.png"))
    .replace("/* AV_LIGHT */", b64(SKILL_DIR / "fonts/Avantt-Light.ttf"))
    .replace("/* AV_REG */",   b64(SKILL_DIR / "fonts/Avantt-Regular.ttf"))
    .replace("/* AV_SB */",    b64(SKILL_DIR / "fonts/Avantt-SemiBold.ttf"))
    .replace("/* AV_BOLD */",  b64(SKILL_DIR / "fonts/Avantt-Bold.ttf"))
    .replace("<!-- PILLARS_CARDS -->", cards)
)

OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT}")
```

---

## Archivos incluidos en la skill

- `SKILL.md` (este archivo)
- `one-abi-way-logo.png` — logo ONE ABI WAY con emblema amarillo
- `fonts/Avantt-Light.ttf`
- `fonts/Avantt-Regular.ttf`
- `fonts/Avantt-SemiBold.ttf`
- `fonts/Avantt-Bold.ttf`

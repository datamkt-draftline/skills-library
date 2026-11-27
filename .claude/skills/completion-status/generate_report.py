"""
Genera el reporte LAS Completion Status a partir de la plantilla maestra,
actualizando:
  - el campo "Last Update" con la fecha de hoy
  - la sección del gantt Skills de Medios:
      · ventana de 14 semanas con la semana actual siempre en posición 8 (1-indexed)
        → 7 semanas antes + actual + 6 después
      · encabezados (Wxx y fecha del lunes), estrella y highlight dinámicos
      · barras recalculadas según rango de cada tarea
Imprime la ruta del archivo generado.
"""
import re
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[3]  # ~/work/2026-09-14_9muktr/
TEMPLATE = ROOT / "reporte_completion_LAS_v2.html"
TODAY    = date.today()
OUT      = ROOT / f"reporte_completion_LAS_{TODAY.strftime('%Y-%m-%d')}.html"

# ── Datos de tareas (actualizar cuando cambie el plan) ───────────────────────
# start/end son números de semana ISO del año actual
TASKS = [
    {"label": "Media-dash",     "func": "Tablero Medios",       "pct": "100%", "color": "#27ae60", "start": 39, "end": 43},
    {"label": "Conent-Tracker", "func": "Analisis Cont. Digl",  "pct": "100%", "color": "#27ae60", "start": 40, "end": 42},
    {"label": "1YP-medios",     "func": "1YP Media Investment", "pct": "0%",   "color": "#e74c3c", "start": 45, "end": 47},
    {"label": "Influs-CMQ",     "func": "Influencers Perfo.",   "pct": "50%",  "color": "#f39c12", "start": 46, "end": 51},
    {"label": "TRPS-CMQ",       "func": "Analisis TRPs",        "pct": "0%",   "color": "#e74c3c", "start": 49, "end": 50},
]

# ── Ventana de semanas (7 antes + actual + 6 después = 14) ───────────────────
monday_cur = TODAY - timedelta(days=TODAY.weekday())   # lunes de la semana actual
window_mondays = [monday_cur + timedelta(weeks=i) for i in range(-7, 7)]
week_nums      = [d.isocalendar()[1] for d in window_mondays]  # Wxx de cada lunes
CUR_IDX        = 7                                              # índice 0-based de la semana actual

def bar_class(pct_str):
    pct = int(pct_str.replace('%', ''))
    if pct == 100: return "bar-full"
    if pct == 0:   return "bar-zero"
    return "bar-half"

def fmt_date(d):
    return f"{d.day}/{d.month}"

# ── Fila de estrella (posición siempre fija) ─────────────────────────────────
# 3 cols meta + 7 semanas antes = colspan 10 antes; 6 semanas después
star_row = (
    '        <tr class="star-row">'
    '<td colspan="10"></td>'
    '<td class="star-cell">★</td>'
    '<td colspan="6"></td>'
    '</tr>'
)

# ── Encabezado de semanas ────────────────────────────────────────────────────
meta_ths = (
    '<th class="meta-col">Skill</th>'
    '<th class="meta-col" style="min-width:120px;">Función</th>'
    '<th class="meta-col" style="min-width:38px;">%</th>'
)
week_ths = []
for i, (wn, mon) in enumerate(zip(week_nums, window_mondays)):
    if i == CUR_IDX:
        week_ths.append(
            f'<th class="wk-cur-th">W{wn}<br>'
            f'<span style="font-weight:400;font-size:9px;">{fmt_date(mon)}</span></th>'
        )
    else:
        week_ths.append(
            f'<th>W{wn}<br>'
            f'<span style="font-weight:400;font-size:9px;color:#8899bb;">{fmt_date(mon)}</span></th>'
        )

thead = (
    '      <thead>\n'
    + star_row + '\n'
    + '        <tr>\n'
    + '          ' + meta_ths + '\n'
    + '          ' + '\n          '.join(week_ths) + '\n'
    + '        </tr>\n'
    + '      </thead>'
)

# ── Filas de tareas ──────────────────────────────────────────────────────────
def build_row(t):
    meta = (
        f'<td class="meta-td">{t["label"]}</td>'
        f'<td class="func-td">{t["func"]}</td>'
        f'<td class="pct-td" style="color:{t["color"]};">{t["pct"]}</td>'
    )

    # Clasificar cada columna de semana como 'bar' o 'empty'
    types = ['bar' if t['start'] <= wn <= t['end'] else 'empty' for wn in week_nums]

    # Construir celdas fusionando consecutivas del mismo tipo
    tds = []
    i = 0
    while i < len(types):
        cell_type = types[i]
        # agrupar consecutivas iguales
        j = i + 1
        while j < len(types) and types[j] == cell_type:
            j += 1
        span      = j - i
        indices   = list(range(i, j))
        has_cur   = CUR_IDX in indices

        if cell_type == 'bar':
            bc = bar_class(t["pct"])
            bg = ' background:#1e3560;' if has_cur else ''
            tds.append(f'<td colspan="{span}" style="padding:4px 3px;{bg}"><span class="{bc}"></span></td>')
        else:
            # celdas vacías: si incluyen la semana actual hay que separarla
            if has_cur and span > 1:
                for idx in indices:
                    cls = ' class="wk-cur-td"' if idx == CUR_IDX else ''
                    tds.append(f'<td{cls}></td>')
            elif has_cur:
                tds.append('<td class="wk-cur-td"></td>')
            else:
                # sin semana actual: se pueden dejar sueltos (no hay beneficio visual en fusionar)
                tds.extend(['<td></td>'] * span)
        i = j

    return (
        '        <tr>\n'
        '          ' + meta + '\n'
        '          ' + '\n          '.join(tds) + '\n'
        '        </tr>'
    )

tbody = (
    '      <tbody>\n'
    + '\n'.join(build_row(t) for t in TASKS)
    + '\n      </tbody>'
)

gantt_block = (
    '  <div class="gantt-wrap">\n'
    '    <table class="gantt-proj">\n'
    + thead + '\n'
    + tbody + '\n'
    '    </table>\n'
    '  </div>'
)

# ── Leer plantilla y aplicar actualizaciones ─────────────────────────────────
html = TEMPLATE.read_text(encoding='utf-8')

# 1. Last Update
html = re.sub(
    r'Last Update:.*?</div>',
    f'Last Update: {TODAY.strftime("%d/%m/%Y")}</div>',
    html,
)

# 2. Reemplazar bloque del gantt Skills de Medios
html = re.sub(
    r'<div class="gantt-wrap">\s*<table class="gantt-proj">.*?</table>\s*</div>',
    gantt_block,
    html,
    flags=re.DOTALL,
)

OUT.write_text(html, encoding='utf-8')
print(OUT)

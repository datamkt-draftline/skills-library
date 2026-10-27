#!/usr/bin/env python3
"""Read a Gantt Excel file and emit a self-contained interactive HTML Gantt.

Usage: python generate_gantt.py <input.xlsx> [output.html]

Expected sheets:
  - Areas:     Area | Color | Orden
  - <AreaName> (one sheet per area, named like the area):
               Tarea | Fecha inicio | Fecha fin | Estado
  - Hitos:     Tarea | Tipo | Fecha | Link
  - TiposHito: Tipo | Color | Icono
  - Config:    Clave | Valor

For backwards compatibility a single-sheet 'Tareas' with an 'Area' column is
still supported.
"""
import json
import os
import sys
from datetime import date, datetime

try:
    from openpyxl import load_workbook
except ImportError as e:
    sys.exit(f"ERROR: openpyxl no está disponible ({e}).")


RESERVED_SHEETS = {"Areas", "Hitos", "TiposHito", "Config", "Tareas"}


def _d(v):
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.date().isoformat()
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, str):
        s = v.strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(s, fmt).date().isoformat()
            except ValueError:
                pass
    return str(v)


def _s(v):
    return str(v).strip() if v is not None else ""


def _rows(ws):
    it = ws.iter_rows(values_only=True)
    try:
        headers = [_s(h) for h in next(it)]
    except StopIteration:
        return []
    out = []
    for row in it:
        if all(v is None or v == "" for v in row):
            continue
        out.append({headers[i]: row[i] if i < len(row) else None for i in range(len(headers))})
    return out


def read_workbook(path):
    wb = load_workbook(path, data_only=True)

    # Areas (defines order and color).
    areas = []
    if "Areas" in wb.sheetnames:
        for r in _rows(wb["Areas"]):
            name = _s(r.get("Area"))
            if not name:
                continue
            areas.append({
                "area": name,
                "color": _s(r.get("Color")) or "#888",
                "orden": r.get("Orden") or 0,
            })

    # Tareas + hitos inline: each area sheet has task rows (Tarea filled) and
    # milestone sub-rows (Tarea empty, Tipo hito filled). Fallback: legacy
    # single 'Tareas' sheet with Area column, and 'Hitos'/'Hitos - <area>' sheets.
    tareas = []
    hitos = []

    for a in areas:
        name = a["area"]
        if name not in wb.sheetnames:
            continue
        current_tarea = None
        for r in _rows(wb[name]):
            tarea_val = _s(r.get("Tarea"))
            tipo_val  = _s(r.get("Tipo hito"))
            if tarea_val:
                current_tarea = tarea_val
                tareas.append({
                    "area": name,
                    "tarea": tarea_val,
                    "inicio": _d(r.get("Fecha inicio")),
                    "fin": _d(r.get("Fecha fin")),
                    "estado": _s(r.get("Estado")),
                    "detalle": _s(r.get("Detalle")),
                })
            elif tipo_val and current_tarea:
                hitos.append({
                    "tarea": current_tarea,
                    "tipo": tipo_val,
                    "fecha": _d(r.get("Fecha hito")),
                    "link": _s(r.get("Link hito")),
                    "detalle": _s(r.get("Detalle")),
                })

    # Legacy: single 'Tareas' sheet with Area column.
    if "Tareas" in wb.sheetnames:
        for r in _rows(wb["Tareas"]):
            if not _s(r.get("Tarea")):
                continue
            tareas.append({
                "area": _s(r.get("Area")),
                "tarea": _s(r.get("Tarea")),
                "inicio": _d(r.get("Fecha inicio")),
                "fin": _d(r.get("Fecha fin")),
                "estado": _s(r.get("Estado")),
                "detalle": _s(r.get("Detalle")),
            })

    # Legacy: 'Hitos - <area>' sheets or single 'Hitos' sheet.
    if not hitos:
        per_area_found = False
        for a in areas:
            sn = f"Hitos - {a['area']}"
            if sn in wb.sheetnames:
                per_area_found = True
                for r in _rows(wb[sn]):
                    if not _s(r.get("Tarea")):
                        continue
                    hitos.append({"tarea": _s(r.get("Tarea")), "tipo": _s(r.get("Tipo")),
                                  "fecha": _d(r.get("Fecha")), "link": _s(r.get("Link"))})
        if not per_area_found and "Hitos" in wb.sheetnames:
            for r in _rows(wb["Hitos"]):
                if not _s(r.get("Tarea")):
                    continue
                hitos.append({"tarea": _s(r.get("Tarea")), "tipo": _s(r.get("Tipo")),
                              "fecha": _d(r.get("Fecha")), "link": _s(r.get("Link"))})

    # TiposHito.
    tipos = []
    if "TiposHito" in wb.sheetnames:
        for r in _rows(wb["TiposHito"]):
            name = _s(r.get("Tipo"))
            if not name:
                continue
            tipos.append({
                "tipo": name,
                "color": _s(r.get("Color")) or "#555",
                "icono": _s(r.get("Icono")) or "flag",
            })

    if not tipos:
        palette = ["#D97706", "#0D9488", "#EA580C", "#16A34A", "#DC2626", "#6366F1"]
        seen, i = {}, 0
        for h in hitos:
            if h["tipo"] and h["tipo"] not in seen:
                seen[h["tipo"]] = True
                tipos.append({"tipo": h["tipo"], "color": palette[i % len(palette)], "icono": "flag"})
                i += 1

    # Config.
    config = {}
    if "Config" in wb.sheetnames:
        for r in _rows(wb["Config"]):
            k = _s(r.get("Clave"))
            if k:
                config[k] = r.get("Valor")

    return {
        "config": {"titulo": str(config.get("Titulo", "Gantt")), "subtitulo": str(config.get("Subtitulo", "") or "")},
        "areas": sorted(areas, key=lambda a: (a.get("orden") or 0, a["area"])),
        "tipos": tipos,
        "tareas": tareas,
        "hitos": hitos,
    }


_TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "template.html")

def _load_template():
    with open(_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()



def _slug(s):
    import re, unicodedata
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "gantt"


def generate(input_path, output_path=None):
    data = read_workbook(input_path)
    if output_path is None:
        slug = _slug(data["config"].get("titulo") or "gantt")
        output_path = os.path.join(os.path.dirname(os.path.abspath(input_path)), f"{slug}-gantt.html")

    html = (_load_template()
            .replace("__TITULO__", data["config"]["titulo"])
            .replace("__SUBTITULO__", data["config"]["subtitulo"])
            .replace("__DATA__", json.dumps(data, ensure_ascii=False)))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Uso: python generate_gantt.py <input.xlsx> [output.html]")
    inp = sys.argv[1]
    outp = sys.argv[2] if len(sys.argv) > 2 else None
    print(generate(inp, outp))

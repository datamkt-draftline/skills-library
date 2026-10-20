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
                })
            elif tipo_val and current_tarea:
                hitos.append({
                    "tarea": current_tarea,
                    "tipo": tipo_val,
                    "fecha": _d(r.get("Fecha hito")),
                    "link": _s(r.get("Link hito")),
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


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>__TITULO__</title>
<style>
  :root {
    --label-w: 240px;
    --date-w: 130px;
    --sticky-w: 370px;
    --bg: #fafaf7;
    --row-h: 46px;
    --col-pendiente-bg: #e5e7eb;
    --col-pendiente-fg: #4b5563;
    --col-pendiente-border: #d1d5db;
    --col-encurso-bg: #fef3c7;
    --col-encurso-fg: #92400e;
    --col-encurso-border: #fde68a;
    --col-completada-bg: #d1fae5;
    --col-completada-fg: #065f46;
    --col-completada-border: #a7f3d0;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: #1f2937; }
  .wrap { padding: 24px 32px; }
  h1 { margin: 0 0 2px; font-size: 22px; font-weight: 700; letter-spacing: -0.01em; }
  h1 .sub { font-weight: 400; color: #6b7280; margin-left: 10px; font-size: 14px; }

  .controls { display: flex; flex-wrap: wrap; gap: 20px; align-items: center; margin: 18px 0 14px; }
  .area-buttons, .status-filters { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  .ctrl-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #6b7280; font-weight: 600; margin-right: 6px; }
  .pill { display: inline-flex; align-items: center; gap: 7px; padding: 6px 12px; border-radius: 999px; font-size: 13px; cursor: pointer; user-select: none; background: #fff; border: 1px solid #e5e7eb; transition: all .15s; font-weight: 500; }
  .pill:hover { border-color: #9ca3af; }
  .pill .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
  .pill.off { opacity: 0.4; background: #f3f4f6; }

  .status-pill { background: #fff; color: #6b7280; border: 1px solid #e5e7eb; }
  .status-pill[data-s="pendiente"].active  { background: var(--col-pendiente-bg);  color: var(--col-pendiente-fg);  border-color: var(--col-pendiente-border); }
  .status-pill[data-s="en curso"].active   { background: var(--col-encurso-bg);    color: var(--col-encurso-fg);    border-color: var(--col-encurso-border); }
  .status-pill[data-s="completada"].active { background: var(--col-completada-bg); color: var(--col-completada-fg); border-color: var(--col-completada-border); }

  /* Tabs de áreas */
  .tabs { display: flex; gap: 0; border-bottom: 2px solid #e5e7eb; margin: 14px 0 12px; }
  .tab { padding: 8px 18px; font-size: 13px; font-weight: 500; cursor: pointer; color: #6b7280; border-bottom: 2px solid transparent; margin-bottom: -2px; user-select: none; transition: color .15s, border-color .15s; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
  .tab:hover { color: #1f2937; }
  .tab.active { color: #1f2937; }
  .tab .dot { width: 8px; height: 8px; border-radius: 50%; }

  /* Search */
  .search-input { padding: 6px 12px; border-radius: 999px; border: 1px solid #e5e7eb; font-size: 13px; width: 180px; background: #fff; font-family: inherit; color: #1f2937; }
  .search-input:focus { outline: none; border-color: #9ca3af; }
  .search-input::placeholder { color: #9ca3af; }

  /* Zoom */
  .zoom-btn.active { background: #1f2937; color: #fff; border-color: #1f2937; }

  /* Overdue indicator - very subtle, after task name */
  .overdue-icon { width: 13px; height: 13px; color: #dc2626; opacity: 0.6; flex-shrink: 0; margin-left: 6px; display: inline-block; vertical-align: middle; }

  .legend { display: flex; flex-wrap: wrap; gap: 16px; padding: 10px 0; margin-bottom: 8px; border-top: 1px solid #e5e7eb; border-bottom: 1px solid #e5e7eb; }
  .legend-item { display: inline-flex; align-items: center; gap: 7px; font-size: 12px; color: #4b5563; line-height: 1; }
  .legend-badge { width: 20px; height: 20px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; color: #fff; flex-shrink: 0; }
  .legend-badge svg { width: 11px; height: 11px; }

  .gantt { position: relative; overflow-x: auto; overflow-y: visible; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; }
  .gantt-inner { position: relative; }

  .timeline-header { position: sticky; top: 0; z-index: 10; background: #fff; border-bottom: 1px solid #e5e7eb; height: 44px; display: flex; }
  .th-sticky { position: sticky; left: 0; z-index: 11; width: var(--sticky-w); min-width: var(--sticky-w); background: #fff; border-right: 1px solid #e5e7eb; display: flex; align-items: center; padding: 0 16px 0 32px; font-size: 11px; letter-spacing: 0.08em; color: #9ca3af; font-weight: 600; text-transform: uppercase; }
  .th-track { position: relative; flex-shrink: 0; }
  .month-label { position: absolute; top: 0; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 11px; letter-spacing: 0.1em; color: #6b7280; font-weight: 600; text-transform: uppercase; pointer-events: none; }
  .week-label { position: absolute; display: flex; align-items: center; justify-content: center; font-size: 10px; letter-spacing: 0.04em; color: #9ca3af; font-weight: 600; pointer-events: none; border-left: 1px solid #f3f4f6; }
  .day-label { position: absolute; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #9ca3af; font-weight: 500; pointer-events: none; }
  .day-label.weekend { color: #d1d5db; }
  .month-divider { position: absolute; top: 0; width: 1px; height: 100%; background: #f3f4f6; }
  .year-divider { background: #d1d5db; }
  .year-badge { color: #9ca3af; margin-left: 6px; font-weight: 500; }

  .today-triangle { position: absolute; top: 0; width: 0; height: 0; border-left: 7px solid transparent; border-right: 7px solid transparent; border-top: 10px solid #dc2626; transform: translateX(-50%); z-index: 15; filter: drop-shadow(0 1px 2px rgba(0,0,0,.1)); }

  .area-section { border-bottom: 1px solid #f3f4f6; }

  .area-header-wrap { height: 38px; position: relative; }
  .area-header { position: sticky; left: 0; z-index: 7; display: inline-flex; align-items: center; gap: 8px; padding: 14px 20px 6px 32px; background: #fff; width: var(--sticky-w); height: 100%; }
  .area-header .dot { width: 10px; height: 10px; border-radius: 50%; }
  .area-header .name { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #1f2937; }

  .row { position: relative; height: var(--row-h); display: flex; align-items: center; background: #fff; }

  .row-label { position: sticky; left: 0; z-index: 4; background: #fff; width: var(--label-w); min-width: var(--label-w); padding: 0 12px 0 32px; display: flex; align-items: center; gap: 8px; height: 100%; }
  .row-label .task-name { font-size: 13px; font-weight: 500; color: #1f2937; line-height: 1.3; }

  .row-date { position: sticky; left: var(--label-w); z-index: 4; background: #fff; width: var(--date-w); min-width: var(--date-w); padding: 0 8px 0 6px; display: flex; align-items: center; gap: 3px; height: 100%; border-right: 1px solid #f3f4f6; font-size: 11px; color: #6b7280; font-variant-numeric: tabular-nums; }
  .row-date .arrow { color: #c7c7c7; margin: 0 1px; }
  .row-date .status-icon { width: 14px; height: 14px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; margin-right: 3px; }
  .row-date .status-icon svg { width: 13px; height: 13px; display: block; }

  .row-track { position: relative; flex-shrink: 0; height: 100%; }

  .bar { position: absolute; top: 50%; transform: translateY(-50%); height: 18px; border-radius: 9px; }
  .bar.pendiente  { background: #9ab3c8; opacity: 0.65; }
  .bar.en-curso   { background: #d4bb8c; opacity: 0.80; }
  .bar.completada { background: #7db87d; opacity: 0.70; }

  .milestone { position: absolute; top: 50%; transform: translate(-50%, -50%); width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; z-index: 2; box-shadow: 0 1px 3px rgba(0,0,0,0.15); }
  .milestone.has-link { cursor: pointer; }
  .milestone.has-link:hover { transform: translate(-50%, -50%) scale(1.15); }
  .milestone svg { width: 12px; height: 12px; display: block; }
  .milestone .tip { position: absolute; bottom: 115%; left: 50%; transform: translateX(-50%); background: #1f2937; color: #fff; padding: 5px 9px; border-radius: 4px; font-size: 11px; white-space: nowrap; opacity: 0; pointer-events: none; transition: opacity .15s; z-index: 20; }
  .milestone:hover .tip { opacity: 1; }

  /* --- Dark mode --- */
  [data-theme="dark"] body { background: #111827; color: #f3f4f6; }
  [data-theme="dark"] h1 { color: #f9fafb; }
  [data-theme="dark"] h1 .sub { color: #6b7280; }
  [data-theme="dark"] .ctrl-label { color: #6b7280; }
  [data-theme="dark"] .pill { background: #1f2937; border-color: #374151; color: #d1d5db; }
  [data-theme="dark"] .pill:hover { border-color: #6b7280; }
  [data-theme="dark"] .pill.off { background: #111827; opacity: 0.45; }
  [data-theme="dark"] .legend { border-color: #374151; }
  [data-theme="dark"] .legend-item { color: #9ca3af; }
  [data-theme="dark"] .gantt { background: #1f2937; border-color: #374151; }
  [data-theme="dark"] .timeline-header { background: #1f2937; border-color: #374151; }
  [data-theme="dark"] .th-sticky { background: #1f2937; border-color: #374151; color: #4b5563; }
  [data-theme="dark"] .month-label { color: #6b7280; }
  [data-theme="dark"] .week-label { color: #6b7280; border-color: #2d3748; }
  [data-theme="dark"] .day-label { color: #6b7280; }
  [data-theme="dark"] .day-label.weekend { color: #4b5563; }
  [data-theme="dark"] .month-divider { background: #2d3748; }
  [data-theme="dark"] .year-divider { background: #4b5563; }
  [data-theme="dark"] .year-badge { color: #6b7280; }
  [data-theme="dark"] .area-section { border-color: #2d3748; }
  [data-theme="dark"] .area-header { background: #1f2937; }
  [data-theme="dark"] .area-header .name { color: #e5e7eb; }
  [data-theme="dark"] .row { background: #1f2937; }
  [data-theme="dark"] .row-label { background: #1f2937; }
  [data-theme="dark"] .row-label .task-name { color: #f3f4f6; }
  [data-theme="dark"] .row-date { background: #1f2937; border-color: #2d3748; color: #9ca3af; }
  [data-theme="dark"] .row-date .arrow { color: #374151; }
  [data-theme="dark"] .bar.pendiente  { background: #5b7b93; opacity: 0.7; }
  [data-theme="dark"] .bar.en-curso   { background: #b89a60; opacity: 0.8; }
  [data-theme="dark"] .bar.completada { background: #4e8c4e; opacity: 0.75; }
  [data-theme="dark"] .milestone .tip { background: #374151; }
  [data-theme="dark"] #dark-toggle { background: #1f2937; border-color: #374151; color: #d1d5db; }
  [data-theme="dark"] #dark-toggle:hover { border-color: #6b7280; }
  [data-theme="dark"] .search-input { background: #1f2937; border-color: #374151; color: #d1d5db; }
  [data-theme="dark"] .search-input::placeholder { color: #6b7280; }
  [data-theme="dark"] .zoom-btn.active { background: #f3f4f6; color: #1f2937; border-color: #f3f4f6; }
  [data-theme="dark"] .tabs { border-color: #374151; }
  [data-theme="dark"] .tab { color: #6b7280; }
  [data-theme="dark"] .tab:hover { color: #e5e7eb; }
  [data-theme="dark"] .tab.active { color: #f3f4f6; }
</style>
</head>
<body>
<div class="wrap">
  <h1>__TITULO__ <span class="sub">__SUBTITULO__</span></h1>

  <div class="controls">
    <div class="status-filters">
      <span class="ctrl-label">Estado</span>
      <div id="status-pills" style="display:flex;flex-wrap:wrap;gap:8px;"></div>
    </div>
    <div class="search-wrap">
      <input id="task-search" type="text" class="search-input" placeholder="Buscar tarea…" oninput="onSearchInput()" />
    </div>
    <div class="zoom-controls" style="display:flex;gap:6px;align-items:center;">
      <span class="ctrl-label">Zoom</span>
      <span class="pill zoom-btn active" data-zoom="mensual" onclick="setZoom('mensual')">Mensual</span>
      <span class="pill zoom-btn" data-zoom="semanal" onclick="setZoom('semanal')">Semanal</span>
    </div>
    <label style="margin-left:auto;display:inline-flex;align-items:center;gap:8px;cursor:pointer;user-select:none;" title="Modo oscuro">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:15px;height:15px;color:#6b7280;flex-shrink:0;"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      <span id="dark-toggle" onclick="toggleDark()" style="position:relative;display:inline-block;width:36px;height:20px;flex-shrink:0;">
        <span id="dark-track" style="display:block;width:100%;height:100%;border-radius:999px;background:#e5e7eb;transition:background .2s;"></span>
        <span id="dark-thumb" style="position:absolute;top:3px;left:3px;width:14px;height:14px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.2);transition:transform .2s;"></span>
      </span>
    </label>
  </div>

  <div class="tabs" id="tabs"></div>

  <div class="legend" id="legend"></div>

  <div class="gantt" id="gantt">
    <div class="gantt-inner" id="gantt-inner"></div>
  </div>
</div>

<script>
const DATA = __DATA__;

function toggleDark() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
  document.getElementById('dark-track').style.background = isDark ? '#e5e7eb' : '#374151';
  document.getElementById('dark-thumb').style.transform = isDark ? '' : 'translateX(16px)';
}
const ICONS = {
  database: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/></svg>',
  chart:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>',
  message:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
  users:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
  flag:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>',
};
const iconFor = n => ICONS[n] || ICONS.flag;

const STATUS_ICONS = {
  'pendiente':  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
  'en curso':   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>',
  'completada': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
};
const STATUS_COLORS = {
  'pendiente':  '#6b7280',
  'en curso':   '#b45309',
  'completada': '#15803d',
};

const ZOOM_LEVELS = { mensual: 4.5, semanal: 13 };
let DAY_PX = ZOOM_LEVELS.mensual;
let currentZoom = 'mensual';
const LABEL_W = 240;
const DATE_W = 130;
const STICKY_W = LABEL_W + DATE_W;

const parseDate = s => { if (!s) return null; const [y,m,d] = s.split('-').map(Number); return new Date(y, m-1, d); };
const daysBetween = (a, b) => Math.round((b - a) / 86400000);
const MONTHS = ['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC'];
const monthShort = m => MONTHS[m];

const TODAY = new Date();
TODAY.setHours(0,0,0,0);
const TODAY_ISO = `${TODAY.getFullYear()}-${String(TODAY.getMonth()+1).padStart(2,'0')}-${String(TODAY.getDate()).padStart(2,'0')}`;
const START = new Date(TODAY.getFullYear(), TODAY.getMonth() - 12, 1);
const END   = new Date(TODAY.getFullYear(), TODAY.getMonth() + 13, 0);
const TOTAL_DAYS = daysBetween(START, END) + 1;
let TRACK_W = TOTAL_DAYS * DAY_PX;
const xFor = d => Math.round(daysBetween(START, parseDate(d)) * DAY_PX);

let searchQuery = '';

// Status order (fixed) and inferred set.
const STATUS_ORDER = ['Pendiente', 'En curso', 'Completada'];
function statusKey(s) { return (s || '').toLowerCase().trim(); }
function orderedStatuses() {
  const found = new Set(DATA.tareas.map(t => t.estado || '').filter(Boolean));
  const out = [];
  STATUS_ORDER.forEach(s => { if (found.has(s)) out.push(s); });
  found.forEach(s => { if (!STATUS_ORDER.includes(s)) out.push(s); });
  if (DATA.tareas.some(t => !t.estado)) out.push('__sin__');
  return out;
}

const activeStates = new Set(orderedStatuses());

let activeTab = 'todos';

const tipoByName = Object.fromEntries(DATA.tipos.map(t => [t.tipo, t]));

function render() {
  renderTabs();
  renderControls();
  renderLegend();
  renderGantt();
}

function renderTabs() {
  const container = document.getElementById('tabs');
  container.innerHTML = '';

  const todosTab = document.createElement('div');
  todosTab.className = 'tab' + (activeTab === 'todos' ? ' active' : '');
  todosTab.textContent = 'Todos';
  todosTab.style.borderBottomColor = activeTab === 'todos' ? '#1f2937' : 'transparent';
  todosTab.onclick = () => { activeTab = 'todos'; renderTabs(); renderGantt(); };
  container.appendChild(todosTab);

  DATA.areas.forEach(a => {
    const tab = document.createElement('div');
    tab.className = 'tab' + (activeTab === a.area ? ' active' : '');
    tab.innerHTML = `<span class="dot" style="background:${a.color}"></span>${a.area}`;
    tab.style.borderBottomColor = activeTab === a.area ? a.color : 'transparent';
    tab.onclick = () => { activeTab = a.area; renderTabs(); renderGantt(); };
    container.appendChild(tab);
  });
}

function renderControls() {
  const statusWrap = document.getElementById('status-pills');
  statusWrap.innerHTML = '';
  orderedStatuses().forEach(s => {
    const lbl = s === '__sin__' ? 'Sin estado' : s;
    const p = document.createElement('span');
    p.className = 'pill status-pill' + (activeStates.has(s) ? ' active' : '');
    p.dataset.s = statusKey(lbl);
    p.textContent = lbl;
    p.onclick = () => {
      activeStates.has(s) ? activeStates.delete(s) : activeStates.add(s);
      render();
    };
    statusWrap.appendChild(p);
  });
}

function onSearchInput() {
  searchQuery = document.getElementById('task-search').value.toLowerCase().trim();
  renderGantt();
}

function setZoom(level) {
  if (!ZOOM_LEVELS[level] || level === currentZoom) return;
  currentZoom = level;
  DAY_PX = ZOOM_LEVELS[level];
  TRACK_W = TOTAL_DAYS * DAY_PX;
  document.querySelectorAll('.zoom-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.zoom === level);
  });
  renderGantt._centered = false;
  renderGantt();
}

function renderLegend() {
  const leg = document.getElementById('legend');
  leg.innerHTML = '';
  DATA.tipos.forEach(t => {
    const el = document.createElement('div');
    el.className = 'legend-item';
    el.innerHTML = `<span class="legend-badge" style="background:${t.color}">${iconFor(t.icono)}</span><span>${t.tipo}</span>`;
    leg.appendChild(el);
  });
}

function fmtShort(iso) {
  const d = parseDate(iso);
  return `${String(d.getDate()).padStart(2,'0')} ${MONTHS[d.getMonth()].toLowerCase()}`;
}

function renderGantt() {
  const inner = document.getElementById('gantt-inner');
  inner.innerHTML = '';
  inner.style.minWidth = (STICKY_W + TRACK_W) + 'px';

  const isWeekly = currentZoom === 'semanal';
  const MONTH_ROW_H = 22;
  const WEEK_ROW_H  = 20;
  const DAY_ROW_H   = 22;
  const HEADER_H    = isWeekly ? (MONTH_ROW_H + WEEK_ROW_H + DAY_ROW_H) : 44;
  const DAY_LETTERS = ['D','L','M','M','J','V','S']; // Date.getDay(): 0=Dom

  // --- Timeline header ---
  const header = document.createElement('div');
  header.className = 'timeline-header';
  header.style.height = HEADER_H + 'px';

  const thSticky = document.createElement('div');
  thSticky.className = 'th-sticky';
  thSticky.textContent = 'Tarea · Fechas';
  header.appendChild(thSticky);

  const thTrack = document.createElement('div');
  thTrack.className = 'th-track';
  thTrack.style.width = TRACK_W + 'px';

  const cursor = new Date(START);
  while (cursor <= END) {
    const monthStart = new Date(cursor.getFullYear(), cursor.getMonth(), 1);
    const monthEnd   = new Date(cursor.getFullYear(), cursor.getMonth() + 1, 0);
    const left = daysBetween(START, monthStart) * DAY_PX;
    const w    = (daysBetween(monthStart, monthEnd) + 1) * DAY_PX;

    const divider = document.createElement('div');
    divider.className = 'month-divider' + (cursor.getMonth() === 0 ? ' year-divider' : '');
    divider.style.left = left + 'px';
    thTrack.appendChild(divider);

    const lbl = document.createElement('div');
    lbl.className = 'month-label';
    lbl.style.left = left + 'px';
    lbl.style.width = w + 'px';
    if (isWeekly) {
      lbl.style.top = '0';
      lbl.style.height = MONTH_ROW_H + 'px';
    }
    lbl.innerHTML = `${monthShort(cursor.getMonth())}${cursor.getMonth() === 0 ? ' <span class="year-badge">' + cursor.getFullYear() + '</span>' : ''}`;
    thTrack.appendChild(lbl);

    if (isWeekly) {
      // Semanas dentro del mes: W1 empieza el día 1; cada lunes incrementa el índice.
      let weekIdx = 1;
      let weekStart = new Date(monthStart);
      let d = new Date(monthStart);
      while (d <= monthEnd) {
        const nextDay = new Date(d);
        nextDay.setDate(d.getDate() + 1);
        const isLastInMonth = nextDay > monthEnd;
        const isSunday = d.getDay() === 0;
        if (isSunday || isLastInMonth) {
          const wLeft = daysBetween(START, weekStart) * DAY_PX;
          const wWidth = (daysBetween(weekStart, d) + 1) * DAY_PX;
          const wl = document.createElement('div');
          wl.className = 'week-label';
          wl.style.left = wLeft + 'px';
          wl.style.width = wWidth + 'px';
          wl.style.top = MONTH_ROW_H + 'px';
          wl.style.height = WEEK_ROW_H + 'px';
          wl.textContent = 'W' + weekIdx;
          thTrack.appendChild(wl);
          weekIdx += 1;
          weekStart = new Date(nextDay);
        }
        d = nextDay;
      }

      // Letras de día (todos los días del mes).
      let dd = new Date(monthStart);
      while (dd <= monthEnd) {
        const dLeft = daysBetween(START, dd) * DAY_PX;
        const dl = document.createElement('div');
        const dow = dd.getDay();
        dl.className = 'day-label' + ((dow === 0 || dow === 6) ? ' weekend' : '');
        dl.style.left = dLeft + 'px';
        dl.style.width = DAY_PX + 'px';
        dl.style.top = (MONTH_ROW_H + WEEK_ROW_H) + 'px';
        dl.style.height = DAY_ROW_H + 'px';
        dl.textContent = DAY_LETTERS[dow];
        thTrack.appendChild(dl);
        dd.setDate(dd.getDate() + 1);
      }
    }

    cursor.setMonth(cursor.getMonth() + 1);
  }

  // Today triangle (in header)
  const todayX = xFor(TODAY.toISOString().slice(0,10));
  const tri = document.createElement('div');
  tri.className = 'today-triangle';
  tri.style.left = todayX + 'px';
  tri.title = `Hoy · ${String(TODAY.getDate()).padStart(2,'0')}/${String(TODAY.getMonth()+1).padStart(2,'0')}/${TODAY.getFullYear()}`;
  thTrack.appendChild(tri);

  header.appendChild(thTrack);
  inner.appendChild(header);

  // --- Area sections ---
  DATA.areas.forEach(a => {
    if (activeTab !== 'todos' && activeTab !== a.area) return;
    const tasks = DATA.tareas.filter(t =>
      t.area === a.area &&
      activeStates.has(t.estado || '__sin__') &&
      (!searchQuery || (t.tarea || '').toLowerCase().includes(searchQuery))
    );
    if (!tasks.length) return;

    const section = document.createElement('div');
    section.className = 'area-section';

    const headWrap = document.createElement('div');
    headWrap.className = 'area-header-wrap';
    const head = document.createElement('div');
    head.className = 'area-header';
    head.innerHTML = `<span class="dot" style="background:${a.color}"></span><span class="name">${a.area}</span>`;
    headWrap.appendChild(head);
    section.appendChild(headWrap);

    tasks.forEach(t => {
      const row = document.createElement('div');
      const stateKey = statusKey(t.estado);
      row.className = 'row ' + stateKey.replace(/\s+/g, '-');

      // Label (name)
      const label = document.createElement('div');
      label.className = 'row-label';
      const isOverdue = t.fin && stateKey !== 'completada' && t.fin < TODAY_ISO;
      const overdueIcon = isOverdue ? '<span title="Tarea vencida" style="display:inline-flex;align-items:center;"><svg class="overdue-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg></span>' : '';
      label.innerHTML = `<span class="task-name">${t.tarea}</span>${overdueIcon}`;
      row.appendChild(label);

      // Date column
      const dateCol = document.createElement('div');
      dateCol.className = 'row-date';
      const sk = statusKey(t.estado);
      const statusIcon = STATUS_ICONS[sk] || '';
      const statusColor = STATUS_COLORS[sk] || '#9ca3af';
      if (t.inicio && t.fin) {
        dateCol.innerHTML = `<span style="flex:1">${fmtShort(t.inicio)}<span class="arrow">→</span>${fmtShort(t.fin)}</span><span class="status-icon" style="color:${statusColor}">${statusIcon}</span>`;
      }
      row.appendChild(dateCol);

      // Track
      const track = document.createElement('div');
      track.className = 'row-track';
      track.style.width = TRACK_W + 'px';

      if (t.inicio && t.fin) {
        const bar = document.createElement('div');
        bar.className = 'bar ' + stateKey.replace(/\s+/g, '-');
        bar.style.left = xFor(t.inicio) + 'px';
        bar.style.width = Math.max(4, (xFor(t.fin) - xFor(t.inicio))) + 'px';
        track.appendChild(bar);
      }

      DATA.hitos.filter(h => h.tarea === t.tarea).forEach(h => {
        if (!h.fecha) return;
        const tipo = tipoByName[h.tipo] || { color: '#555', icono: 'flag' };
        const m = document.createElement('div');
        m.className = 'milestone' + (h.link ? ' has-link' : '');
        m.style.left = xFor(h.fecha) + 'px';
        m.style.background = tipo.color;
        const d = parseDate(h.fecha);
        const tipDate = `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`;
        m.innerHTML = `${iconFor(tipo.icono)}<span class="tip">${h.tipo} · ${tipDate}${h.link ? ' ↗' : ''}</span>`;
        if (h.link) m.onclick = () => window.open(h.link, '_blank');
        track.appendChild(m);
      });

      row.appendChild(track);
      section.appendChild(row);
    });

    inner.appendChild(section);
  });

  // Center on today the first time (deferred so clientWidth is computed after layout)
  if (!renderGantt._centered) {
    renderGantt._centered = true;
    requestAnimationFrame(() => {
      const g = document.getElementById('gantt');
      g.scrollLeft = Math.max(0, todayX - Math.round((g.clientWidth - STICKY_W) / 2));
    });
  }

  // Today vertical line through body (rendered last so it sits on top)
  const todayLine = document.createElement('div');
  todayLine.style.cssText = `position:absolute;top:${HEADER_H}px;left:${STICKY_W + todayX}px;width:1px;height:calc(100% - ${HEADER_H}px);background:#dc2626;opacity:0.25;pointer-events:none;z-index:3;`;
  inner.appendChild(todayLine);
}

render();
</script>
</body>
</html>
"""


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

    html = (HTML_TEMPLATE
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

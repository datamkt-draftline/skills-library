#!/usr/bin/env python3
"""Build the ABI 2026 investment dashboard HTML from the source Excel.

Reads the "Inversion x Marca y Quarter ABInBev 2026.xlsx" workbook,
aggregates per country / brand / system / campaign, computes USD layer
from "FX LAS", and embeds the resulting JSON into the template HTML.

The resulting HTML is standalone (no fetch, no external JSON).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from pathlib import Path

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

MONTH_ORDER = [
    "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
    "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE",
]

GROUPS = ["TV", "RADIO", "OOH", "DIGITAL", "OTROS", "PRODUCCIÓN", "IMPUESTOS/FEE"]

# Canonical brand map. Keys are UPPER + accent-stripped forms of the raw value.
BRAND_CANONICAL = {
    "QUILMES": "Quilmes",
    "PATAGONIA": "Patagonia",
    "BRAHMA": "Brahma",
    "STELLA ARTOIS": "Stella Artois",
    "MICHELOB": "Michelob",
    "MICHELOB ULTRA": "Michelob",
    "BUDWEISER": "Budweiser",
    "BUD66": "Bud66",
    "CORONA": "Corona",
    "ANDES": "Andes",
    "ANDES ORIGEN": "Andes",
    "PATRICIA": "Patricia",
    "PILSEN": "Pilsen",
    "ZILLERTAL": "Zillertal",
    "PACENA": "Paceña",
    "HUARI": "Huari",
    "BECKER": "Becker",
    "GOLDEN": "Golden",
    "SKOL": "Skol",
}

# Preferred display order (brands not here fall at the end, alphabetical).
BRAND_ORDER = [
    "Quilmes", "Patagonia", "Brahma", "Stella Artois", "Michelob",
    "Budweiser", "Bud66", "Corona", "Andes", "Patricia", "Pilsen",
    "Zillertal", "Paceña", "Huari", "Becker", "Golden", "Skol",
]

BRAND_COLORS = {
    "Quilmes": "#f6c342",
    "Patagonia": "#2e7d32",
    "Brahma": "#1a73e8",
    "Stella Artois": "#b91c1c",
    "Michelob": "#8b5cf6",
    "Budweiser": "#ef4444",
    "Bud66": "#f97316",
    "Corona": "#f59e0b",
    "Andes": "#06b6d4",
    "Patricia": "#a855f7",
    "Pilsen": "#eab308",
    "Zillertal": "#14b8a6",
    "Paceña": "#f87171",
    "Huari": "#c026d3",
    "Becker": "#059669",
    "Golden": "#ca8a04",
    "Skol": "#dc2626",
}

FALLBACK_PALETTE = [
    "#3b82f6", "#ec4899", "#10b981", "#f97316", "#8b5cf6",
    "#06b6d4", "#f59e0b", "#ef4444", "#22c55e", "#a855f7",
]


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def canonical_brand(raw: str) -> str:
    if not raw:
        return "Sin marca"
    key = strip_accents(raw).strip().upper()
    if key in BRAND_CANONICAL:
        return BRAND_CANONICAL[key]
    # Title case fallback that preserves accents from the original string.
    cleaned = raw.strip()
    return cleaned if cleaned.isupper() is False else cleaned.title()


def canonical_month(raw: str) -> str | None:
    if not raw:
        return None
    key = strip_accents(raw).strip().upper()
    return key if key in MONTH_ORDER else None


def system_group(system: str) -> str:
    """Map a free-form system name to one of the dashboard groups."""
    if not system:
        return "OTROS"
    s = strip_accents(system).strip().upper()

    # Fee / taxes / debit impressions
    if "FEE" in s or "IMPUESTO" in s or s.startswith("IMP AL") or s == "IMP AL DEB":
        return "IMPUESTOS/FEE"
    if "PRODUCCION" in s or s == "PRODUCCIÓN":
        return "PRODUCCIÓN"

    # Digital platforms / adtech
    digital_tokens = (
        "META", "FACEBOOK", "TIKTOK", "TIK TOK", "TWITTER", "YOUTUBE",
        "GOOGLE", "SPOTIFY", "STREAMING", "PROGRAMATIC", "PROGRAMMATIC",
        "PROGRAMATICA", "PROGRAMATICA", "MERCADO LIBRE", "OOH DIGITAL",
        "TWITCH", "TAP TAP", "TAPTAP", "CABIFYADS", "LA JUNTA DIGITAL",
        "DAP MEDIA", "DLT SPORTS", "MEDIOS WEB", "AUDIENCIA",
        "ADSERVING", "OTHER MEDIA DIGITAL", "MEDIOS DIRECTOS",
    )
    for t in digital_tokens:
        if t in s:
            return "DIGITAL"

    # Radio BEFORE TV (RADIO contains an "A" not "TV")
    if s.startswith("RADIO") or " RADIO" in s or s in {"FM DOS PRODUCCION", "PLAY FM PRODUCCION",
                                                        "PLAYFM.CL", "40 PRINCIPALES.CL",
                                                        "CAROLINA.CL", "REVISTA ATREVETE"}:
        return "RADIO"

    # OOH
    ooh_tokens = ("OOH", "BILLBOARD", "VIA PUBLICA", "UBER")
    for t in ooh_tokens:
        if t in s:
            return "OOH"

    # TV
    tv_tokens = ("TV", "TVA", "TVC", "TVI", "CINE", "CLASE BASICA", "TVN")
    for t in tv_tokens:
        if t in s.split() or t in s:
            # Avoid matching 'TVA' inside RADIO etc. — already handled above.
            return "TV"

    # Print / magazine
    print_tokens = ("PRINT", "GRAFICA", "PRENSA", "REVISTA")
    for t in print_tokens:
        if t in s:
            return "OTROS"

    return "OTROS"


# ---------- xlsx reading -----------------------------------------------------

def read_xlsx(path: Path) -> dict:
    """Return a dict with sheet-name -> list of row-lists."""
    with zipfile.ZipFile(path) as z:
        # Shared strings
        strings: list[str] = []
        try:
            with z.open("xl/sharedStrings.xml") as f:
                root = ET.parse(f).getroot()
            for si in root.findall("m:si", NS):
                t = si.find("m:t", NS)
                if t is not None and t.text is not None:
                    strings.append(t.text)
                else:
                    parts = []
                    for r in si.findall("m:r", NS):
                        tt = r.find("m:t", NS)
                        if tt is not None and tt.text is not None:
                            parts.append(tt.text)
                    strings.append("".join(parts))
        except KeyError:
            pass

        # Workbook rels + sheets
        with z.open("xl/workbook.xml") as f:
            wb_root = ET.parse(f).getroot()
        with z.open("xl/_rels/workbook.xml.rels") as f:
            rels_root = ET.parse(f).getroot()
        rels = {}
        for rel in rels_root:
            rels[rel.get("Id")] = rel.get("Target")

        sheets = {}
        for sheet in wb_root.findall("m:sheets/m:sheet", NS):
            name = sheet.get("name")
            rid = sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = rels.get(rid, "")
            if not target.startswith("/"):
                target = "xl/" + target
            else:
                target = target[1:]
            sheets[name] = target

        def cell_value(c):
            t = c.get("t")
            v = c.find("m:v", NS)
            if v is None:
                is_ = c.find("m:is/m:t", NS)
                return is_.text if is_ is not None else None
            if t == "s":
                return strings[int(v.text)]
            if t == "e":  # error cell
                return None
            return v.text

        parsed = {}
        for name, target in sheets.items():
            try:
                with z.open(target) as f:
                    root = ET.parse(f).getroot()
            except KeyError:
                continue
            rows = []
            sd = root.find("m:sheetData", NS)
            if sd is None:
                parsed[name] = rows
                continue
            for row in sd.findall("m:row", NS):
                cells = {}
                for c in row.findall("m:c", NS):
                    ref = c.get("r") or ""
                    col_match = re.match(r"([A-Z]+)", ref)
                    if not col_match:
                        continue
                    col = col_match.group(1)
                    cells[col] = cell_value(c)
                rows.append(cells)
            parsed[name] = rows
    return parsed


def find_sheet(parsed: dict, needle: str) -> str | None:
    needle_u = strip_accents(needle).upper()
    for name in parsed:
        if strip_accents(name).upper().startswith(needle_u):
            return name
    for name in parsed:
        if needle_u in strip_accents(name).upper():
            return name
    return None


# ---------- aggregation -----------------------------------------------------

def to_float(v) -> float:
    if v is None or v == "":
        return 0.0
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def build_country_layer(records: list[dict], months_present: list[str], last_loaded: str,
                        value_key: str) -> dict:
    """records: list of {marca, campana, sistema, grupo, pais, mes, value}"""
    data_agg: dict[tuple, dict] = {}
    for r in records:
        key = (r["marca"], r["sistema"])
        row = data_agg.setdefault(key, {
            "marca": r["marca"],
            "sistema": r["sistema"],
            "grupo": r["grupo"],
            "anual": 0.0,
            **{m: 0.0 for m in MONTH_ORDER},
        })
        row[r["mes"]] += r[value_key]
        row["anual"] += r[value_key]

    camp_agg: dict[tuple, dict] = {}
    for r in records:
        key = (r["marca"], r["campana"], r["sistema"])
        row = camp_agg.setdefault(key, {
            "marca": r["marca"],
            "campaña": r["campana"],
            "sistema": r["sistema"],
            "grupo": r["grupo"],
            "inversion": 0.0,
        })
        row["inversion"] += r[value_key]

    data = sorted(data_agg.values(), key=lambda d: (d["marca"], d["sistema"]))
    campaign_system = sorted(camp_agg.values(), key=lambda d: (d["marca"], -d["inversion"]))

    plan: dict[str, float] = defaultdict(float)
    for row in data:
        plan[row["marca"]] += row["anual"]
    plan_total = sum(plan.values())

    all_brands = list(plan.keys())
    brands = [b for b in BRAND_ORDER if b in all_brands] + sorted(
        [b for b in all_brands if b not in BRAND_ORDER]
    )

    colors = {}
    for i, b in enumerate(brands):
        colors[b] = BRAND_COLORS.get(b, FALLBACK_PALETTE[i % len(FALLBACK_PALETTE)])

    return {
        "months": MONTH_ORDER,
        "lastLoadedMonth": last_loaded,
        "brands": brands,
        "colors": colors,
        "plan": {k: round(v, 2) for k, v in plan.items()},
        "planTotal": round(plan_total, 2),
        "data": data,
        "campaignSystem": campaign_system,
    }


def build_payload(xlsx_path: Path, last_loaded_month: str | None) -> dict:
    parsed = read_xlsx(xlsx_path)

    master_sheet = find_sheet(parsed, "Distribución x Sistema x Q x Ma") or \
                   find_sheet(parsed, "Distribucion x Sistema x Q x Ma")
    if not master_sheet:
        raise SystemExit("No encuentro la pestaña master 'Distribución x Sistema x Q x Ma'.")
    fx_sheet = find_sheet(parsed, "FX LAS")

    fx_rates: dict[str, float] = {}
    if fx_sheet:
        for r in parsed[fx_sheet][1:]:
            country = (r.get("A") or "").strip()
            rate = to_float(r.get("C"))
            if country and rate:
                fx_rates[country] = rate

    master_rows = parsed[master_sheet]
    header = master_rows[0]
    # Columns from exploration:
    # A Sistema | B Q | C Mes | D Inversion | E Marca | F Campaña | G Pais | H Año | I USD

    per_country: dict[str, list[dict]] = defaultdict(list)
    months_present: dict[str, set] = defaultdict(set)

    for row in master_rows[1:]:
        sistema_raw = (row.get("A") or "").strip()
        if not sistema_raw:
            continue
        mes = canonical_month(row.get("C"))
        if not mes:
            continue
        marca = canonical_brand(row.get("E"))
        campana = (row.get("F") or "Sin campaña").strip() or "Sin campaña"
        pais = (row.get("G") or "").strip()
        if not pais:
            continue
        valor = to_float(row.get("D"))
        usd = to_float(row.get("I"))
        if usd == 0 and valor != 0 and fx_rates.get(pais):
            usd = valor / fx_rates[pais]
        grupo = system_group(sistema_raw)

        rec = {
            "marca": marca,
            "campana": campana,
            "sistema": sistema_raw,
            "grupo": grupo,
            "pais": pais,
            "mes": mes,
            "local": valor,
            "usd": usd,
        }
        per_country[pais].append(rec)
        months_present[pais].add(mes)

    # Determine lastLoadedMonth
    if not last_loaded_month:
        # Scan sheet names for "Consumido x Sistema <MES>"
        last_loaded_month = "JUNIO"
        for sheet_name in parsed:
            m = re.search(r"CONSUMIDO\s+X\s+SISTEMA\s+([A-Za-zÁÉÍÓÚÑáéíóúñ]+)",
                          strip_accents(sheet_name).upper())
            if m:
                mes = canonical_month(m.group(1))
                if mes and MONTH_ORDER.index(mes) >= MONTH_ORDER.index(last_loaded_month):
                    last_loaded_month = mes

    countries_payload: dict[str, dict] = {}
    for country, recs in per_country.items():
        local = build_country_layer(recs, sorted(months_present[country]),
                                    last_loaded_month, "local")
        usd = build_country_layer(recs, sorted(months_present[country]),
                                  last_loaded_month, "usd")
        local["usd"] = usd
        countries_payload[country] = local

    # Ensure the 5 countries show up even if empty, so the HTML selector works
    for required in ("Argentina", "Bolivia", "Chile", "Paraguay", "Uruguay"):
        if required not in countries_payload:
            countries_payload[required] = {
                "months": MONTH_ORDER,
                "lastLoadedMonth": last_loaded_month,
                "brands": [],
                "colors": {},
                "plan": {},
                "planTotal": 0,
                "data": [],
                "campaignSystem": [],
                "usd": {
                    "months": MONTH_ORDER,
                    "lastLoadedMonth": last_loaded_month,
                    "brands": [],
                    "colors": {},
                    "plan": {},
                    "planTotal": 0,
                    "data": [],
                    "campaignSystem": [],
                },
            }

    default_country = "Argentina" if "Argentina" in countries_payload else next(iter(countries_payload))

    return {
        "defaultCountry": default_country,
        "defaultCurrency": "LOCAL",
        "countries": countries_payload,
    }


# ---------- HTML assembly ---------------------------------------------------

def embed(payload: dict, template_html: str) -> str:
    json_str = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    marker = "/*__DATA__*/null"
    if marker not in template_html:
        raise SystemExit("El template no contiene el marcador /*__DATA__*/null.")
    # Protect against accidental '</script>' inside the JSON (none expected,
    # but be defensive).
    safe = json_str.replace("</script>", "<\\/script>")
    return template_html.replace(marker, safe, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="Ruta al .xlsx fuente")
    ap.add_argument("--output", required=True, help="Ruta del .html a generar")
    default_tpl = Path(__file__).resolve().parent.parent / "template.html"
    ap.add_argument("--template", default=str(default_tpl),
                    help="Ruta al template HTML (default: template.html del skill)")
    ap.add_argument("--last-loaded",
                    help="Nombre del último mes 'consumido' (ENERO..DICIEMBRE). Si se omite se infiere.")
    args = ap.parse_args()

    xlsx = Path(args.input)
    out = Path(args.output)
    tpl = Path(args.template)
    if not xlsx.exists():
        print(f"[error] no existe {xlsx}", file=sys.stderr)
        return 1
    if not tpl.exists():
        print(f"[error] no existe el template {tpl}", file=sys.stderr)
        return 1

    last_loaded = args.last_loaded.upper() if args.last_loaded else None
    if last_loaded and last_loaded not in MONTH_ORDER:
        print(f"[error] mes inválido: {last_loaded}", file=sys.stderr)
        return 1

    print(f"[info] Leyendo {xlsx.name}...")
    payload = build_payload(xlsx, last_loaded)

    totals_by_country = {c: round(payload["countries"][c]["planTotal"], 2)
                         for c in payload["countries"]}
    print(f"[info] Totales por país (moneda local): {totals_by_country}")

    print(f"[info] Leyendo template {tpl}...")
    template_html = tpl.read_text(encoding="utf-8")

    out_html = embed(payload, template_html)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(out_html, encoding="utf-8")
    size_kb = out.stat().st_size / 1024
    print(f"[ok] Escrito {out} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

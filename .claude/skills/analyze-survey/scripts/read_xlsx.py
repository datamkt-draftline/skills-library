"""Lector de xlsx con stdlib únicamente.

Uso rápido:
    from read_xlsx import read_xlsx
    sheets = read_xlsx("archivo.xlsx")
    # sheets == {"NombreHoja": [{"col1": "val", "col2": "val"}, ...]}

Devuelve, por hoja, una lista de dicts (la primera fila se usa como header).
Los headers vacíos o repetidos se completan con "col_<N>".
Los valores numéricos se devuelven como float, las fechas como datetime.
"""
from __future__ import annotations
import zipfile
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timedelta

_NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# Formatos numéricos "built-in" que representan fechas/horas en xlsx.
# Referencia: ECMA-376. Cualquier custom con "d", "y" o "m" seguido de contexto de fecha
# también se trata como fecha (heurística).
_BUILTIN_DATE_FMTS = {14, 15, 16, 17, 18, 19, 20, 21, 22, 30, 45, 46, 47}


def _col_letter_to_idx(letters: str) -> int:
    n = 0
    for c in letters:
        n = n * 26 + (ord(c) - 64)
    return n - 1


def _cell_ref_to_col(ref: str) -> int:
    m = re.match(r"([A-Z]+)", ref)
    return _col_letter_to_idx(m.group(1))


def _excel_serial_to_datetime(serial: float) -> datetime:
    # Excel considera 1900 como bisiesto (bug); ajuste para serials >= 60.
    epoch = datetime(1899, 12, 30)
    return epoch + timedelta(days=float(serial))


def _load_shared_strings(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("s:si", _NS):
        text = "".join(t.text or "" for t in si.iter(_MAIN + "t"))
        out.append(text)
    return out


def _load_styles(z: zipfile.ZipFile) -> list[int]:
    """Devuelve una lista donde el índice es el style_id y el valor es el numFmtId."""
    if "xl/styles.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/styles.xml"))
    xfs = root.find("s:cellXfs", _NS)
    if xfs is None:
        return []
    return [int(x.get("numFmtId", "0")) for x in xfs.findall("s:xf", _NS)]


def _load_custom_num_fmts(z: zipfile.ZipFile) -> dict[int, str]:
    if "xl/styles.xml" not in z.namelist():
        return {}
    root = ET.fromstring(z.read("xl/styles.xml"))
    nfmts = root.find("s:numFmts", _NS)
    if nfmts is None:
        return {}
    return {int(nf.get("numFmtId")): nf.get("formatCode", "") for nf in nfmts.findall("s:numFmt", _NS)}


def _is_date_fmt(num_fmt_id: int, custom_fmts: dict[int, str]) -> bool:
    if num_fmt_id in _BUILTIN_DATE_FMTS:
        return True
    fmt = custom_fmts.get(num_fmt_id, "")
    if not fmt:
        return False
    # Heurística: contiene y/m/d/h fuera de comillas.
    stripped = re.sub(r'".*?"', "", fmt).lower()
    return bool(re.search(r"[ymdh]", stripped))


def _parse_cell_value(cell: ET.Element, strings: list[str], styles: list[int], custom_fmts: dict[int, str]):
    ctype = cell.get("t")
    style_id = cell.get("s")
    v = cell.find("s:v", _NS)
    is_ = cell.find("s:is", _NS)

    if ctype == "s" and v is not None:
        try:
            return strings[int(v.text)]
        except (ValueError, IndexError):
            return v.text
    if ctype == "inlineStr" and is_ is not None:
        return "".join(t.text or "" for t in is_.iter(_MAIN + "t"))
    if ctype == "b" and v is not None:
        return v.text == "1"
    if ctype in ("str", "e") and v is not None:
        return v.text
    if v is None:
        return None

    # Numérico (ctype == "n" o None).
    text = v.text
    try:
        num = float(text)
    except (TypeError, ValueError):
        return text

    if style_id is not None:
        try:
            num_fmt_id = styles[int(style_id)]
            if _is_date_fmt(num_fmt_id, custom_fmts):
                return _excel_serial_to_datetime(num)
        except (IndexError, ValueError):
            pass

    if num.is_integer():
        return int(num)
    return num


def _sheet_relations(z: zipfile.ZipFile) -> dict[str, str]:
    rels_path = "xl/_rels/workbook.xml.rels"
    if rels_path not in z.namelist():
        return {}
    root = ET.fromstring(z.read(rels_path))
    ns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
    return {rel.get("Id"): rel.get("Target") for rel in root.findall("r:Relationship", ns)}


def _sheet_targets(z: zipfile.ZipFile) -> list[tuple[str, str]]:
    """Devuelve [(sheet_name, xml_path), ...] en el orden del workbook."""
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = _sheet_relations(z)
    out = []
    for s in wb.findall("s:sheets/s:sheet", _NS):
        name = s.get("name")
        rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rels.get(rid, "")
        # Los targets vienen relativos a xl/, normalizar.
        path = "xl/" + target if not target.startswith("/") else target.lstrip("/")
        if path not in z.namelist():
            path = "xl/" + target.lstrip("/").split("xl/", 1)[-1]
        out.append((name, path))
    return out


def _dedupe_headers(headers: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for i, h in enumerate(headers):
        h = (h or "").strip()
        if not h:
            h = f"col_{i}"
        if h in seen:
            seen[h] += 1
            h = f"{h}__{seen[h]}"
        else:
            seen[h] = 0
        out.append(h)
    return out


def read_xlsx(path: str) -> dict[str, list[dict]]:
    """Lee un xlsx y devuelve {sheet_name: [row_dict, ...]}.

    La primera fila de cada hoja se usa como encabezado.
    """
    with zipfile.ZipFile(path) as z:
        strings = _load_shared_strings(z)
        styles = _load_styles(z)
        custom_fmts = _load_custom_num_fmts(z)
        result: dict[str, list[dict]] = {}
        for sheet_name, sheet_path in _sheet_targets(z):
            root = ET.fromstring(z.read(sheet_path))
            grid: list[list] = []
            max_col = 0
            for row in root.findall("s:sheetData/s:row", _NS):
                cells: dict[int, object] = {}
                for c in row.findall("s:c", _NS):
                    ref = c.get("r")
                    if not ref:
                        continue
                    ci = _cell_ref_to_col(ref)
                    val = _parse_cell_value(c, strings, styles, custom_fmts)
                    cells[ci] = val
                    if ci > max_col:
                        max_col = ci
                if cells:
                    grid.append(cells)
            if not grid:
                result[sheet_name] = []
                continue
            width = max_col + 1
            header_raw = [str(grid[0].get(i, "") or "") for i in range(width)]
            headers = _dedupe_headers(header_raw)
            rows_out = []
            for row in grid[1:]:
                if not any(row.get(i) not in (None, "") for i in range(width)):
                    continue
                rows_out.append({headers[i]: row.get(i) for i in range(width)})
            result[sheet_name] = rows_out
        return result


def rows_of(sheets: dict[str, list[dict]], sheet_name: str | None = None) -> list[dict]:
    """Atajo: devuelve las filas de la primera hoja (o la nombrada)."""
    if sheet_name is None:
        return next(iter(sheets.values()), [])
    return sheets[sheet_name]


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("uso: python read_xlsx.py <archivo.xlsx>")
        raise SystemExit(1)
    data = read_xlsx(sys.argv[1])
    for name, rows in data.items():
        print(f"=== {name} ({len(rows)} filas) ===")
        if rows:
            print("columnas:", list(rows[0].keys()))
            print("primeras filas:")
            for r in rows[:3]:
                print(" ", {k: (str(v)[:50] if v is not None else None) for k, v in r.items()})

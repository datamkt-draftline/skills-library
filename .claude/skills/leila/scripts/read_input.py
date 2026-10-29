"""Lector de archivos de comentarios de redes sociales (xlsx y csv) con stdlib.

Expone dos funciones:
    - read_file(path): devuelve {sheet_name: [row_dict, ...]} para xlsx,
      o {"Sheet1": [row_dict, ...]} para csv.
    - detect_comments(sheets): heurística que inspecciona las hojas y devuelve
      {"comments": [str], "dates": [datetime|None], "comment_col": str,
       "date_col": str|None, "sheet": str}

Diseñado para funcionar sin pandas ni openpyxl.
"""
from __future__ import annotations
import zipfile
import xml.etree.ElementTree as ET
import re
import csv
import io
import os
from datetime import datetime, timedelta
from typing import Optional

_NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_BUILTIN_DATE_FMTS = {14, 15, 16, 17, 18, 19, 20, 21, 22, 30, 45, 46, 47}


# ---------- XLSX ----------

def _col_letter_to_idx(letters: str) -> int:
    n = 0
    for c in letters:
        n = n * 26 + (ord(c) - 64)
    return n - 1


def _cell_ref_to_col(ref: str) -> int:
    m = re.match(r"([A-Z]+)", ref)
    return _col_letter_to_idx(m.group(1))


def _excel_serial_to_datetime(serial: float) -> datetime:
    epoch = datetime(1899, 12, 30)
    return epoch + timedelta(days=float(serial))


def _load_shared_strings(z: zipfile.ZipFile) -> list:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("s:si", _NS):
        text = "".join(t.text or "" for t in si.iter(_MAIN + "t"))
        out.append(text)
    return out


def _load_styles(z: zipfile.ZipFile) -> list:
    if "xl/styles.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/styles.xml"))
    xfs = root.find("s:cellXfs", _NS)
    if xfs is None:
        return []
    return [int(x.get("numFmtId", "0")) for x in xfs.findall("s:xf", _NS)]


def _load_custom_num_fmts(z: zipfile.ZipFile) -> dict:
    if "xl/styles.xml" not in z.namelist():
        return {}
    root = ET.fromstring(z.read("xl/styles.xml"))
    nfmts = root.find("s:numFmts", _NS)
    if nfmts is None:
        return {}
    return {int(nf.get("numFmtId")): nf.get("formatCode", "") for nf in nfmts.findall("s:numFmt", _NS)}


def _is_date_fmt(num_fmt_id: int, custom_fmts: dict) -> bool:
    if num_fmt_id in _BUILTIN_DATE_FMTS:
        return True
    fmt = custom_fmts.get(num_fmt_id, "")
    if not fmt:
        return False
    stripped = re.sub(r'".*?"', "", fmt).lower()
    return bool(re.search(r"[ymdh]", stripped))


def _parse_cell_value(cell, strings, styles, custom_fmts):
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


def _sheet_relations(z: zipfile.ZipFile) -> dict:
    rels_path = "xl/_rels/workbook.xml.rels"
    if rels_path not in z.namelist():
        return {}
    root = ET.fromstring(z.read(rels_path))
    ns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
    return {rel.get("Id"): rel.get("Target") for rel in root.findall("r:Relationship", ns)}


def _sheet_targets(z: zipfile.ZipFile) -> list:
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = _sheet_relations(z)
    out = []
    for s in wb.findall("s:sheets/s:sheet", _NS):
        name = s.get("name")
        rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rels.get(rid, "")
        path = "xl/" + target if not target.startswith("/") else target.lstrip("/")
        if path not in z.namelist():
            path = "xl/" + target.lstrip("/").split("xl/", 1)[-1]
        out.append((name, path))
    return out


def _dedupe_headers(headers: list) -> list:
    seen = {}
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


def read_xlsx(path: str) -> dict:
    with zipfile.ZipFile(path) as z:
        strings = _load_shared_strings(z)
        styles = _load_styles(z)
        custom_fmts = _load_custom_num_fmts(z)
        result = {}
        for sheet_name, sheet_path in _sheet_targets(z):
            root = ET.fromstring(z.read(sheet_path))
            grid = []
            max_col = 0
            for row in root.findall("s:sheetData/s:row", _NS):
                cells = {}
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


# ---------- CSV ----------

def read_csv_file(path: str) -> dict:
    with open(path, "rb") as f:
        raw = f.read()
    # Try utf-8-sig first (handles BOM), then latin-1 fallback.
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    # Sniff delimiter.
    sniff = text[:4096]
    delim = ","
    for cand in [",", ";", "\t", "|"]:
        if sniff.count(cand) > sniff.count(delim):
            delim = cand
    reader = csv.reader(io.StringIO(text), delimiter=delim)
    rows = list(reader)
    if not rows:
        return {"Sheet1": []}
    headers = _dedupe_headers([(h or "").strip() for h in rows[0]])
    out = []
    for row in rows[1:]:
        if not any((c or "").strip() for c in row):
            continue
        out.append({headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))})
    return {"Sheet1": out}


# ---------- Entry point ----------

def _read_text_file(path: str) -> str:
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _looks_like_csv(text: str) -> bool:
    sample = text[:4096]
    lines = [l for l in sample.split("\n") if l.strip()][:10]
    if len(lines) < 2:
        return False
    for cand in [",", ";", "\t", "|"]:
        counts = [l.count(cand) for l in lines]
        if counts[0] >= 1 and all(c == counts[0] for c in counts):
            return True
    return False


def read_file(path: str) -> dict:
    """Lee xlsx, csv, tsv o txt. Para xlsx/csv devuelve {sheet: [rows]}.
    Para txt (texto crudo de redes sociales) devuelve {"__text__": raw_string}.
    """
    low = path.lower()
    if low.endswith(".xlsx") or low.endswith(".xlsm"):
        return read_xlsx(path)
    if low.endswith(".csv") or low.endswith(".tsv"):
        return read_csv_file(path)
    if low.endswith(".txt"):
        text = _read_text_file(path)
        if _looks_like_csv(text):
            return read_csv_file(path)
        return {"__text__": text}
    # Try xlsx by signature; fall back to text/csv.
    try:
        with open(path, "rb") as f:
            sig = f.read(4)
        if sig[:2] == b"PK":
            return read_xlsx(path)
    except Exception:
        pass
    text = _read_text_file(path)
    if _looks_like_csv(text):
        return read_csv_file(path)
    return {"__text__": text}


# ---------- Detection heuristics ----------

_COMMENT_NAME_HINTS = [
    "comment", "comentario", "coment", "mensaje", "message", "texto",
    "text", "caption", "content", "body", "post", "description", "descripcion",
    "respuesta", "reply", "reseña", "resena", "review", "opinion", "opinión",
    "snippet",
]
_DATE_NAME_HINTS = [
    "date", "fecha", "timestamp", "created", "created_at", "createdat",
    "published", "published_at", "publicado", "time", "hora", "datetime",
    "publish_date", "post_date",
]
_AUTHOR_NAME_HINTS = [
    "author", "autor", "user", "usuario", "username", "name", "handle",
    "screen_name", "profile",
]


def _norm(s) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(s or "").lower())


def _is_date_like(val) -> bool:
    if isinstance(val, datetime):
        return True
    if isinstance(val, str):
        s = val.strip()
        if not s:
            return False
        patterns = [
            r"^\d{4}-\d{1,2}-\d{1,2}",
            r"^\d{1,2}/\d{1,2}/\d{2,4}",
            r"^\d{1,2}-\d{1,2}-\d{2,4}",
        ]
        return any(re.match(p, s) for p in patterns)
    return False


def _parse_date(val):
    if val is None or val == "":
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, (int, float)):
        # Treat as excel serial if plausible.
        if 20000 < val < 80000:
            try:
                return _excel_serial_to_datetime(float(val))
            except Exception:
                return None
    s = str(val).strip()
    for fmt in (
        "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M", "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y",
        "%m/%d/%Y %H:%M:%S", "%m/%d/%Y",
        "%d-%m-%Y", "%d-%b-%Y", "%b %d, %Y",
    ):
        try:
            return datetime.strptime(s[:len(fmt) + 4], fmt[: len(fmt)])
        except Exception:
            pass
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def _score_comment_col(name: str, values: list) -> float:
    nname = _norm(name)
    name_score = 0.0
    for hint in _COMMENT_NAME_HINTS:
        if hint in nname:
            name_score = 1.0
            break
    non_empty = [str(v) for v in values if v not in (None, "")]
    if not non_empty:
        return -1.0
    avg_len = sum(len(v) for v in non_empty) / len(non_empty)
    # Prefer longer text; penalize if looks like a date column.
    date_like_frac = sum(1 for v in non_empty if _is_date_like(v)) / len(non_empty)
    if date_like_frac > 0.5:
        return -1.0
    uniqueness = len(set(non_empty)) / len(non_empty)
    return name_score * 10 + avg_len * 0.1 + uniqueness


def _score_date_col(name: str, values: list) -> float:
    nname = _norm(name)
    hinted = any(h in nname for h in _DATE_NAME_HINTS)
    sample = [v for v in values if v not in (None, "")][:200]
    if not sample:
        return -1.0
    date_frac = sum(1 for v in sample if _parse_date(v)) / len(sample)
    return (10 if hinted else 0) + date_frac * 100


def detect_comments(sheets: dict) -> dict:
    """Choose the sheet + column that most likely contains the comments.

    Returns a dict with keys: comments (list[str]), dates (list[datetime|None]),
    authors (list[str|None]), comment_col, date_col, author_col, sheet.
    """
    # If this is a raw-text payload (from a .txt), delegate to the text parser.
    if "__text__" in sheets:
        return parse_social_text(sheets["__text__"])
    best = None
    for sheet_name, rows in sheets.items():
        if not rows:
            continue
        cols = list(rows[0].keys())
        if not cols:
            continue
        for col in cols:
            vals = [r.get(col) for r in rows]
            score = _score_comment_col(col, vals)
            if score < 0:
                continue
            if best is None or score > best[0]:
                best = (score, sheet_name, col)
    if best is None:
        raise ValueError("No se pudo detectar una columna de comentarios en el archivo.")
    _, sheet_name, comment_col = best

    rows = sheets[sheet_name]
    cols = list(rows[0].keys())

    # Pick date column.
    date_col = None
    best_date = -1.0
    for col in cols:
        if col == comment_col:
            continue
        vals = [r.get(col) for r in rows]
        s = _score_date_col(col, vals)
        if s > best_date:
            best_date = s
            date_col = col
    if best_date < 20:
        date_col = None

    # Pick author column.
    author_col = None
    for col in cols:
        if col == comment_col:
            continue
        if any(h in _norm(col) for h in _AUTHOR_NAME_HINTS):
            author_col = col
            break

    comments, dates, authors = [], [], []
    for r in rows:
        c = r.get(comment_col)
        if c is None or (isinstance(c, str) and not c.strip()):
            continue
        comments.append(str(c).strip())
        dates.append(_parse_date(r.get(date_col)) if date_col else None)
        authors.append(str(r.get(author_col)).strip() if author_col and r.get(author_col) else None)

    return {
        "comments": comments,
        "dates": dates,
        "authors": authors,
        "comment_col": comment_col,
        "date_col": date_col,
        "author_col": author_col,
        "sheet": sheet_name,
    }


# ---------- Social-media raw text parser ----------

_TIME_UNITS = {
    "s": "s", "seg": "s", "segundo": "s", "segundos": "s", "sec": "s",
    "min": "min", "minuto": "min", "minutos": "min", "m": "min",
    "h": "h", "hora": "h", "horas": "h", "hr": "h", "hrs": "h",
    "d": "d", "día": "d", "dia": "d", "días": "d", "dias": "d", "day": "d", "days": "d",
    "sem": "w", "semana": "w", "semanas": "w", "w": "w", "week": "w", "weeks": "w",
    "mes": "mo", "meses": "mo", "mo": "mo", "month": "mo", "months": "mo",
    "año": "y", "años": "y", "ano": "y", "anos": "y", "y": "y", "yr": "y", "year": "y", "years": "y",
}

# Spanish "Hace 6 d" / "Hace 2 h" / "Hace 1 min" / "Hace 10 h" ...
_HACE_RE = re.compile(
    r"^\s*hace\s+(\d+)\s*([a-záéíóúñ]+)\.?\s*$",
    re.IGNORECASE,
)
# English "6d ago", "2 hours ago", ...
_AGO_RE = re.compile(
    r"^\s*(\d+)\s*([a-z]+)\s+ago\s*$",
    re.IGNORECASE,
)
# Short IG/Twitter "6d", "2h", "1min" alone (very loose, must be short line)
_SHORT_TIME_RE = re.compile(
    r"^\s*(\d+)\s*(s|m|h|d|w|mo|y|min|hr)\s*$",
    re.IGNORECASE,
)

# Noise lines that appear in TikTok / IG dumps.
_NOISE_PATTERNS = [
    re.compile(r"^responder$", re.IGNORECASE),
    re.compile(r"^reply$", re.IGNORECASE),
    re.compile(r"^ver\s+\d+\s+respuestas?$", re.IGNORECASE),
    re.compile(r"^ver\s+1\s+respuesta$", re.IGNORECASE),
    re.compile(r"^view\s+\d+\s+repl(y|ies)$", re.IGNORECASE),
    re.compile(r"^(foto|photo|sticker|new|me gusta|like|likes)$", re.IGNORECASE),
    re.compile(r"^\d+(\.\d+)?\s*[kKmM]?$"),  # like count
    re.compile(r"^·+$"),
]


def _parse_relative(num: int, unit_raw: str, ref: Optional[datetime] = None) -> Optional[datetime]:
    unit = _TIME_UNITS.get(unit_raw.lower().rstrip("."))
    if not unit:
        return None
    if ref is None:
        ref = datetime.now()
    try:
        n = int(num)
    except Exception:
        return None
    if unit == "s":
        return ref - timedelta(seconds=n)
    if unit == "min":
        return ref - timedelta(minutes=n)
    if unit == "h":
        return ref - timedelta(hours=n)
    if unit == "d":
        return ref - timedelta(days=n)
    if unit == "w":
        return ref - timedelta(weeks=n)
    if unit == "mo":
        return ref - timedelta(days=30 * n)
    if unit == "y":
        return ref - timedelta(days=365 * n)
    return None


def _is_anchor(line: str) -> Optional[tuple]:
    """Devuelve (num, unit_raw) si la línea es un ancla de tiempo, o None."""
    s = line.strip()
    if not s or len(s) > 40:
        return None
    m = _HACE_RE.match(s)
    if m:
        return int(m.group(1)), m.group(2)
    m = _AGO_RE.match(s)
    if m:
        return int(m.group(1)), m.group(2)
    m = _SHORT_TIME_RE.match(s)
    if m:
        # Short time alone — only accept if it fits a known unit pattern.
        return int(m.group(1)), m.group(2)
    return None


def _is_noise_line(s: str) -> bool:
    s = s.strip()
    if not s:
        return True
    for pat in _NOISE_PATTERNS:
        if pat.match(s):
            return True
    return False


def parse_social_text(text: str, now: Optional[datetime] = None) -> dict:
    """Extrae comentarios desde un volcado de texto de TikTok/IG/etc.

    Estrategia: cada bloque de líneas termina en un 'ancla' temporal
    ("Hace X d", "2 hours ago", "6d"). Antes del ancla, el bloque puede tener:
      - una línea de autor (opcional) + línea en blanco + texto del comentario,
      - o solo el texto del comentario.
    Las líneas de ruido ("Responder", counts de likes, "Ver X respuestas",
    "Foto", "sticker") se filtran.

    Devuelve el mismo shape que detect_comments():
      {comments: [str], dates: [datetime|None], authors: [str|None],
       comment_col, date_col, author_col, sheet}
    """
    if now is None:
        now = datetime.now()
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    # Indexes of anchors.
    anchor_info = []
    for i, l in enumerate(lines):
        a = _is_anchor(l)
        if a:
            anchor_info.append((i, a[0], a[1]))

    comments, dates, authors = [], [], []
    prev_end = -1
    for idx, num, unit in anchor_info:
        raw_entry = lines[prev_end + 1:idx]
        # Strip edge blanks.
        while raw_entry and not raw_entry[0].strip():
            raw_entry.pop(0)
        while raw_entry and not raw_entry[-1].strip():
            raw_entry.pop()

        if raw_entry:
            author = None
            entry = []
            blank_idx = next((i for i, l in enumerate(raw_entry) if not l.strip()), None)

            if blank_idx is not None and blank_idx > 0:
                author_part = raw_entry[:blank_idx]
                body_part = raw_entry[blank_idx + 1:]
                body_clean = [l.rstrip() for l in body_part if l.strip() and not _is_noise_line(l)]
                has_author_shape = (
                    len(author_part) == 1
                    and 0 < len(author_part[0].strip()) <= 60
                )
                if has_author_shape and body_clean:
                    author = author_part[0].strip()
                    entry = body_clean
                elif has_author_shape and not body_clean:
                    # Author-shaped line + body is only noise (Foto/sticker) → photo-only post, skip.
                    entry = []
                else:
                    entry = [l.rstrip() for l in raw_entry if l.strip() and not _is_noise_line(l)]
            else:
                entry = [l.rstrip() for l in raw_entry if l.strip() and not _is_noise_line(l)]

            text_body = "\n".join(entry).strip()

            if text_body and text_body.lower() not in ("foto", "sticker", "photo", "new"):
                comments.append(text_body)
                dates.append(_parse_relative(num, unit, now))
                authors.append(author)

        # Skip trailing noise after the anchor to find real start of next entry.
        j = idx + 1
        while j < len(lines) and _is_noise_line(lines[j]):
            j += 1
        prev_end = j - 1

    return {
        "comments": comments,
        "dates": dates,
        "authors": authors,
        "comment_col": "text",
        "date_col": "time_rel",
        "author_col": "author",
        "sheet": "__text__",
    }


# ---------- Unified loader ----------

def load_comments(source) -> dict:
    """Función unificada: aceptá una ruta (xlsx/csv/txt) o un string de texto crudo.
    Devuelve siempre el shape de detect_comments().
    """
    if isinstance(source, str) and ("\n" in source or len(source) > 500) and not os.path.exists(source):
        # Treat as raw text.
        return parse_social_text(source)
    if isinstance(source, str) and os.path.exists(source):
        sheets = read_file(source)
        return detect_comments(sheets)
    raise ValueError("source debe ser una ruta de archivo o un string de texto crudo.")


# ---------- Volume aggregation ----------

def volume_buckets(dates: list) -> dict:
    """Agrupa las fechas en buckets apropiados (día / semana / mes) según rango.
    Devuelve {"granularity": str, "labels": [str], "counts": [int]}.
    Si no hay fechas, devuelve granularity "none".
    """
    valid = [d for d in dates if d is not None]
    if not valid:
        return {"granularity": "none", "labels": [], "counts": []}
    valid.sort()
    span = (valid[-1] - valid[0]).days
    if span <= 2:
        gran = "hour"
    elif span <= 60:
        gran = "day"
    elif span <= 365:
        gran = "week"
    else:
        gran = "month"

    def key(d):
        if gran == "hour":
            return d.strftime("%Y-%m-%d %H:00")
        if gran == "day":
            return d.strftime("%Y-%m-%d")
        if gran == "week":
            iso = d.isocalendar()
            return f"{iso[0]}-W{iso[1]:02d}"
        return d.strftime("%Y-%m")

    counts = {}
    for d in valid:
        k = key(d)
        counts[k] = counts.get(k, 0) + 1
    labels = sorted(counts.keys())
    return {
        "granularity": gran,
        "labels": labels,
        "counts": [counts[k] for k in labels],
    }


# ---------- Emoji / content detection ----------

_EMOJI_PATTERN = re.compile(
    "["                       # emoji unicode ranges
    "\U0001F300-\U0001FAFF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U00002600-\U000027BF"
    "\U0001F900-\U0001F9FF"
    "\U00002700-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "‍️♀♂⚕⚖✈❤"
    "]"
)


def is_emoji_only(text: str) -> bool:
    stripped = _EMOJI_PATTERN.sub("", text or "").strip()
    stripped = re.sub(r"[\s\.\!\?……]+", "", stripped)
    return len(stripped) == 0 and (text or "").strip() != ""


def emoji_level(comments: list) -> str:
    if not comments:
        return "ninguno"
    frac = sum(1 for c in comments if is_emoji_only(c)) / len(comments)
    if frac < 0.10:
        return "Bajo"
    if frac < 0.35:
        return "Medio"
    return "Alto"


# ---------- xlsx writer (single-column, inline strings) ----------

def write_comments_xlsx(path: str, comments: list, header: str = "Comentarios") -> None:
    """Escribe un .xlsx con una sola columna (header + comentarios), stdlib puro.

    Usa inlineStr para no necesitar sharedStrings. Sanitiza chars de control
    inválidos en XML 1.0 (todo lo <0x20 excepto tab, LF y CR).
    """
    import xml.sax.saxutils as sx

    _CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

    def esc(s):
        s = _CTRL_RE.sub("", str(s))
        return sx.escape(s)

    rows_xml = []
    rows_xml.append(
        '<row r="1"><c r="A1" t="inlineStr"><is><t xml:space="preserve">'
        + esc(header) + '</t></is></c></row>'
    )
    for i, c in enumerate(comments, start=2):
        rows_xml.append(
            f'<row r="{i}"><c r="A{i}" t="inlineStr"><is><t xml:space="preserve">'
            + esc(c) + '</t></is></c></row>'
        )

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetData>' + "".join(rows_xml) + '</sheetData>'
        '</worksheet>'
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Comentarios" sheetId="1" r:id="rId1"/></sheets>'
        '</workbook>'
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        'Target="worksheets/sheet1.xml"/>'
        '</Relationships>'
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        '</Relationships>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '</Types>'
    )

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook_xml)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)


# ---------- Beer / brand search ----------

_BEER_KEYWORDS = [
    r"cerveza", r"cervezas", r"birra", r"birras", r"chela", r"chelas",
    r"CMQ", r"cerveceria quilmes", r"cervecería quilmes",
    r"quilmes", r"brahma", r"corona", r"stella", r"stella artois",
    r"budweiser", r"andes origen", r"andes", r"temple",
    r"patagonia", r"patricia",
]

def find_beer_mentions(comments: list) -> list:
    pat = re.compile(r"\b(" + "|".join(_BEER_KEYWORDS) + r")\b", re.IGNORECASE)
    out = []
    for i, c in enumerate(comments):
        if pat.search(c):
            out.append({"idx": i, "text": c, "match": pat.search(c).group(0)})
    return out


# ---------- Platform detection ----------

def detect_platform(source) -> str:
    """Devuelve una etiqueta de red: 'TikTok', 'Instagram', 'YouTube', 'X',
    'Reddit', 'Facebook' o 'Desconocida'. Acepta ruta de archivo, dict de
    sheets, o texto crudo. Usa señales estructurales del volcado."""
    text = None
    if isinstance(source, dict):
        if "__text__" in source:
            text = source["__text__"]
        else:
            # Join all cells into a pseudo-text for signal detection
            buf = []
            for rows in source.values():
                for r in rows[:200]:
                    for v in r.values():
                        if v is not None:
                            buf.append(str(v))
            text = "\n".join(buf)
    elif isinstance(source, str):
        if os.path.exists(source):
            try:
                text = _read_text_file(source) if source.lower().endswith((".txt",)) else None
                if text is None:
                    sheets = read_file(source)
                    return detect_platform(sheets)
            except Exception:
                return "Desconocida"
        else:
            text = source
    if not text:
        return "Desconocida"

    low = text.lower()
    score = {"TikTok": 0, "Instagram": 0, "YouTube": 0, "X": 0, "Reddit": 0, "Facebook": 0}

    # TikTok: "Hace X d" + "Responder" + "Ver N respuestas"
    if "ver " in low and "respuestas" in low:
        score["TikTok"] += 3
    if re.search(r"ver\s+\d+\s+respuestas?", low):
        score["TikTok"] += 3
    if re.search(r"\bhace\s+\d+\s*(d|h|min)\b", low):
        score["TikTok"] += 1
        score["Instagram"] += 1
    if "responder" in low:
        score["TikTok"] += 1
        score["Instagram"] += 1
        score["YouTube"] += 1

    # Instagram: hearts, "Ver traducción", "mo" (meses), @ mentions dense
    if "ver traducción" in low or "ver traduccion" in low:
        score["Instagram"] += 3
    if re.search(r"\d+\s+me gusta", low):
        score["Instagram"] += 2

    # YouTube: "Mostrar respuestas", "¿X respuestas?", "Hace X" (ES) + likes
    if "mostrar respuestas" in low or "ver respuesta" in low and "hace" in low:
        score["YouTube"] += 2
    if "suscri" in low or "me gusta" in low and "no me gusta" in low:
        score["YouTube"] += 2

    # X (Twitter): "Retweet", "Retwittear", "veces", "Me gusta", "@" dense
    if "retwittear" in low or "retwitt" in low or "retweet" in low:
        score["X"] += 3
    if re.search(r"\d+(,|\.)\d+\s*(mil|k)\b", low) and "me gusta" in low:
        score["X"] += 2

    # Reddit: "·" + "ago" (EN) or "share" "report" "comments"
    if "u/" in low and "r/" in low:
        score["Reddit"] += 4
    if " share " in low and " report " in low and " reply " in low:
        score["Reddit"] += 3
    if re.search(r"\d+\s*(points?|upvotes?)", low):
        score["Reddit"] += 2

    # Facebook: "Like" + "Comment" + "Share" (EN) or "Compartir"
    if "compartir" in low and "comentar" in low and "me gusta" in low:
        score["Facebook"] += 3

    best, best_score = max(score.items(), key=lambda kv: kv[1])
    if best_score == 0:
        return "Desconocida"
    return best


# ---------- Spanish stopwords ----------

_STOPWORDS_ES = set("""
a al algo algún alguna algunas alguno algunos ambos ante antes aquel aquella
aquellas aquello aquellos aqui aquí así cada cierta ciertas cierto ciertos como
cómo con contra cual cuales cuáles cuan cuando cuanta cuántas cuanto cuántos de
del demás dentro desde donde dos durante el él ella ellas ello ellos en entre era
eran eras eres es esa esas ese eso esos esta ésta estaba estaban estamos están
estar estas éstas este éste esto estos estoy fue fuera fueron ha habia había
hace hacen hacer hago han hasta hay he hemos hicieron hizo incluso ir la las le
les lo los luego mas más me mi mía mías mío míos mientras mio mis mucha muchas
mucho muchos muy nada ni ninguna ningunas ninguno ningunos no nos nosotras
nosotros nuestra nuestras nuestro nuestros o os otra otras otro otros para pero
poco pocos por porque qué que quien quién quienes quiénes se sea sean según ser
si sí sido sin sobre sois solo sólo somos son soy su sus suya suyas suyo suyos
tal también tampoco tan tanta tantas tanto tantos te tenemos tener tenia tenía
tiene tienen tengo ti todas todo todos tu tú tus tuya tuyas tuyo tuyos un una
unas uno unos usted ustedes va vamos van varias varios vosotras vosotros voy y
ya yo me nos nosotros vos ustedes además aunque mientras quizás quizá
siempre nunca jamás jaja jajaja jajajaja jajajajaja ja je ji jo ju ok si no sí
pq xq k vs re q d e p ah oh eh uh hm mm hola chau pero pa aca acá aqui aquí
ahí allá allí ahora bueno bien mal más menos tan muy ver sacar poner dar hacer
hace hacen hacer ir estar estan están ser son fue fueron sea sean soy somos
eres era eran había habían hay habrá
""".split())

_STOPWORDS_SOCIAL = set("""
ja jaja jajaja jajajaja jajajajaja jajjaja jajs jajsjjaja hahaha haha lol jeje
jajá je jajaja jajajajajajaja jsjs xd lmao lmfao ha hahahah
""".split())

_STOPWORDS = _STOPWORDS_ES | _STOPWORDS_SOCIAL


def _tokenize(text: str) -> list:
    text = text.lower()
    # Remove emojis for the word analysis
    text = _EMOJI_PATTERN.sub(" ", text)
    # Remove URLs and @mentions / hashtags (keep hashtag word)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#(\w+)", r"\1", text)
    # Keep only letters (incl. accented) and spaces
    text = re.sub(r"[^a-záéíóúñüà-ÿ\s]", " ", text)
    tokens = text.split()
    return tokens


def top_tokens(comments: list, n: int = 40, min_len: int = 4) -> list:
    """Devuelve [(token, count), ...] con los n tokens más frecuentes,
    excluyendo stopwords y tokens de menos de min_len caracteres."""
    from collections import Counter
    c = Counter()
    for cm in comments:
        for tok in _tokenize(cm):
            if len(tok) < min_len:
                continue
            if tok in _STOPWORDS:
                continue
            # Dedup elongations: "jaaaa" → "ja" if too many repeats
            if re.match(r"^(.)\1{3,}$", tok):
                continue
            c[tok] += 1
    return c.most_common(n)


def top_emojis(comments: list, n: int = 12) -> list:
    """Devuelve [(emoji, count), ...] con los emojis más frecuentes."""
    from collections import Counter
    c = Counter()
    for cm in comments:
        for ch in _EMOJI_PATTERN.findall(cm):
            c[ch] += 1
    return c.most_common(n)


# ---------- CLI ----------

if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("uso: python read_input.py <archivo> [--summary|--json]")
        raise SystemExit(1)
    mode = sys.argv[2] if len(sys.argv) > 2 else "--summary"
    sheets = read_file(sys.argv[1])
    det = detect_comments(sheets)
    vol = volume_buckets(det["dates"])
    beer = find_beer_mentions(det["comments"])
    out = {
        "sheet": det["sheet"],
        "comment_col": det["comment_col"],
        "date_col": det["date_col"],
        "author_col": det["author_col"],
        "total_comments": len(det["comments"]),
        "emoji_level": emoji_level(det["comments"]),
        "volume": vol,
        "beer_mentions_count": len(beer),
        "beer_examples": beer[:10],
        "sample_comments": det["comments"][:20],
    }
    if mode == "--json":
        # Full dump including every comment.
        out["comments"] = det["comments"]
        out["dates"] = [d.isoformat() if d else None for d in det["dates"]]
        out["authors"] = det["authors"]
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))

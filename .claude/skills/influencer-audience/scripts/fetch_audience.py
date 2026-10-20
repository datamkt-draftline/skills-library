#!/usr/bin/env python3
"""
CreatorIQ Audience Fetcher — v2

Workflow:
  handle + network  →  lookup_creator()  →  publisherId  →  get_audience()
  publisherId                             →  get_audience()

Endpoints used:
  GET /crm/v1/api/accounts/lookup?network=NETWORK&search=HANDLE
      Params confirmed: network (required), search (required)
      Response schema: NOT fully documented. Extracted conservatively.

  GET /crm/v1/api/publisher/{publisherId}/audience
      Path confirmed. Response schema: NOT fully documented.
      Normalization is conservative (see normalize_audience()).

Usage:
  python fetch_audience.py --handle HANDLE --network NETWORK --api-key KEY
  python fetch_audience.py --publisher-id ID --api-key KEY
  python fetch_audience.py --handle HANDLE --network NETWORK --api-key KEY --debug --raw

Output:
  All [INFO]/[DEBUG] lines go to stdout (prefixed).
  The LAST LINE is always a single JSON object (the result).
  Parse the last line as JSON.
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error

DEFAULT_BASE_URL = "https://apis.creatoriq.com"

# ── Network normalization ────────────────────────────────────────────────────
# Values accepted by /accounts/lookup (confirmed from docs research)
VALID_NETWORKS = {"instagram", "tiktok", "youtube", "twitter", "facebook", "twitch", "pinterest"}

NETWORK_ALIASES = {
    "ig":        "instagram",
    "tt":        "tiktok",
    "yt":        "youtube",
    "tw":        "twitter",
    "x":         "twitter",
    "fb":        "facebook",
    "pin":       "pinterest",
}


def normalize_network(raw):
    if not raw:
        return None
    s = raw.strip().lower()
    return NETWORK_ALIASES.get(s, s if s in VALID_NETWORKS else None)


# ── HTTP helper ──────────────────────────────────────────────────────────────

def http_get(url, api_key):
    """
    Perform GET request with x-api-key auth (per CreatorIQ Publisher/Social OpenAPI spec).
    Returns dict:
      ok: bool
      status: int
      data: parsed JSON | raw string
    API key is NEVER logged.
    """
    headers = {
        "x-api-key": api_key,
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = raw
            return {"ok": True, "status": resp.status, "data": data}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = raw
        return {"ok": False, "status": e.code, "data": data}
    except urllib.error.URLError as e:
        return {"ok": False, "status": 0, "data": str(e)}


def classify_http_error(status, body):
    """Return a human-readable error with context for each HTTP status."""
    body_str = body if isinstance(body, str) else json.dumps(body)

    if status == 401:
        return {
            "code": "UNAUTHORIZED",
            "message": "API key inválida o expirada (HTTP 401).",
            "hint": "Verificá que la api_key en config.json sea correcta.",
        }
    if status == 403:
        # Distinguish proxy block from real 403
        if "proxy" in body_str.lower() or "blocked" in body_str.lower():
            return {
                "code": "PROXY_BLOCKED",
                "message": "El dominio está bloqueado por el proxy de red (HTTP 403).",
                "hint": "Este entorno no puede alcanzar apis.creatoriq.com. Ejecutá el script desde un entorno con acceso externo.",
                "_proxy_message": body_str,
            }
        return {
            "code": "FORBIDDEN",
            "message": "Sin permisos para este recurso (HTTP 403).",
            "hint": "Tu cuenta de CreatorIQ puede no tener habilitado este endpoint.",
        }
    if status == 404:
        return {
            "code": "NOT_FOUND",
            "message": "Recurso no encontrado (HTTP 404).",
            "hint": "El handle/publisherId no existe o no está en tu catálogo de CreatorIQ.",
        }
    if status == 0:
        return {
            "code": "NETWORK_ERROR",
            "message": "No se pudo conectar a la API.",
            "hint": str(body),
        }
    if status >= 500:
        return {
            "code": "SERVER_ERROR",
            "message": f"Error interno del servidor de CreatorIQ (HTTP {status}).",
        }
    return {
        "code": f"HTTP_{status}",
        "message": f"Respuesta inesperada: HTTP {status}.",
        "detail": body if isinstance(body, str) else None,
    }


# ── Step 1: resolve publisherId from handle ──────────────────────────────────

def lookup_creator(base_url, api_key, handle, network, debug):
    """
    GET /crm/v1/api/accounts/lookup?network=NETWORK&search=HANDLE

    Confirmed parameters (from API docs research):
      - network: required. One of the VALID_NETWORKS values.
      - search: required. The handle/username to look up.

    Response schema: NOT fully confirmed.
    We extract publisherId conservatively from common shapes.

    Returns: (publisher_id, error_dict | None)
    """
    if not network:
        return None, {
            "code": "MISSING_NETWORK",
            "message": "accounts/lookup requiere `network`. Especificá la plataforma (ej: instagram, tiktok, youtube).",
            "hint": "También podés pasar publisherId directamente para saltear este paso.",
        }

    url = (
        f"{base_url}/crm/v1/api/accounts/lookup"
        f"?network={urllib.parse.quote(network)}"
        f"&search={urllib.parse.quote(handle)}"
    )

    if debug:
        print(f"[DEBUG] endpoint: GET {url}")

    res = http_get(url, api_key)

    if debug:
        print(f"[DEBUG] status: {res['status']}")

    if not res["ok"]:
        if debug:
            print(f"[DEBUG] error body: {json.dumps(res['data'], ensure_ascii=False) if isinstance(res['data'], (dict, list)) else res['data']}")
        return None, classify_http_error(res["status"], res["data"])

    publisher_id = _extract_publisher_id(res["data"])

    if publisher_id is None:
        return None, {
            "code": "PUBLISHER_ID_NOT_FOUND",
            "message": "accounts/lookup respondió OK pero no se encontró publisherId en el response.",
            "hint": (
                "El schema del response de accounts/lookup no está completamente documentado. "
                "Usá --raw para inspeccionar el response completo."
            ),
            "_lookup_response": res["data"],
        }

    if debug:
        print(f"[DEBUG] publisherId resuelto: {publisher_id}  (fuente: accounts/lookup)")

    return publisher_id, None


def _extract_publisher_id(data):
    """
    Extract publisherId from accounts/lookup response.

    Handles shapes:
      - Direct object: {"publisherId": "123", ...}
      - Array:         [{"publisherId": "123"}, ...]
      - Paginated:     {"items": [...], "data": [...], "publishers": [...], ...}

    Field names tried: publisherId, publisher_id, ciqPublisherId, id
    (conservative — only common CRM API conventions)
    """
    CANDIDATE_FIELDS = ("publisherId", "publisher_id", "ciqPublisherId", "ciq_publisher_id")

    def _from_dict(obj):
        for key in CANDIDATE_FIELDS:
            if key in obj and obj[key] not in (None, ""):
                return str(obj[key])
        return None

    if isinstance(data, dict):
        # Try direct fields first
        pid = _from_dict(data)
        if pid:
            return pid
        # Try nested arrays
        for wrap_key in ("items", "data", "publishers", "results", "accounts", "content"):
            if wrap_key in data and isinstance(data[wrap_key], list):
                for item in data[wrap_key]:
                    if isinstance(item, dict):
                        pid = _from_dict(item)
                        if pid:
                            return pid
        return None

    if isinstance(data, list) and data:
        for item in data:
            if isinstance(item, dict):
                pid = _from_dict(item)
                if pid:
                    return pid
        return None

    return None


# ── Step 2: fetch audience ───────────────────────────────────────────────────

def get_audience(base_url, api_key, publisher_id, debug):
    """
    GET /crm/v1/api/publisher/{publisherId}/audience

    Returns aggregate audience demographics — NOT individual follower data.

    Returns: (raw_response_dict, error_dict | None)
    """
    url = f"{base_url}/crm/v1/api/publisher/{urllib.parse.quote(str(publisher_id))}/audience"

    if debug:
        print(f"[DEBUG] endpoint: GET {url}")

    res = http_get(url, api_key)

    if debug:
        print(f"[DEBUG] status: {res['status']}")

    if not res["ok"]:
        return None, classify_http_error(res["status"], res["data"])

    return res["data"], None


# ── Step 3: normalize ────────────────────────────────────────────────────────

def normalize_audience(raw, debug):
    """
    Normalize raw audience response to a consistent structure.

    Output format:
      {
        "gender":  [{"label": str, "percentage": float}],
        "age":     [{"label": str, "percentage": float}],
        "country": [{"label": str, "percentage": float}]
      }

    NOTE: This represents AGGREGATE audience demographics (e.g., % of followers
    per gender/age group/country). NOT individual follower records.

    NOTE: "country" refers to the geographic location of the audience,
    NOT nationality or citizenship.

    Field mapping strategy:
    - PRIMARY: field names commonly used in documented CRM APIs and influencer platforms.
    - COMPATIBILITY: additional variants that are clearly labeled.
    - NEVER: generic keys that could accidentally match unrelated data.

    When debug=True, logs which fields were found and which mapping was applied.
    """

    # ── Gender ──────────────────────────────────────────────────────────────
    # PRIMARY — most likely field names for a CRM influencer API
    GENDER_PRIMARY = [
        ("genders",  "gender",     "percentage"),   # e.g. [{gender: "female", percentage: 63.2}]
        ("gender",   "label",      "percentage"),   # e.g. [{label: "female", percentage: 63.2}]
        ("gender",   "name",       "percentage"),
    ]
    # COMPATIBILITY — additional variants, labeled explicitly
    GENDER_COMPAT = [
        ("genderDistribution",  "gender",    "percentage"),
        ("gender_distribution", "gender",    "percentage"),
        ("genderSplit",         "gender",    "percentage"),
    ]

    # ── Age ─────────────────────────────────────────────────────────────────
    AGE_PRIMARY = [
        ("ageRanges",  "ageRange",  "percentage"),  # e.g. [{ageRange: "18-24", percentage: 31.4}]
        ("ages",       "age",       "percentage"),
        ("age",        "label",     "percentage"),
        ("age",        "name",      "percentage"),
    ]
    AGE_COMPAT = [
        ("ageDistribution",  "ageRange",  "percentage"),
        ("age_distribution", "age",       "percentage"),
        ("ageGroups",        "ageGroup",  "percentage"),
    ]

    # ── Country / Location ──────────────────────────────────────────────────
    # IMPORTANT: "country" = geographic location of audience, NOT nationality.
    COUNTRY_PRIMARY = [
        ("countries",  "country",   "percentage"),  # e.g. [{country: "Argentina", percentage: 58.4}]
        ("locations",  "location",  "percentage"),
        ("country",    "label",     "percentage"),
        ("country",    "name",      "percentage"),
    ]
    COUNTRY_COMPAT = [
        ("countryDistribution",   "country",   "percentage"),
        ("country_distribution",  "country",   "percentage"),
        ("topCountries",          "country",   "percentage"),
        ("top_countries",         "country",   "percentage"),
        ("audience_country",      "country",   "percentage"),
    ]

    if not isinstance(raw, dict):
        if debug:
            print(f"[DEBUG] audience response no es un objeto JSON — tipo: {type(raw).__name__}")
        return {"gender": [], "age": [], "country": []}, []

    top_keys = list(raw.keys())
    if debug:
        print(f"[DEBUG] claves top-level del response: {top_keys}")

    def extract_section(mapping_list, label):
        for (field, name_key, pct_key) in mapping_list:
            if field not in raw:
                continue
            val = raw[field]
            items = []
            if isinstance(val, list):
                for item in val:
                    if not isinstance(item, dict):
                        continue
                    name = item.get(name_key) or item.get("label") or item.get("name") or item.get("key")
                    pct = item.get(pct_key) or item.get("pct") or item.get("percent") or item.get("value")
                    if name is None or pct is None:
                        continue
                    try:
                        items.append({"label": str(name), "percentage": round(float(pct), 1)})
                    except (ValueError, TypeError):
                        continue
            elif isinstance(val, dict):
                # Flat dict: {"female": 63.2, "male": 36.8}
                for k, v in val.items():
                    try:
                        items.append({"label": str(k), "percentage": round(float(v), 1)})
                    except (ValueError, TypeError):
                        continue
            if items:
                if debug:
                    tier = "PRIMARY" if (field, name_key, pct_key) in mapping_list[:len(mapping_list)] else "COMPAT"
                    print(f"[DEBUG] {label}: encontrado campo '{field}' ({name_key}/{pct_key}) — {len(items)} entradas")
                return items, field
        return [], None

    gender_items,  gender_field  = extract_section(GENDER_PRIMARY  + GENDER_COMPAT,  "gender")
    age_items,     age_field     = extract_section(AGE_PRIMARY     + AGE_COMPAT,     "age")
    country_items, country_field = extract_section(COUNTRY_PRIMARY + COUNTRY_COMPAT, "country")

    # Sort country by percentage desc
    country_items.sort(key=lambda x: x["percentage"], reverse=True)

    found_fields = [f for f in (gender_field, age_field, country_field) if f]
    if debug:
        if not found_fields:
            print("[DEBUG] No se encontraron campos de demographics conocidos en el response.")
        else:
            print(f"[DEBUG] campos de demographics encontrados: {found_fields}")

    return {
        "gender":  gender_items,
        "age":     age_items,
        "country": country_items,
    }, found_fields


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch CreatorIQ audience demographics")
    parser.add_argument("--handle",       default=None, help="Creator handle (without @)")
    parser.add_argument("--network",      default=None, help=f"Social network. Supported: {', '.join(sorted(VALID_NETWORKS))}")
    parser.add_argument("--publisher-id", default=None, help="Skip lookup, use this publisherId directly")
    parser.add_argument("--api-key",      required=True, help="CreatorIQ Bearer API key")
    parser.add_argument("--base-url",     default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--raw",          action="store_true", help="Include raw API responses in output")
    parser.add_argument("--debug",        action="store_true", help="Print debug info (endpoints, statuses, fields). API key is never shown.")
    args = parser.parse_args()

    if not args.handle and not args.publisher_id:
        _exit_error("MISSING_INPUT", "Falta --handle o --publisher-id.")

    base_url = args.base_url.rstrip("/")
    network = normalize_network(args.network)
    handle = (args.handle or "").lstrip("@")
    debug = args.debug

    if args.network and not network:
        print(f"[INFO] Red '{args.network}' no reconocida. Redes soportadas: {', '.join(sorted(VALID_NETWORKS))}")

    # ── Resolve publisherId ────────────────────────────────────────────────
    publisher_id = args.publisher_id
    raw_lookup = None

    if not publisher_id:
        print(f"[INFO] Buscando @{handle}" + (f" en {network}" if network else " (sin red especificada)") + "...")
        publisher_id, err = lookup_creator(base_url, args.api_key, handle, network, debug)
        if err:
            _exit_error(
                err.get("code", "LOOKUP_ERROR"),
                err.get("message", "Error en lookup"),
                step="lookup",
                hint=err.get("hint"),
                extra={"_lookup_response": err.get("_lookup_response")} if args.raw and "_lookup_response" in err else None,
            )
        print(f"[INFO] Publisher ID: {publisher_id}")

    # ── Fetch audience ─────────────────────────────────────────────────────
    print("[INFO] Obteniendo datos de audiencia...")
    raw_audience, err = get_audience(base_url, args.api_key, publisher_id, debug)
    if err:
        _exit_error(
            err.get("code", "AUDIENCE_ERROR"),
            err.get("message", "Error obteniendo audience"),
            step="audience",
            publisher_id=publisher_id,
            hint=err.get("hint"),
        )

    # ── Check if audience data exists ──────────────────────────────────────
    is_empty = (
        raw_audience is None
        or raw_audience == {}
        or raw_audience == []
        or (isinstance(raw_audience, dict) and not any(raw_audience.values()))
    )

    # ── Normalize ─────────────────────────────────────────────────────────
    demographics, found_fields = normalize_audience(raw_audience, debug)
    audience_available = bool(found_fields)

    # ── Build output ───────────────────────────────────────────────────────
    result = {
        "success": True,
        "publisherId": str(publisher_id),
        "handle": handle or None,
        "network": network or None,
        "audienceAvailable": audience_available,
        "demographics": demographics,
        "metadata": {
            "fieldsFound": found_fields,
            "rawKeys": list(raw_audience.keys()) if isinstance(raw_audience, dict) else [],
            "emptyResponse": is_empty,
        },
    }

    if not audience_available and not is_empty:
        result["_notice"] = (
            "El endpoint respondió pero no se encontraron campos de demographics reconocidos. "
            "Usá --raw para ver el response completo y reportar los campos reales."
        )

    if args.raw:
        result["_raw"] = {"audience": raw_audience}

    # Last line: JSON result (always)
    print(json.dumps(result, ensure_ascii=False))


def _exit_error(code, message, step=None, publisher_id=None, hint=None, extra=None):
    out = {"success": False, "code": code, "message": message}
    if step:
        out["step"] = step
    if publisher_id:
        out["publisherId"] = str(publisher_id)
    if hint:
        out["hint"] = hint
    if extra:
        out.update(extra)
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(1)


if __name__ == "__main__":
    main()

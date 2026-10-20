#!/usr/bin/env python3
"""
CreatorIQ Creator Fetcher — v1 (full-creator version)

Hits the CreatorIQ Audience MCP's /api/creator route and returns the full
creator payload (publisher info + all networks with per-network audience and
followers history). Shape matches what pptx_report_generator.js expects.

Usage:
  python fetch_creator.py --handle HANDLE [--network NETWORK] \
      [--base-url BASE_URL] [--out OUT_PATH]

Behavior:
  - Prints [INFO] / [ERROR] diagnostic lines to stderr.
  - On success: writes the JSON payload to --out (if given) and prints the
    same JSON to stdout as the last line.
  - On failure: last stdout line is {"success": false, "error": ..., "code": ...}.

Defaults:
  --network    "instagram"
  --base-url   https://creatoriq-audience-2ea2c44baa-rj.a.run.app
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://creatoriq-audience-2ea2c44baa-rj.a.run.app"
VALID_NETWORKS = {"instagram", "tiktok", "youtube", "twitter", "facebook", "twitch", "pinterest"}
NETWORK_ALIASES = {
    "ig": "instagram", "tt": "tiktok", "yt": "youtube",
    "tw": "twitter", "x": "twitter", "fb": "facebook", "pin": "pinterest",
}


def log(msg):
    print(f"[INFO] {msg}", file=sys.stderr, flush=True)


def err(msg):
    print(f"[ERROR] {msg}", file=sys.stderr, flush=True)


def normalize_network(raw):
    if not raw:
        return None
    s = raw.strip().lower()
    return NETWORK_ALIASES.get(s, s if s in VALID_NETWORKS else None)


def clean_handle(raw):
    s = (raw or "").strip()
    if s.startswith("@"):
        s = s[1:]
    return s


def http_post_json(url, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
            return {"ok": True, "status": resp.status, "data": json.loads(raw)}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = raw
        return {"ok": False, "status": e.code, "data": data}
    except urllib.error.URLError as e:
        return {"ok": False, "status": 0, "data": str(e.reason)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--handle", required=True, help="Social handle, with or without @")
    parser.add_argument("--network", default="instagram", help="Lookup network (default: instagram)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--out", default=None, help="Optional path to write the raw JSON payload")
    args = parser.parse_args()

    handle = clean_handle(args.handle)
    network = normalize_network(args.network) or "instagram"

    if not handle:
        print(json.dumps({"success": False, "code": "MISSING_HANDLE", "error": "handle is required"}))
        sys.exit(1)

    url = args.base_url.rstrip("/") + "/api/creator"
    log(f"POST {url}  handle={handle}  network={network}")

    result = http_post_json(url, {"handle": handle, "network": network})

    if not result["ok"]:
        err(f"HTTP {result['status']} — {result['data']}")
        print(json.dumps({
            "success": False,
            "code": f"HTTP_{result['status']}",
            "error": result["data"] if isinstance(result["data"], str) else json.dumps(result["data"]),
        }))
        sys.exit(2)

    data = result["data"]
    if not isinstance(data, dict) or not data.get("success"):
        err(f"API returned non-success: {str(data)[:200]}")
        print(json.dumps({"success": False, "code": "API_ERROR", "error": data}))
        sys.exit(3)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        log(f"wrote {args.out}")

    # Last stdout line = full JSON (so the caller can parse it)
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()

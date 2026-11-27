#!/usr/bin/env python3
"""Prepare a Typeform POST /images body locally; never make network requests."""
import argparse
import base64
import json
import os
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("image", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--background", action="store_true", help="Apply conservative 2 MB background size limit")
    a = p.parse_args()
    raw = a.image.read_bytes()
    max_bytes = 2_000_000 if a.background else 4_000_000
    if not raw or len(raw) > max_bytes:
        p.error(f"Image must be nonempty and <= {max_bytes} bytes; resize without losing transparency first")
    if raw.startswith(b"\x89PNG\r\n\x1a\n") and a.image.suffix.lower() == ".png":
        pass
    elif raw.startswith(b"\xff\xd8\xff") and a.image.suffix.lower() in {".jpg", ".jpeg"}:
        pass
    elif raw[:6] in {b"GIF87a", b"GIF89a"} and a.image.suffix.lower() == ".gif":
        pass
    else:
        p.error("Unsupported image or file extension does not match PNG/JPEG/GIF signature")
    body = {"file_name": a.image.name, "image": base64.b64encode(raw).decode("ascii")}
    # Exclusive creation avoids overwriting another file; owner-only mode.
    fd = os.open(a.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(body, f, ensure_ascii=False)
    print(f"Prepared image payload: {a.output} ({len(raw)} image bytes). No upload performed.")


if __name__ == "__main__":
    main()

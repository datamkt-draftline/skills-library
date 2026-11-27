#!/usr/bin/env python3
"""Offline sanity checks for Typeform create/update payloads, not an API schema validator."""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

FIELD_TYPES = set("calendly checkbox contact_info date dropdown email file_upload google_calendar group legal long_text matrix multi_format multiple_choice nps number opinion_scale payment phone_number picture_choice ranking rating short_text signature statement website yes_no".split())


def walk_fields(fields):
    for field in fields:
        yield field
        yield from walk_fields(field.get("properties", {}).get("fields", []))


def resources(form):
    for f in walk_fields(form.get("fields", [])):
        yield "field", f
        for choice in f.get("properties", {}).get("choices", []):
            yield "choice", choice
    for key in ("welcome_screens", "thankyou_screens"):
        for item in form.get(key, []):
            yield key, item


def check(form, before=None):
    errors, warnings = [], []
    fields = list(walk_fields(form.get("fields", [])))
    old = list(resources(before)) if before else []
    previous = {(k, item.get("id") or item.get("ref")): item for k, item in old if item.get("id") or item.get("ref")}
    current = list(resources(form))
    refs = set()
    if not isinstance(form.get("title"), str) or not form["title"].strip():
        errors.append("title is required")
    if not fields:
        errors.append("No fields in payload")
    for kind, item in current:
        ref = item.get("ref")
        name = f"{kind}:{ref or item.get('id') or '(no ref)'}"
        if ref:
            if ref in refs:
                errors.append(f"Duplicate ref: {ref}")
            refs.add(ref)
        elif not item.get("id"):
            warnings.append(f"Assign stable ref to {name}")
        if kind == "field":
            typ = item.get("type")
            if typ not in FIELD_TYPES:
                warnings.append(f"Check current schema for type {typ!r} in {name}")
            if not item.get("title"):
                errors.append(f"Missing title: {name}")
            v = item.get("validations", {})
            if "min_value" in v and "max_value" in v and v["min_value"] > v["max_value"]:
                errors.append(f"min_value > max_value: {name}")
            if typ == "picture_choice":
                for c in item.get("properties", {}).get("choices", []):
                    if c.get("attachment", {}).get("type") != "image" or not c.get("attachment", {}).get("href"):
                        errors.append(f"Missing image for picture choice {c.get('ref', '(no ref)')}")
        layout = item.get("layout", {}) or {}
        prior = previous.get((kind, item.get("id") or ref))
        # Do not force a legacy layout to change in unrelated updates.
        unchanged = prior is not None and prior.get("layout") == item.get("layout") and prior.get("attachment") == item.get("attachment")
        if layout.get("type") in {"split", "float"} and not unchanged:
            if layout.get("placement") not in {"left", "right"}:
                errors.append(f"Missing/invalid lateral placement: {name}")
            inner = layout.get("attachment", {}) or {}
            outer = item.get("attachment", {}) or {}
            if inner.get("type") == "image" and (outer.get("type") != "image" or not outer.get("href") or inner.get("href") != outer.get("href")):
                errors.append(f"Lateral image must use matching attachment and layout.attachment: {name}")
        for att in (item.get("attachment"), layout.get("attachment")):
            if isinstance(att, dict) and att.get("type") == "image":
                url = urlsplit(att.get("href", ""))
                if url.scheme != "https" or not url.netloc:
                    errors.append(f"Invalid image href: {name}")
    field_refs = {f.get("ref") for f in fields if f.get("ref")}
    choice_refs = {i.get("ref") for k, i in current if k == "choice" and i.get("ref")}
    endings = {i.get("ref") for k, i in current if k == "thankyou_screens" and i.get("ref")} | {"default"}
    variables = set(form.get("variables", {}))
    hidden = set(form.get("hidden", []))
    def check_operand(op):
        if not isinstance(op, dict):
            return
        typ, val = op.get("type"), op.get("value")
        known = {"field": field_refs, "choice": choice_refs, "variable": variables, "hidden": hidden}
        if typ in known and isinstance(val, str) and val not in known[typ]:
            errors.append(f"Unknown {typ} operand: {val}")
        for nested in op.get("vars", []):
            check_operand(nested)
    for block in form.get("logic", []):
        if block.get("type") == "field" and block.get("ref") not in field_refs:
            errors.append(f"Unknown logic field: {block.get('ref')}")
        for action in block.get("actions", []):
            details = action.get("details", {})
            if action.get("action") == "jump":
                to = details.get("to", {})
                if to.get("type") == "field" and to.get("value") not in field_refs:
                    errors.append(f"Unknown field destination: {to.get('value')}")
                elif to.get("type") == "thankyou" and to.get("value") not in endings:
                    errors.append(f"Unknown thank-you destination: {to.get('value')}")
            else:
                check_operand(details.get("target"))
                check_operand(details.get("value"))
            check_operand(action.get("condition", {}))
    if before is not None:
        now = {(k, key, i[key]) for k, i in current for key in ("id", "ref") if i.get(key)}
        for k, item in old:
            # Compare id and ref separately; both must survive ordinary updates.
            for key in ("id", "ref"):
                if item.get(key) and (k, key, item[key]) not in now:
                    errors.append(f"Existing {k} {key} lost: {item[key]}")
        for k in ("theme", "workspace", "settings", "logic", "hidden", "variables", "thankyou_screens", "welcome_screens"):
            if k in before and k not in form:
                warnings.append(f"Existing top-level property omitted: {k}; review before PUT")
    return errors, warnings


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("payload", type=Path)
    p.add_argument("--before", type=Path)
    a = p.parse_args()
    try:
        form = json.loads(a.payload.read_text(encoding="utf-8"))
        before = json.loads(a.before.read_text(encoding="utf-8")) if a.before else None
        errors, warnings = check(form, before)
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        print(f"Invalid or unsupported JSON structure: {type(exc).__name__}", file=sys.stderr)
        return 2
    for warning in warnings:
        print("WARN:", warning)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("Basic offline checks passed. Review live API schema, placeholders, scope and intended changes before sending.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

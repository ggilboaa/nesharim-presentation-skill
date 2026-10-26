#!/usr/bin/env python3
"""Validate structural invariants of a finished Nesharim HTML deck."""

import argparse
import re
import sys
from pathlib import Path


def validate(text: str, require_editor: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def need(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    need(bool(re.search(r"<html\b[^>]*\blang=['\"]he['\"][^>]*\bdir=['\"]rtl['\"]", text, re.I)), "html must declare lang=he and dir=rtl")
    need('id="stage"' in text or "id='stage'" in text, "missing #stage")
    need('id="presentation"' in text or "id='presentation'" in text, "missing #presentation")
    slides = re.findall(r"class=['\"][^'\"]*\bslide\b[^'\"]*['\"]", text, re.I)
    need(len(slides) >= 2, "expected at least two .slide elements")
    need(any(re.search(r"\bactive\b", item) for item in slides), "no active slide")
    need("Paamon" in text, "Paamon font is not referenced")
    need("חזקי גלבוע" in text, "opening speaker name is missing")
    need("לייעוץ ומענה:" in text, "fixed closing headline is missing")
    need("053-766-1500" in text, "fixed closing phone is missing")
    need("nesharim.org.il" in text, "fixed closing website is missing")
    need(bool(re.search(r"1920\s*px", text, re.I)) and bool(re.search(r"1080\s*px", text, re.I)), "fixed 1920x1080 canvas not evident")
    need("Math.min" in text and "innerWidth" in text and "innerHeight" in text, "uniform fitStage scaling not evident")
    need("@media print" in text, "missing print CSS")

    # JavaScript legitimately contains words such as `src=` and `file:` while
    # implementing the editor. Asset portability is a markup/CSS invariant, so
    # exclude script bodies before inspecting resource references.
    portable_markup = re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.I | re.S)
    relative_assets = re.findall(
        r"(?:url\(\s*|\b(?:src|href)\s*=\s*)['\"]?(?!data:|https?:|mailto:|tel:|#)([^)'\"\s>]+)",
        portable_markup,
        re.I,
    )
    if relative_assets:
        errors.append("non-self-contained asset references: " + ", ".join(sorted(set(relative_assets))[:8]))
    if re.search(r"(?:file://|/Users/|/home/|/mnt/)", portable_markup):
        errors.append("local filesystem path found")
    if "bgfullblue" in text and "bgfullgreen" in text:
        warnings.append("both theme names appear; confirm the deck does not mix themes")
    if require_editor:
        need("__brainEdInit" in text, "Edit Mode requested but editor marker is missing")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html")
    parser.add_argument("--require-editor", action="store_true")
    args = parser.parse_args()
    path = Path(args.html)
    errors, warnings = validate(path.read_text(encoding="utf-8"), args.require_editor)
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    if errors:
        sys.exit(1)
    print(f"OK: {path} ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()

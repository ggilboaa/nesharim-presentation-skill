#!/usr/bin/env python3
"""Validate structural invariants of a finished Nesharim HTML deck."""

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class SlideReader(HTMLParser):
    """Collect actual slide markup without matching JavaScript strings."""
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__()
        self.slides = []
        self.current = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.current is None and 'slide' in attrs.get('class', '').split():
            self.current = {'text': '', 'divider': False}
            self.depth = 0
        if self.current is not None:
            if tag not in self.VOID:
                self.depth += 1
            if 'speaker-divider' in attrs.get('class', '').split() or attrs.get('data-role') == 'speaker-divider':
                self.current['divider'] = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.current is not None and tag not in self.VOID:
            self.depth -= 1
            if self.depth == 0:
                self.slides.append(self.current)
                self.current = None

    def handle_data(self, data):
        if self.current is not None:
            self.current['text'] += data


def validate(text: str, require_editor: bool = False, publish: bool = False) -> tuple[list[str], list[str]]:
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

    has_editor = '__brainEdInit' in text or bool(re.search(r'id=[\'"]ed-(?:fab|toolbar)[\'"]', portable_markup))
    if not require_editor:
        need(not has_editor, 'Edit Mode must be absent by default; use --require-editor only for an explicitly requested editable copy')
    if publish:
        need(not has_editor, 'publication copy must not contain Edit Mode')
    parsed = SlideReader()
    parsed.feed(portable_markup)
    need(len(parsed.slides) >= 2, 'expected distinct opening and closing slide elements')
    if parsed.slides:
        need('חזקי גלבוע' in parsed.slides[0]['text'], 'speaker must be on the opening slide, not a content slide')
        need(parsed.slides[0]['divider'], 'opening needs a speaker-divider below the lecture subtitle')
        for value in ('לייעוץ ומענה:', '053-766-1500', 'nesharim.org.il'):
            need(value in parsed.slides[-1]['text'], 'closing slide missing ' + value)
    need(bool(re.search(r'<meta\b[^>]*name=[\'"]format-detection[\'"][^>]*content=[\'"][^\'"]*telephone=no', text, re.I)), 'missing mobile phone format-detection protection')
    if publish:
        need('nav-visible' in text, 'publication needs quiet reveal-on-interaction navigation')
        fs = re.search(r'<button\b[^>]*id=[\'"]fs[\'"][^>]*>(.*?)</button>', portable_markup, re.S)
        need(bool(fs and '<svg' in fs[1]), 'fullscreen control must use a small icon')

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--require-editor", action="store_true")
    mode.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    path = Path(args.html)
    errors, warnings = validate(path.read_text(encoding="utf-8"), args.require_editor, args.publish)
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    if errors:
        sys.exit(1)
    print(f"OK: {path} ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()

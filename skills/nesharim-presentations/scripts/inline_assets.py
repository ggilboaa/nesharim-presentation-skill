#!/usr/bin/env python3
"""Inline packaged Nesharim fonts and backgrounds into a deck HTML."""

import argparse
import base64
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
BACKGROUNDS = ASSETS / "backgrounds"

PRINT_CSS = """
@media print {
  @page { size: 13.333333in 7.5in; margin: 0; }
  html, body { width: 1920px !important; height: 1080px !important; overflow: visible !important; }
  #stage { width: 1920px !important; height: auto !important; display: block !important; }
  #presentation { width: 1920px !important; height: auto !important; transform: none !important; }
  .slide { display: block !important; position: relative !important; width: 1920px !important; height: 1080px !important; break-after: page; page-break-after: always; overflow: hidden !important; }
  .slide:last-child { break-after: auto; page-break-after: auto; }
  #ed-toolbar, #ed-fab, #ed-hint, #ed-toast, #ed-restore { display: none !important; }
}
""".strip()


def data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def inline(html: str) -> str:
    font_css = (ASSETS / "paamon-fonts.css").read_text(encoding="utf-8")
    html = re.sub(
        r"@import\s+url\((['\"]?)paamon-fonts\.css\1\)\s*;?",
        font_css,
        html,
        flags=re.IGNORECASE,
    )
    for path in sorted(BACKGROUNDS.glob("*.jpg")):
        # Finished decks may already contain large base64 assets. Avoid running
        # URL regexes across them when this packaged filename is not referenced.
        if path.name.lower() not in html.lower():
            continue
        uri = data_uri(path)
        name = re.escape(path.name)
        html = re.sub(rf"url\((['\"]?)(?:[^)'\"]*/)?{name}\1\)", f"url('{uri}')", html)
        html = re.sub(rf"(src\s*=\s*['\"])(?:[^'\"]*/)?{name}(['\"])", rf"\1{uri}\2", html)
    if "@media print" not in html:
        closing_head = re.search(r"</head\s*>", html, re.I)
        block = f"\n<style id=\"nesharim-print\">\n{PRINT_CSS}\n</style>\n"
        if closing_head:
            html = html[: closing_head.start()] + block + html[closing_head.start() :]
        else:
            html = block + html
    return html


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html")
    parser.add_argument("--output")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    source = Path(args.html).resolve()
    if args.in_place and args.output:
        parser.error("choose --in-place or --output")
    target = source if args.in_place else Path(args.output).resolve() if args.output else source.with_name(source.stem + "-self-contained.html")
    target.write_text(inline(source.read_text(encoding="utf-8")), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()

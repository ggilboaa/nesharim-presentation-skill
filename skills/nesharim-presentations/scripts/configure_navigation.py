#!/usr/bin/env python3
"""Add idempotent, self-contained quiet navigation and mobile phone protection."""
import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SVG = '<svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H3v5M16 3h5v5M21 16v5h-5M3 16v5h5"/></svg>'


def configure(text: str) -> str:
    if not re.search(r'class=[\'"][^\'"]*\bcontrols\b', text):
        raise ValueError('Expected .controls outside #presentation with #fs, #count, #prev, #next')
    for ident in ('fs', 'count', 'prev', 'next'):
        if not re.search(rf'id=[\'"]{ident}[\'"]', text):
            raise ValueError(f'Missing #{ident}')
    text = re.sub(r'<style\b[^>]*id=[\'"]nesharim-navigation-css[\'"][^>]*>.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<script\b[^>]*id=[\'"]nesharim-navigation-js[\'"][^>]*>.*?</script>', '', text, flags=re.S)
    text = re.sub(r'(<button\b[^>]*id=[\'"]fs[\'"][^>]*>).*?(</button>)', lambda m: m[1]+SVG+m[2], text, count=1, flags=re.S)
    text = re.sub(r'<meta\b[^>]*name=[\'"]format-detection[\'"][^>]*>', '', text, flags=re.I)
    protection = '\na[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important}\n'
    css = (HERE / 'navigation.css').read_text(encoding='utf-8') + protection
    head = '<meta name="format-detection" content="telephone=no">\n<style id="nesharim-navigation-css">\n'+css+'</style>\n'
    if '</head>' not in text or '</body>' not in text:
        raise ValueError('Expected closing head and body tags')
    text = text.replace('</head>', head+'</head>')
    script = '<script id="nesharim-navigation-js">\n'+(HERE / 'navigation.js').read_text(encoding='utf-8')+'</script>\n'
    return text.replace('</body>', script+'</body>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    args = parser.parse_args()
    args.html.write_text(configure(args.html.read_text(encoding='utf-8')), encoding='utf-8')
    print(f'Quiet navigation configured: {args.html}')


if __name__ == '__main__':
    main()

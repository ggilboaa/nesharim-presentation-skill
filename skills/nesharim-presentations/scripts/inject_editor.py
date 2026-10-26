#!/usr/bin/env python3
"""
inject_editor.py - inject (or upgrade) the Brain deck Edit Mode into a deck HTML.

Usage:
  python3 scripts/inject_editor.py path/to/deck.html

Additive: appends editor.css before the last </style> and editor.js before
</body>. If a previous version is present (CSS marker / __brainEdInit script),
it is replaced in place. Always make a backup before running on a deck you
care about.
"""
from html.parser import HTMLParser
import argparse
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS_MARK = '/* ===== BRAIN DECK · EDIT MODE UI'   # matches v1 + v2 markers
JS_MARK = '__brainEdInit'


def inject(path: str) -> None:
    target = Path(path).resolve()
    src = target.read_text(encoding='utf-8')
    css = (HERE / 'editor.css').read_text(encoding='utf-8')
    js = (HERE / 'editor.js').read_text(encoding='utf-8')

    required = ('id="presentation"', 'class="slide')
    missing = [token for token in required if token not in src]
    if missing:
        raise ValueError(f"incompatible deck; missing: {', '.join(missing)}")

    backup = target.with_suffix(target.suffix + '.pre-editor')
    if not backup.exists():
        shutil.copy2(target, backup)

    # ---- CSS: replace existing editor block, else append before last </style>
    ci = src.find(CSS_MARK)
    if ci != -1:
        ce = src.find('</style>', ci)
        assert ce != -1, 'editor CSS marker found but no closing </style>'
        src = src[:ci] + css.strip() + '\n' + src[ce:]
    else:
        si = src.rfind('</style>')
        assert si != -1, 'no </style> in deck'
        src = src[:si] + css + '\n' + src[si:]

    # ---- JS: replace the <script> containing __brainEdInit, else append
    ji = src.find(JS_MARK)
    if ji != -1:
        js_start = src.rfind('<script>', 0, ji)
        js_end = src.find('</script>', ji)
        assert js_start != -1 and js_end != -1, 'editor JS marker found but script bounds missing'
        src = src[:js_start] + '<script>\n' + js + '\n</script>' + src[js_end + len('</script>'):]
    else:
        bi = src.rfind('</body>')
        assert bi != -1, 'no </body> in deck'
        src = src[:bi] + '<script>\n' + js + '\n</script>\n' + src[bi:]

    target.write_text(src, encoding='utf-8')
    print(f'editor injected into {target} ({len(src)} bytes)')


class RuntimeEditorStripper(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.output = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        ident = dict(attrs).get('id', '')
        if self.skip or ident.startswith('ed-'):
            if tag not in self.VOID:
                self.skip += 1
        else:
            self.output.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if not self.skip and not dict(attrs).get('id', '').startswith('ed-'):
            self.output.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.skip:
            if tag not in self.VOID:
                self.skip -= 1
        else:
            self.output.append('</'+tag+'>')

    def handle_data(self, data):
        if not self.skip:
            self.output.append(data)

    def handle_entityref(self, name):
        self.handle_data('&'+name+';')

    def handle_charref(self, name):
        self.handle_data('&#'+name+';')

    def handle_comment(self, data):
        self.handle_data('<!--'+data+'-->')

    def handle_decl(self, decl):
        self.handle_data('<!'+decl+'>')


def remove(path: str) -> None:
    target = Path(path).resolve()
    text = target.read_text(encoding='utf-8')
    text = re.sub(r'<script\b[^>]*>(?:(?!</script>).)*__brainEdInit(?:(?!</script>).)*</script>', '', text, flags=re.S)
    start = text.find(CSS_MARK)
    if start >= 0:
        end = text.find('</style>', start)
        if end < 0:
            raise ValueError('Unterminated editor CSS')
        text = text[:start] + text[end:]
    # Runtime-exported copies may retain editor UI and selection state.
    parser = RuntimeEditorStripper()
    parser.feed(text)
    text = ''.join(parser.output)
    text = re.sub(r'\scontenteditable=(?:"[^"]*"|\'[^\']*\')', '', text)
    text = re.sub(r'\bed-(?:on|hover|selected)\b', '', text)
    target.write_text(text, encoding='utf-8')
    print(f'editor removed from {target}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html')
    parser.add_argument('--remove', action='store_true', help='Remove editor code, CSS and runtime UI')
    args = parser.parse_args()
    if args.remove:
        remove(args.html)
    else:
        inject(args.html)

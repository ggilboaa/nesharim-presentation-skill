"""Regression checks for opt-in editing, opening/closing and quiet navigation."""
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from configure_navigation import configure
from inject_editor import inject, remove
from validate_deck import validate

DECK = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>
body{font-family:Paamon}#presentation{width:1920px;height:1080px}
@media print{.slide{break-after:page}}
</style></head><body><main id="stage"><div id="presentation">
<section class="slide full active"><h1>שם הרצאה</h1><p>תת כותרת</p><hr class="speaker-divider"><p>חזקי גלבוע</p></section>
<section class="slide full"><p>לייעוץ ומענה:</p><bdi>053-766-1500</bdi><p>nesharim.org.il</p></section>
</div></main><nav class="controls"><button id="prev">→</button><span id="count">1 / 2</span><button id="next">←</button><button id="fs">מסך מלא</button></nav>
<script>function fitStage(){return Math.min(innerWidth/1920,innerHeight/1080)}</script></body></html>'''


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.clean = configure(DECK)

    def test_clean_publication(self):
        self.assertEqual(validate(self.clean, publish=True)[0], [])

    def test_default_rejects_editor_and_explicit_mode_accepts(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'deck.html'
            p.write_text(self.clean)
            inject(str(p))
            edited = p.read_text()
            self.assertTrue(any('Edit Mode' in e for e in validate(edited)[0]))
            self.assertEqual(validate(edited, require_editor=True)[0], [])
            self.assertTrue(validate(edited, publish=True)[0])
            remove(str(p))
            self.assertEqual(validate(p.read_text(), publish=True)[0], [])
            self.assertNotIn('__brainEdInit', p.read_text())
            self.assertNotIn('BRAIN DECK · EDIT MODE UI', p.read_text())

    def test_nested_runtime_editor_ui_is_removed_without_losing_content(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'deck.html'
            runtime = '<div id="ed-toolbar"><div id="ed-row"><button>עריכה</button></div><div>כלים</div></div><p id="keep">תוכן שנשמר</p>'
            p.write_text(self.clean.replace('</body>', runtime+'</body>'))
            remove(str(p))
            self.assertNotIn('כלים', p.read_text())
            self.assertIn('<p id="keep">תוכן שנשמר</p>', p.read_text())
            self.assertEqual(validate(p.read_text(), publish=True)[0], [])

    def test_opening_and_closing_are_checked_in_position(self):
        misplaced = self.clean.replace('<p>חזקי גלבוע</p>', '').replace('לייעוץ ומענה:', 'לייעוץ ומענה: חזקי גלבוע')
        self.assertTrue(any('speaker must be' in e for e in validate(misplaced)[0]))
        self.assertTrue(any('speaker-divider' in e for e in validate(self.clean.replace('class="speaker-divider"', ''))[0]))
        self.assertTrue(any('closing slide missing' in e for e in validate(self.clean.replace('<bdi>053-766-1500</bdi>', ''))[0]))

    def test_navigation_can_be_configured_twice(self):
        again = configure(self.clean)
        self.assertEqual(again.count('id="nesharim-navigation-css"'), 1)
        self.assertEqual(again.count('id="nesharim-navigation-js"'), 1)
        self.assertEqual(again.count('name="format-detection"'), 1)
        self.assertNotIn('id="fs">מסך מלא', again)
        self.assertIn('pointerup', again)
        self.assertIn('focus-visible', again)
        self.assertEqual(validate(again, publish=True)[0], [])


if __name__ == '__main__':
    unittest.main()

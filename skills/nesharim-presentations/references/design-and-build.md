# Design and HTML build

## Canvas contract

Build `#stage > #presentation > .slide` on a fixed 1920x1080 canvas. `#stage` fills the viewport and centers `#presentation`. Only `#presentation` receives `transform: scale(...)`, calculated as `min(innerWidth/1920, innerHeight/1080)` on load, resize, and fullscreen changes.

Slides use fixed pixels. Do not use viewport-driven slide reflow or max-width/max-height breakpoints. Portrait phones see a letterboxed 16:9 deck, not a document. Keep navigation/editor controls outside the scaled canvas where possible, with keyboard, buttons, swipe, fullscreen, progress, and LTR direction on numeric counters.

## Layouts

- A — opening, closing, or section transition; full background.
- B — one large statement; framed background.
- C — 3-6 independent items as real bordered cards, never bullet dots.
- D — a 50/50 comparison or 40/60 emphasis using two distinct columns.
- E — a compact 2x3, 2x4, 3x3, or 3x4 grid of short labels.
- F — a visible causal or sequential flow with 2-5 steps and arrows.

Split content that does not fit instead of shrinking below the typography system or inventing a layout.

## Output and verification

Run `scripts/inline_assets.py` so final HTML has no local or relative asset dependencies, then `scripts/validate_deck.py`. Add print CSS that removes scaling/chrome and renders every slide as a full 1920x1080 page.

Inspect opening, representative content layouts, and closing. Verify contrast, safe margins, no duplicated branding, theme/highlight pairing, exact fixed details, layout semantics, uniform scaling at wide and narrow/tall viewports, and usable navigation/touch targets.

## Focus slides and quiet navigation

For layout B focus slides such as `אמפתיה | גבולות` or `מודל המפה`, center the entire keyword group. Balance the vertical intervals between title, central statement, and lower closing line (for example centers at y=300, 540, 780), rather than applying a card-slide template.

Use `.controls` outside `#presentation`, with buttons `#prev`, `#next`, `#fs` and an LTR `#count`. Preserve the deck's navigation and fullscreen handlers. Run `scripts/configure_navigation.py deck.html` after base behavior works. This adds a small fullscreen SVG with accessible label/title, hides the panel below the viewport by default, and reveals it near the bottom pointer area, on keyboard focus/navigation, or on touch. Touch/keyboard reveals auto-hide; keep it visible while a mouse is over the panel. Respect safe areas and reduced motion, and hide all chrome in print. Never depend on hover alone on mobile.

Keep Edit Mode absent unless explicitly requested. For an older editable deck, remove the editor with `scripts/inject_editor.py deck.html --remove` before delivering a clean copy. Publication copies must always be editor-free unless the user explicitly changes this publication requirement.

## Verify delivered versions

After saving a revision, check every save result and retain the returned version identity. A local correction does not prove the downloadable file was updated. On a failed or uncertain save, do not claim success or return a stale artifact as corrected. Verify the delivered version when a previous save failed or the user reports seeing an old result.

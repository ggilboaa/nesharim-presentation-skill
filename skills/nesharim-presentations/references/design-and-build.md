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

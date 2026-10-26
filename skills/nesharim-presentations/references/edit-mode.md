# Edit Mode

Edit Mode provides selection, dragging, inline text editing, image paste/drop, duplication, z-order, color controls, undo/redo, local autosave, and edited-HTML download.

Inject it after the base deck renders correctly:

```bash
python3 scripts/inject_editor.py path/to/deck.html
```

The deck must use `#presentation`, `.slide`, and `.active`. The editor derives scale from the transformed 1920x1080 canvas. After injection, verify present mode and test selection, dragging at a non-1920 viewport, Hebrew editing, undo, and save. A clean presentation-only copy may omit Edit Mode when requested.

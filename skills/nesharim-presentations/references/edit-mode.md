# Edit Mode

Edit Mode provides selection, dragging, inline text editing, image paste/drop, duplication, z-order, color controls, undo/redo, local autosave, and edited-HTML download.

Do not inject Edit Mode by default, even in intermediate HTML. Add it only when the user explicitly asks for editing controls, after the base deck renders correctly:

```bash
python3 scripts/inject_editor.py path/to/deck.html
```

The deck must use `#presentation`, `.slide`, and `.active`. The editor derives scale from the transformed 1920x1080 canvas. After injection, verify present mode and test selection, dragging at a non-1920 viewport, Hebrew editing, undo, and save. Keep the requested editable copy separate from the clean publication copy. Remove the editor with `python3 scripts/inject_editor.py path/to/deck.html --remove`; validate the clean copy without `--require-editor` (and with `--publish` before publication).

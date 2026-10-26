---
name: nesharim-presentations
description: Create, revise, validate, export, or publish branded Hebrew RTL presentations for Nesharim as self-contained HTML and optional PDF. Use for a new מצגת, converting notes into slides, updating an existing Nesharim deck, adding visual edit mode, or publishing a finished deck. Do not use for unrelated presentations or ordinary documents.
metadata:
  short-description: Branded Hebrew presentations for Nesharim
---

# Nesharim Presentations

Create clear Hebrew RTL presentations that preserve the Nesharim visual system and remain usable from desktop and mobile. Treat publishing as a separate, explicitly authorized action.

## Skill development and cross-device synchronization

The canonical source for this skill and its packaged resources is https://github.com/ggilboaa/nesharim-presentation-skill (default branch: `main`).

- Every update or future development of this skill must include a commit and push to this repository, including changes to instructions, references, scripts, assets, and plugin metadata. An authenticated GitHub connector write that creates the remote commit is equivalent to a local commit and push.
- Before editing from any device, fetch the latest remote state and reconcile local changes without discarding anyone's work. When editing through the connector, read the current file and use its current SHA for the update.
- Validate the changed skill or resources as appropriate, review the diff, and commit only the changes belonging to the requested skill update. Increment `plugin.json` version when the packaged skill changes.
- Push the completed update to `main` when repository rules allow it. If a protected branch requires a pull request, push the update branch, create the pull request, and clearly report that cross-device availability is pending merge; do not bypass protections.
- Verify the remote commit and changed files after pushing, and return the commit or pull request link. Do not report an update as synchronized until it is verified on the remote branch.
- If authentication, connectivity, permissions, or conflicts prevent synchronization, preserve the work, explicitly report the pending push and the reason, and provide the next action. Never silently leave an update only on one device or use force-push to resolve a conflict.
- Other devices must update or refresh their installed copy to consume the new version; a GitHub push alone does not guarantee that an already installed plugin refreshes automatically.
- This synchronization requirement applies to developing the skill itself. Presentation content and generated decks follow the separate delivery and publication approvals below.

## Route the request

- For a new deck or substantial rewrite, follow the full workflow below.
- For a focused change, preserve approved content and design unless the request requires otherwise.
- For Edit Mode only, read [references/edit-mode.md](references/edit-mode.md) and use `scripts/inject_editor.py`.
- For PDF or GitHub delivery, read [references/delivery.md](references/delivery.md) only after validation.

## Full workflow

1. Read [references/brand-system.md](references/brand-system.md) and [references/content-workflow.md](references/content-workflow.md).
2. Draft slide-level content in readable Hebrew. Use defaults instead of asking about audience, tone, depth, length, or theme unless the user supplied different values.
3. Present content for approval before visual production. Apply edits and repeat until approved. A user may explicitly waive this checkpoint.
4. Read [references/design-and-build.md](references/design-and-build.md). Build one self-contained HTML deck on a fixed 1920x1080 canvas with no slide-content reflow.
5. Add Edit Mode unless the user asks for a clean presentation-only file. Inject it only after the base deck works.
6. Run `scripts/inline_assets.py`, then `scripts/validate_deck.py`; fix every error.
7. Render and inspect the opening, one representative content slide, and the closing. Spot-check wide and narrow/tall viewports; scaling must remain uniform.
8. For the review round, deliver both validated HTML and a PDF proof. Do not publish yet.
9. After the user explicitly approves the final deck, regenerate the final PDF and publish the HTML to the presentations repository. Return the PDF and verified public link.

## Non-negotiable invariants

- Hebrew decks use `<html lang="he" dir="rtl">` and Paamon.
- Use one theme: blue by default, green only when requested.
- Use only layouts A-F. Split overloaded slides instead of inventing another layout.
- Supplied backgrounds already contain logo, footer, and decorative lines; never duplicate them in HTML.
- Use fixed opening speaker details and closing contact details from the brand reference.
- Author at 1920x1080 with fixed pixels. Scale `#presentation` uniformly inside `#stage`; do not reflow slide content for mobile.
- Keep navigation and Edit Mode chrome outside the scaled canvas where practical.
- Review approval and publication approval are separate. Never publish before explicit final approval, and never overwrite an existing slug without resolving that conflict with the user.
- Never request a long-lived personal access token in chat. Prefer an authorized GitHub connector or authenticated repository environment.

## Expected artifacts

- Review stage: validated self-contained HTML plus a PDF proof with one 16:9 slide per page.
- Final stage, after explicit approval: regenerated final PDF plus a verified GitHub Pages URL under an ASCII kebab-case slug ending in `-matzeget`.

Report what was built, what was visually checked, and any requested artifact that could not be produced.

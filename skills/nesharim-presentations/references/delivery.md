# Delivery and publishing

Create a lowercase ASCII kebab-case slug based on the main title and end it with `-matzeget`. Use it for HTML, PDF, repository folder, and public URL. Never use `-mitzeget` or Hebrew in a path.

## Review delivery

For every review round, deliver both:

- validated self-contained HTML;
- a PDF proof with one 1920x1080 slide per page, backgrounds enabled, and zero margins.

Inspect both artifacts. Do not publish a review version.

## Final delivery

After the user explicitly approves the finished deck, regenerate and inspect the final PDF, then publish the approved self-contained HTML. Return the final PDF and verified public URL. The HTML remains available at that URL; include the standalone file as well when useful or requested.

Publication uses the separate presentations repository, not the skill repository:

- Repository: `ggilboaa/presentation`
- Branch: `main`
- Path: `<slug>/index.html`
- URL: `https://ggilboaa.github.io/presentation/<slug>/`

Never overwrite root `index.html`. If a slug exists, disclose it and obtain confirmation before updating it. Prefer the connected GitHub integration or authenticated repository environment. Never ask for a long-lived PAT in chat. Verify the commit and, when possible, the public URL.

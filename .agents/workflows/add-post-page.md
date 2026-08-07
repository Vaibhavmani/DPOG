# /add-post-page

Add a new duty post to the app. Use this when a tenth post is issued, or when an existing post is split.

The whole point of the content model is that this workflow touches JSON and icons, not markup. If you find yourself editing a template to accommodate a new post, the data layer is wrong — stop and fix that instead.

1. Read Serena memories `core` and `conventions` before starting.
2. Confirm the new post's source text with the human — English and Hindi, plus key directives. Do not author either language yourself.
3. Add the post object to `content/content.json`. Required keys: `id`, `slug`, `icon`, and parallel `en` / `hi` objects each with `name`, `keyDirectives`, and `instructions`.
4. Verify the parity check passes: `en.instructions.length === hi.instructions.length`.
5. Add the icon to the icon set, matching the existing solid-fill line style in `DESIGN.md`. Single colour, no gradient.
6. Confirm the home grid renders the new tile without any template change. If it does not, report that as a defect in the data layer rather than patching the template.
7. Bump `meta.version` and set `meta.updated` to today.
8. Update the service worker cache version so existing installs pick up the new content instead of serving a stale nine-post cache.
9. Run `/verify-offline`.
10. Generate the QR code for the new route into `qr/`, matching the slug.
11. In the Walkthrough: note that a new printed card is required for the new post, and that the QR code has not been printed yet.

---
activation: Always On
---

# Frontend standards

## Stack limits

Vanilla HTML, CSS, and JavaScript. ES modules, no bundler required. A single `content/content.json` loaded at runtime. No React, Vue, Svelte, Tailwind build, or CSS-in-JS.

Pre-render the home page and all nine post pages as real HTML. JavaScript enhances — search, language toggle, offline — but the content must be readable with JS disabled.

## Performance budget — pass/fail

- HTML + CSS + JS combined: **under 100KB gzipped**, fonts excluded
- Interactive under 2.5s on Slow 4G with 4x CPU throttle
- Zero render-blocking third-party requests
- Fonts self-hosted, subset, `font-display: swap`

Report the actual gzipped total in every Walkthrough that changes shipped assets. An estimate is not a measurement.

## Styling

Every colour comes from the CSS custom properties in `DESIGN.md`. No literal hex values in component CSS. No colour outside that palette.

Watch selector specificity. It is easy to write a type-based selector and an element-based selector that cancel each other out, and it happens most often with section padding and margins. Keep specificity flat and predictable.

## Stitch exports are reference material

`docs/design-exports/` holds Stitch output. Read it for layout, spacing relationships, and visual structure. **Do not paste it into `src/`.**

Stitch emits Tailwind-classed markup and its output has documented accessibility gaps — insufficient contrast, undersized touch targets, missing ARIA attributes. Both conflict directly with this project's constraints. Reimplement from the design; do not adopt the markup.

Where a Stitch export and `DESIGN.md` disagree, `DESIGN.md` wins.

## Accessibility floor — pass/fail

- Contrast ≥ 7:1 on body text
- Touch targets ≥ 48x48px with 8px spacing
- Visible focus ring in `--alert-yellow`. Never `outline: none` without a replacement.
- Semantic HTML. `<nav>`, `<main>`, heading order without skips, `<ol>` for numbered instructions.
- `lang` attribute correct and updated when language toggles. `lang="hi"` on Devanagari content is required for both rendering and screen readers.
- Language toggle is a labelled `<button>` with `aria-pressed`
- Layout survives 200% zoom and OS text-size settings
- `prefers-reduced-motion` honoured

## Offline

- Service worker, cache-first for app shell, content JSON, and fonts
- Web app manifest: name, 192 and 512 icons, theme colour, `display: standalone`
- Offline indicator that is informative, not alarming, shown alongside the cached content's version stamp
- Cache versioning strategy that actually invalidates when `content.json` changes — a stale cache serving superseded instructions is the worst failure mode this app has

## Routing

Clean, deep-linkable paths — `/rooftop`, `/morcha`, `/machan`, `/vehicle-checking`, `/dfmd`, `/qrt`, `/xray`, `/cctv`, `/medical`. These slugs are fixed: printed QR codes point at them, so renaming one invalidates physical cards.

Language persists across navigation and across a full app restart.

## Testing

Test at 360px width first, not desktop. A layout that works at 1440px and breaks at 360px has failed; the reverse is merely inconvenient.

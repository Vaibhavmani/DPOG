# tech_stack

Vanilla HTML, CSS, and ES modules. No framework, no bundler, no Tailwind build, no CSS-in-JS.

## Why no framework

The payload budget is 100KB gzipped for HTML+CSS+JS combined. A framework runtime spends a large fraction of that before any project code exists, buys nothing for nine mostly-static pages, and complicates the JS-disabled requirement. This was a deliberate decision, not an oversight — see `mem:decisions`.

If a future session believes a framework is warranted, it must be argued in an Implementation Plan and approved by a human, not introduced mid-build.

## Composition

- Static HTML, pre-rendered for the home page and all nine post routes
- `content/content.json` — the single content source, loaded at runtime for search and language switching
- CSS custom properties for the entire palette; no hex literals in component CSS
- Service worker, cache-first for app shell, content, and fonts
- Web app manifest for install-to-home-screen

## Fonts

Self-hosted and subset. Archivo Condensed (display), Inter (Latin body), **Noto Sans Devanagari** (Hindi body). No Google Fonts CDN — it breaks offline and adds a render-blocking round trip.

Devanagari needs a larger line-height than Latin at the same size. Set it per script.

## Hosting

Any static host over HTTPS. HTTPS is required, not preferred: both service workers and phone QR scanners need it.

## Serena language server note

`html` and `scss` are experimental in Serena and are not auto-detected — they are listed explicitly in `.serena/project.yml`. `typescript` is the correct key for plain JavaScript. Expect symbol tools to work well on the JS modules and poorly on markup; read markup files directly rather than fighting the tooling.

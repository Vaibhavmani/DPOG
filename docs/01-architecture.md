# 01 — Architecture

## Shape

A pre-rendered static site with a runtime JSON content layer and a service worker. There is no server, no build-time framework, and no bundler requirement.

```
first visit                       later visits (any network state)
─────────────                     ────────────────────────────────
HTML from host                    service worker serves app shell
  ↓                                 ↓
CSS + fonts (self-hosted)         content.json from cache
  ↓                                 ↓
service worker registers          render, no network touched
  ↓
content.json cached
  ↓
all nine routes + both
languages pre-cached
```

The first visit is the only one that requires a network. Everything after it is cache-first by design, because the deployment context guarantees a congested network exactly when the app is needed.

## File layout

```
src/
  index.html              home — post picker
  rooftop/index.html      ─┐
  morcha/index.html        │
  machan/index.html        │
  vehicle-checking/…       ├─ nine pre-rendered post pages
  dfmd/…                   │
  qrt/…                    │
  xray/…                   │
  cctv/…                   │
  medical/index.html      ─┘
  search/index.html
  assets/
    css/app.css           all styles; tokens in :root
    js/
      content.js          loads and indexes content.json
      lang.js             language state + persistence
      search.js           substring search across both languages
      app.js              wiring
    fonts/                self-hosted, subset
    icons/                nine post icons + UI icons
  sw.js                   service worker
  manifest.webmanifest
  robots.txt

content/content.json      single content source
```

Post pages are pre-rendered rather than client-routed. This is what makes the JS-disabled requirement cheap instead of painful, and it means a QR scan lands on real HTML rather than a loading spinner over a slow connection.

## Routes

```
/                    home
/rooftop             Rooftop / Elevated Post
/morcha              Morcha / Barricade Point
/machan              Machan / Observation Post
/vehicle-checking    Vehicle Checking Team
/dfmd                DFMD / Access Control
/qrt                 Quick Reaction Team
/xray                X-Ray Baggage Scanner
/cctv                CCTV / Control Room
/medical             Medical / Ambulance
/search              search
```

**These slugs are frozen.** Ten printed QR codes point at them. Renaming one invalidates laminated cards already issued to duty points, which is a physical reprint, not a redeploy. Treat them as an external contract.

## Language

Language is a query parameter — `/morcha?lang=hi` — persisted to `localStorage` and applied on load. Pick one mechanism and keep it: a path prefix (`/hi/morcha`) is equally valid but doubles the pre-rendered page count and the QR code surface, so the query parameter is the cheaper choice here.

Rules:
- Default to English on first visit; honour the stored preference thereafter
- Persist across navigation and across a full app restart
- Update the `lang` attribute on the document when it changes
- Never render both languages simultaneously

## Search

Plain substring match across post names, key directives, and instruction text, in **both languages at once** — so "drone" and "ड्रोन" each return the rooftop result regardless of which language is currently displayed. No fuzzy matching library; nine posts and roughly seventy instruction lines do not need one, and a search library would consume a meaningful share of the payload budget.

Build the index once from `content.json` at load.

## Service worker

Cache-first for the app shell, `content.json`, fonts, and icons. Network-first for nothing — there is nothing here that benefits from freshness at the cost of availability.

**Cache invalidation is the risk that matters.** A cache that never updates will serve superseded operational instructions to someone standing at a post. Key the cache on `meta.version` from `content.json` so a version bump forces a refresh, and verify that path explicitly — it is step 10 of `/verify-offline` and the step most likely to be skipped.

Show an offline indicator alongside the cached version stamp so a reader always knows which revision they are looking at.

## Content model

```
meta
  title, directive, issuedBy      { en, hi }
  version, updated                 strings, rendered on every page
  controlRoom[]                    { label: {en,hi}, number }

posts[]
  id, slug, icon
  en / hi
    name
    keyDirectives[]                short imperatives, 3–4
    instructions[]                 full text, verbatim
```

Invariant, enforced by a build-failing check: `en.instructions.length === hi.instructions.length` for every post. A mismatch means a line was dropped in one language — the most likely content bug in this project, and nearly invisible by eye.

Adding a tenth post must require editing only `content.json` and adding an icon. If it requires a template change, the data layer is wrong.

## Performance budget

Under 100KB gzipped for HTML + CSS + JS combined, fonts excluded. Interactive under 2.5s on Slow 4G with 4x CPU throttle.

Fonts are the largest asset and are excluded from that figure precisely because they must be subset aggressively. Noto Sans Devanagari unsubset is large; subset to the glyphs actually present in `content.json` plus digits and punctuation.

## What is deliberately absent

No accounts, analytics, location tracking, CMS, admin panel, push notifications, incident reporting, duty rosters, or embedded PDF viewer. No external CDN, font host, or telemetry — this may run on a departmental network and every external request is both a privacy surface and an offline failure point.

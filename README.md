# Deployment Quick Instructions — Delhi Police

A bilingual (English / Hindi), offline-first web app providing quick instruction sets for police personnel deployed at 9 distinct duty posts. Officers scan a QR code at their duty post card and land directly on that post's instructions, with zero login and full offline access once loaded.

---

## Technical Stack & Architecture

- **Static Site Engine**: Pure HTML, CSS, Vanilla JS (No JS frameworks, no bundlers)
- **Design & Typography**: Self-hosted Noto Sans Devanagari & Inter fonts, custom high-contrast CSS (7:1 contrast ratio, 48px touch targets)
- **Offline Reliability**: Service Worker (v12.0) with offline fallback and pre-cached core assets
- **Security & Headers**: Vercel Edge Middleware for path access controls, restrictive Content Security Policy (CSP), anti-clickjacking (`DENY`), `nosniff`, and custom `Disallow` rules in `robots.txt`
- **Payload Budget**: ~87KB gzipped total shipped payload (under 100KB budget)

---

## Repository Structure

```
.agents/                      Agent guardrails, standards, and workflow rules
.serena/                      Serena project definitions and persistent memories
content/
  content.json                Single source of truth for all post instructions (EN/HI)
docs/
  01-architecture.md          System architecture, routing, and PWA strategy
  05-qa-and-acceptance.md     Verification protocols and browser testing criteria
qr/                           Vector SVG QR codes for all 9 posts + homepage
src/                          Deployed web assets
  assets/                     CSS, fonts, icons, and hero briefing photos
  cctv/ ... xray/             Public duty post pages (9 posts)
  search/                     Client-side substring search
  manifest.webmanifest        PWA manifest
  robots.txt                  Search engine crawler rules
  sw.js                       Offline service worker
AGENTS.md                     Cross-tool project guidelines and core constraints
DESIGN.md                     Design system contract and UI specification
build.py                      Build engine: validates invariants, pre-renders HTML, generates QR codes
middleware.js                 Vercel Edge Middleware (HTTP Basic Auth for internal routes)
vercel.json                   Vercel deployment configuration & security headers
README.md                     Repository documentation
```

---

## Internal Operations & Access Security

In addition to the 9 public duty-post instruction pages, the system includes two internal operational utility routes (Duty Shift Compliance Checklist and QR Card Reference).

- **Access Protection**: These endpoints are protected by Vercel Edge Middleware HTTP Basic Auth.
- **Obscured Routing**: Slugs for internal utilities are obfuscated for defense-in-depth and excluded from navigation and sitemaps.
- **Search Exclusions**: Explicit `Disallow` entries in `robots.txt` prevent search engine discovery.

---

## Build & Local Development

To pre-render all static pages and validate structural invariants:

```bash
python build.py
```

This validates line-by-line parity between English and Hindi instructions across all 9 posts, generates SVG QR codes, pre-renders HTML pages into `src/`, and verifies payload budget compliance (< 100KB gzipped).

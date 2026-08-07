# 05 — QA and acceptance

Two layers. The agent runs the first; a human must run the second. Neither substitutes for the other.

---

## Layer 1 — Agent verification (browser subagent)

Requires the Antigravity Chrome extension installed and permitted. Without it none of this works, so confirm it during setup rather than discovering it here.

Serve over `localhost` or HTTPS. A `file://` open silently skips service worker registration and makes every offline result meaningless.

### Per-change

- Load the affected page, exercise the interaction, screenshot into the Walkthrough
- Viewport at 360px, not desktop
- Compare against the corresponding Stitch screenshot in `docs/design-exports/screenshots/`

### Routing, content, or service worker changes

Run `/verify-offline` in full. The step that catches real bugs is the last one: bump `meta.version`, rebuild, confirm an existing install picks it up. A cache that never invalidates passes every other check and fails the only one that matters in the field.

### Bilingual changes

- Parity check across all nine posts
- Devanagari rendering verified against a conjunct-heavy string — anything containing `क्षेत्र` or `सुनिश्चित` — compared to a known-good screenshot. Fallback fonts are subtle at small sizes and easy to miss.
- Language persists across navigation and a full app restart

### Automated gates

- Gzipped HTML + CSS + JS under 100KB, fonts excluded. **Measured, not estimated** — state the number.
- Lighthouse mobile: Performance, Accessibility, Best Practices each ≥ 95
- Network panel shows zero external requests
- All ten routes render with JavaScript disabled

---

## Layer 2 — Human verification

The agent cannot do these. Do not sign off without them.

### On a real budget Android phone, outdoors, in daylight

This is the actual operating environment and no amount of simulated throttling substitutes for it.

- [ ] Every route readable at maximum screen brightness in direct sun
- [ ] Reachable and operable one-handed, thumb only
- [ ] Every tap target comfortably hittable without zooming
- [ ] Devanagari legible at arm's length

### QR codes

- [ ] All ten scan with the **built-in camera app** on both an iPhone and an Android. Not a third-party scanner app — that is not what anyone will use.
- [ ] Each lands on the correct route
- [ ] Test a printed code at final size, not just the code on a screen. Screen-to-screen scanning hides contrast and size problems that appear on paper.
- [ ] Plain URL printed beneath each code as a fallback

### Network reality

- [ ] Cold start on a genuinely congested connection, not simulated throttling. If possible, test at a busy location.
- [ ] Load once, enable airplane mode, walk away for an hour, return and navigate all nine posts in both languages
- [ ] Restart the phone while offline and reload

### Content sign-off — blocking

- [ ] **Every instruction line verified word-for-word against the source PDF by the issuing officer.** This is the single most important item on this page. The Hindi in `content.json` was transcribed and has not been through departmental review.
- [ ] Control Room numbers are real and the `tel:` link dials correctly on both platforms
- [ ] Version and updated date correct on every page, including offline
- [ ] No placeholder strings anywhere

### Policy sign-off — blocking

- [ ] Indexing policy confirmed. The app ships `noindex`; confirm the department wants it that way.
- [ ] Hosting location and dynamic-QR redirect ownership confirmed. Whoever controls the redirect controls what every printed card resolves to — that should be the department, not an individual's personal account on a free tier.

---

## Failure modes worth checking for specifically

These are the ones that pass casual testing and fail in the field.

| Failure | How it hides | How to catch it |
|---|---|---|
| Stale cache serving old instructions | Everything works, content is just wrong | Version-bump test, `/verify-offline` step 10 |
| Devanagari falling back mid-sentence | Looks almost right at small sizes | Screenshot comparison on mixed-script lines |
| Hindi line count drifting from English | Nothing errors, a line is simply absent | Parity check as a build failure |
| Service worker never registering | Works fine online, dies offline | Test over `localhost`, never `file://` |
| QR code decoding in a library but not a phone camera | Automated check passes | Scan the printed code with a real camera |
| Contrast passing WCAG AA but failing in sun | Lighthouse is green | Take the phone outside |
| Route slug renamed during refactor | Site works perfectly; printed cards do not | Slugs frozen in `mem:conventions` |

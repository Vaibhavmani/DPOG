# core

## What this project is

An offline-first, bilingual (English / Hindi) web app that replaces a printed nine-page PDF of duty instructions for a police deployment. A constable at a duty point scans a QR code on the laminated card at that post and lands directly on that post's instructions. No login, no PDF viewer, works in airplane mode after first load.

Nine duty posts: Rooftop, Morcha (barricade), Machan (observation), Vehicle Checking, DFMD (access control), QRT, X-Ray Baggage, CCTV/Control Room, Medical/Ambulance.

## The framing that resolves most decisions

This is not a document to read. It is a reference someone checks while standing at a post, outdoors, in sunlight, one-handed, on a saturated network. Every design and technical choice resolves toward: *can they find the right procedure in under fifteen seconds*.

When a trade-off is unclear, that sentence usually decides it.

## Non-negotiables

- Offline after first load — network at large gatherings is congested exactly when the app is needed
- 100KB gzipped budget, fonts excluded
- 7:1 contrast, 48px touch targets, 360px baseline viewport
- Hindi is first-class, in self-hosted Noto Sans Devanagari, never a system fallback
- Instruction text is verbatim — see `mem:conventions`

## Toolchain division

Stitch designs, Antigravity implements and verifies, Serena provides code semantics and this memory layer. Stitch output is reference material, never shipped code — it is Tailwind-classed and has accessibility gaps that violate the constraints above.

## Why Serena is in this project

Antigravity resets agent context between sessions. These memories are the only continuity that survives. On a codebase this small the symbol tools are a minor benefit; persistence is the real one. Read `mem:conventions` and `mem:decisions` before planning anything.

## Open items blocking sign-off

1. Control Room numbers are placeholders in `content/content.json`
2. Hindi text is transcribed from the source PDF and awaits line-by-line officer sign-off
3. `noindex` policy is defaulted on; the department has not formally confirmed it

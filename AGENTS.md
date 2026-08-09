# AGENTS.md

Project context for any agent working in this repository. Antigravity reads this at session start; it is also the cross-tool file for Claude Code, Cursor, and Codex if they are used.

## What this is

A bilingual (English / Hindi) offline-first reference web app holding nine duty-post instruction sets for a police deployment governed by **DPOG (Delhi Police Operational Guide) Strategies**. A constable at a barricade scans a QR code on the laminated card at that post and lands directly on that post's instructions. No login. No PDF. Works with the phone in airplane mode after first load.

This is an operational document, not a marketing site. Every decision resolves toward *can someone standing outside, in sunlight, on a congested network, find the right procedure in under fifteen seconds*.

## Non-negotiable constraints & DPOG Strategies

These override any competing instinct about what makes a good web app. See `docs/DPOG_STRATEGIES.md` for full implementation standards.

- **Offline is a feature, not an enhancement.** Network at a large public gathering is saturated. After one successful load, all nine posts in both languages must render with the device in airplane mode.
- **Payload budget: 100KB gzipped** for HTML + CSS + JS combined, excluding fonts. Any dependency over 20KB gzipped must be justified in the Implementation Plan before it is added.
- **Contrast target 7:1** on body text. This is read in direct sunlight, not in an office.
- **Touch targets minimum 48x48px** with 8px spacing. Read one-handed, possibly with gloves.
- **Hindi is a first-class language (DPOG Sizing Strategy):** Devanagari font rules are scoped to `.lang-hi` (0.92em font size) to match Inter bounding boxes, maintaining 100% identical component sizing and zero layout pop across English and Hindi.
- **Tactical 2-Phase Crossfade (DPOG Transition Strategy):** Synchronous button highlight with 80ms/40ms content crossfade and zero page scroll ratio jump.
- **Instruction text is verbatim.** See `.agents/rules/20-content-integrity.md`. Do not paraphrase, reorder, summarise, or "improve" any line.

## Baseline device

Design and test against: 360px viewport, budget Android, Slow 4G with 4x CPU throttle. Not a desktop browser at 1440px.

## Stack

Static site. Vanilla HTML/CSS/JS with a single `content/content.json`. No React, no Vue, no bundler-heavy framework, no Tailwind build step. Service worker for offline. Deployable to any static host over HTTPS.

If you believe a framework is warranted, argue it in the Implementation Plan artifact and wait for human approval. Do not introduce one mid-build.

## Out of scope — do not build

Accounts, login, analytics that identify individuals, location tracking, a CMS, an admin panel, push notifications, incident reporting, duty rosters, or an embedded PDF viewer. If a request seems to call for one of these, stop and ask.

## Content model

`content/content.json` is the single source of content truth. Nine posts, each with an `id`, `slug`, `icon`, and parallel `en` / `hi` objects. Nothing is hardcoded in markup or components. Adding a tenth post must require editing only the JSON.

Invariant: for every post, `en.instructions.length === hi.instructions.length`. Enforce this with a check that fails the build, not a comment.

## Design source

`DESIGN.md` is the design contract. Stitch generates against it; the implementation binds to it. Where a Stitch export and `DESIGN.md` disagree, `DESIGN.md` wins.

Stitch exports live in `docs/design-exports/` and are **reference material only**. Do not paste Stitch markup into `src/`. Stitch output is Tailwind-classed and has documented accessibility gaps that violate the constraints above.

## Verification

A task is not done because the code was written. It is done when the browser subagent has loaded the page, exercised the interaction, and the screenshot matches the design. See `docs/05-qa-and-acceptance.md`. Include the offline check — a build that passes online and fails in airplane mode has failed.

## Safety

- Never commit the Stitch API key, any Control Room phone number placeholder replacement, or any `.env` file.
- Never run destructive git operations (`reset --hard`, `push --force`, branch deletion) without explicit human confirmation in the same turn.
- Never modify `content/content.json` instruction text. Structural edits to the JSON are fine; the strings are not yours to change.
- This repo may end up on a departmental network. Do not add third-party CDN references, external font loads, telemetry, or analytics beacons.

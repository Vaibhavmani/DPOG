---
activation: Always On
---

# Project guardrails

## Scope discipline

Build only what `AGENTS.md` lists as in scope. If a task seems to require accounts, analytics, a CMS, an admin panel, location tracking, push notifications, or an embedded PDF viewer, stop and ask rather than building it. These were excluded deliberately, not by oversight.

## Plan before you build

Produce an Implementation Plan artifact before touching `src/`. Use `docs/03-implementation-plan.md` as the seed, not as the finished plan — restate it in your own structure, check it against the current state of the repo, and surface anything in it that no longer holds.

Every Implementation Plan for this project must contain, in addition to your normal sections:

- **Payload impact** — bytes added by this change, and the running total against the 100KB budget
- **Offline impact** — what changes in the service worker, and what must be re-cached
- **Bilingual impact** — whether this touches Hindi rendering, and how it was checked

If a plan cannot fill those three sections honestly, it is not ready for review.

## Verification is part of the task

A task is not complete because the code compiles or the file was written. It is complete when the browser subagent has loaded the affected page, exercised the interaction, and the result matches the design. Screenshots go in the Walkthrough artifact.

Every Walkthrough must state the result of the airplane-mode check for any change that touched routing, content loading, or the service worker. "Works online" is not a result.

## Never do these without asking

- Introduce a framework, bundler, or dependency over 20KB gzipped
- Add a third-party CDN reference, external font load, analytics beacon, or telemetry of any kind
- Run `git reset --hard`, `git push --force`, or delete a branch
- Modify instruction strings in `content/content.json`
- Commit an API key, credential, or `.env` file
- Change the `noindex` meta tag or `robots.txt` policy

## Working state

Start editing tasks from a clean git state so the diff is legible and you can inspect your own changes with `git diff`. If the tree is dirty when you begin, say so rather than building on top of unexplained changes.

## When you are stuck

Say so and stop. Do not substitute a simpler thing that looks similar — a stubbed language toggle, a hardcoded post list, a placeholder that renders but is not wired to `content.json`. A visibly incomplete build is recoverable; a build that looks finished and is subtly hollow is not.

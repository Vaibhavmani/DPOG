# decisions

Decisions already made and argued. Reopening one requires a reason that is new, not a preference.

## No framework

Rejected React/Vue/Svelte. The 100KB gzipped budget is spent largely on runtime before any project code exists, nine mostly-static pages get no benefit from a virtual DOM, and the JS-disabled requirement becomes awkward. See `mem:tech_stack`.

## Stitch output is not shipped

Rejected pasting Stitch's HTML export into `src/`. Stitch emits Tailwind-classed markup and its output has documented accessibility gaps — contrast, touch target sizing, missing ARIA. Both conflict with this project's floor. Stitch is a design source; the implementation is written against `DESIGN.md`.

## No photographs

The printed card uses photographs of personnel at each post because it is a poster read at distance. On a phone they cost payload and scroll length and buy nothing. Replaced with solid-fill line icons.

## Language toggles, never stacks

Rejected showing English and Hindi together. Doubling scroll length on a 360px screen is the exact failure the printed PDF already has on a phone, and it is the thing this app exists to fix.

## Ten QR codes, not one

Rejected a single code pointing at the home page. Each duty point gets a code pointing directly at its own route, printed on the card issued at that post, so a constable at a barricade navigates zero screens. Dynamic short URLs are used so the destination can be repointed without reprinting physical cards.

Consequence: route slugs are now an external contract. See `mem:conventions`.

## noindex by default

The app ships with `noindex` and a `robots.txt` disallow: reachable by anyone who scans, absent from public search results. This is a default pending departmental confirmation, not a settled policy. One-line change either way. Do not flip it without written human instruction.

## Onboarding disabled in Serena

`.serena/memories/` was hand-seeded rather than derived by Serena's onboarding pass, and `no-onboarding` is set in `project.yml`. The hand-written memories carry reasoning that an automated pass over an empty `src/` could not have produced. Do not re-run onboarding and overwrite them.

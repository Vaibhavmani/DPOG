# conventions

## Content is verbatim

Instruction strings in `content/content.json` are reproduced exactly. Never paraphrase, reorder, shorten, merge, or correct them.

This includes text that reads as an error. The source says "dickiey" and "the staff should not leave the rooftop dominance". Reproduce both. If a line looks wrong, flag it for human review in the Walkthrough — do not fix it.

Abbreviations stay as written: I/C, AoR, DFMD, HHMD, UVSS, QRT, SOP, PTZ, VEHISCAN, NSG, SWAT. No expansion, no casing changes, no explanatory tooltips.

## Hindi handling

- Self-hosted Noto Sans Devanagari, never a system fallback. Font load failure is a build failure.
- Hindi strings contain embedded Latin fragments — `I/C Roof Top`, `Control Room North District`, `visual Anti-Sabotage check`. These are in the source and stay. The font stack must render mixed-script lines without falling back mid-sentence.
- `lang="hi"` on Hindi content, updated when the toggle changes.
- Never author new Hindi copy. If a UI string needs Hindi that is not in `content.json`, flag it for human translation.

## Structural invariants

- `en.instructions.length === hi.instructions.length` for every post. Enforced by a build-failing check.
- Every post has a `slug` matching its route
- `keyDirectives` non-empty in both languages
- `meta.version` and `meta.updated` render on every page, including offline

## Route slugs are frozen

`/rooftop`, `/morcha`, `/machan`, `/vehicle-checking`, `/dfmd`, `/qrt`, `/xray`, `/cctv`, `/medical`.

Printed QR codes point at these. Renaming one invalidates physical laminated cards already issued to duty points. Treat them as an external contract, not an implementation detail.

## Colour and type

Every colour from the CSS custom properties in `DESIGN.md`. No hex literals in component CSS. Yellow appears at most twice per screen; red is reserved for the standing directive strip and the Control Room action only.

## Language is a toggle, never a stack

Do not render English and Hindi on the same screen simultaneously. That doubles scroll length and is the printed card's main failure mode on a phone.

## Testing order

360px first, desktop second. A layout that works at 1440px and breaks at 360px has failed.

---
activation: Always On
---

# Content integrity

This app carries operational duty instructions. Text errors here are not cosmetic bugs.

## Instruction text is verbatim

Do not paraphrase, summarise, reorder, shorten, split, merge, or otherwise improve any instruction string in `content/content.json`. Render exactly what is there.

This includes text you believe is grammatically wrong. The source document says "dickiey" and "the staff should not leave the rooftop dominance." Reproduce it. If you think a line is an error, note it in the Walkthrough for human review — do not fix it yourself.

## Abbreviations stay as written

`I/C`, `AoR`, `DFMD`, `HHMD`, `UVSS`, `QRT`, `SOP`, `PTZ`, `VEHISCAN`, `NSG`, `SWAT`. Do not expand, standardise casing, or add tooltips explaining them. The audience knows them; the source uses them.

## Hindi

- Devanagari renders in self-hosted Noto Sans Devanagari. Never a system fallback. If the font fails to load, that is a build failure, not a graceful degradation.
- Hindi strings contain embedded Latin fragments — `I/C Roof Top`, `Control Room North District`, `visual Anti-Sabotage check`, `SOP`. These are in the source and stay. Do not translate them, do not strip them, and make sure your font stack renders mixed-script lines without falling back mid-sentence.
- Set line-height per script. Devanagari needs more leading than Latin at the same size.
- Set `lang="hi"` on Hindi content.

## Structural invariant

For every post, `en.instructions.length === hi.instructions.length`. Enforce this with a check that fails the build. A mismatch means a line was dropped in one language, which is the single most likely content bug in this project and the hardest to notice by eye.

Also assert that every post has a `slug` matching its route and that `keyDirectives` is non-empty in both languages.

## Version stamp

`meta.version` and `meta.updated` appear on every page, including offline. Someone reading cached content must be able to tell which revision they are looking at. This is not decoration.

## Placeholders block deployment

`content.json` contains `REPLACE-WITH-REAL-NUMBER` for the Control Room. The build may proceed with it. The deploy may not. Fail `/ship` if any placeholder string remains.

## The Hindi has not been signed off

The Hindi in `content.json` was transcribed from the source PDF and is pending line-by-line verification by the issuing officer. Treat it as provisional. If you generate any new Hindi string for any reason — an error message, an empty state, a button label — flag it explicitly in the Walkthrough as requiring review. Never quietly author Hindi copy.

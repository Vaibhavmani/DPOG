# task_completion

A task is not done when the code is written. Work through this before reporting completion.

## Always

1. The browser subagent has loaded the affected page and exercised the interaction — not just confirmed the file was written
2. Screenshot in the Walkthrough
3. Checked at 360px viewport, not only desktop
4. No colour literals introduced outside the `DESIGN.md` custom properties
5. `git diff` reviewed by you before you report

## If the change touched routing, content loading, or the service worker

6. Run the `/verify-offline` workflow in full
7. Including the last step — bump `meta.version`, rebuild, confirm an existing install picks it up. A cache that never invalidates serves superseded operational instructions, which is the worst failure this app has.

## If the change touched shipped assets

8. Measure the gzipped HTML+CSS+JS total and state the real number against the 100KB budget. An estimate is not a measurement.

## If the change touched content or bilingual rendering

9. Parity check passes for all nine posts
10. Devanagari renders in the real font — verify on a conjunct-heavy string such as one containing "क्षेत्र" or "सुनिश्चित", compared against a known-good screenshot
11. Language toggle persists across navigation and a full app restart

## If the change touched anything a user taps

12. Touch targets ≥ 48x48px with 8px spacing
13. Contrast ≥ 7:1 on body text
14. Visible focus ring in `--alert-yellow`
15. Keyboard navigable

## Before reporting

Write a memory if this task resolved something a future session would otherwise rediscover — a rejected approach, a non-obvious constraint, a convention established mid-build. Do not write memories for routine progress; that is what the Task List artifact is for.

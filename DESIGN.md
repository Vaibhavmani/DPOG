# DESIGN.md

The design contract. Stitch generates against this; the implementation binds to it. Where a Stitch export and this file disagree, this file wins.

## Direction

The reference object is the printed briefing card that this app replaces: a navy header band, the department emblem, a red standing-directive strip, instructions in bordered blocks. The app should feel like the digital form of that same issued object — official, legible, unfussy. Not a consumer app. Not a marketing page.

Restraint is the default. One element is allowed to be bold; everything else stays quiet.

## Colour tokens

Declare these as CSS custom properties on `:root`. No colour outside this list appears anywhere in the app.

```css
--navy-deep:    #0B1F6B;  /* header bands, primary surfaces */
--navy-ink:     #071543;  /* deepest text tone */
--signal-red:   #D62027;  /* standing directive strip, Control Room action — nothing else */
--alert-yellow: #FFD100;  /* the single accent; also the focus ring */
--khaki:        #C8B187;  /* dividers, inactive states */
--paper:        #F7F5F0;  /* page background */
--white:        #FFFFFF;
```

**Yellow is scarce by rule.** On the printed card it is the colour of one word. In the app it marks the single most important thing on a screen, and the keyboard focus ring. If yellow appears more than twice on one screen, something is wrong.

**Red is reserved** for the standing directive strip and the Control Room call action. It is never a border, never a hover state, never an icon fill.

## Typography

| Role | Face | Notes |
|---|---|---|
| Display / post titles | Archivo Condensed (or Barlow Condensed) | Uppercase for post titles only |
| Body, Latin | Inter | |
| Body, Devanagari | **Noto Sans Devanagari** | Non-negotiable, self-hosted |
| Numerals in lists | Inter, tabular figures | |

Self-host every face. No Google Fonts CDN, no external font request — it breaks offline and adds a render-blocking round trip.

Set line-height per script, not globally: Devanagari needs more leading than Latin at the same size. Verify conjuncts and matras render correctly at every weight you ship.

**Sizes.** Body 17px minimum. Key directives 20px or larger. Nothing below 15px anywhere in the app, including the version stamp. No font weight under 400. No opacity-reduced text.

## Layout

**Home.** Masthead (emblem, title, standing directive strip) → language toggle → search field → 2-column grid of nine post tiles. Tiles minimum 88px tall, each carrying an icon, the post name, and its shortest key directive. Three or four columns from tablet up.

**Post detail.** Back button → navy title band → key directives block (the visually heaviest element on the page; this is what gets read in five seconds) → numbered instruction list → inline language switch → Control Room action → version stamp.

Do **not** stack English and Hindi on the same screen. That doubles scroll length and is the printed card's main failure on a phone. Language is a toggle.

**Persistent.** A fixed bottom Control Room bar on every screen.

## Signature element

The fixed bottom **Control Room bar** — red, always present, thumb-reachable. It is the one thing this app does that a printed card cannot. It is allowed to be the most confident element in the design. Everything else stays disciplined.

## Iconography

Nine post icons, solid-fill line style, single colour, no gradients. Drawn from the equipment and vocabulary of each post: a building silhouette with a sightline for Rooftop, a barricade for Morcha, a raised platform for Machan, a vehicle with an inspection mirror for Vehicle Checking, a door-frame arch for DFMD, a response vehicle for QRT, a scanned bag for X-Ray, a monitor wall for CCTV, an ambulance cross for Medical.

## What must not appear

Stock photography. Hero images of personnel. Gradients. Glassmorphism. Nested card shadows. Illustration. Decorative dividers. Numbered `01 / 02 / 03` eyebrows on anything that is not an actual ordered sequence.

The printed card uses photographs because it is a poster and a photograph carries at three metres. On a phone at arm's length they cost payload and scroll length and buy nothing. Icons instead.

## Motion

A fast page transition and a pressed state on tiles. Nothing else. Honour `prefers-reduced-motion`.

## Accessibility floor

Not aspirational — these are pass/fail.

- Contrast ≥ 7:1 on body text
- Touch targets ≥ 48x48px, 8px minimum spacing
- Visible focus ring in `--alert-yellow`, never `outline: none`
- Semantic HTML: `<nav>`, `<main>`, heading order without skips, `<ol>` for numbered instructions
- `lang` attribute correct and updated when the language toggles
- Language toggle is a labelled button with `aria-pressed`, not a bare icon
- Layout survives 200% zoom and the OS text-size setting
- Home and all nine post pages render with JavaScript disabled

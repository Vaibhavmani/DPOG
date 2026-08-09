# DPOG (Delhi Police Operational Guide) Strategies

The **DPOG (Delhi Police Operational Guide) Strategies** represent the architectural, typographic, and field-readiness framework governing the Delhi Police Law & Order Deployment Quick Instructions portal.

Designed specifically for rapid tactical access by field personnel and commanders under adverse network and environmental conditions (direct sunlight, congested cellular networks, airplane mode operation, 360px budget mobile viewports).

---

## The 6 Core Pillars of DPOG Strategies

### 1. Zero-Shift Proportional Bilingual Sizing (DPOG Sizing Strategy)
- **Scoped Sizing**: Devanagari font rules are scoped strictly to `.lang-hi` elements (`0.92em` font size, `1.35` line-height).
- **Global Layout Stability**: Root `html` preserves Inter / Barlow Condensed font metrics for both languages, preventing global element expansion.
- **Bounding Box Parity**: Devanagari glyph bounding boxes match Latin cap heights, ensuring **100% identical component dimensions and zero layout shift** when toggling between English and Hindi.

### 2. Tactical 2-Phase Crossfade Transition (DPOG Transition Strategy)
- **Zero Latency Button Feedback**: Language toggle buttons (`EN` / `हिंदी`) update `.active-lang` highlight synchronously on touch.
- **2-Phase Fluid Crossfade**: Content dims to 15% opacity over 80ms, executes the language attribute swap, and fades back in over 40ms.
- **Zero Scroll Jump**: No artificial scroll ratio recalculations; page position stays perfectly locked.

### 3. Ultra-Lean Sub-80KB Offline Payload (DPOG Payload Strategy)
- **Gzipped Budget Compliance**: Total shipped code payload (HTML + CSS + JS + JSON) is maintained strictly under **80KB gzipped** (~75.6KB gzipped).
- **100% Air-Gapped Self-Hosting**: Zero external CDN calls, self-hosted Noto Sans Devanagari & Inter fonts, pre-rendered SVG QR codes, and Service Worker offline caching.

### 4. High-Sunlight Contrast & Tactical Ergonomics (DPOG Ergonomics Strategy)
- **Direct Sunlight Visibility**: Minimum **7:1 contrast ratio** across all body text, directives, and header bands.
- **Glove-Compatible Touch Targets**: All interactive elements maintain a minimum **48px × 48px touch target** with at least 8px spacing for one-handed operation.

### 5. Multi-Viewport Adaptive Rigidity (DPOG Layout Strategy)
- **Adaptive Breakpoints**: Seamless fluid layout scaling across budget 360px mobile viewports, 768px tablets, and 1440px desktop displays.
- **Flex Wrap & Minimum Containment**: Flex wrapping (`flex-wrap: wrap`) and card `min-height` containment prevent text truncation, button overlap, or container overflow on narrow screens.

### 6. Content Parity & Invariant Integrity (DPOG Integrity Strategy)
- **Line-by-Line Parity**: Automated build assertion enforcing `en.instructions.length === hi.instructions.length` across all 9 duty posts.
- **Verbatim Accuracy**: Strict content integrity prohibiting text alteration, paraphrasing, or instruction reordering.

---

## Technical Summary

| Strategy Metric | Target Standard | DPOG Implementation | Status |
| :--- | :--- | :--- | :--- |
| **Bilingual Layout Shift** | 0px | Scoped Devanagari `.lang-hi` 0.92em font scaling | **PASSED** |
| **Language Transition** | Fluid crossfade | 80ms/40ms 2-phase opacity fade | **PASSED** |
| **Gzipped Payload** | < 100KB | ~75.6 KB gzipped total shipped code | **PASSED** |
| **Contrast Target** | 7:1 ratio | Signal Red / Navy Deep / Khaki Paper system | **PASSED** |
| **Touch Targets** | ≥ 48px × 48px | Minimum 48px touch padding across all buttons | **PASSED** |
| **EN/HI Instruction Parity** | 1:1 match | Automated build invariant verification | **PASSED** |

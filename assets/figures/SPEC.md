# Figure spec — hand authored inline SVG

Every figure is one file: `assets/figures/<id>.svg`, containing a bare `<svg>` element and nothing
else (no XML prolog, no doctype, no comments outside the svg). The build inlines it into the page.

## Hard rules

1. **Depict a mechanism, not a label.** A box that says "boycott" is worthless. The five professional
   edges that one ethical clause severs is a figure. If a sentence says it faster, the figure should
   not exist.
2. **Theme safe.** Strokes, text and arrowheads use `currentColor` so the drawing inherits the page
   foreground in light and dark. You may use these CSS custom properties for meaning, and each has a
   fallback baked in via `var(--x, #hex)`:
   - `var(--fig-accent, #a95a22)` the one element the argument turns on
   - `var(--fig-brand, #0f5f66)` the supported or surviving path
   - `var(--fig-warn, #b4423a)` the blocked, failed or refuted path
   - `var(--fig-mute, #8a939e)` de emphasized scaffolding
   Never fill a large area with a solid dark or solid light color, because it will invert badly.
   Fills for shapes should be `none`, or `var(--fig-fill, rgba(127,127,127,.08))` which reads on
   both grounds.
3. **Sizing.** `viewBox="0 0 W H"` chosen for the content. Add `role="img"` and an `aria-label`
   carrying the figure's claim. Do not set width or height attributes; CSS handles it.
4. **Text.** Font size 12 to 15 in viewBox units at a drawn width of about 720. Use
   `font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif"` on a wrapping `<g>`.
   Short labels only. Explanation goes in the caption, which lives in the chapter markup, not here.
5. **Arrows.** Use a `<defs><marker>` with an id **prefixed by the figure id** so two inlined
   figures on one page cannot collide: `id="arrow-cn8"`, referenced as `marker-end="url(#arrow-cn8)"`.
   Every id in the file must carry that prefix.
6. **Label the arrows.** `impinges`, `no path`, `severed by Principle 3`. An unlabeled arrow means
   "related somehow".
7. **Self contained.** No `<script>`, no `<style>`, no `<foreignObject>`, no external images, no
   web fonts. Gradients and markers reference ids inside the same file.
8. **No hyphens and no em dashes in any visible text.** House rule. Write "1907 to 1974",
   "head to head", "non musculoskeletal". Hyphens inside id attributes are fine.
9. **Align to a grid.** Even gaps and shared baselines. Eyeballed offsets read as noise.
10. Target width 720 viewBox units unless the content genuinely needs more. Height whatever the
    content needs, usually 280 to 460.

## Worked example — the shape to copy

`assets/figures/fig-antitrust-choice.svg`

<svg viewBox="0 0 720 300" role="img" aria-label="Two possible legal routes: a defamation claim would have required the court to rule on whether chiropractic works, while the antitrust claim routed around that question entirely.">
  <defs>
    <marker id="arrow-antitrust" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="arrow-antitrust-warn" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--fig-warn, #b4423a)"/>
    </marker>
  </defs>
  <g font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="13">
    <rect x="16" y="118" width="150" height="64" rx="8" fill="var(--fig-fill, rgba(127,127,127,.08))" stroke="currentColor"/>
    <text x="91" y="145" text-anchor="middle" font-weight="600">Chiropractors</text>
    <text x="91" y="164" text-anchor="middle" fill="var(--fig-mute, #8a939e)">shut out of practice</text>

    <path d="M170 138 L 300 86" stroke="var(--fig-warn, #b4423a)" fill="none" marker-end="url(#arrow-antitrust-warn)"/>
    <text x="212" y="104" font-size="12" fill="var(--fig-warn, #b4423a)">defamation</text>

    <path d="M170 162 L 300 214" stroke="var(--fig-brand, #0f5f66)" fill="none" marker-end="url(#arrow-antitrust)" stroke-width="2"/>
    <text x="206" y="200" font-size="12" fill="var(--fig-brand, #0f5f66)">antitrust</text>

    <rect x="304" y="54" width="196" height="66" rx="8" fill="none" stroke="var(--fig-warn, #b4423a)" stroke-dasharray="5 4"/>
    <text x="402" y="80" text-anchor="middle" font-weight="600" fill="var(--fig-warn, #b4423a)">Is the claim true?</text>
    <text x="402" y="99" text-anchor="middle" font-size="12" fill="var(--fig-mute, #8a939e)">court must judge the science</text>

    <rect x="304" y="182" width="196" height="66" rx="8" fill="var(--fig-fill, rgba(127,127,127,.08))" stroke="var(--fig-brand, #0f5f66)"/>
    <text x="402" y="208" text-anchor="middle" font-weight="600">Was trade restrained?</text>
    <text x="402" y="227" text-anchor="middle" font-size="12" fill="var(--fig-mute, #8a939e)">court judges conduct only</text>

    <path d="M504 215 L 610 215" stroke="var(--fig-brand, #0f5f66)" fill="none" marker-end="url(#arrow-antitrust)" stroke-width="2"/>
    <rect x="614" y="186" width="92" height="58" rx="8" fill="none" stroke="var(--fig-brand, #0f5f66)"/>
    <text x="660" y="212" text-anchor="middle" font-weight="600">Wilk</text>
    <text x="660" y="230" text-anchor="middle" font-size="12">1987</text>

    <text x="504" y="88" font-size="12" fill="var(--fig-mute, #8a939e)">route not taken</text>
  </g>
</svg>

Notice what makes it a comparison rather than an option list: both routes leave the same box, and
the reader can point at the single question each route forces a court to answer.

# Making a figure interactive

Every diagram is enhanced by one shared runtime, `assets/figures/figures.js` with
`assets/figures/figures.css`. You never write JavaScript in an SVG. You declare what the diagram can
do with data attributes and the runtime builds the controls.

**Progressive enhancement is the rule.** With scripting off, the SVG must still render complete and
readable, exactly as it does today. The runtime only ever hides things after it has loaded.

## The three patterns

### 1. Steps — reveal the mechanism in the order the argument needs it

On the `<svg>` element:

```
data-steps='["What step one shows and why it matters.","Step two.","Step three."]'
```

Each string is the sentence the reader sees while that step is current. Write them as prose that
carries the argument, not as labels. Two to five steps. More than five and nobody clicks to the end.

On elements inside:

```
data-step="2"              appears when step 2 is reached and stays visible afterwards
data-step="2" data-only="" visible only while step 2 is current, then hidden again
data-step="3" data-pulse="" arrives with an attention pulse. Use once or twice per figure, on the
                            element the step is actually about.
```

An element with no `data-step` is always visible. Use that for the frame: titles, axes, the
background structure the reader needs from the start.

A "Show all" control is added automatically, so a reader who does not want to click through can see
the finished drawing in one press.

### 2. Layers — let the reader switch between alternatives

On the `<svg>`:

```
data-layers='[{"k":"a","label":"Defamation route","note":"What this route forces a court to decide."},
              {"k":"b","label":"Antitrust route","note":"What this one asks instead."}]'
```

On elements: `data-layer="a"`. Elements without `data-layer` stay visible in every layer. `note` is
optional and appears in the readout when that layer is chosen.

Use layers where the figure genuinely compares two things: before and after, route taken and route
not taken, one model against another. Do not use layers to hide clutter.

### 3. Hotspots — the detail that does not fit on the drawing

On any element:

```
data-hot="Short title" data-tip="One or two sentences of the thing this part is actually worth."
```

The runtime makes it focusable, gives it a keyboard role, adds an aria-label from the two strings,
and shows the text in a readout under the diagram on hover, focus or tap. Clicking pins it.

Three to eight hotspots per figure. Put them on the parts a student would point at and ask "what is
that". The `data-tip` should say something the caption does not.

**Put the hotspot on a `<g>` that wraps everything the reader would point at**, not on a lone shape.
A bare `<circle>` with a numeral drawn on top of it is unhoverable, because the numeral swallows the
pointer. Group the shape, its number and its label together and put `data-hot` and `data-tip` on the
group:

```xml
<g data-step="1" data-hot="referral out" data-tip="A physician sending a patient to a chiropractor.">
  <circle cx="168" cy="112" r="9" fill="none" stroke="currentColor"/>
  <text x="168" y="116" text-anchor="middle" font-size="12">1</text>
  <text x="186" y="104" font-size="12">referral out</text>
</g>
```

Grouping is also how you give several elements one shared `data-step`.

## Rules

- **Steps and layers can be combined**, but not on the same elements. If a figure has both, keep the
  layer switch about *what is being shown* and the steps about *the order it appears in*.
- **Every figure must end up complete.** Test the last step, and test "Show all".
- **No hyphens, no en dashes and no em dashes** in any `data-steps`, `data-hot`, `data-tip`, `label`
  or `note` string. They are read by students. Write "1907 to 1974", "head to head".
- **Attributes must be XML valid**: write `data-pulse=""` and `data-only=""`, never bare.
- **Do not restructure the drawing.** Add attributes, group existing elements where you must, and
  leave the geometry alone. If you need to wrap several elements in one `<g>` to give them a shared
  step or hotspot, that is fine and often the tidiest way.
- **The aria-label on the `<svg>` stays** and must still describe the finished figure.

## Worked example

`fig-boycott.svg` is fully annotated. It uses four steps (the five ordinary connections, the clause
arriving, the five cuts landing together, the tally) and six hotspots (one per connection plus
Principle 3). Read it before annotating anything else.

## What the reader sees

One readout line sits under the diagram. Steps and layers write the current narration into it;
hovering or focusing a hotspot temporarily replaces that narration and releasing restores it;
clicking a hotspot pins it until the reader clicks away. You do not manage any of that. Just write
good sentences.

## Check your work

```bash
python3 /root/chiro-history/assets/figures/check-interactive.py
```

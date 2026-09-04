# The Spine You Will Touch

The companion text for **HOH 3015: Chiropractic History, Theory, and Practice**, Vermont State
University, VTSU Online. Seven chapters, one for each week of a seven week session. It is the
required reading for the course and it replaces a purchased textbook, so it costs students nothing.

**[Read it online](https://kashee12345.github.io/hoh3015-companion-text/)** &middot;
**[Download the PDF](HOH3015_Companion_Text.pdf)** (127 pages)

Akash Garg, D.C.

---

## The chapters

| | Chapter | Week | Course objective |
|---|---|---|---|
| 01 | Origins and First Principles | One | Explore the history and core principles of chiropractic care |
| 02 | The Spine You Will Touch | Two | Understand the structure and function of the spine in chiropractic theory |
| 03 | The Art of Technique | Three | Compare various chiropractic techniques and the evidence for its efficacy |
| 04 | Becoming One | Four | Discover what it takes and what it is like to be a chiropractor |
| 05 | In the Clinic | Five | Review various clinical applications of chiropractic |
| 06 | Alongside Everyone Else | Six | Explore integrating chiropractic care with other healthcare modalities |
| 07 | What You Do With This | Seven | All six |

About 59,000 words and 32 diagrams.

## What is different about it

**The diagrams are interactive.** Anatomy is spatial and a flat picture fights that. Nineteen figures
step through a mechanism one link at a time, six switch between layers so you can compare cervical
against lumbar on the same drawing, and 172 hotspots carry a sentence each. All of it is hand drawn
SVG with no drawing library, and every figure still renders complete and readable with scripting off.

**It says where the evidence stops.** Every factual claim traces to a reference file built before a
word of prose was written, with a source and a check date on each entry. Where that file could not
verify something, the book does not state it. So the text says out loud that it will not give a
number for thrust excursion because none could be sourced, and will not repeat a casualty count on
secondhand authority in either direction. Where the record is genuinely contested, all sides are
presented and none is chosen. The 1895 founding story gets three incompatible accounts side by side
with no verdict.

**It is written by a practitioner.** Not a defence and not a debunking. A course that leaves a future
chiropractor ashamed of the field has failed, and so has one that leaves them unable to answer a
skeptic.

## Reading it

`index.html` is one self contained file. Open it from disk, drop it in a learning management system,
or serve it from GitHub Pages. No build step, no server, no dependencies, no tracking. Your place is
saved in your own browser and nowhere else.

- Click a vertebra on the cover to open that chapter
- Arrow keys turn pages, `c` opens the contents
- Click any diagram to open it large
- The A buttons change the text size

## Building it

Everything is generated from the sources in this repository.

```
python3 make-cover.py     # draws cover.svg, the spine whose vertebrae are the contents
python3 build.py          # src/ch-0N.html + assets/figures/*.svg  ->  index.html
python3 build-print.py    # the same chapters laid out for US Letter -> print.html
```

The PDF is produced by rendering `print.html` in headless Chromium at Letter size.

| Path | What it is |
|---|---|
| `src/ch-01.html` … `ch-07.html` | The chapters, as HTML fragments |
| `src/FACTS.md` | The verified reference file every claim traces to |
| `src/BRIEF.md` | The authoring brief: voice, structure, house rules, chapter scope |
| `assets/figures/*.svg` | The 32 diagrams, one file each, hand authored |
| `assets/figures/SPEC.md` | How a figure is drawn |
| `assets/figures/INTERACTIVE.md` | The data attribute runtime: steps, layers, hotspots |
| `assets/figures/figures.js` | The one shared script that builds every figure control |
| `template.html` | The reader shell |

`python3 assets/figures/check-interactive.py` validates the figure set.

## House rules

Two conventions run through the whole text and are checked automatically.

**No hyphens, en dashes or em dashes in visible prose.** The book writes "high velocity low
amplitude", "non musculoskeletal", "1963 to 1975". Where a quotation contains one, the book says so
rather than silently altering the quoted wording.

**Straight apostrophes and quotes only.**

## License

The prose and diagrams are the author's own work. The text is provided for students of this course
and for anyone who finds it useful for teaching. Please credit it if you use it.

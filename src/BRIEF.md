# The companion text — authoring brief

The book is the required reading for HOH 3015 Chiropractic History, Theory, and Practice at Vermont
State University, session 7B, October 19 to December 6, 2026. It replaces a purchased textbook, so
it has to carry the whole reading load by itself. Seven chapters, one per week.

The instructor is a licensed Doctor of Chiropractic who also holds an M.S. in pharmacology. The book
is written in his voice. That voice is the whole point: a practitioner explaining his own field to
students who mostly have no background, without defending it and without sneering at it.

## The audience

Undergraduates in a Holistic Health program. Most have no science background. Some are heading for
chiropractic school and are reading this to find out whether they want the life. Some are curious.
A few will be skeptical from the first page. Write so all four finish the chapter.

Assume nothing. If you use a word like proprioception or kappa or cavitation, define it in the
sentence where it first appears, in plain language, without a parenthetical that reads like a
glossary entry.

## The voice

Write the way a good teacher talks when he respects the room. Concretely:

- **First person is allowed and encouraged** where the instructor's own clinical experience earns
  it. "I have had this conversation with a parent more times than I can count" is better than "the
  practitioner may encounter parental concern." Use it for judgment and experience, not for padding.
- **Plain sentences.** Short ones are fine. Vary the length so the page has rhythm.
- **Name the thing before you evaluate it.** The reader cannot weigh an idea she cannot state. Always
  present a position in its strongest form, in its own vocabulary, before examining it.
- **Say where the evidence stops.** Every chapter has at least one place where the honest answer is
  "we do not know" or "this is argued about." Write those plainly. Do not hedge them into mush and do
  not use them as a gotcha.
- **No cheerleading and no debunking.** This book is for students who may enter the profession. A
  book that leaves them ashamed has failed. So has one that leaves them unable to answer a skeptic.
- **Concrete over abstract.** A named patient in an invented but realistic scenario beats a general
  claim. A number beats an adjective.

## Hard rules

1. **No hyphens, no en dashes, no em dashes in visible prose.** Write "high velocity low amplitude",
   "non musculoskeletal", "1963 to 1975", "day to day". Use commas, colons, or a new sentence where
   you want a dash. Hyphens are permitted only inside a quoted title, a proper name, or an HTML
   attribute. This rule is checked automatically and a chapter that breaks it is rejected.
2. **Straight apostrophes and straight quotes only.** No curly quotes.
3. **Every factual claim must trace to /root/chiro-history/vtsu/book/src/FACTS.md.** Read that file
   in full before writing a word. If a fact you want is not there, either do not use it or research
   it yourself and add it to FACTS.md with a source. Anything FACTS.md marks NOT VERIFIED must not
   be stated as fact; either omit it or write around it honestly.
4. **Where FACTS.md marks something CONTESTED, present the contest.** Do not resolve it. The Lillard
   story in particular gets all three accounts side by side, with no verdict.
5. **Use the anatomy range of motion numbers from Set B** in FACTS.md, consistently, so chapters do
   not disagree with each other.
6. **When quoting Palmer's 1910 title, use his word order:** Science, Art and Philosophy. The course
   catalog uses the modern reordering, philosophy, art and science. If a chapter mentions both, say
   plainly that the modern order is a later convention.

## Structure of a chapter

Every chapter file is `/root/chiro-history/vtsu/book/src/ch-0N.html`, a single `<section>`, no
`<html>`, `<head>` or `<body>`, and no `<style>` or `<script>`. Exactly this shape:

```html
<section class="chap" id="ch-0N" data-title="The Chapter Title">
  <p class="ch-num">Chapter N</p>
  <h2>The Chapter Title</h2>
  <p class="ch-hook">One question, in one sentence, that the chapter answers.</p>

  <p>Opening paragraph...</p>

  <h3>A section heading</h3>
  <p>...</p>

  <figure class="ch-fig" data-fig="fig-example">
    <figcaption>One sentence saying what the figure shows and why it matters. Not a title.</figcaption>
  </figure>

  <p class="ch-pull">A single sentence worth pulling out. One or two per chapter, no more.</p>

  <aside class="ch-note"><h3>A note on...</h3><p>...</p></aside>

  <div class="ch-terms"><h3>Terms from this chapter</h3><dl>
    <dt>Term</dt><dd>Definition in one or two plain sentences.</dd>
  </dl></div>

  <div class="ch-check"><h3>Before you move on</h3><ol>
    <li>A question a reader should be able to answer from this chapter.</li>
  </ol></div>
</section>
```

The `ch-terms` block carries 8 to 14 terms. The `ch-check` block carries 5 to 7 questions, at least
two of which require judgment rather than recall. Both go at the end, in that order. Use `ch-note`
asides two to four times per chapter for material that is important but breaks the flow: a note on
the sources, a note on a common misconception, a note on what a practitioner actually does.

Do not number your `h3` headings. Do not use `h1` or `h4`.

## Length

**6,500 to 8,500 words of body prose per chapter**, except chapter 7, which is 3,500 to 4,500. This
is deliberate: students are told to spend 5 to 6 hours a week on the reading and its figures, and the
book is the only assigned reading. Long paragraphs are fine. Thin chapters are not.

## Figures

You may only reference figure ids from the list assigned to your chapter below. The figure files are
being drawn separately and will be inlined by the build; you write the `<figure>` element and the
caption only, never the SVG. Place 4 to 7 figures per chapter, spread through it rather than
clustered. The caption states the claim the figure makes, in one sentence.

## The seven chapters

Each chapter serves one week and one course learning objective. Stay in your lane: if your topic
touches a neighbor's, gesture at it and cite the chapter number rather than covering it.

### Chapter 1 — Origins and First Principles (week 1)
Objective: explore the history and core principles of chiropractic care.

What was already there before 1895: bonesetting, the Hippocratic writings, the crowded and weakly
licensed American medical marketplace, magnetic healing, and Still's osteopathy three years earlier.
Then the 1895 account, presented with all three versions of the Lillard story. Then D.D. and B.J.,
the name, the school, the Green Books as the profession's own literature. Then the philosophy in its
own vocabulary: the body as self healing and self regulating, the nervous system as the coordinating
system, the practitioner's job as removing interference rather than adding something from outside.
Innate Intelligence in Palmer's own terms. Stephenson's 33 principles as a deductive system starting
from the Major Premise, quoted exactly. Subluxation as four different concepts wearing one word, and
the three modern readings of innate intelligence: literal, metaphorical, discarded. End by asking the
reader which reading they are inclined toward and telling them they will be asked again in week 7.

Figures: `fig-marketplace`, `fig-still-vs-palmer`, `fig-1895-sources`, `fig-principles-chain`,
`fig-vitalism`, `fig-subluxation-drift`

### Chapter 2 — The Spine You Will Touch (week 2)
Objective: understand the structure and function of the spine in chiropractic theory.

Straight anatomy, taught for the hands. The vertebra part by part and what each part is for. The
five regions and why each is shaped the way it is. The three joint complex: disc in front, two facet
joints behind, and why that arrangement determines what each region can and cannot do. Ligaments and
the deep muscles, briefly. The cord, the nerve roots, and the intervertebral foramen, with an honest
account of what would have to be true anatomically for a subluxation to interfere with a nerve, and
what the size relationships actually are. Range of motion by region, Set B numbers. Then the part
students will use: palpable landmarks, how to find them on yourself, and the measured error rates
(C7 prominent in only 60 to 70 percent of people, the iliac crest plane hitting L5 in about 20
percent). Posture, what it tells you and what it does not. Close on why careful observation is a real
skill even when the hands are not certified.

Figures: `fig-vertebra`, `fig-regions`, `fig-disc-facet`, `fig-nerve-exit`, `fig-landmarks`, `fig-rom`

### Chapter 3 — The Art of Technique (week 3)
Objective: compare various chiropractic techniques and the evidence for its efficacy.

What an adjustment physically is: patient position, contact, tissue slack, pre load, then a high
velocity low amplitude thrust of small excursion. What the pop actually is, using the 2015 real time
MRI work on tribonucleation, and why the sound is not the point. Then the technique families, each
described the same way so they can be compared: how the practitioner decides where to work, and how
the correction is delivered. Diversified, Gonstead, Activator, Thompson, SOT, Flexion Distraction,
upper cervical. Then the uncomfortable part, told straight: reliability studies on the assessment
methods, with real kappa values, showing that pain provocation is reasonably reliable while detecting
segmental motion restriction is poor to near chance. What that does and does not imply about whether
the treatment works. How a practitioner actually chooses a technique, honestly: mentorship, school,
hand size, patient population, what the body in front of you tolerates. Close with the structured
observation method students will use.

Figures: `fig-hvla`, `fig-cavitation`, `fig-technique-families`, `fig-reliability`,
`fig-technique-assumptions`

### Chapter 4 — Becoming One (week 4)
Objective: discover what it takes and what it is like to be a chiropractor.

The road, concretely: prerequisite credit hours and science courses, the CCE standards, program
length in instructional and clinical hours, NBCE Parts I through IV and Physiotherapy and when each
is taken, then state licensure and what varies. Cost and typical debt at graduation, stated plainly.
Then the life. The first year. Associate versus your own practice. What a day actually contains,
including the parts nobody mentions: documentation, insurance, no shows, the business of it. Scope of
practice differences between states and what that means for where you can work. Risk, malpractice,
and the paperwork that protects you. Longevity, hands, and burnout. Close with what practitioners
say they wish someone had told them, written as a practitioner telling them.

Figures: `fig-licensure-road`, `fig-scope-map`, `fig-licensure-span`

### Chapter 5 — In the Clinic (week 5)
Objective: review various clinical applications of chiropractic.

What walks in the door, and what the evidence says about each. Low back pain acute and chronic, neck
pain, cervicogenic headache, migraine, quoting the 2017 ACP guideline exactly and naming the major
reviews. Then the harder territory: non musculoskeletal claims, what the reviews actually found, and
why the honest answer is thinner than the marketing. Pediatric and perinatal care handled as a
consent and disclosure problem rather than a verdict, presenting what professional bodies say and
what independent reviewers say, without resolving it. Risk: adverse events, the cervical artery
dissection literature, what a case crossover design can and cannot establish. Red flags that require
referral instead of treatment. How to read a trial well enough not to be fooled. The patient who does
not improve, and what a good practitioner does then. Close on informed consent as the practitioner's
actual obligation.

Figures: `fig-evidence-bands`, `fig-trial-anatomy`, `fig-dissection`, `fig-red-flags`, `fig-consent`

### Chapter 6 — Alongside Everyone Else (week 6)
Objective: explore integrating chiropractic care with other healthcare modalities.

Who else is in the building: physicians, physical therapists, osteopathic physicians, massage
therapists, acupuncturists. What each is trained to do, where the scopes overlap, and where the real
differences are. Then the history that made integration hard: the AMA Committee on Quackery from 1963,
Principle 3 of the AMA ethics code quoted exactly, Wilk filed in 1976, and Judge Getzendanner's 1987
finding quoted exactly, with the remedy she ordered and what she declined to order. Tell this
carefully. It is a real finding by a federal court and it does not need embellishment, and the
chapter should also say plainly what the ruling did not decide, which is whether chiropractic works.
Then the present: integrated clinics, hospital and VA practice, Medicare and insurance, and how a
referral letter is actually written and read. Close on what a practitioner owes a colleague in
another profession.

Figures: `fig-boycott`, `fig-antitrust-choice`, `fig-wilk-path`, `fig-professions`, `fig-referral`

### Chapter 7 — What You Do With This (week 7)
Objective: all six. Shorter chapter, 3,500 to 4,500 words.

No new material. This is the chapter that makes the course add up. Return to the question from
chapter 1 and ask the reader where they now land on innate intelligence and on subluxation, and why.
Give them three things they should be able to do: say what the evidence supports, say where it stops,
and say why the work is still worth doing. Then the practical piece: how to talk to a skeptical
patient or relative without getting defensive, and how to talk to a patient about uncertainty without
losing their trust. For the students heading toward chiropractic school, an honest paragraph about
how to decide. Close by framing the final video assignment: explaining this profession to someone who
knows nothing about it is the hardest and most useful thing in the course.

Figures: `fig-course-arc`, `fig-three-questions`

## What to do before you write

1. Read FACTS.md in full.
2. Read `/root/chiro-history/book/src/ch-01.html` for the prose register and the HTML shape. That is
   from an earlier version of this book with a different framing, so take the voice and the structure
   from it, not the content or the argument.
3. Check your assigned figure ids against this brief. Do not invent new ones.

Write the chapter. Then reread it once against the hard rules above, particularly the dash rule, and
fix what you find before you finish.

## Late notes from the figure authors

- Lumbar axial rotation in FACTS.md Set B is **15.3 degrees to each side**, not 15 degrees total. The
  figures say "to each side". Match them.
- FACTS.md carries no sourced number for the excursion or the duration of a thrust, and none for how
  much of the intervertebral foramen the nerve occupies. The figures therefore state both
  qualitatively. Do not put a number on either in prose.
- FACTS.md gives no located assessment method for Sacro Occipital Technique, Flexion Distraction, or
  Thompson Drop Table. The technique figure says so openly rather than inventing one. Chapter 3
  should do the same: name it as a gap in the accessible sources, not as an absence in the technique.
- The Cassidy case crossover odds ratios could not be verified against the primary paper, so no
  effect estimate appears in any figure. Chapter 5 must not quote one either. Describe the direction
  of the finding and the design problem instead.

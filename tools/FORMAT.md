# Slide Markdown format

One file per session: `<course>/slides/session-NN.md`. Build with `python tools/build.py` (needs `python-pptx` and `Pillow`).

```markdown
---
course: Data Management
session: 1
title: Why Data Matters
subtitle: Short line under the title
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# Why Data Matters {.title}        <- title slide, filled from the front matter

---

# Slide title {.optional}           <- classes: title, section, optional, exercise, references

Paragraph text with **bold**, *italic*, `code` and [links](https://example.org).

- Bullet
  - Sub-bullet (2-space indent)
1. Numbered item

| Column | Column |
|---|---|
| Cell | Cell |

::: callout
Highlighted key message or definition.
:::

::: cards
### Card title
Card text.
### Second card
Card text.
:::

::: layers
- Top layer: description
- Bottom layer: description
:::

::: columns
Left column content
|||
Right column content
:::

![Alt text](img/figure.png){width=60%}

::: source
Author (Year).                     <- citation line at the bottom of the slide
:::

::: notes
Speaker notes (PPTX only; included in HTML only with --notes).
:::
```

Slides are separated by a line containing only `---`.

The lecturer name is not stored in the slide files (they are public). It comes from `tools/local.json` (gitignored), e.g. `{"lecturer": "Name"}`, and appears on the PPTX title slide only.

Other private values (e.g. partner company names) use a placeholder `{{private:key|Public fallback}}` anywhere in a slide file. The PPTX gets the value of `key` from `tools/local.json`; the public HTML always shows the fallback text. Never write the private value itself into a slide file, including speaker notes (the Markdown is public).

## Rules

- **No timings or formats on slides.** Minutes, clock times and formats (input, pair work …) go into the speaker notes only, so students don't feel rushed.
- **Core vs. optional:** slides without a class are core (exam-relevant); `{.optional}` marks self-study slides.
- **Citations:** every slide based on a source has a `::: source` block in APA 7 short form, and the full reference goes on the `{.references}` slide. Diagrams drawn from a textbook figure say "Adapted from Author (Year, p. X)"; own diagrams say "Own illustration based on …".
- **Fit:** the build picks the largest font size (24 pt down to 14 pt) at which the content fits, and prints a warning if it does not fit at all — then split the slide.
- **Preview:** `python tools/build.py <file> --preview` exports every slide as PNG via PowerPoint into `build/preview/` for a visual check.

# Worksheet Markdown format

One worksheet per session: `<course>/worksheets/session-NN.md`. Worksheets are for students to practise the session's content on their own or in the lab, and to prepare for the exam or portfolio. They complement the exercise slides: they repeat the core in-class exercise only where useful and add further practice tasks of increasing difficulty.

The build turns each worksheet into two pages:

- **Student version** (no solutions) → `docs/<course>/worksheet-NN.html`, linked from the course page next to the slides; printable as A4 via the browser
- **Lecturer version** (with solutions) → `build/<course>/worksheet-NN-solutions.html` (not published)

```markdown
---
course: Data Management
session: 4
title: Semantic Data Modelling II
subtitle: Practice tasks for weak entity types, recursive relationships and specialisation
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

Intro paragraph: what the worksheet covers and what students need (e.g. paper, Jupyter, a dataset).

## Task title                       <- numbered task (1, 2, 3 ... added automatically)

Task text, lists, tables, code blocks, `::: callout`, `::: cards`, `::: columns`, images as on slides.
Links to local files, e.g. [orders.csv](data/orders.csv), are copied next to the built page.
Lines starting with `>` are shown as a callout box. A code block can sit inside a list item: start it on the item line (`1. ```sql`) or indent it under the item; indented text after it continues the item.

### Sub-heading                     <- optional structure within a task

## Optional challenge {.optional}   <- marked as optional

::: answer lines=6
Optional prompt shown inside the box, e.g. "Owner: ___  Partial key: ___"
:::                                 <- ruled box to write in (student version only)

::: hint
A hint students can unfold on the web (hidden when printed).
:::

::: solution
Model answer (lecturer version only). Never visible on the public page — but the Markdown
source is public in the repository, so solutions here are not secret.
:::

## References {.references}        <- unnumbered, full APA 7 references
```

## Rules for worksheets

- **Same rules as slides:** English, no timings, sources in APA 7 (short form in the text, full reference in the `{.references}` section), private placeholders only via `{{private:key|Fallback}}`.
- **Every task has a solution** block, written so that a student tutor could mark the task with it.
- **Difficulty rises** within a sheet: recall and understanding first, then application, then one transfer or exam-style task. Mark extra tasks beyond the core as `{.optional}`.
- **Exam style** for courses with a written exam: at least one task per sheet in the form and length of an exam question.
- **Training only:** worksheets and their solutions are public practice material. Real exam questions and final tests are never written into this repository.

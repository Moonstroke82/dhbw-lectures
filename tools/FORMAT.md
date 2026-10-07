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

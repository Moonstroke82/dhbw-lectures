# Lectures

Lecture material for DHBW, Digital Business Management (Business IT), Bachelor. All material is in English.

| Folder | Module | Semester | Hours | Assessment | First run |
|---|---|---|---|---|---|
| [data-management](data-management/MODULE.md) | Data Management | 2 | 60 h | Exam + design project (weighting open) | 2027 |
| [it-management-eam](it-management-eam/MODULE.md) | IT Management and Enterprise Architecture Management | 4 | 55 h | Written exam | 2028 |

## Outputs

Each session is written once in Markdown (`<course>/slides/session-NN.md`) and built into two formats:

- **PowerPoint (.pptx)** with speaker notes, for teaching → `build/<course>/` (not published)
- **Web slides on GitHub Pages** for students → `docs/<course>/` (published from the `docs/` folder)

Build: `python tools/build.py` (all sessions) or `python tools/build.py data-management/slides/session-01.md --preview`. Slide format and citation rules: [tools/FORMAT.md](tools/FORMAT.md). The look is defined in `tools/theme.py`; the official slide template will be applied there later.

## Files per lecture

- `MODULE.md`: official module description (English translation + German original)
- `SESSION_PLAN.md`: approved session plan and teaching principles
- `STATUS.md`: session tracker, feedback from lecturer and students, decisions and changes (kept private, not in the public repo)
- `slides/`: slide sources, one Markdown file per session

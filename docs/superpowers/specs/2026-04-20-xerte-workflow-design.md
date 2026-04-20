# Design Spec: Xerte Development Workflow Guide

**Date:** 2026-04-20
**Status:** Approved

---

## Goal

A single markdown document (`PROJECTS/XOT-DEV-WORKFLOW.md`) that serves as both an onboarding checklist at the start of each Xerte project and an ongoing platform reference throughout development. Audience: the author only (and Claude when handed at project start).

**Scope:** This workflow applies to the **XOT project template only** (XOT1 / Modern Nottingham theme). The Bootstrap template has a different file structure and DOM layout and is out of scope for this document.

---

## Output File

```
PROJECTS/XOT-DEV-WORKFLOW.md
```

Sits above individual project folders so it is easy to locate and reference across projects.

---

## Document Structure

### Section 1: Project Setup Checklist

Four sequential phases. Each phase has:
- An entry condition (what must be true before starting this phase)
- A checkbox task list
- A brief "watch out for" note where relevant

**Phase 1: Platform Investigation**
Entry condition: none — this is always the first phase, before writing any CSS or JS.
Tasks: identify the active theme, read the CSS loading pipeline for that theme, inspect the accessibility theme files, map the content DOM structure for the page types in scope.
Note: the single biggest time-saver; skipping this phase means refactoring colour selectors later.

**Phase 2: Design System Setup**
Entry condition: Phase 1 complete.
Tasks: create `design.json` with token categories (colours, typography, spacing, border radius, shadows, components); scaffold `custom.css` (@import first, then CSS custom properties, then base styles, then utilities); scaffold `custom.js`; set up project directory structure (`docs/`, `components/`, `demos/`); create `changelog.md`.

**Phase 3: Component Development**
Entry condition: Phase 2 complete (design tokens and utilities in place).
Tasks: write a component design spec before building each component; build the component HTML/CSS/JS; create a demo/reference HTML page; update `changelog.md`.

**Phase 4: Handover and Cleanup**
Entry condition: all content complete and published.
Tasks: ensure every component has usage documentation; verify publish produces expected output in play.php; clean up docs; final changelog entry.

---

### Section 2: Platform Reference

Nine named topics. Each is a short paragraph (the rule and why it matters) followed by a code block or key rule callout. Topics are independent — jump to whichever is relevant.

1. **CSS Loading Pipeline** — load order, what `#lo_css` is, why `!important` is not needed
2. **The @import Constraint** — must be the absolute first line; silent failure otherwise
3. **Accessibility Theme Problem** — specificity trap and inheritance trap explained
4. **Colour vs Structure Rule** — which CSS properties are safe at high specificity vs which must stay low
5. **Font Awesome Preservation** — never override `font-family` on `#x_footerBlock button`
6. **CSS Grid Breakout Pattern** — target `#pageContents`; set `.innerPage { width: 100% }`
7. **Preview vs Publish** — custom CSS only appears after publishing to `data.xml`
8. **Content DOM Targeting** — scope grid layout to `.x_text_page` only; other page types have different DOM structures
9. **Known Xerte Gaps** — `#lo_css` not disabled in accessibility modes; heading colour contrast issue; `disableBespokeCSS()` TODO in source

---

## Source Material

All reference content is extracted from the I-Prehab project:

| Source file | Used for |
|---|---|
| `docs/xerte-custom-css-guide.md` | Sections 1, 2, 3, 4, 5, 6, 7, 8, 9 |
| `docs/dev-summary.md` | Phase structure, "things I'd do differently", known limitations |
| `changelog.md` | Phase sequencing, milestone order |
| `design.json` | Token category list for Phase 2 checklist |

---

## Constraints

- Scope is XOT template only — Bootstrap template has different file/DOM structure and is not covered
- No new technical content — everything in the document must already exist in the source material above
- Plain markdown only — no HTML, no embedded scripts
- Short entries in the reference section — enough to remind, not enough to teach from scratch
- The checklist phases must be sequential with explicit entry conditions to enforce the investigation-first order

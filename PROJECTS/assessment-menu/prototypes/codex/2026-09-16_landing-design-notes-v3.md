---
title: Assessment Menu Landing Designs v3 - Build and Review Notes
date: 2026-09-16
type: output
status: prototype
tags:
  - assessment-menu
  - design
---

# Assessment Menu landing designs v3

Three standalone landing pages, with a comparison gallery, created for Nan's request for distinct Cardiff-branded designs. Existing prototypes are retained.

## Open the designs

- [[2026-09-16_assessment-menu-landing-options-v3.html|Comparison gallery]] — actual desktop previews, design trade-offs, Xerte fit, preferred option and comments export.
- [[2026-09-16_assessment-menu-landing-editorial-v1.html|Editorial]] — large title paired with a manually controlled question preview; all six questions before the type finder. Suggested starting point for the main landing page.
- [[2026-09-16_assessment-menu-landing-type-finder-v1.html|Type finder]] — dark introductory sidebar beside a searchable directory. Best suited to returning visitors; the design questions follow the directory.
- [[2026-09-16_assessment-menu-landing-design-studio-v1.html|Design studio]] — six-question navigator, optional temporary notes and copy export, followed by type discovery. Intended for design conversations; it makes no automatic lane or assessment recommendation.

## Content and provenance

These are designs based on the local project record as read on 16 September 2026. The external guidance pages were not re-snapshotted for this design task.

| Source | What it supplies |
| --- | --- |
| `2026-09-16_assessment-menu-landing-options-v2.html` | Latest content direction; exact English wording of the six questions; short framework, inclusion and programme briefs; supporting resources and further reading. |
| [[2026-09-08-landing-page-draft-1]] | Hannah and Carys's source context, menu purpose and six-question framing. The v2 prototype records the application of the Word draft's tracked changes and comments. |
| [[Assessment Menu - Xerte Page Structure and Landing Page]] | Page structure, 17-type register, per-type fields, guidance-not-policy framing and open content decisions. |
| [[2026-09-08-assessment-types-for-menu-draft]] | Seventeen assessment types across seven categories; source status and content gaps. |
| `2026-09-15_assessment-menu-xerte-prototype-v1.html` | Existing assessment entry routes and detailed guidance destinations. |
| [[2026-07-14 Assessment Menu Prototype Review Meeting]] | Prototype as a discussion tool; usefulness and wider content dependencies remain separate from visual polish. |
| [[Cardiff Design Tokens]] and the html-it Cardiff University theme | Cardiff red, white and charcoal, blue body links, dark red focus rings, supplied bilingual logo and local font substitutes. |

The designs retain the six English questions verbatim from v2. Hints connect questions to entry fields. There is no separate “Using the Assessment Menu” section. Each design includes search and category filters, both lane purposes, guidance-not-policy framing, the proposed student-choice position, programme-level thinking, related guidance, further reading and the LTA contact route.

## Evidence and publication boundaries

- The student-choice/no-compulsion wording remains **proposed D1**, clearly labelled next to the text. It is not presented as agreed policy.
- All three pages offer English and Welsh interface/content views. **Welsh translations are newly drafted for these prototypes and require language review**, including lane labels and assessment terminology. They are not approved institutional translations. Existing linked resources may be English-only.
- Assessment principles, programme approval and assessment brief template destinations remain unresolved. The prototypes list these in their review notes instead of providing dead links.
- The underlying entry content and its existing review flags are unchanged. An entry link opens the existing Xerte-style HTML prototype; the landing pages do not publish to Xerte.
- No new citations, case studies, student quotations, assessment ratings or policy decisions have been invented. Further reading is carried forward from v2.

## Design and implementation

Applied html-it Level 3 with the Cardiff University theme and Hallmark's structural-variety, responsive and interaction guidance. Brand requirements take priority over Hallmark's generic advice to tint whites or rotate palettes. Each page deliberately shares the same institutional identity while using a different opening structure: split editorial, index-first directory, and guided workflow.

The Cardiff theme's Franklin Gothic/system and Georgia substitutes are used; licensed Marr Sans and Darby Serif files were not available in the inspected output assets. The existing bilingual Cardiff logo is embedded unchanged.

All HTML files contain their own CSS, JavaScript and embedded logo. The comparison gallery embeds actual Chrome screenshots. There are no external font, CSS or JavaScript dependencies and no build step. `tokens.css` exports the same token block for reuse; tokens are inlined in the HTML files to preserve single-file portability. Keep the files in this output folder so relative links to assessment entries and the design guide resolve.

Search matches English and Welsh assessment names and category names, combines with the category filter, announces result counts, provides a reset/empty state and exports the visible list. The studio keeps six note values in memory when moving between questions or changing language. Notes are lost on reload/close unless copied. No notes are transmitted or stored on a server. Clipboard failure exposes a selected text area for manual copying.

## Validation

Checked in headless Google Chrome on 16 September 2026:

- **56 layout cases:** three landing pages in English and Welsh, plus the comparison gallery, at 320, 375, 414, 768, 1024, 1280, 1600 and 1920 CSS pixels. No elements extending beyond the viewport after correcting the studio’s Welsh button row at 320px.
- **Visual inspection:** desktop previews of all three pages and the gallery, mobile Editorial/Studio views, and the assessment finder section.
- **Text contrast scan:** no failures detected against WCAG text thresholds on the three landing pages. This is a targeted check, not a complete accessibility certification.
- **Interactions:** search, combined search/category filters, reset, empty results, 17-type restoration, question preview, note retention between questions, final-step state, language views, and gallery design selection/comments.
- **Keyboard:** native Enter activation of the Written filter passed on each landing page after enabling focus in the headless browser. The initial unfocused test did not deliver the keystroke.
- **Export:** visible-type text captured through a clipboard stub; studio and gallery clipboard-denied paths expose selected text with real newlines and preserve entered notes/comments. Actual OS clipboard contents were not read.
- **Files and routing:** JavaScript syntax, unique IDs, local file links and in-page fragments checked. All 17 entry slugs match the existing destination prototype. No runtime JavaScript exceptions recorded.
- `git diff --check` passed. The project index and newest-first log link the new outputs. Earlier prototype files were not edited.

This checks the HTML prototypes locally, not deployment into the Xerte editor, live external-link availability, screen-reader operation, or approval of policy wording and Welsh translations.

## Xerte considerations

| Design | Likely implementation |
| --- | --- |
| Editorial | Two-column Text element, theme CSS, small script for the question preview and shared search. |
| Type finder | Custom browse section with search/filter script. Sidebar becomes an introductory panel on smaller screens. |
| Design studio | Custom component for six-step navigation, temporary notes and clipboard fallback; the most scripting and testing. |

Before publishing, confirm content decisions and resource destinations, review Welsh copy, and test what the Xerte editor retains. The exported notes and comparison choice are review aids, not changes to the live resource.

# Codex — Assessment Menu outputs

Only Codex-generated outputs belong here. Other-model prototypes, original assets and the separate Xerte Option C package remain in the parent `assessment-menu/` folder. This follows Nan's clarification on 17 September 2026.

## Start here

- [[2026-09-17_assessment-menu-landing-combined-v1.html|Combined landing page]] — search-first Assessment Menu landing-page prototype: a simple 17-type finder, list/grid comparison and the retained six-question conversation with local notes and copy fallback.
- [[cardiff-resource-design-guide.html|Current generic Cardiff resource design guide]] — shared across all resource prototypes.
- [[🎨 Cardiff University Design System/design-system/DESIGN|Canonical shared DESIGN.md]].
- [[2-lane Assessment/Outputs/assessment-menu/codex/Assessment Menu Requirements|Assessment-specific requirements]].

- [[2026-09-17_assessment-menu-design-system-v1.html|Original Assessment Menu component guide]] — inspect colours, typography, spacing, rules and controls; try the six-question conversation and switch discovery between grid and list.
- [[2-lane Assessment/Outputs/assessment-menu/codex/DESIGN|DESIGN.md — route to the shared system]] — the visual language Nan approved and instructions for future builds.
- [[2026-09-16_assessment-menu-landing-options-v3.html|Previous landing-page comparison]] — the three reference designs, with review/export controls.
- [[2026-09-16_landing-design-notes-v3|Previous build and source notes]].

## Portable component package

`design-system/v1/` contains scoped tokens, reusable component CSS/JavaScript, editable conversation/discovery HTML fragments, [[2-lane Assessment/Outputs/assessment-menu/codex/design-system/v1/Xerte Integration|Xerte integration notes]] and `validation.json`.

The visual guide is self-contained; the standalone entry links still depend on the existing menu prototype in the parent folder. The HTML fragments are source snippets, not standalone styled pages. Adapt discovery URLs before pasting into Xerte.

The root `tokens.css` belongs to the original landing-page prototypes and is retained unchanged. **This original component package uses `design-system/v1/tokens.css`; use the shared Cardiff system for new generic components**: it preserves the palette and font stacks while namespacing the tokens and completing the spacing scale.

## Decisions and status

- The shared design language is accepted; the final combined landing page is not selected.
- Keep the conversation component for further Xerte testing.
- List/grid remains an open choice; the guide allows comparison without changing the data.
- D1 remains proposed. Welsh translation and language review remain required.
- Source record: [[2026-09-17 Assessment Menu Design Review]].

## Validation on 17 September

The component guide passed layout checks at 320, 375, 414, 768, 1024, 1280 and 1920px, with desktop/mobile screenshots inspected. Search, combined category filtering, list/grid state preservation, reset, empty state, keyboard filter activation and manual-copy fallback passed.

Recreating the conversation node and firing the instrumented Xerte event restored its selected step and notes. Repeated initialisation did not duplicate navigation. With JavaScript disabled, all six questions and 17 types remain visible. No runtime exceptions or broken local HTML links were detected. JavaScript syntax and `git diff --check` passed.

These are standalone browser checks with an instrumented event, not a test inside the actual Xerte editor/player. See the integration notes for the remaining save/reload, published clipboard-context and language checks.

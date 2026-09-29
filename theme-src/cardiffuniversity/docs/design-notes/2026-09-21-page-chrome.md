# Page chrome: footer, feedback tab, back-to-top and glossary

Implemented 21 September 2026. This is the first item under "Remaining theme migration" in the
[follow-up checklist](../plans/2026-09-21-follow-up.md).

## Problem

Phase 1 restyled the header, navbar and sidebar. Four pieces of page chrome still had the v2
look:

- The footer was grey-80 with centred text and no layout for the author's HTML.
- The feedback tab was brand red with a large soft shadow. Its link, as the fixture models it,
  took the player's link blue: 1.38:1 against the tab, effectively invisible text.
- The back-to-top button looked red but for the wrong reason. The player gives it both
  `.btn-mini` and `.top-round`; `.btn-mini` is compiled later, so the `.top-round` colours in
  `_xerte-components.scss` never applied. The player's own CSS also draws a shadow halo on hover.
- The glossary tip was brand red.

The design system does not define these elements, and the Red Usage Decisions note had no
decision for any of them.

## Decisions

Made by Nan on 21 September 2026.

| Element | Treatment |
| --- | --- |
| Footer | Ink (`#121212`), white links, grey-30 secondary text, no red top edge. Follows the simple two-column footer in the Assessment Menu prototype (15 September), not the University website's four-column footer. |
| Feedback tab | Action red (`#C21F16`), hover `#A11A12`, white text (6.0:1), no shadow. |
| Back-to-top | Ink with a white arrow, grey-90 on hover and focus, no shadow. |
| Glossary tip | Ink with white text. |

Shadows are for overlays. The tab and the button are fixed or floating controls, not overlays,
so they carry none.

## What changed

- **Footer** (`_layouts.scss`). The author's `customFooter` HTML lands in `#customFooter`
  wherever the player puts it, so that element is the layout container: an `auto-fit` grid whose
  columns stack once one would be narrower than 16rem. No new classes are needed. Headings are
  body-size bold instead of the display `h2`; link lists lose the bullet indent; link focus rings
  turn white, because the global ink ring cannot be seen on ink. In "replace" mode the player
  appends its accessibility link as one more child; it is pinned to column 1 so it takes its own
  row. Spanning every column would stop `auto-fit` collapsing empty tracks and squeeze the real
  columns to a quarter of the width each.
- **Feedback tab** (`_layouts.scss`). Action red, no shadow, and the link colour is forced to
  white so it can no longer inherit link blue.
- **Back-to-top** (`_xerte-components.scss`, `_buttons.scss`). Colours now select on
  `.btn.topBtn`, which both player variants carry and which does not depend on compile order.
  The hover halo is removed, and so is the `:active` shadow on the legacy `.btn-mini`.
- **Glossary tip** (`_xerte-components.scss`). Ink.
- **Base-template duplicates.** The stray `.footer h3` rule in `_base-elements.scss` and the
  commented-out `::before` block in the footer are gone.
- **Demo.** A "Page chrome" section in `demos/components.html` shows the footer and both
  back-to-top variants, and documents the feedback tab and glossary in text.

Two values from the prototype were mapped to the nearest design-system token: its `#C9C9C9`
secondary text became grey-30 (`#CCCCCC`), and its 17px footer heading became the body size.

## Verification

- 133 automated checks pass (110 before), including 23 new `chrome` checks. The fixture gained
  a footer, feedback tab, back-to-top and glossary term shaped like the player's markup. Of the
  first 19 checks, 10 failed against the old CSS for real reasons. The other 9 guard behaviour
  that was already right (contrast of the chosen colours, the glossary's dotted underline, the
  back-to-top focus ring, stacking at narrow width). The focus-ring check first failed only
  because it read the ring mid-transition (the player fades it in over 300ms); it now reads the
  settled value. The four checks added afterwards were each seen to fail before their fix.
- The generated reference is in sync and no theme class is undocumented.
- The fixture was rendered in headless Chrome at 1280px and 390px wide, including a simulated
  "replace" footer built the way `application.js` builds it, and the results were reviewed by eye.

Not verified:

- **The real Xerte player.** None of this ran in a Xerte project.
- **Hover, `:active` and the feedback tab's slide-out.** Headless checks cannot trigger them.
- **The feedback tab's markup.** The player does not create `#feedback_button`, and no markup
  for it exists in this repository. The fixture assumes an icon and a link, inferred from the
  v2 theme's CSS. Check it against a real project.

## Left as it was

- The Red Usage Decisions note in the vault has not been updated with these four decisions.
- In "replace" mode the player sets a 10px inline left margin on `#customFooter`, so the content
  is not aligned with the page container. The theme does not override an inline style.
- The feedback tab stays at `top: 62%` on narrow screens and may overlap content. The prototype
  moves it to the bottom edge; that was not measured or changed here.
- The player's `.top-round { transition: all .3s !important }` and its springy easing remain.
- The glossary tip keeps the base template's 4px radius. That belongs to the hardcoded-values
  audit, the third "Remaining theme migration" item.
- No reversed (white) Cardiff logo is bundled. Authors supply an official one for the footer.

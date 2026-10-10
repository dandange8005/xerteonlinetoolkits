# Demo page fixes

Done 9 October 2026, before pointing authors at the demos while the author guide is unfinished. Four
problems were reported on the demo pages, and fixing them turned up a fifth.

## What was wrong and what changed

| Problem | Cause | Fix |
| --- | --- | --- |
| Homepage callout icons were empty squares | `index.html` did not load the Font Awesome stylesheet. A callout's icon is a Font Awesome character, so only the exclamation mark (a plain "!") showed. | `index.html` now loads it, as the other pages do. |
| A code strip ran out of its box and the page scrolled sideways | `.code-label` is a `<code>`, and Bootstrap 2 sets `white-space: nowrap` on `code`. | `.code-label` wraps and stays inside its block (`demo-styles.css`). |
| The section menu did not move with the page | The player pins the menu with Bootstrap's `affix` plugin (`application.js`). The demos did not load the player's script, and their Bootstrap script was broken (next row). | `assets/demo-sidebar.js` does the same job. It computes the pin point from the menu's own position, because the player's fixed offsets are for its own header. All 11 pages with a menu load it. |
| Demo pages had no working Bootstrap JavaScript | `assets/bootstrap/bootstrap.min.js` was 50 bytes of text, an error message from a failed download ("Couldn't find the requested release version 2.3.2."), committed with the first demos. Tabs, collapse sections, alert dismissal, the carousel and the scroll highlight never worked. | Replaced with the player's own Bootstrap 2.3.2 script. |
| The demos taught legacy classes | `button--small` (9 uses), `button--outline`, `list--tick` and `list--cross`, `c20` to `c80` widths and `topMargin`. | See below. |

## Legacy classes

- `button--small` became `button-sm` where it sets a size. The "Compact" button demo and the "Legacy Button
  Styles" block were removed, as they were from the author guide.
- `list--tick` and `list--cross` are a known bug in the theme's own list ("icons stack on multi-item
  lists"). The paired Do and Don't lists now use Font Awesome's `fa-ul` and `fa-li`, which the theme's
  guidance recommends and which hang the icons in the margin.
- The flexbox page's "Legacy Support (System 2)" section now shows only the widths the theme still treats
  as current: `c25`, `c33` and `c50`. Rows of 40/60, 30/70, 20/80, 30/40/30 and five columns of 20 were
  removed, and the image and text example is 50/50. `topMargin` has no current equivalent, so the second
  heading in that example, which existed only to show it, was removed.
- The older names are still listed, as legacy, in the generated table on the Code and utilities page.

## Checks

- `tests/test_demos.py`: no demo page uses a legacy class (live markup and the samples beside it), pages
  that use Font Awesome or callouts load the font, pages with a menu load the pinning script, and the demo
  Bootstrap script is Bootstrap.
- `tests/check_demos.py` (headless Chrome, run in CI): the callout icons have their font, no code label
  or its text runs out of its block on any page at desktop and phone width, the images page does not
  scroll sideways, Bootstrap's plugins are loaded, and the menu is pinned in view after scrolling.
- The first version of the code label check compared only the box and passed while the text still ran
  out of it. It now also requires the text to fit its own box.
- Looked at in a real browser: the callouts, the icon buttons with the pinned menu, the paired lists and
  the flexbox columns.

## Homepage callouts in three columns

The three callouts on `index.html` are now one responsive row, using the theme's flex utilities (the page's
recommended system): a `flex flex-wrap gap-md` container, with `flex-300` on each callout. Three columns
of equal height when there is room, then two and one, then stacked on a phone. The flex class is on the
callout itself, so the three stretch to the same height. The older System 2 classes (`flexContainer`,
`c33`) would also work, but the flexbox page lists them under "Legacy Support", so they were not used.

## Phone width

Checking the new row at phone width showed the homepage scrolled sideways, before any of today's changes.
Bootstrap 2 sets `white-space: nowrap` on `code`, and one list of long file paths forced the whole page
to 615px. Inline code in demo content now wraps (`.demo-section code`), which fixed the homepage and the
flexbox and typography pages.

Three pages still scrolled sideways at phone width after that, and were fixed on 10 October 2026:

- **Cause.** The page body is a column flex container (from the player's `custom.css`), and Bootstrap gives
  `.container` auto side margins. In a flex column, auto margins stop an item stretching, so the container
  sized itself to its content: 969px on `lists-tables`, however narrow the phone. A scroll wrapper inside it
  could not help, because the container simply grew to fit the wrapper. `main.container` now has
  `max-width: 100%`. `base-elements-demo.html` has its own inline style block and got the same rule.
- **Tables.** With the container the right width, four ordinary tables (472 to 554px) were wider than a
  phone. They are now wrapped in `cu-table-scroll` with `tabindex="0"`, `role="region"` and an
  `aria-label`, as the Tables page teaches: three on `lists-tables`, two on `base-elements-demo`.
- **`images-media.html`** was only 2px over, from the same cause, and needed nothing more.
- **Not a theme problem.** The real player puts its content containers inside `<div id="aboveFooter">`, an
  ordinary block, so they fill the page. The demos put `<main class="container">` directly under `body`,
  which is what triggered it. Authors' pages are not affected.
- A rule letting the row shrink (`.container > .row-fluid { min-width: 0 }`) was tried first and changed
  nothing, so it was not kept.
- A check that every `cu-table-scroll` wrapper in the demos has `tabindex`, `role` and `aria-label` now
  runs in `test_demos.py`, since nothing else checks them.

All demo pages are now checked for sideways scroll at desktop and phone width.

## Not changed

The demos still load the theme and Font Awesome from paths into the repo (`../../../themes/...`,
`../../../modules/...`), so they only work from a checkout of the repository. They also use external
placeholder images (`placehold.co`, `picsum.photos`). Neither stops them working locally.

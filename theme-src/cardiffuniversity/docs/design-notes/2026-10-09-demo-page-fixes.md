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

## Not changed

The demos still load the theme and Font Awesome from paths into the repo (`../../../themes/...`,
`../../../modules/...`), so they only work from a checkout of the repository. They also use external
placeholder images (`placehold.co`, `picsum.photos`). Neither stops them working locally.

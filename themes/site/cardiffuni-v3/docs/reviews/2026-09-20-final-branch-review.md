> **Historical review, with follow-up status updated 21 September 2026.**
> Important findings I1, I2, I4–I6 were addressed in `9ca3786`; I3 was addressed in
> `f241986`. The subsequent JavaScript findings were addressed in `79fcdeb`, then
> smooth scrolling was removed in `4def076`.
>
> The 21 September tidy-up addresses Minor 1–8: unused breakpoints, stale comments,
> focus fallbacks, current version documentation, colour comparison, missing-element
> checks, focused-control checking and the fixture scope note. The tick/cross classes
> are now explicitly listed as legacy with a warning. These changes are recorded with
> the token consolidation in this branch. Later on 21 September: Minor 9 (wide tables) was
> reproduced and deferred to an opt-in `.cu-table-scroll` wrapper ([tables note](../design-notes/2026-09-21-tables.md));
> Minor 10 (right-logo headers) was fixed, along with a two-logo case the review did not mention;
> Minor 13 (callout title leading) was checked and left unchanged
> ([header and callout note](../design-notes/2026-09-21-header-logos-and-callout-titles.md)).
> Minor 11 and 12 remain open; see the
> [follow-up checklist](../plans/2026-09-21-follow-up.md). The original review below is
> preserved verbatim; its “Needs work” verdict describes the reviewed commit, not today's tree.

# Final review — `feature/cardiffuni-v3-ds-v1.3`

Base `6497709c9` · head `f139ad201` · 23 commits · 34 files.
Reviewed: `scss/`, `cardiffuni-v3.js`, `tests/check_theme.py`, `tests/fixture.html`,
`tools/build-reference.py`, the plan and docs, and the interaction with
`modules/site/parent_templates/site/common/css/custom.css`,
`modules/site/parent_templates/site/common/js/application.js` and
`modules/site/player_html5/rloObject.htm`. Compiled CSS and the `.map` were judged for
consistency with the SCSS only, as instructed.

Two focused commands were run (both read-only):

- `npx -y sass@1 cardiffuni-v3.scss /tmp/cu-verify/out.css --source-map` — the output is
  **byte-identical** to the committed `cardiffuni-v3.css` apart from the
  `sourceMappingURL` comment, which differs only because I wrote to another filename. The
  committed `.css.map` carries correct repo-relative `sources`. The compiled artefacts and
  the SCSS agree.
- `python3 tools/build-reference.py --check` → `In sync … (264 classes documented)`, and
  `--coverage` → `0 theme classes no guide page documents or shows`. The generator and its
  committed output agree.

## Summary

This is careful, well-evidenced work. The generator-driven token pipeline does what the
plan set out, the compiled artefacts are reproducible, and nothing outside
`themes/site/cardiffuni-v3` changed. The strongest thing about the diff is its
traceability: almost every override in `_layouts.scss` names the base rule it beats and
the test round that found the fault.

The weak spot is the new runtime layer. `cardiffuni-v3.js` is safe — it cannot throw on
absent elements and the CSS falls back correctly when it never loads — but it measures the
wrong element in one of the two navbar configurations the theme explicitly supports, and
the CSS it feeds is overridden outright by an inline style the player sets on larger
projects. Neither is covered by a check, because the fixture never loads the script.

No Critical findings. Six Important findings, all small and well-scoped; four of them are
a few lines each.

## Strengths

- **Reproducible build.** A fresh `sass@1` compile reproduces the committed CSS exactly.
  That is rare and it makes the 4,589-line CSS diff reviewable by proxy.
- **Constraint 1 holds.** `git diff --stat` shows every changed path under
  `themes/site/cardiffuni-v3/`. `cardiffuni-v2` untouched.
- **Constraint 3 holds.** No new raw hex in theme CSS. Every hex left in `scss/` is either
  the generated `_cu-tokens.scss` block (which is the token definition, as designed),
  `$token-color-tint` (explicitly sanctioned by the plan, with the sanctioning comment
  carried over), documentation comments, or files this diff did not touch
  (`_bootstrap-components.scss`, `components/_links.scss`, `.evenSection`/`.oddSection`).
- **Overrides are documented against their cause.** `_layouts.scss:53-56`, `68-72`,
  `126-128`, `133-136`, `144-147`, `237-240`, `294-295`, `317-319` each quote the base
  `custom.css` rule being beaten and, where relevant, the test-round observation. I was
  able to verify each claim against the real `custom.css` and each one was accurate.
- **The demos exercise the real cascade.** `demos/assets/bootstrap/custom.css` is
  byte-identical to the player's `custom.css`. The demos are therefore not a flattering
  environment.
- **Some checks are genuinely behavioural, not token echoes.** The navbar-toggle
  containment check (`check_theme.py:116-119`) forces the toggle taller than the bar and
  asserts geometry, then restores the DOM. The "title sits beside the logo, one gap away"
  check (`134-139`) computes the expected x from the measured gap. The float-containment
  check (`109-110`) proves `flow-root` still works after `overflow: visible`. These are
  the kind of checks that would actually catch a regression.
- **The JS degrades correctly by construction.** Every consumer uses
  `var(--cu-sticky-nav, 0px)` (`_layouts.scss:245, 321, 322`), and three checks
  (`check_theme.py:122-124`) assert exactly the no-JS fallback values. The script is also
  correctly ordered behind Bootstrap's own `load` scrollspy initialiser by the 150 ms
  debounce, so `$('body').data('scrollspy')` is populated when `apply()` runs.
- **Honest records.** `docs/test-rounds/2026-09-phase1.md` records the two red-use
  deviations as decisions taken on the day rather than quietly absorbing them, and flags
  the malformed upstream `<script>` tag in `application.js:397` for reporting rather than
  working around it.

## Critical

None.

## Important

### I1. The theme script measures the wrong element when the navbar sits below the header

`themes/site/cardiffuni-v3/cardiffuni-v3.js:21-31`

```js
var nav = document.getElementById('topnav');
...
var position = window.getComputedStyle(nav).position;
if (position !== 'sticky' && position !== 'fixed') { return 0; }
```

In the below-header configuration the player moves `#topnav` into a new wrapper and makes
**the wrapper**, not `#topnav`, sticky:

- `application.js:1269-1270` — `$('#overview').after('<div id="pageLinks"></div>'); $('#topnav').appendTo('#pageLinks');`
- `application.js:1920-1924` — `if ($("#pageLinks").length > 0) { $("#pageLinks").addClass("stickyTop"); } else { $(".navbar-fixed-top").addClass("stickyTop"); }`
- `custom.css:128` — `#pageLinks.stickyTop, .navbar-fixed-top.stickyTop { position: sticky; top: 0 }`
- `custom.css:120` — `.navbar-fixed-top { position: static }`, which the theme does not override.

So with `navbarPos=below` and `fixedheader=true`, `#topnav` computes to `position: static`,
`stickyNavHeight()` returns 0, and `--cu-sticky-nav` stays 0 — the section menu sits under
the bar and anchor scrolls land behind it, which is the exact fault the script exists to
fix. This matters because the theme explicitly supports and styles that configuration
(`_layouts.scss:129-131`, and `fixture.html:19-21` even models it).

Fix: measure the sticky ancestor, not `#topnav` alone. Something like

```js
var nav = document.getElementById('pageLinks') || document.getElementById('topnav');
```

or walk up from `#topnav` to the nearest ancestor whose computed `position` is
`sticky`/`fixed`, and measure that.

### I2. An inline style from the player defeats the affix clearance on larger projects

`themes/site/cardiffuni-v3/scss/_layouts.scss:320-324` vs `application.js:1317`

```js
if (itemCount > 10) { $(".bs-docs-sidenav.affix").css("top", "65px"); }
```

That is an inline style, so it beats the theme's
`.bs-docs-sidenav.affix { top: calc(var(--cu-sticky-nav, 0px) + var(--cu-space-6)) }`
unconditionally — no specificity contest, the theme rule simply never applies. Any project
with more than ten pages in the page menu gets a hardcoded 65px offset instead of the
measured one. The Assessment Menu is likely to exceed ten pages.

This one can't be fixed in CSS without `!important` (which the plan discourages), so the
natural place is the script that already runs: have `apply()` set the affix element's
`top` directly when `--cu-sticky-nav` is non-zero, or clear the stale inline `top` it
finds. Either way, note it explicitly — at present the theme silently loses this fix on
exactly the projects it was written for.

### I3. The affix `max-height` / `overflow-y` is applied even when the menu is not affixed

`themes/site/cardiffuni-v3/scss/_layouts.scss:320-324`

```scss
&.affix {
  top: calc(var(--cu-sticky-nav, 0px) + var(--cu-space-6));
  max-height: calc(100vh - var(--cu-sticky-nav, 0px) - var(--cu-space-12));
  overflow-y: auto;
}
```

The base template takes the `.affix` class out of fixed positioning in two cases while
leaving the class on the element:

- `custom.css:~450` (`@media (max-width: 767px)`) — `.bs-docs-sidenav.affix { position: static; width: auto; top: 0 }`
- `custom.css:213` — `.bs-docs-sidenav.affix.staticPosition { position: static }`, applied
  by `fixSideBar()` (`application.js:364-373`) whenever the menu is taller than the window.

In both cases the theme still imposes a viewport-height cap and an inner scrollbar on a
menu that is now in normal flow — so a long section menu on a phone, or any menu taller
than the viewport on desktop, becomes a nested scroll box instead of flowing with the
page. Scope the two declarations, e.g.

```scss
&.affix:not(.staticPosition) { … }
```

inside `@media (min-width: 768px)`, leaving only `top` unscoped.

### I4. The CSS-drawn callout disc disappears entirely on browsers without `content` alt-text syntax

`themes/site/cardiffuni-v3/scss/components/_callout.scss` (compiled at
`cardiffuni-v3.css:2067`)

```css
content: var(--cu-callout-glyph, "\f005")/"";
```

The `<string> / <alt-text>` form is comparatively recent (Firefox 122, Safari 17.4). Where
it is not understood the *whole* `content` declaration is invalid, so the `::before` never
generates — but `padding-left: calc(var(--cu-space-6) + 28px + var(--cu-space-4))` on
`.cu-callout:not(:has(.cu-callout-icon))` still reserves the gutter. The result is a
callout with a 68px empty column and no icon, which reads as a layout bug rather than a
missing decoration.

One free line fixes it, since a later valid declaration wins and an invalid one is
discarded:

```css
content: var(--cu-callout-glyph, "\f005");
content: var(--cu-callout-glyph, "\f005") / "";
```

(The related `:has()` dependency is fine — support is broad enough now, and when it is
absent the callout falls back to `display: block` with its surface and left rule intact,
which is a reasonable degradation.)

### I5. The new JavaScript has no test coverage at all

`themes/site/cardiffuni-v3/tests/fixture.html` never loads `../cardiffuni-v3.js`. The three
checks that mention it (`check_theme.py:122-124`) assert the CSS *fallbacks* that apply
when it is absent — which is worth having, but means 88 checks cover zero lines of the only
executable code the theme has ever shipped. I1 is precisely the kind of defect a check
would have caught: add a second fixture (or a `?sticky=1` variant) that gives `#topnav` /
`#pageLinks` `position: sticky`, loads the script, and asserts that `--cu-sticky-nav`
equals the bar's height in both navbar configurations.

At minimum, wrap the body of `apply()` in a `try`/`catch`. The brief's bar is "cannot
throw"; today that holds by inspection of jQuery and Bootstrap 2.3 internals rather than by
construction, and it is one line to make it structural.

### I6. `build-reference.py` can emit broken output for values it does not currently see

`themes/site/cardiffuni-v3/tools/build-reference.py:190, 205, 254`

Two gaps, both latent today (I checked the committed block: 288 rows, all tags balanced, no
`<`, `>`, `&` or `\` in any cell):

1. **No escaping.** Cell values go straight from the compiled CSS into
   `<td>{v}</td>` with no `html.escape()`. Any future utility whose value contains `<`,
   `>` or `&` silently corrupts the guide.
2. **Generated HTML used as an `re.sub` replacement template** (line 254):

   ```python
   fresh = re.sub(re.escape(START) + r".*?" + re.escape(END),
                  START + "\n" + tables + "\n" + END, guide, flags=re.S)
   ```

   Backslashes in `tables` are interpreted as escapes/group references. A utility class
   whose value contains a CSS escape (`content: "\f0eb"`, `\2014`, …) would raise
   `re.error: bad escape` or silently mangle the guide. The theme already uses exactly that
   kind of value in `--cu-callout-glyph`; it is only excluded today because those rules
   aren't single-class utilities.

   Fix both cheaply: `html.escape(v)` at lines 190/205, and a function replacement at 254:
   `re.sub(pattern, lambda _: START + "\n" + tables + "\n" + END, guide, flags=re.S)`.

## Minor

1. **Three new dead primitives.** `scss/_tokens.scss:144-146` defines
   `$token-breakpoint-narrow/-tablet/-collapse`, and nothing references them — every media
   query in `scss/` is a literal. The commit that added them is
   `324e32854 refactor(…): prune dead primitives`. Either use them in the `@media` rules
   (`_layouts.scss:73, 148, 176`, `_callout.scss`) or drop them.
2. **Stale comment.** `scss/_tokens.scss:14` still says
   `2. Reference primitives: t.$token-color-brand-primary` — that variable was deleted in
   this diff.
3. **Old focus red survives as a fallback.** Nine occurrences of
   `outline: var(--focus-ring, 2px solid #7F140E)` (`_base-elements.scss:67, 495, 538, 560`;
   `_bootstrap-components.scss:66, 145, 279, 393, 657`). `#7F140E` is the *pre-change*
   focus colour; the plan moved focus to black. The fallback is unreachable while
   `--focus-ring` is defined, so this is cosmetic, but it is a wrong value sitting in the
   file the next person will read. Outside the diff's hunks, but the diff is what made it
   wrong.
4. **Version drift in the docs.** `MIGRATION.md:46` and
   `docs/design-notes/2026-09-20-documentation-system.md:55` say `v1.4`; the `.info`
   description, `cardiffuni-v3.scss`, `_allvariables.scss` and the plan all say v1.3.
   Resolve which it is.
5. **A brittle expected value.** `check_theme.py:102` expects the literal string
   `"color(srgb 0.993647 0.948706 0.946353)"` — a Chrome-specific serialisation of
   `color-mix()` to six decimal places. A Chrome update that changes serialisation
   precision breaks the check with no real regression. Prefer comparing against
   `v('color-mix(in srgb, var(--cu-red) 6%, var(--cu-bg))')` computed through the same
   probe, so both sides move together.
6. **Two checks can pass vacuously.** `check_theme.py:130-133` use
   `String(cs(a,…)===cs(b,…))`; `cs()` returns the string `'MISSING'` for an absent
   element, so `'MISSING' === 'MISSING'` → `true` → PASS if both selectors stop matching.
   The blast radius is small (sibling checks at 127-129 assert concrete values on
   `#section-title` and would fail), but the pattern is worth avoiding. Have `cs()` return
   a unique sentinel per call, or assert a concrete value alongside.
7. **The focus-ring check tests a token, not a control.** `check_theme.py:111-113` sets
   `#focus-btn`'s inline `outline` to `var(--focus-ring)` and reads it back — it proves the
   token resolves, not that any element receives the ring on focus. It also leaves the
   inline style set (unlike the navbar-toggle check at 116-119, which restores it). Nothing
   downstream reads `#focus-btn`, so it is harmless today.
8. **The fixture's "player order" is approximate.** `fixture.html:7-11` loads four of the
   player's stylesheets. `rloObject.htm` also loads, before the theme, `fonts.css` (66),
   `v4-shims.min.css` (71), `v5-font-face.min.css` (72), `highlight/css/default.css` (58),
   featherlight and mediaelement. `fonts.css` is empty today so nothing is currently
   mis-measured, but the fixture's comment claims player order and doesn't deliver it.
   Worth a note in the fixture, or add the missing links.
9. **`section { overflow: visible }` removes a per-section scroll container.**
   `_layouts.scss:241-246`. The base's `section { overflow: auto }` (`custom.css:265`) gave
   wide content its own horizontal scrollbar; `flow-root` contains floats but does not
   scroll. `pre` has its own `overflow-x: auto` (`_base-elements.scss:403`) and Bootstrap
   caps image width, so the realistic exposure is a wide table with `nowrap` cells causing
   page-level horizontal scroll. The fix itself is right — just worth adding
   `overflow-x: auto` on `table` (or a wrapper) rather than relying on authors.
10. **`logoR` headers are handled asymmetrically.** `_layouts.scss:62-66` resets
    `#overview.logoR .titles`, but the `@media (max-width: 980px)` block (73-87) covers only
    `logoL`. Below 980px the base's
    `#overview.logoR .titles, #overview.logoL .titles { text-align: center; float: right; width: 100% }`
    wins back for `logoR`, so a right-logo header reverts to centred and stacked while a
    left-logo one does not. Probably unused in practice; cheap to make symmetric.
11. **`--coverage` can be fooled.** `build-reference.py:226` collects "mentioned" classes
    with `re.findall(r"\.(-?[A-Za-z_][\w-]*)", html)` over the whole page, so any dotted
    token in prose (`index.html`, `sync-theme.py`, `tools/build-reference.py`) counts as a
    class mention. The clean `0 undocumented` result is therefore weaker evidence than it
    looks — see the `.list--tick` triage below for a case it does not catch.
12. **The hand-rolled CSS parser is string-naive.** `build-reference.py:84-121` tracks
    braces without tracking string literals, so a `{` or `}` inside a CSS string would
    desynchronise it. Comments are stripped first, which covers the common case.
13. **`.cu-callout-title { line-height: 28px }`** (`_callout.scss`) is deliberate — it
    matches the disc so the two share a line box — but it is a fixed 28px on a title that
    can wrap, giving loose leading on a two-line title. Consider applying it only to the
    first line via the `::before`'s own alignment.

## Triage of deferred items

| # | Item | Verdict |
|---|---|---|
| 1 | `tests/check_theme.py` hardcodes the macOS Chrome path | **Fine to defer.** Plan-mandated, single-developer tool, and it fails loudly with a message that names the cause (`check_theme.py:131`). A one-line `os.environ.get("CHROME", …)` would remove the objection whenever convenient. |
| 2 | `sync-theme.py` greedy regex on `tokens.css` | **Fine to defer.** It lives outside this repo, so it is out of scope for this merge, and the generated `_cu-tokens.scss` is committed and verifiable. The greedy `\{(.*)\}` is only safe while `tokens.css` has exactly one `.cu-resource` block — worth a guard in the vault copy, not a blocker here. |
| 3 | `scss/components/_rules.scss` doesn't reset `background-color` | **Fine to defer.** `height: 0` with `border: 0` means the base `hr` background paints nothing. Note that `.cu-rule-strong` used *without* `.cu-rule` gets no reset at all, so the documented pairing is load-bearing — the file's header comment already states it. |
| 4 | Narrow-width header fix relies on the theme loading after `custom.css` | **Fine to defer — verified true.** `rloObject.htm:66` links `custom.css` statically; the theme is injected at runtime by `insertCSS` (`application.js:398`) and therefore always lands later in the cascade. The assumption is structural, not incidental. |
| 5 | `.list--tick` / `.list--cross` position icons against the list, not each item | **Fine to defer, with one action.** It is a pre-existing component bug, not introduced here, and the demos route authors to Font Awesome instead. But the class is still shipped and still documented-adjacent: `build-reference.py --coverage` reports it as covered only because the demo prose mentions it (Minor 11). Add both classes to `LEGACY` in `build-reference.py:61-70` with "known bug: multiple icons stack — use Font Awesome" so the generated guide warns authors off, or record it in the mapping backlog. That is a two-line change, not a fix. |

## Verdict

**Needs work** — but narrowly, and none of it is deep.

Plan alignment is good and the constraints hold: nothing outside the theme changed, no new
raw hex, page content is flat and square, and the two departures from the "no change to
existing red use" constraint (charcoal navbar, quieter selected sidebar item) are the ones
the author approved on 20 September and are recorded as decisions in
`docs/test-rounds/2026-09-phase1.md`. The plan file itself still carries the superseded
constraint text; that is acceptable given the test-round record, but a one-line amendment
to the plan's Global Constraints would close the loop for anyone reading the plan alone.

What should be fixed before merge: **I1** and **I2**, because together they mean the new
script delivers nothing in the below-header configuration and nothing on projects with more
than ten navbar pages — plausibly both true of the Assessment Menu it was written for.
**I3** and **I4** are each a few lines and prevent visible layout faults on narrow screens
and older Safari. **I5** and **I6** are the right follow-ups but need not block.

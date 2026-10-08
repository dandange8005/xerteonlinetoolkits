# A structured author guide for the Cardiff University theme

*Design spec, 6 October 2026. Status: revised after review on 6 October, awaiting approval.
Nothing here is built.*

This spec turns the "Author guide" section of [migration status](../../MIGRATION.md) into a
design. It builds on the [documentation system proposal](2026-09-20-documentation-system.md)
of 20 September, which was written to be argued with. Where the two differ, this spec is the
decision. The proposal's reasoning about drift still applies and is not repeated here.

## Purpose

Content authors who build Xerte pages with the `cardiffuniversity` theme need to know what the
theme offers, which element to use for a job, what HTML to paste, and how to get the most from
each element. Today that lives in `demos/`, thirteen hand-written pages ordered by technology
(Bootstrap, flexbox, forms, colours). The 20 September audit found it had drifted from the
theme: 226 classes nobody documented, demos of classes the theme does not have.

The goal is a structured, hosted guide for authors, led by tasks, with a component reference
behind it, that stays in step with the theme because the build checks it.

**Audience.** Content authors, not theme developers. Maintainer material stays in
`THEMING-GUIDE.md` and `MIGRATION.md`.

**Success looks like**
- An author can open the home page, choose what they want to do, and reach a component page with
  a live preview and code they can paste into Xerte.
- A change to the theme that removes or renames a class a page relies on, or adds a class no page
  covers, fails the build or warns. The checks prove the classes exist; they do not prove the
  theme looks right, which still needs the Docker test rounds.
- The guide is a static site that GitHub Pages can serve.

## Decisions

| Decision | Choice | Reason |
| --- | --- | --- |
| Delivery | Hosted static web pages | Always current, searchable later, examples use the real CSS |
| Host | GitHub Pages (public) | Nan's choice. See [Open items](#open-items) for the licence question. |
| Structure | Task-first, then component reference | Authors think in jobs, not class names |
| Build approach | Small Python generator; one record per component with TOML front-matter and a Markdown body | One source per fact; drift fails the build; no install step |
| Visual direction | Home and task pages follow direction B; component pages follow direction A | Chosen by Nan on 6 October 2026 |
| Search, playground | Deferred | Not needed for a guide this size; direction C stays an option |

Direction A is a documentation layout: a persistent side menu, an "on this page" list and one
scrolling page per component. Direction B opens with "What do you want to do?" task tiles and a
four-step pattern (choose, copy, adjust, check). Direction C, a live playground where the author
picks a callout type and edits its text while the preview and code update, is a possible later
tab on component pages. The HTML mock-ups were reviewed in the working session and were not
added to the repository.

## Layout and build flow

```
theme-src/cardiffuniversity/
  guide/
    site.toml           navigation: component groups and their order, top menu, task order
    content/
      components/       one record per component, for example callout.md
      tasks/            one file per task page
      pages/            index.md, getting-started.md
    templates/          page, component, task and navigation templates
    assets/             the guide's own stylesheet and script only
  tools/
    theme_css.py        shared by both tools: class extraction, LEGACY, FRAME_PREFIXES,
                        utility tables (moved out of build-reference.py)
    build-guide.py      standard library only; reads guide/, writes site/
    build-reference.py  keeps writing demos/code-utilities.html until demos/ is retired
  site/                 git-ignored output served by GitHub Pages
```

- `./build.sh guide` runs `tools/build-guide.py` after the normal theme build. `./build.sh`
  without the argument behaves as it does today.
- All links are relative, so the site works at any URL path, including a project page such as
  `user.github.io/repo/`.
- The runtime theme folder `themes/site/cardiffuniversity/` is not touched. `demos/` stays until
  phase 3.
- The generator needs Python 3.11 or later for `tomllib`. This Mac has 3.14 and GitHub's Ubuntu
  runners have 3.12.

### What the guide loads, and in what order

Examples must look as they do in the player, so the guide loads what the player loads, copied
into `site/` from `modules/site/parent_templates/site/common/` (the player is the source; the
copies in `demos/assets/` are identical today but are not used):

1. `css/bootstrap.css`, then `css/bootstrap-responsive.css`
2. `css/custom.css`
3. `fontawesome-6.6.0/css/all.min.css`, `v4-shims.min.css` and `v5-font-face.min.css`, with
   `webfonts/`. The v4 shims matter because authors paste older icon names.
4. `cardiffuniversity.css`, last, as the player appends it after the page has loaded
5. `js/jquery-1.9.1.min.js` and `js/bootstrap.js`, so interactive Bootstrap examples (tabs,
   accordions) work. The demos use jQuery 1.12.4; the guide uses the player's version.

`css/fonts.css` is left out because it holds only a commented placeholder today. If fonts are
added to it, it joins the list after `bootstrap-responsive.css`. `cardiffuniversity.js` is not
loaded: it corrects the player's sticky menu and scrollspy, which the guide does not have.

### The theme styles the whole page

The theme's CSS is not scoped. It styles headings, links, tables and Bootstrap classes wherever
they appear, so the guide's own header and menus are styled by the theme too. That is acceptable
and keeps the guide on brand, with two rules:

- The guide navigation uses only its own `g-` prefixed classes and never Bootstrap class names
  (`.nav`, `.navbar`, `.row`, `.span*`, `.btn`), so the theme's rules for those cannot reshape it.
- Page-frame parts (header and logos, navbar, section menu, footer, feedback tab, back-to-top)
  cannot be shown inside a preview box: they are fixed, sticky or tied to the player's IDs, and
  authors set them in Xerte rather than paste them. They are covered in Getting started as
  settings, with screenshots, not as component pages. `FRAME_PREFIXES` already excludes their
  classes from coverage (it also excludes tabs, accordions and other Bootstrap widgets the theme
  deliberately left as they are).

## Pages and navigation

| Page type | Appearance | Source | Phase 1 |
| --- | --- | --- | --- |
| Home | Direction B: hero, task tiles, four-step strip | `pages/index.md` | 1 |
| Getting started | Direction A layout: choose the theme, logos, colourways, page-frame settings | `pages/getting-started.md` | 1 |
| Task page | Goal, components to use, worked example, checklist | `tasks/*.md` | 1 (draw attention) |
| Component page | Direction A layout | `components/*.md` | 1 (callouts) |
| Reference | An overview, Colours, Type, space and shape, and Utility classes, all generated from the theme | generated | 2a |

- The home page has no search box. Direction B's mock-up showed one, but search is out of scope,
  and a box that does nothing would mislead. It comes back with search.
- The top menu has Home, Getting started, Tasks, Components and Reference. An Accessibility entry
  joins when that page exists. (The Reference entry replaces "Colours and type": the section holds
  colours, type and spacing, and utility classes.)
  Its entries, the component groups and their order, and the task order live in
  `guide/site.toml`. Menu items whose pages do not exist yet are left out, not shown as dead
  links.
- A task page names its components, and each component page lists the tasks that use it. Only the
  task file holds the link: the component page works its task list out from the task files, so
  the two cannot disagree. The home page's task tiles come from the task files, in the order
  `site.toml` gives.
- Below 800px the side menu collapses behind a button. Below 1100px the "on this page" list is
  hidden.
- Components not yet migrated link to their existing `demos/` page.

### Component page sections, in order

Revised on 7 October 2026 after the NHS digital service manual's design system pages
(<https://service-manual.nhs.uk/design-system>): example first, code behind a toggle, and fixed
guidance headings. Branding, colours and fonts stay Cardiff.

1. Title and one-line lead.
2. The first example, with no heading: its variant class and purpose, the rendered example in a
   frame, and an "HTML" toggle that reveals the code, the copy button and the line
   "In Xerte: add a Text content item, open its Source view, then paste."
3. When to use it.
4. When not to use it.
5. How to use it, with a Do list and a Don't list.
6. Variants: every other variant, each with its own label, class, purpose, frame and HTML toggle.
7. Parts: a table of the component's parts.
8. Accessibility.
9. Evidence: status, the design system version it dates from, and the editor evidence (result,
   date and Xerte version), or "Not tested in the Xerte editor yet" when the record has no
   `[editor]` table.
10. Related components and tasks, then "Page updated" (the last commit to the record, left out
    when git cannot say) and previous and next links.

## The component record

One file per component. TOML front-matter between `+++` lines holds the facts and examples,
read with Python's `tomllib`. A Markdown body holds the prose.

```toml
+++
name = "callout"
title = "Callouts"
group = "emphasis"                        # an id from site.toml
status = "current"                        # current | legacy
since = "v1.4"
related = ["alert", "well"]
scss = ["scss/components/_callout.scss"]  # for the stale-evidence check

# [editor] is optional. Leave it out until the component has been tested in the Xerte editor;
# the page then says "Not tested in the Xerte editor yet".
[editor]
survives = true
checked = 2026-09-20                      # a TOML date
xerte = "3.14"                            # a string: as a number, 3.10 would read as 3.1

[parts]
cu-callout = "The container. On its own it gives the Key point style."
cu-callout-title = "The short bold title. Always say the type in words."
cu-callout-icon = "Only for the older fa-stack markup, which still works."

[[examples]]
class = "cu-callout-tip"                  # omit for a component with no variants
label = "Tip"
purpose = "A shortcut or recommendation"
html = '''
<div class="cu-callout cu-callout-tip">
  <strong class="cu-callout-title">Tip</strong>
  <p>Explain the recommendation here.</p>
</div>
'''

[[examples]]
class = "cu-callout-warning"
label = "Warning"
purpose = "A risk the reader must avoid"
html = '''...'''
+++

## When to use it
Use a callout when one idea must stand out.

## When not to use it
Do not use a callout for text every reader needs anyway.

## How to use it
### Do
- Use one callout per idea.
### Don't
- Stack more than two in a row.

## Accessibility
The type is stated in the title, so meaning never relies on colour alone.
```

- An example's `html` is written once. The page renders it and shows it as code from the same
  string, so the two cannot disagree.
- The variants table comes from `examples`, and the parts table from `parts`. A class is either
  a variant or a part, never both.
- The body allows a small Markdown subset: `##` and `###` headings, paragraphs, `-` and `1.`
  lists, `**bold**`, `*italic*`, inline code and `[links](url)`. Anything else, including raw
  HTML, fails the build with the file and line, so nothing is silently mangled. The allowed
  headings are fixed (`When to use it`, `When not to use it`, `How to use it`, `Do`, `Don't`,
  `Accessibility`); an unknown heading also
  fails. Task and page files use the same subset with their own fixed headings.
- A malformed record fails the build and names the file and the problem. `tomllib` reports TOML
  errors with a line number.

## Build checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Every class in every example, part and variant exists in the stylesheets the guide loads (the list above), not only the theme's CSS, so Font Awesome and unstyled Bootstrap classes pass | Fails the build |
| 2 | Coverage: every author-facing theme class is claimed by a record (`parts` or an example's `class`) or appears in a generated reference table | Warns in phases 1 and 2 and prints the count; fails from phase 3 |
| 3 | Every `related` and `group` value, every component a task file names, and every task `site.toml` lists points at something that exists; groups are checked against `site.toml` | Fails the build |
| 4 | A record's `editor.checked` date is older than the last commit to any file in its `scss` list | Warns |
| 5 | An example has an `<img>` without `alt`, an empty heading, or unbalanced tags (an unclosed element, a stray end tag, or crossed elements; elements whose end tag HTML makes optional, such as `p` and `li`, are not counted) | Warns |

**What check 2 counts.** "Author-facing theme classes" reuses the definition `build-reference.py`
already has: the classes the theme's CSS adds beyond Bootstrap, `custom.css` and Font Awesome
(`theme_classes()`), less the deliberately untaught `LEGACY` classes and the page-frame
`FRAME_PREFIXES`. On 6 October 2026 that is 374 theme classes, 355 of them author-facing. The
generated utility tables already cover 259, which leaves 96 for component records. Only 13
theme classes start with `cu-`, so a check limited to that prefix would miss nearly everything.

The two lists move from `build-reference.py` into `tools/theme_css.py` so both tools read one
copy. There is no separate list of internal classes.

**Who owns what.** Until phase 3, `build-reference.py` keeps writing the utility tables into
`demos/code-utilities.html`, and its coverage check (which counts any mention in `demos/`) keeps
running. From phase 2 the guide's reference page renders the same tables through
`tools/theme_css.py`. In phase 3, check 2 replaces `build-reference.py --coverage`, and
`build-reference.py` is retired with `demos/`.

Today `build.sh` only warns when the author guide drifts (`build-reference.py --check`). The new
checks are stricter on purpose, because a warning is easy to ignore.

## Keeping the guide current

1. Generate what can be generated (tables of utility classes, colours and tokens).
2. Render every example with the stylesheets the player loads, in the player's order.
3. Fail the build on drift (checks 1 to 3).
4. Run the checks automatically, and fail when the committed CSS is out of date (next section).
5. Flag stale editor evidence (check 4).

What this cannot do: the usage advice ("one callout per idea") is judgement, and the checks do
not prove the theme looks right in the real Xerte player. The Docker test rounds still do that.
Rule for maintainers: a change to a component's SCSS needs a look at its record.

## Publishing

- A new GitHub Actions workflow, separate from the existing manual SonarCloud one, runs on every
  pull request that touches `theme-src/cardiffuniversity/**` or `themes/site/cardiffuniversity/**`.
- It checks out the full history (`fetch-depth: 0`), because check 4 reads commit dates and a
  shallow clone would make every record look stale.
- It runs `./build.sh guide` (Node for `sass`, Python 3.11 or later), then fails if the compiled
  `cardiffuniversity.css` differs from the committed one. Otherwise an SCSS change committed
  without recompiling would give a guide showing a theme that is not the one shipped.
- On a merge to the chosen branch it publishes `site/` to GitHub Pages.
- Which repository and branch publish is decided at this step. The build does not depend on it.
- Until the open items below are settled, nothing is published.

## Testing

- **Unit tests** (standard library `unittest`, in `tests/`) for record loading, the Markdown
  subset (each allowed construct, and rejection of anything else), each of the five checks, and
  the navigation and link generation. Each check has a bad-input test that must fail or warn as
  the table says.
- **Browser check** in headless Chrome, in the style of `tests/check_theme.py`: examples are
  styled by the theme, there is no horizontal scroll at 485px or 1280px, the phone menu opens and
  closes, and the guide navigation keeps its layout under the theme's global rules.
- **Manual:** keyboard traversal of the side menu and copy buttons, a read at 200% zoom, and the
  copy button on a served page, since clipboard access can fail on `file://`.

## Rollout

1. **Phase 1.** A thin slice through the whole path: `tools/theme_css.py`, the generator, the page
   model and `site.toml`, the home page, Getting started, one task page ("Draw attention to
   something") and one component, callouts. The task page is needed so the home page has a tile
   and the callout page has a task to link to.
2. **Phase 2**, in three plans so each batch can be reviewed:
   - **2a.** The foundations and the reference pages: optional editor evidence ("Not tested in the
     Xerte editor yet"), one source for task and component links, a check for unbalanced example
     HTML, and the Colours, Type, space and shape, and Utility classes pages.
   - **2b.** Buttons, cards, tables, alerts, images, layout and typography, in small batches.
   - **2c.** Two or three more task pages.
3. **Phase 3.** Migrate the remaining `demos/` pages one at a time. Make check 2 a hard failure,
   retire `build-reference.py` and `demos/`.

Each phase ends with a site that builds, passes its checks and could be published.

## Out of scope

Search, Welsh translation, the playground, any change to the theme's CSS, and any change to
Xerte itself.

## Open items

- **Licence and publishing.** The README says the theme is for internal Cardiff University use.
  A public site shows Cardiff branding and colours. Confirm this is cleared before the first
  publish. The guide header shows the theme's Cardiff logo (`logo_left.svg`), added on 6 October
  2026 at Nan's request to match the approved design directions; that makes the clearance a
  condition of publishing, not of building.
- **Repository.** `origin` is `dandange8005/xerteonlinetoolkits`, the account named as the
  theme's author, which may not be the repository Nan wants to publish from.
- **Maintenance owner.** `MIGRATION.md` asks who maintains a published guide. Not decided.
- **Component records.** Settled: they live in the theme, not the shared design system. See
  [ADR 0001](../adr/0001-component-records-live-in-the-theme.md).
- **Tokens.** Phase 2 reads `tokens.json` for the token tables. If the first reference pages show
  tokens are not enough for authors, revisit.

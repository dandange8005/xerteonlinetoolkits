# A structured author guide for the Cardiff University theme

*Design spec, 6 October 2026. Status: awaiting review. Nothing here is built.*

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
- Changing the theme's CSS cannot leave the guide silently wrong: the build fails or warns.
- The guide is a static site that GitHub Pages can serve.

## Decisions

| Decision | Choice | Reason |
| --- | --- | --- |
| Delivery | Hosted static web pages | Always current, searchable later, examples use the real CSS |
| Host | GitHub Pages (public) | Nan's choice. See [Open items](#open-items) for the licence question. |
| Structure | Task-first, then component reference | Authors think in jobs, not class names |
| Build approach | Small Python generator plus one Markdown record per component | One source per fact; drift fails the build |
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
    content/
      components/       one record per component, for example callout.md
      tasks/            one file per task page
      pages/            index.md, getting-started.md
      internal-classes.txt   theme classes that are deliberately undocumented
    templates/          page, component, task and navigation templates
    assets/             the guide's own stylesheet and script only
  tools/build-guide.py  standard library only; reads guide/, writes site/
  site/                 git-ignored output served by GitHub Pages
```

- `./build.sh guide` runs `tools/build-guide.py` after the normal theme build. `./build.sh`
  without the argument behaves as it does today.
- The build copies the compiled `cardiffuniversity.css`, the Bootstrap base the theme sits on and
  Font Awesome into `site/`. The demos load these from repository paths a hosted site cannot
  reach.
- All links are relative, so the site works at any URL path, including a project page such as
  `user.github.io/repo/`.
- The runtime theme folder `themes/site/cardiffuniversity/` is not touched. `demos/` stays until
  phase 3.
- The guide's own chrome (header, menus, panels) uses its own small stylesheet with a `g-`
  prefix. Examples sit inside a preview frame and are styled only by the theme.

## Pages and navigation

| Page type | Appearance | Source | Phase 1 |
| --- | --- | --- | --- |
| Home | Direction B: hero with search-style prompt, task tiles, four-step strip | `pages/index.md` | 1 |
| Getting started | Direction A layout, short steps | `pages/getting-started.md` | 1 |
| Task page | Goal, components to use, worked example, checklist | `tasks/*.md` | 1 (draw attention) |
| Component page | Direction A layout | `components/*.md` | 1 (callouts) |
| Reference | Colours, tokens, utility classes, mostly generated | generated | 3 |

- The top menu has Home, Getting started, Tasks, Components, Colours and type, and Accessibility.
- The component side menu is grouped (for example Content, Emphasis, Layout, Interaction). The
  group comes from each record's `group` field.
- A task page names its components, and each component page lists the tasks that use it. The
  home page's task tiles come from the task files, so adding a file adds a tile.
- Below 800px the side menu collapses behind a button. Below 1100px the "on this page" list is
  hidden.
- Components not yet migrated link to their existing `demos/` page.
- There is no search in phase 1. Plain HTML pages leave it easy to add.

### Component page sections, in order

1. Title, one-line lead, and status chips (status, since version, editor evidence, main class).
2. Preview and code: the first snippet rendered, then shown as copyable code, with the line
   "In Xerte: open the Text element, choose Source, then paste."
3. Types or variants: a rendered example per variant and a table of classes with what each is for.
4. When to use it: a Do list and a Don't list.
5. Accessibility.
6. Related components and tasks, and previous and next links.

## The component record

One Markdown file per component. The front-matter holds facts. The body holds prose under fixed
headings that map to the sections above.

```markdown
---
name: callout
title: Callouts
group: Emphasis
status: current            # current | legacy | internal
since: v1.4
tasks: [draw-attention]
classes: [cu-callout, cu-callout-info, cu-callout-tip, cu-callout-good,
          cu-callout-important, cu-callout-warning, cu-callout-example,
          cu-callout-key, cu-callout-title]
editor: {survives: true, checked: 2026-09-20, xerte: 3.14}
related: [alert, well]
snippets:
  - id: tip
    html: |
      <div class="cu-callout cu-callout-tip">
        <strong class="cu-callout-title">Tip</strong>
        <p>Explain the recommendation here.</p>
      </div>
---
## When to use it
## Do and Don't
## Accessibility
```

- A snippet's `html` is written once. The page renders it and shows it as code from the same
  string, so the two cannot disagree.
- The types table is built from `classes`, so adding a class to the record adds a row.
- The front-matter uses a small subset of YAML (scalars, flow lists, one level of mapping and
  block scalars), so the generator needs no install step. A malformed record fails the build and
  names the file and line.

## Build checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Every class in `classes` and in the snippets exists in the compiled CSS | Fails the build |
| 2 | Every `cu-` class in the CSS is claimed by a record or listed in `internal-classes.txt` | Warns in phases 1 and 2 and prints the count; fails from phase 3 |
| 3 | Every `related`, `tasks` and `group` value points at something that exists | Fails the build |
| 4 | A record's `editor.checked` date is older than the last change to its SCSS | Warns |
| 5 | A snippet has an `<img>` without `alt`, or an empty heading | Warns |

Check 2 starts as a warning because a few records cannot claim most of the theme's classes.
Today `build.sh` only warns when the author guide drifts (`build-reference.py --check`). These
checks are stricter on purpose, because a warning is easy to ignore.

Generated, not written: the utility class tables and the colour and token tables, read from the
compiled CSS and `tokens/tokens.json`. `build-reference.py` already does this for the utility
tables, and the guide should reuse its parsing rather than copy it.

## Keeping the guide current

1. Generate what can be generated (tables of classes, colours and tokens).
2. Render every example with the real compiled CSS.
3. Fail the build on drift (checks 1 to 3).
4. Run the checks automatically (next section).
5. Flag stale editor evidence (check 4).

What this cannot do: the usage advice ("one callout per idea") is judgement, and the checks do
not prove the theme looks right in the real Xerte player. The Docker test rounds still do that.
Rule for maintainers: a change to a component's SCSS needs a look at its record.

## Publishing

- A new GitHub Actions workflow, separate from the existing manual SonarCloud one, runs the
  build and checks on every pull request that touches `scss/`, `tokens/` or `guide/`. On a merge
  to the chosen branch it publishes `site/` to GitHub Pages.
- Which repository and branch publish is decided at this step. The build does not depend on it.
- Until the open items below are settled, nothing is published.

## Testing

- **Unit tests** (standard library `unittest`) for the record parser, each of the five checks and
  the navigation and link generation. Each check has a bad-input test that must fail the build.
- **Browser check** in headless Chrome, in the style of `tests/check_theme.py`: examples are
  styled by the theme, there is no horizontal scroll at 485px or 1280px, and the phone menu
  opens and closes.
- **Manual:** keyboard traversal of the side menu and copy buttons, and a read at 200% zoom.
  The copy button needs checking on a served page, since clipboard access can fail on `file://`.

## Rollout

1. **Phase 1.** The generator, page model, home page, getting started, three reference pages,
   one task page ("Draw attention to something") and one component, callouts, to prove the whole
   path. The task page is needed so the home page has a tile and the callout record's `tasks`
   link passes check 3.
2. **Phase 2.** Buttons, cards, tables, alerts, images, layout and typography, plus two or three
   more task pages.
3. **Phase 3.** Migrate the remaining `demos/` pages one at a time. Make check 2 a hard failure
   and retire `demos/`.

Each phase ends with a site that builds, passes its checks and could be published.

## Out of scope

Search, Welsh translation, the playground, any change to the theme's CSS, and any change to
Xerte itself.

## Open items

- **Licence and publishing.** The README says the theme is for internal Cardiff University use.
  A public site shows Cardiff branding and colours. Confirm this is cleared before the first
  publish. Leave the Cardiff logo out of published pages unless it is confirmed.
- **Repository.** `origin` is `dandange8005/xerteonlinetoolkits`, the account named as the
  theme's author, which may not be the repository Nan wants to publish from.
- **Maintenance owner.** `MIGRATION.md` asks who maintains a published guide. Not decided.
- **Component records.** `MIGRATION.md` also asks whether records live in the theme or in the
  shared design system. This spec keeps them in the theme. The design system remains a reference,
  consistent with the 24 September decision that it is not a build input.
- **Tokens.** Phase 1 reads `tokens.json` for the token tables. If the first reference pages show
  tokens are not enough for authors, revisit.

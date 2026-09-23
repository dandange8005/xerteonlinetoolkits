# A documentation system for cardiffuni-v3

*Design note, 20 September 2026. Written to be argued with, not followed. Nothing here is built.*

## What this is for

Content authors writing Xerte pages with this theme need to know what they can use, what it
looks like, what HTML to paste, and what the editor will do to it. Today that lives in
`demos/`, which grew out of a component gallery and still behaves like one: hand-written HTML
pages where the rendered example and the code beside it are separate strings that can disagree.

The audit on 20 September found 226 theme classes that no demo showed or mentioned, demos of
three classes the theme has never had (`.image-full`, `.w-md-25/33/50`), and a description of
`.image-screenshots` promising a shadow the theme stopped drawing. None of that was carelessness.
It is what hand-maintained documentation does over a year.

## Principles

1. **A fact is written once.** If it can be read from the compiled theme, generate it.
2. **Examples render the real thing.** The guide loads the compiled `cardiffuni-v3.css`, in the
   same order the player loads it. Examples rendered against a simplified copy start lying.
3. **Drift fails the build**, rather than waiting for someone to notice.
4. **Author first.** The default path is task-shaped. The component reference sits behind it.
5. **No install step.** Standard-library Python writing into marked regions, like `sync-theme.py`
   and `sync-guide.py`. The output ships with the theme and works offline.

## Who owns which fact

Three documents describe the same components today, and a change to the callout icon meant
editing all three. Ownership should be explicit:

| Fact | Owner | How it gets into the guide |
| --- | --- | --- |
| Why a component exists, when to use it, colour roles, accessibility rules | `DESIGN.md` in the design system | Quoted or linked, never restated |
| What a component looks like rendered | The compiled theme | Rendered live in the page |
| Class names, values, spacing steps | The compiled theme | Generated |
| The HTML an author pastes | Component record (below) | Rendered and shown from one string |
| What the Xerte editor does to that HTML | Test rounds | Field on the record, with a date |
| What changed between versions | Git history and the design system's version line | Generated changelog |

The rule of thumb: the design system says what is true of Cardiff resources anywhere; the theme
guide says how to do it in Xerte. When they disagree, the design system wins and the guide is
wrong.

## The content model

One record per component, holding everything the guide needs. Front-matter plus prose, in
`docs/components/<name>.md`, so it reads well in Obsidian and parses in twenty lines of Python:

```markdown
---
name: callout
title: Callouts
status: current            # current | legacy | frame | internal
since: v1.4
classes: [cu-callout, cu-callout-info, cu-callout-tip, cu-callout-good, cu-callout-important,
          cu-callout-warning, cu-callout-example, cu-callout-key, cu-callout-title, cu-callout-icon]
editor:
  survives: true
  checked: 2026-09-20
  xerte: 3.14
  note: The short form has no empty tags for the editor to strip.
snippet: |
  <div class="cu-callout cu-callout-tip">
    <strong class="cu-callout-title">Tip</strong><p>...</p>
  </div>
---

## What it is for
One or two per screen, for something a reader would otherwise miss...

## When not to use it
Not for content every reader needs — that belongs in the body text...

## Accessibility
The title carries the meaning. Colour and icon support it, never replace it.
```

Four properties follow from this:

- The live example and the copy-paste block are **the same string**, so they cannot drift.
- `classes:` is what the coverage check reconciles against the compiled CSS.
- `status: legacy` generates the "do not use, use X instead" table rather than a page someone
  maintains by hand.
- `editor:` puts the Xerte-specific knowledge where authors will see it, with the date and
  version it was true for.

## Structure

Task-shaped for authors, reference behind it:

```
Home            what this is, how to paste into a Text element, what to check before publishing
Tasks           add a callout · embed a video · lay out columns · link to a file · show a quote
Components      one page per record, grouped: content, layout, navigation
Reference       utilities (generated), colour roles, type scale, legacy classes (generated)
For developers  generated from the SCSS PURPOSE/USAGE/VARIANTS comment blocks
```

The "Tasks" layer is the part the current demos lack entirely, and the part an author actually
arrives with. A task page is mostly prose plus one or two component snippets pulled in by name.

## Generator contract

One script, `tools/build-guide.py`, extending what `build-reference.py` already does:

| Input | Output |
| --- | --- |
| `docs/components/*.md` | a page per component, and the snippets used by task pages |
| compiled `cardiffuni-v3.css` | utility tables with resolved values (`4px`, not `var(--spacing-1)`) |
| `scss/**/*.scss` doc comments | the developer appendix |
| git tags | the changelog |

Commands, matching the existing scripts so there is nothing new to learn:

- `build-guide.py` — write the generated regions
- `--check` — exit 1 if any generated region is out of date (for CI or a pre-commit hook)
- `--coverage` — exit 1 if any class is undocumented

## The lint rules

These are the point of the whole exercise. Each one corresponds to something that actually went
wrong here:

1. **Every theme class is claimed** by a record, or marked frame, legacy or internal.
   *(226 were claimed by nothing.)*
2. **Every class in a snippet exists** in the compiled CSS.
   *(`.w-md-50` did not, for about a year.)*
3. **Every generated region matches its source.**
   *(The utility tables had drifted from the theme.)*
4. **Every snippet parses** as well-formed HTML, and its classes resolve.
5. **Every legacy record names its replacement.**
   *(`action-link` → `link-action`.)*
6. **Every image and iframe in a snippet has alt text or a title.**
   Documentation teaches by example, so the examples must be correct.

Rule 1 needs an explicit escape hatch — `status: frame` for things the player owns, like
`.jumbotron` and `.bs-docs-sidenav`, and `internal` for developer helpers like `.focus-visible`.
Without it people will add classes to the ignore list to make the build pass, and the check
stops meaning anything.

## Things that will bite

- **Load order.** `.cu-callout-icon` versus Font Awesome's `.fa-stack` was decided by which
  stylesheet loaded last, and the demos had the opposite order from the player. Guide pages must
  load Bootstrap, `custom.css`, Font Awesome, then the theme — the order in `rloObject.htm`.
  Worth asserting in a test rather than trusting.
- **External assets.** The demos fetch placeholder images from `placehold.co`. Bundle local ones,
  or the guide renders differently on a locked-down network.
- **The theme now ships JavaScript.** `cardiffuni-v3.js` publishes the sticky navbar height and
  corrects the scroll-spy offset. That needs saying somewhere, or the next person will wonder why
  a CSS-only theme has a script.
- **Two callout markups.** Short form is the default; the design system's `fa-stack` form still
  renders. The record should show the first and mention the second, not treat them as equals.
- **Scope creep into a design system.** This guide documents one Xerte theme. The moment it starts
  restating colour rationale, it has become a second copy of `DESIGN.md`.

## Migration

Nothing needs rewriting at once, and the current guide is usable meanwhile:

1. Write records for the seven or eight components authors use most, generate those pages, and
   leave the rest of `demos/` in place.
2. Turn on rules 1–3 as warnings, then as failures once the backlog is claimed.
3. Add the task pages, which is where the real writing effort goes.
4. Retire the hand-written demo pages as records replace them.
5. Fold in the developer appendix last; it has the fewest readers.

## Decisions for you

1. **Where does it live?** In the theme (ships with it, versioned with it, but invisible to anyone
   not browsing the repo) or as a published site? Being in the theme has served the demos well.
2. **Does the design system get the same treatment?** The component records could live in the
   vault and generate both the design guide and this one. More correct, more moving parts.
3. **How much task content will you write?** The generator handles the reference; the tasks are
   genuine writing, and they are what makes it a guide rather than a catalogue.
4. **Who else edits it?** If colleagues will, a Markdown record per component is friendlier than
   HTML. If it stays yours, this matters less.
5. **Is the editor-reality data worth the upkeep?** It is the most valuable thing here and the
   most perishable; it needs a re-check each Xerte upgrade.

## What I would not do

Reach for a static-site generator on day one. The value is in the content model and the lint
rules, not the renderer. If search and versioned docs become worth a dependency later, the records
are already structured for one.

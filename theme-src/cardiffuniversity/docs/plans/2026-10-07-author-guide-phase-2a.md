# Author Guide Phase 2a Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Testing reference:** use `mattpocock-skills:tdd`, not `superpowers:test-driven-development`. Test only at the seams listed under [Seams under test](#seams-under-test). The plan already contains code that has been run against its tests, so do not delete it and rewrite it from scratch; follow each task's red, then green, steps.

**Goal:** Fix two weak spots in the phase 1 author guide, add an honest "Not tested in the Xerte editor yet" state for component records, and add three generated reference pages (colours, type and spacing, utility classes).

**Architecture:** Component records gain an optional `[editor]` table. Task files become the only place that links tasks to components; component pages work their task list out from them. Check 5 gains an unbalanced-HTML warning. A new module `tools/guidelib/reference.py` reads `tokens/tokens.json`, the compiled CSS facts from `tools/theme_css.py`, and a new `guide/reference.toml` of author-facing titles and intros; `pages.py` renders four reference pages from it.

**Tech Stack:** Python 3.11+ standard library only (`tomllib`, `json`, `html.parser`, `unittest`), headless Google Chrome for the browser checks. No new dependencies.

**Spec:** `theme-src/cardiffuniversity/docs/design-notes/2026-10-06-author-guide.md`. Glossary: `theme-src/cardiffuniversity/CONTEXT.md`. Phase 1 plan: `theme-src/cardiffuniversity/docs/plans/2026-10-06-author-guide-phase-1.md`.

## Where this fits

Phase 2 of the spec is delivered as three plans, so Nan can review the wording of each batch:

- **2a (this plan):** the foundations and the reference pages.
- **2b:** the seven components (buttons, cards, tables, alerts, images, layout, typography), in small batches.
- **2c:** two or three more task pages.

Nothing in 2a adds a component record or a task page.

## Global Constraints

- Python 3.11 or later (`tomllib`). Standard library only: no `pip install`, no third-party packages.
- Run every command from `theme-src/cardiffuniversity/` unless a step says otherwise.
- Do not edit the runtime folder `themes/site/cardiffuniversity/` by hand. Do not change the theme's SCSS or tokens. Out of scope.
- The guide navigation uses only `g-` prefixed classes, never Bootstrap class names (`.nav`, `.navbar`, `.row`, `.span*`, `.btn`).
- Guide blocks are `<div class="g-section">`, never `<section>` (the theme styles every `<section>` as a Xerte page section). Only a preview wraps examples in `<section>`.
- No deploy or GitHub Pages job. Nothing is published.
- All guide text in UK English, without em dashes, using the `CONTEXT.md` terms: content author, component, variant, part, example, text content item, page frame, guide navigation, guide page, drift. Never "snippet", "type" (for variants), "Text element", "user", "chrome".
- Facts shown on guide pages must come from the repo (the tokens, the compiled CSS, the demos, the design notes, the test rounds). Do not invent evidence, policy or numbers.
- `python3 tools/build-reference.py --check` must keep printing `In sync`.
- Work on the branch `feat/author-guide-phase-2a`, which already holds this plan. Commit after every task. End every commit message with the `Co-Authored-By` line from the session's attribution instructions.
- Unit tests run with `python3 -m unittest discover -s tests -p "test_*.py"`.
- Edit blocks below read: **Edit `path`:** replace the first block with the second. The first block must match the file exactly once.

## Review Focus

1. **A token group in `tokens.json` that `reference.toml` does not describe** (someone adds a group): the build fails and names the group; the group is never silently left off the pages. Test in Task 4: `test_token_group_without_an_entry`.
2. **A token alias that points nowhere, or loops**: a `ReferenceDataError` naming the token, not a crash or a blank value. Tests in Task 4: `test_alias_to_nothing`, `test_alias_loop`.
3. **Contrast at the AA boundary**: a colour at 4.54:1 passes and reads `4.5:1`; one at 4.48:1 fails and reads `4.4:1`. A failing ratio must never be rounded up to look like a pass. Test in Task 4: `test_aa_boundary_never_reads_as_passing`.
4. **A narrow screen**: the wide colour and utility tables scroll inside their own box and never make the page scroll sideways. Checks in Task 6: "no sideways scroll" and "the colour table scrolls inside its own box" at 485px.
5. **A new task file that uses a component**: it appears on that component's page without anyone editing the component record. Test in Task 2: `test_a_new_task_appears_on_the_component_page_without_editing_the_record`.

## Seams under test

Same boundaries as phase 1, plus one new data seam. Helpers are tested only through these.

| Seam | What the tests observe | Test file |
| --- | --- | --- |
| `records.load_component()`, `load_site()`, `load_content()` | What a record file loads as, and the error a bad one gives | `test_records.py` |
| `checks.check_*()` | The findings each check reports | `test_checks.py` |
| `reference.load_reference()`, `reference.contrast()`, `ratio_text()`, `passes_aa()` | The reference data a token file and a copy file produce | `test_reference.py` |
| `pages.write_site()` | The pages written to disk, read back with `tests/html_tree.py` | `test_pages.py` |
| `build-guide.build()` | The finished site on disk, its exit code and what it prints | `test_build_guide.py`, `test_guide_content.py` |
| The built site in Chrome | Layout and behaviour in a real browser | `check_guide.py` |

**About the first red in each task.** The first run of a new test usually fails because a field, function or module does not exist yet, which only proves the test runs. The behavioural reds are the bad-input tests and the browser checks.

## Decisions this plan makes inside the spec

Each is deliberate. Nan can overrule any of them in review.

- **Editor evidence is optional.** The spec's record format required `[editor]`. The Xerte editor has been tested only for callouts, rules and flex classes (Phase 1 test round, row 5), so requiring it would force invented evidence for the other seven components. A record with no `[editor]` shows "Not tested in the Xerte editor yet", and check 4 stays silent for it.
- **Task files are the only source of task and component links.** A component record may no longer list `tasks`. It is rejected with a message saying where to put the link.
- **Check 5 stays a warning** for unbalanced HTML, as the spec says for check 5.
- **The menu entry is "Reference", not "Colours and type".** The reference section holds colours, type and spacing, and utility classes, so neither "Colours" nor "Colours and type" fits. The Accessibility menu entry is still left out until its page exists.
- **`guide/reference.toml` holds each token group's author-facing title and intro.** `tokens.json` descriptions are written for maintainers ("Tier 1", "DESIGN.md §2"). A token group with no entry fails the build, so a new group cannot be forgotten.
- **Token notes are shown as written** in `tokens.json` (two colour tokens and one shape token have one). To change the wording, change `tokens.json`.
- **Contrast is shown as one ratio against white and one against ink, each marked "passes AA" or "fails AA"** (4.5:1, WCAG AA for body text). A ratio is the same whichever colour is the text, so there is no separate "white text on it" column.
- **Not in 2a:** the other deferred phase 1 review findings (control characters in link schemes, task icon checks, duplicate example ids, CI Node version). They stay deferred.

## File structure

| Path (under `theme-src/cardiffuniversity/` unless shown) | Responsibility |
| --- | --- |
| `tools/guidelib/reference.py` (create) | Reference data: colour and other token groups, contrast, utility and legacy tables |
| `guide/reference.toml` (create) | Author-facing title and intro for each token group |
| `tools/guidelib/records.py` (modify) | Optional `[editor]`; no `tasks` on components; `reference` menu page |
| `tools/guidelib/checks.py` (modify) | Check 4 skips untested components; check 3 drops `component.tasks`; check 5 finds unbalanced HTML |
| `tools/guidelib/pages.py` (modify) | Evidence for untested components; tasks worked out from task files; four reference pages |
| `tools/build-guide.py` (modify) | Loads the reference data, passes the utility classes to check 2, writes the reference pages |
| `guide/site.toml`, `guide/content/components/callout.md` (modify) | Reference menu entry; no `tasks` on the callout record |
| `guide/assets/guide.css` (modify) | Swatches, scrolling tables, token notes |
| `tests/test_reference.py` (create) | Reference data tests |
| `tests/guide_fixture.py`, `tests/test_records.py`, `tests/test_checks.py`, `tests/test_pages.py`, `tests/test_build_guide.py`, `tests/test_guide_content.py`, `tests/check_guide.py` (modify) | New behaviour |
| `docs/design-notes/2026-10-06-author-guide.md`, `THEMING-GUIDE.md`, `MIGRATION.md` (modify) | Keep the docs true |

---

### Task 1: Optional editor evidence

A component record with no `[editor]` table is "not tested yet". The Evidence section says so, and the stale-evidence check ignores it.

**Files:**
- Modify: `tools/guidelib/records.py`, `tools/guidelib/pages.py`, `tools/guidelib/checks.py`
- Modify: `tests/test_records.py`, `tests/test_pages.py`, `tests/test_checks.py`
- Modify: `docs/design-notes/2026-10-06-author-guide.md`, `THEMING-GUIDE.md`

**Interfaces:**
- Consumes: nothing new.
- Produces: `Component.editor` is `Editor | None`. `pages.evidence(component)` shows "Not tested in the Xerte editor yet" when it is `None`. `checks.check_stale_evidence` skips components whose `editor` is `None`.

- [ ] **Step 1: Confirm the branch**

Run: `git branch --show-current`
Expected: `feat/author-guide-phase-2a`

- [ ] **Step 2: Write the failing tests**

**Edit `tests/test_records.py`:** replace

```python
    def test_name_must_match_the_file(self):
```

with

```python
    def test_untested_component_has_no_editor_evidence(self):
        untested = fx.CALLOUT.replace('[editor]\nsurvives = true\nchecked = 2026-09-20\nxerte = "3.14"\n\n', "")
        self.assertNotIn("[editor]", untested)
        self.assertIsNone(self.component(untested).editor)

    def test_editor_evidence_must_be_complete_when_present(self):
        self.assertComponentError(fx.CALLOUT.replace('xerte = "3.14"\n', ""), r"\[editor\]: missing 'xerte'")

    def test_name_must_match_the_file(self):
```

**Edit `tests/test_checks.py`:** replace

```python
    def test_stale_evidence_ignores_unknown_dates(self):
```

with

```python
    def test_untested_component_has_no_stale_evidence(self):
        untested = component(editor=None, scss=("scss/components/_callout.scss",))
        self.assertEqual(checks.check_stale_evidence(content([untested]), lambda path: datetime.date(2026, 9, 28)), [])

    def test_stale_evidence_ignores_unknown_dates(self):
```

**Edit `tests/test_pages.py`:** replace

```python
if __name__ == "__main__":
    unittest.main()
```

with

```python
class UntestedEvidenceTest(unittest.TestCase):
    def test_untested_component_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            untested = fx.CALLOUT.replace('[editor]\nsurvives = true\nchecked = 2026-09-20\nxerte = "3.14"\n\n', "")
            guide = fx.write_guide(tmp, CALLOUT=untested)
            out = Path(tmp) / "site"
            pages.write_site(out, records.load_site(guide / "site.toml"), records.load_content(guide / "content"),
                             support.GUIDE / "templates" / "base.html")
            page = parse((out / "components" / "callout.html").read_text(encoding="utf-8"))
        evidence = page.find(cls="g-evidence")
        rows = dict(zip([dt.text() for dt in evidence.find_all("dt")], [dd.text() for dd in evidence.find_all("dd")]))
        self.assertEqual(rows["Xerte editor"], "Not tested in the Xerte editor yet")
        self.assertEqual(rows["Status"], "Current")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"`
Expected: `ERROR: test_untested_component_has_no_editor_evidence`, `ERROR: test_untested_component_says_so`, `ERROR: test_untested_component_has_no_stale_evidence`, and `FAIL`ures for the incomplete-evidence test; `FAILED`.

- [ ] **Step 4: Make `[editor]` optional**

**Edit `tools/guidelib/records.py`:** replace

```python
    editor: Editor
    parts: dict
```

with

```python
    editor: Editor | None  # None until the component has been tested in the Xerte editor
    parts: dict
```

**Edit `tools/guidelib/records.py`:** replace

```python
    editor = _field(data, "editor", dict, path)
    _only(editor, {"survives", "checked", "xerte"}, path, "[editor]")
```

with

```python
    editor = None
    editor_data = _field(data, "editor", dict, path, required=False, default=None)
    if editor_data is not None:
        _only(editor_data, {"survives", "checked", "xerte"}, path, "[editor]")
        editor = Editor(survives=_field(editor_data, "survives", bool, path, "[editor]"),
                        checked=_field(editor_data, "checked", datetime.date, path, "[editor]"),
                        xerte=_field(editor_data, "xerte", str, path, "[editor]"))
```

**Edit `tools/guidelib/records.py`:** replace

```python
        editor=Editor(survives=_field(editor, "survives", bool, path, "[editor]"),
                      checked=_field(editor, "checked", datetime.date, path, "[editor]"),
                      xerte=_field(editor, "xerte", str, path, "[editor]")),
```

with

```python
        editor=editor,
```

- [ ] **Step 5: Show "not tested" and skip the stale check**

**Edit `tools/guidelib/pages.py`:** replace

```python
def evidence(component):
    editor = component.editor
    verdict = "Survives the editor" if editor.survives else "Changed by the editor"
    rows = (("Status", esc(component.status.capitalize())),
            ("Since", f"Design system {esc(component.since)}"),
            ("Xerte editor", f"{verdict} (checked {long_date(editor.checked)}, Xerte {esc(editor.xerte)})"),
```

with

```python
def evidence(component):
    editor = component.editor
    if editor is None:
        editor_text = "Not tested in the Xerte editor yet"
    else:
        verdict = "Survives the editor" if editor.survives else "Changed by the editor"
        editor_text = f"{verdict} (checked {long_date(editor.checked)}, Xerte {esc(editor.xerte)})"
    rows = (("Status", esc(component.status.capitalize())),
            ("Since", f"Design system {esc(component.since)}"),
            ("Xerte editor", editor_text),
```

**Edit `tools/guidelib/checks.py`:** replace

```python
    for component in content.components.values():
        for path in component.scss:
            changed = last_changed(path)
```

with

```python
    for component in content.components.values():
        if component.editor is None:
            continue
        for path in component.scss:
            changed = last_changed(path)
```

- [ ] **Step 6: Update the spec and the maintainer guide**

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
[editor]
survives = true
checked = 2026-09-20                      # a TOML date
xerte = "3.14"                            # a string: as a number, 3.10 would read as 3.1
````

with

````markdown
# [editor] is optional. Leave it out until the component has been tested in the Xerte editor;
# the page then says "Not tested in the Xerte editor yet".
[editor]
survives = true
checked = 2026-09-20                      # a TOML date
xerte = "3.14"                            # a string: as a number, 3.10 would read as 3.1
````

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
9. Evidence: status, the design system version it dates from, and the editor evidence (result,
   date and Xerte version).
````

with

````markdown
9. Evidence: status, the design system version it dates from, and the editor evidence (result,
   date and Xerte version), or "Not tested in the Xerte editor yet" when the record has no
   `[editor]` table.
````

**Edit `THEMING-GUIDE.md`:** replace

````markdown
`build.sh` so the CI workflow's compile matches the committed CSS; update the pin with care.
````

with

````markdown
`build.sh` so the CI workflow's compile matches the committed CSS; update the pin with care.

A component record's `[editor]` table records a test in the Xerte editor: paste the component's
examples into a Text content item, save, close and reopen the editor, and see whether the markup
is still there. Leave the table out until you have tested; the guide then says "Not tested in the
Xerte editor yet". After a test, add `survives` (true or false), `checked` (a TOML date) and
`xerte` (a string, such as `"3.14"`). The build warns when the component's SCSS changes after
the `checked` date.
````

- [ ] **Step 7: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3`
Expected: `OK`

- [ ] **Step 8: Commit**

```bash
git add tools/guidelib/records.py tools/guidelib/pages.py tools/guidelib/checks.py tests/test_records.py tests/test_pages.py tests/test_checks.py docs/design-notes/2026-10-06-author-guide.md THEMING-GUIDE.md
git commit -m "feat(cardiffuniversity): show 'Not tested in the Xerte editor yet' for untested components"
```

---

### Task 2: One source for task and component links

Only a task file says which components it uses. A component page works out its tasks from the task files.

**Files:**
- Modify: `tools/guidelib/records.py`, `tools/guidelib/pages.py`, `tools/guidelib/checks.py`
- Modify: `guide/content/components/callout.md`
- Modify: `tests/guide_fixture.py`, `tests/test_records.py`, `tests/test_checks.py`, `tests/test_pages.py`
- Modify: `docs/design-notes/2026-10-06-author-guide.md`, `THEMING-GUIDE.md`

**Interfaces:**
- Consumes: `Task.components`, `Site.tasks`.
- Produces: `Component` has no `tasks` field; a record with a `tasks` key is a `RecordError`. `pages.tasks_using(ctx, component) -> list[Task]` (in `site.toml` order). Fixture: `guide_fixture.TASK_B`, `SITE_TWO`, and `write_guide(..., TASK_B=text)`.

- [ ] **Step 1: Write the failing tests and fixture**

**Edit `tests/guide_fixture.py`:** replace

```python
since = "v1.4"
tasks = ["draw-attention"]
related = []
```

with

```python
since = "v1.4"
related = []
```

**Edit `tests/guide_fixture.py`:** replace

```python
FILES = {
```

with

```python
TASK_B = TASK.replace('name = "draw-attention"', 'name = "add-a-tip"').replace(
    'title = "Draw attention to something"', 'title = "Add a tip to a page"')
SITE_TWO = SITE.replace('tasks = ["draw-attention"]', 'tasks = ["draw-attention", "add-a-tip"]')

FILES = {
```

**Edit `tests/guide_fixture.py`:** replace

```python
    "GETTING_STARTED": "content/pages/getting-started.md",
}
```

with

```python
    "GETTING_STARTED": "content/pages/getting-started.md",
    "TASK_B": "content/tasks/add-a-tip.md",
}
```

**Edit `tests/guide_fixture.py`:** replace

```python
    texts = {"SITE": SITE, "CALLOUT": CALLOUT, "TASK": TASK, "INDEX": INDEX, "GETTING_STARTED": GETTING_STARTED}
```

with

```python
    texts = {"SITE": SITE, "CALLOUT": CALLOUT, "TASK": TASK, "INDEX": INDEX, "GETTING_STARTED": GETTING_STARTED,
             "TASK_B": None}
```

**Edit `tests/test_records.py`:** replace

```python
    def test_name_must_match_the_file(self):
```

with

```python
    def test_component_tasks_field_is_rejected_with_a_pointer(self):
        self.assertComponentError(fx.CALLOUT.replace("related = []", 'related = []\ntasks = ["draw-attention"]'),
                                  "'tasks' is not a component field.*components")

    def test_name_must_match_the_file(self):
```

**Edit `tests/test_checks.py`:** replace

```python
                  since="v1.4", tasks=(), related=(), scss=(), editor=
```

with

```python
                  since="v1.4", related=(), scss=(), editor=
```

**Edit `tests/test_checks.py`:** replace

```python
        good = content([component(tasks=("draw-attention",))], [task()])
```

with

```python
        good = content([component()], [task()])
```

**Edit `tests/test_checks.py`:** replace

```python
        bad = component(group="layout", tasks=("missing-task",), related=("alert",), scss=("scss/nope.scss",))
```

with

```python
        bad = component(group="layout", related=("alert",), scss=("scss/nope.scss",))
```

**Edit `tests/test_checks.py`:** replace

```python
        self.assertIn("error 3 group 'layout' is not in site.toml", found)
        self.assertIn("error 3 task 'missing-task' has no task file", found)
```

with

```python
        self.assertIn("error 3 group 'layout' is not in site.toml", found)
```

**Edit `tests/test_pages.py`:** replace

```python
    def test_on_this_page_links_resolve(self):
```

with

```python
    def test_component_page_lists_the_tasks_that_use_it(self):
        related = self.section(self.page("components/callout.html"), "Related")
        link = related.find("a", href="../tasks/draw-attention.html")
        self.assertEqual(link.text(), "Task: Draw attention to something")

    def test_on_this_page_links_resolve(self):
```

**Edit `tests/test_pages.py`:** replace

```python
class UntestedEvidenceTest(unittest.TestCase):
```

with

```python
class TaskLinksTest(unittest.TestCase):
    def test_a_new_task_appears_on_the_component_page_without_editing_the_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            guide = fx.write_guide(tmp, TASK_B=fx.TASK_B, SITE=fx.SITE_TWO)
            out = Path(tmp) / "site"
            pages.write_site(out, records.load_site(guide / "site.toml"), records.load_content(guide / "content"),
                             support.GUIDE / "templates" / "base.html")
            related = parse((out / "components" / "callout.html").read_text(encoding="utf-8")).find(cls="g-related")
        self.assertEqual([a.text() for a in related.find_all("a")],
                         ["Task: Draw attention to something", "Task: Add a tip to a page"])


class UntestedEvidenceTest(unittest.TestCase):
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"`
Expected: failures including `test_component_tasks_field_is_rejected_with_a_pointer`, `test_component_page_lists_the_tasks_that_use_it` and `test_a_new_task_appears_on_the_component_page_without_editing_the_record`, and errors in `test_checks` because `Component` still wants `tasks`.

- [ ] **Step 3: Remove `tasks` from component records**

**Edit `tools/guidelib/records.py`:** replace

```python
    since: str
    tasks: tuple
    related: tuple
```

with

```python
    since: str
    related: tuple
```

**Edit `tools/guidelib/records.py`:** replace

```python
    _only(data, {"name", "title", "lead", "group", "status", "since", "tasks", "related", "scss",
                 "editor", "parts", "examples"}, path)
```

with

```python
    if "tasks" in data:
        raise RecordError(path, "'tasks' is not a component field; list the component under 'components' "
                                "in a task file instead")
    _only(data, {"name", "title", "lead", "group", "status", "since", "related", "scss",
                 "editor", "parts", "examples"}, path)
```

**Edit `tools/guidelib/records.py`:** replace

```python
        tasks=_field(data, "tasks", "strings", path, required=False, default=()),
        related=_field(data, "related", "strings", path, required=False, default=()),
```

with

```python
        related=_field(data, "related", "strings", path, required=False, default=()),
```

**Edit `guide/content/components/callout.md`:** replace

```toml
since = "v1.4"
tasks = ["draw-attention"]
related = []
```

with

```toml
since = "v1.4"
related = []
```

**Edit `tools/guidelib/checks.py`:** replace

```python
        for name in component.tasks:
            if name not in content.tasks:
                error(component.source, f"task '{name}' has no task file")
        for name in component.related:
```

with

```python
        for name in component.related:
```

- [ ] **Step 4: Work the task list out from the task files**

**Edit `tools/guidelib/pages.py`:** replace

```python
def related_links(ctx, component, root):
    links = [f'<a href="{name}.html">{esc(ctx.content.components[name].title)}</a>' for name in component.related]
    links += [f'<a href="{root}tasks/{name}.html">Task: {esc(ctx.content.tasks[name].title)}</a>' for name in component.tasks]
```

with

```python
def tasks_using(ctx, component):
    """Tasks whose task file lists this component, in site.toml's task order."""
    found = (ctx.content.tasks.get(name) for name in ctx.site.tasks)
    return [task for task in found if task and component.name in task.components]


def related_links(ctx, component, root):
    links = [f'<a href="{name}.html">{esc(ctx.content.components[name].title)}</a>' for name in component.related]
    links += [f'<a href="{root}tasks/{task.name}.html">Task: {esc(task.title)}</a>' for task in tasks_using(ctx, component)]
```

- [ ] **Step 5: Update the spec and the maintainer guide**

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
since = "v1.4"
tasks = ["draw-attention"]
related = ["alert", "well"]
````

with

````markdown
since = "v1.4"
related = ["alert", "well"]
````

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
- A task page names its components, and each component page lists the tasks that use it. The
  home page's task tiles come from the task files, in the order `site.toml` gives.
````

with

````markdown
- A task page names its components, and each component page lists the tasks that use it. Only the
  task file holds the link: the component page works its task list out from the task files, so
  the two cannot disagree. The home page's task tiles come from the task files, in the order
  `site.toml` gives.
````

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
| 3 | Every `related`, `tasks` and `group` value points at something that exists; groups are checked against `site.toml` | Fails the build |
````

with

````markdown
| 3 | Every `related` and `group` value, every component a task file names, and every task `site.toml` lists points at something that exists; groups are checked against `site.toml` | Fails the build |
````

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
   and the callout record's `tasks` link passes check 3.
````

with

````markdown
   and the callout page has a task to link to.
````

**Edit `THEMING-GUIDE.md`:** replace

````markdown
Xerte editor yet". After a test, add `survives` (true or false), `checked` (a TOML date) and
`xerte` (a string, such as `"3.14"`). The build warns when the component's SCSS changes after
the `checked` date.
````

with

````markdown
Xerte editor yet". After a test, add `survives` (true or false), `checked` (a TOML date) and
`xerte` (a string, such as `"3.14"`). The build warns when the component's SCSS changes after
the `checked` date.

A task file lists the components it uses under `components`. That is the only place the link is
written: a component page finds its tasks from the task files, and a component record that has a
`tasks` field is rejected.
````

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3 && ./build.sh guide 2>&1 | tail -1 | cut -c1-90`
Expected: `OK`, then `Built .../site (6 pages, 2 warning(s)).`

- [ ] **Step 7: Commit**

```bash
git add tools/guidelib/records.py tools/guidelib/pages.py tools/guidelib/checks.py guide/content/components/callout.md tests/guide_fixture.py tests/test_records.py tests/test_checks.py tests/test_pages.py docs/design-notes/2026-10-06-author-guide.md THEMING-GUIDE.md
git commit -m "feat(cardiffuniversity): link tasks to components in the task file only"
```

---

### Task 3: Warn about unbalanced example HTML

Check 5 warns when an example has an unclosed element, a stray end tag, or crossed elements.

**Files:**
- Modify: `tools/guidelib/checks.py`
- Modify: `tests/test_checks.py`
- Modify: `docs/design-notes/2026-10-06-author-guide.md`

**Interfaces:**
- Consumes: `checks.scan(markup)`, `checks.check_examples(content)`.
- Produces: `checks.scan(markup).unbalanced` is a list of messages. `check_examples` adds `warning 5 example '<label>' has unbalanced HTML: <first problem>`.

- [ ] **Step 1: Write the failing tests**

**Edit `tests/test_checks.py`:** replace

```python
    def test_heading_with_text_is_fine(self):
```

with

```python
    def test_unclosed_element_warns(self):
        self.assertEqual(self.check("<div><p>text</p>"),
                         ["warning 5 example 'E' has unbalanced HTML: <div> is not closed"])

    def test_stray_end_tag_warns(self):
        self.assertEqual(self.check("<p>text</p></span>"),
                         ["warning 5 example 'E' has unbalanced HTML: </span> has no start tag"])

    def test_crossed_elements_warn(self):
        self.assertEqual(self.check("<div><span>text</div></span>"),
                         ["warning 5 example 'E' has unbalanced HTML: <span> is not closed before </div>"])

    def test_optional_end_tags_and_void_elements_are_fine(self):
        for markup in ("<ul><li>a<li>b</ul>", "<table><tr><td>x<td>y</table>", "<p>one<p>two", "<p>a<br>b<hr></p>",
                       '<img src="a.png" alt="">', "<dl><dt>t<dd>d</dl>", '<div class="x"><i class="fa-solid"></i></div>'):
            with self.subTest(markup=markup):
                self.assertEqual(self.check(markup), [])

    def test_heading_with_text_is_fine(self):
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_checks.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"`
Expected: `FAIL` for the unclosed, stray and crossed tests (the optional-end test already passes); `FAILED`.

- [ ] **Step 3: Track open elements in the scanner**

**Edit `tools/guidelib/checks.py`:** replace

```python
class _Scan(HTMLParser):
    """Collects an example's class names, images without alt text and empty headings."""
    HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self):
        super().__init__()
        self.classes, self.images_without_alt, self.empty_headings = set(), 0, 0
        self._heading, self._text = None, ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.classes.update((attrs.get("class") or "").split())
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt += 1
        if tag in self.HEADINGS:
            self._heading, self._text = tag, ""

    def handle_data(self, data):
        if self._heading:
            self._text += data

    def handle_endtag(self, tag):
        if tag == self._heading:
            if not self._text.strip():
                self.empty_headings += 1
            self._heading = None
```

with

```python
class _Scan(HTMLParser):
    """Collects an example's class names, images without alt text, empty headings and unbalanced tags."""
    HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
    # HTML lets these end without an end tag, so a missing end tag is not a mistake.
    OPTIONAL_END = {"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody", "tfoot", "caption", "colgroup",
                    "option", "optgroup"}

    def __init__(self):
        super().__init__()
        self.classes, self.images_without_alt, self.empty_headings = set(), 0, 0
        self._heading, self._text = None, ""
        self._open, self._problems = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.classes.update((attrs.get("class") or "").split())
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt += 1
        if tag in self.HEADINGS:
            self._heading, self._text = tag, ""
        if tag not in self.VOID and tag not in self.OPTIONAL_END:
            self._open.append(tag)

    def handle_data(self, data):
        if self._heading:
            self._text += data

    def handle_endtag(self, tag):
        if tag not in self.VOID and tag not in self.OPTIONAL_END:
            self._close(tag)
        if tag == self._heading:
            if not self._text.strip():
                self.empty_headings += 1
            self._heading = None

    def _close(self, tag):
        if self._open and self._open[-1] == tag:
            self._open.pop()
        elif tag in self._open:
            self._problems.append(f"<{self._open[-1]}> is not closed before </{tag}>")
            while self._open.pop() != tag:
                pass
        else:
            self._problems.append(f"</{tag}> has no start tag")

    @property
    def unbalanced(self):
        """Problems found so far, plus every element still open."""
        return self._problems + [f"<{tag}> is not closed" for tag in self._open]
```

**Edit `tools/guidelib/checks.py`:** replace

```python
        if found.empty_headings:
            findings.append(Finding("warning", 5, str(source), f"example '{example.label}' has an empty heading"))
```

with

```python
        if found.empty_headings:
            findings.append(Finding("warning", 5, str(source), f"example '{example.label}' has an empty heading"))
        if found.unbalanced:
            findings.append(Finding("warning", 5, str(source),
                                    f"example '{example.label}' has unbalanced HTML: {found.unbalanced[0]}"))
```

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
| 5 | An example has an `<img>` without `alt`, or an empty heading | Warns |
````

with

````markdown
| 5 | An example has an `<img>` without `alt`, an empty heading, or unbalanced tags (an unclosed element, a stray end tag, or crossed elements; elements whose end tag HTML makes optional, such as `p` and `li`, are not counted) | Warns |
````

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3 && ./build.sh guide 2>&1 | grep -c "check 5"`
Expected: `OK`, then `0` (the real examples are balanced).

- [ ] **Step 5: Commit**

```bash
git add tools/guidelib/checks.py tests/test_checks.py docs/design-notes/2026-10-06-author-guide.md
git commit -m "feat(cardiffuniversity): warn about unbalanced HTML in guide examples"
```

---

### Task 4: Reference data

`tools/guidelib/reference.py` reads the token file, the copy file and the utility tables, and returns what the reference pages need.

**Files:**
- Create: `tools/guidelib/reference.py`, `guide/reference.toml`, `tests/test_reference.py`

**Interfaces:**
- Consumes: `tokens/tokens.json`; `theme_css.utility_groups(theme_css.utilities())` and `theme_css.LEGACY` (passed in by the caller, not imported here).
- Produces: `ReferenceDataError(ValueError)` (message `"{source}: {message}"`); frozen dataclasses `Token(name, value, resolved, alias_of, note)`, `Group(id, title, intro, tokens)`, `Reference(palette, tokens, utilities, legacy, white, ink)`; `luminance(colour) -> float`; `contrast(a, b) -> float`; `ratio_text(ratio) -> str`; `passes_aa(ratio) -> bool`; `load_reference(tokens_path, copy_path, utilities, legacy) -> Reference`.

- [ ] **Step 1: Write the failing tests**

`tests/test_reference.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

import support
from guidelib import reference

TOKENS = {
    "$description": "Test tokens.",
    "primary": {
        "$description": "Tier 1",
        "cu-white": {"$value": "#FFFFFF"},
        "cu-black": {"$value": "#121212"},
        "cu-red": {"$value": "#E4251B"},
    },
    "roles": {
        "cu-bg": {"$value": "{cu-white}"},
        "cu-link": {"$value": "#045bc6", "$description": "recorded deviation"},
    },
    "space": {"cu-space-1": {"$value": "4px"}},
}

COPY = """\
[[groups]]
id = "primary"
title = "Primary colours"
intro = "Red, white and black."

[[groups]]
id = "roles"
title = "Colour roles"
intro = "Named by job."

[[groups]]
id = "space"
title = "Spacing"
intro = "A 4px base."
"""

UTILITIES = (("Spacing", "Margin and padding.", (("mt-4", "margin-top: 16px"),)),)
LEGACY = (("c10", "Legacy System 2 column width."),)


class LoadReferenceTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def load(self, tokens=TOKENS, copy=COPY):
        (self.dir / "tokens.json").write_text(json.dumps(tokens), encoding="utf-8")
        (self.dir / "reference.toml").write_text(copy, encoding="utf-8")
        return reference.load_reference(self.dir / "tokens.json", self.dir / "reference.toml", UTILITIES, LEGACY)

    def assertLoadError(self, pattern, **kwargs):
        with self.assertRaisesRegex(reference.ReferenceDataError, pattern):
            self.load(**kwargs)

    def test_colour_groups_and_other_groups_are_split(self):
        ref = self.load()
        self.assertEqual([g.id for g in ref.palette], ["primary", "roles"])
        self.assertEqual([g.id for g in ref.tokens], ["space"])

    def test_titles_and_intros_come_from_the_copy_file(self):
        ref = self.load()
        self.assertEqual((ref.palette[0].title, ref.palette[0].intro), ("Primary colours", "Red, white and black."))
        self.assertEqual(ref.tokens[0].title, "Spacing")

    def test_alias_is_resolved_and_remembered(self):
        roles = self.load().palette[1].tokens
        self.assertEqual(roles[0], reference.Token("cu-bg", "{cu-white}", "#FFFFFF", "cu-white", ""))

    def test_note_is_kept(self):
        roles = self.load().palette[1].tokens
        self.assertEqual(roles[1].note, "recorded deviation")
        self.assertEqual(roles[1].resolved, "#045bc6")

    def test_white_and_ink_come_from_the_tokens(self):
        ref = self.load()
        self.assertEqual((ref.white, ref.ink), ("#FFFFFF", "#121212"))

    def test_utilities_and_legacy_pass_through(self):
        ref = self.load()
        self.assertEqual(ref.utilities, UTILITIES)
        self.assertEqual(ref.legacy, LEGACY)

    def test_utility_classes_sort_numbers_in_order(self):
        rows = (("m-10", "margin: 40px"), ("m-2", "margin: 8px"), ("m-1", "margin: 4px"),
                ("mb-2", "margin-bottom: 8px"))
        self.load()
        ref = reference.load_reference(self.dir / "tokens.json", self.dir / "reference.toml",
                                       (("Spacing", "Margins.", rows),), LEGACY)
        self.assertEqual([cls for cls, _ in ref.utilities[0][2]], ["m-1", "m-2", "m-10", "mb-2"])

    def test_token_group_without_an_entry(self):
        self.assertLoadError(r"reference\.toml: no entry for token group\(s\): space",
                             copy=COPY.split('[[groups]]\nid = "space"')[0])

    def test_entry_for_a_missing_group(self):
        self.assertLoadError(r"tokens\.json does not have: shadows",
                             copy=COPY + '\n[[groups]]\nid = "shadows"\ntitle = "Shadows"\nintro = "Flat."\n')

    def test_alias_to_nothing(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["roles"]["cu-bg"]["$value"] = "{cu-nope}"
        self.assertLoadError(r"token cu-bg refers to \{cu-nope\}, which does not exist", tokens=tokens)

    def test_alias_loop(self):
        tokens = json.loads(json.dumps(TOKENS))
        tokens["roles"]["cu-a"] = {"$value": "{cu-b}"}
        tokens["roles"]["cu-b"] = {"$value": "{cu-a}"}
        self.assertLoadError(r"token cu-[ab] is part of an alias loop", tokens=tokens)

    def test_white_and_ink_are_required(self):
        tokens = json.loads(json.dumps(TOKENS))
        del tokens["primary"]["cu-white"]
        tokens["roles"]["cu-bg"]["$value"] = "#FFFFFF"
        self.assertLoadError(r"need a cu-white token", tokens=tokens)

    def test_copy_entry_needs_every_key(self):
        self.assertLoadError(r"\[\[groups\]\] entry 1: missing 'intro'",
                             copy='[[groups]]\nid = "primary"\ntitle = "Primary"\n')

    def test_copy_group_id_must_be_a_slug(self):
        self.assertLoadError(r"entry 1: id must use only a-z, 0-9 and hyphens",
                             copy='[[groups]]\nid = "Primary Colours"\ntitle = "t"\nintro = "i"\n')

    def test_copy_group_listed_twice(self):
        self.assertLoadError(r"group 'primary' is listed twice", copy=COPY + COPY.split("\n\n")[0] + "\n")

    def test_unreadable_tokens_file(self):
        with self.assertRaisesRegex(reference.ReferenceDataError, r"tokens\.json: cannot read"):
            reference.load_reference(self.dir / "tokens.json", self.dir / "reference.toml", UTILITIES, LEGACY)

    def test_real_tokens_are_all_described(self):
        """Every token group in the real tokens.json has an entry in the real guide/reference.toml."""
        ref = reference.load_reference(support.THEME / "tokens" / "tokens.json", support.GUIDE / "reference.toml",
                                       UTILITIES, LEGACY)
        names = {t.name for g in ref.palette + ref.tokens for t in g.tokens}
        self.assertIn("cu-brand-red", names)
        self.assertIn("cu-space-4", names)
        self.assertIn("cu-brand-red", {t.name for t in ref.palette[0].tokens})
        self.assertNotIn("cu-space-4", {t.name for g in ref.palette for t in g.tokens})


class ContrastTest(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertEqual(reference.ratio_text(reference.contrast("#000000", "#FFFFFF")), "21.0:1")

    def test_contrast_is_the_same_whichever_colour_is_the_text(self):
        self.assertEqual(reference.contrast("#E4251B", "#FFFFFF"), reference.contrast("#FFFFFF", "#E4251B"))

    def test_white_on_the_ink_colour(self):
        self.assertEqual(reference.ratio_text(reference.contrast("#FFFFFF", "#121212")), "18.7:1")

    def test_aa_boundary_never_reads_as_passing(self):
        # #767676 on white is the lightest grey that passes AA for body text (4.54:1);
        # #777777 is just under (4.48:1). The failing one must not round up to 4.5:1.
        passing = reference.contrast("#767676", "#FFFFFF")
        failing = reference.contrast("#777777", "#FFFFFF")
        self.assertEqual((reference.ratio_text(passing), reference.passes_aa(passing)), ("4.5:1", True))
        self.assertEqual((reference.ratio_text(failing), reference.passes_aa(failing)), ("4.4:1", False))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_reference.py" 2>&1 | grep -E "^(FAIL|ERROR):|Error|^Ran|FAILED" | head -4`
Expected: `ImportError: cannot import name 'reference' from 'guidelib'`

- [ ] **Step 3: Write the reference module**

`tools/guidelib/reference.py`:

```python
"""Data for the reference pages: colours, other design tokens, utility classes and legacy classes.

Colours and tokens are read from tokens/tokens.json, so the pages cannot drift from the theme.
guide/reference.toml gives each token group an author-facing title and intro; a token group with
no entry is a ReferenceDataError, so a new group cannot be left off the pages by accident.
"""
import json
import math
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
ALIAS = re.compile(r"^\{(cu-[\w-]+)\}$")
SLUG = re.compile(r"^[a-z0-9-]+$")
AA_TEXT = 4.5  # WCAG AA contrast for body text
WHITE_TOKEN, INK_TOKEN = "cu-white", "cu-black"


class ReferenceDataError(ValueError):
    def __init__(self, source, message):
        super().__init__(f"{source}: {message}")


@dataclass(frozen=True)
class Token:
    name: str  # as in tokens.json, so without the leading --
    value: str  # as written
    resolved: str  # the value with any alias followed
    alias_of: str | None
    note: str


@dataclass(frozen=True)
class Group:
    id: str
    title: str
    intro: str
    tokens: tuple


@dataclass(frozen=True)
class Reference:
    palette: tuple  # groups whose tokens are all colours
    tokens: tuple  # every other group
    utilities: tuple  # (heading, guidance, ((class, value), ...))
    legacy: tuple  # ((class, reason), ...)
    white: str
    ink: str


def luminance(colour):
    """Relative luminance of a #RRGGBB colour (WCAG 2)."""
    channels = []
    for start in (1, 3, 5):
        value = int(colour[start:start + 2], 16) / 255
        channels.append(value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(first, second):
    """Contrast ratio between two colours. It is the same whichever one is the text."""
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def ratio_text(ratio):
    """The ratio rounded down, so a ratio just under a threshold never reads as passing it."""
    return f"{math.floor(ratio * 10) / 10:.1f}:1"


def passes_aa(ratio):
    return ratio >= AA_TEXT


def _natural(name):
    """A sort key that puts m-2 before m-10."""
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", name)]


def _resolve(name, table, source, seen=()):
    """The value of a token with any alias followed, and the name it is an alias of (or None)."""
    value = table[name]
    match = ALIAS.match(value)
    if not match:
        return value, None
    target = match.group(1)
    if target == name or target in seen:
        raise ReferenceDataError(source, f"token {name} is part of an alias loop")
    if target not in table:
        raise ReferenceDataError(source, f"token {name} refers to {{{target}}}, which does not exist")
    return _resolve(target, table, source, seen + (name,))[0], target


def _read_copy(path):
    try:
        data = tomllib.loads(Path(path).read_text(encoding="utf-8-sig"))
    except OSError as error:
        raise ReferenceDataError(path, f"cannot read ({error})") from None
    except UnicodeDecodeError:
        raise ReferenceDataError(path, "is not saved as UTF-8") from None
    except tomllib.TOMLDecodeError as error:
        raise ReferenceDataError(path, f"not valid TOML ({error})") from None
    entries = data.get("groups")
    if not isinstance(entries, list) or not entries:
        raise ReferenceDataError(path, "needs at least one [[groups]] entry")
    out, seen = [], set()
    for number, entry in enumerate(entries, 1):
        where = f"[[groups]] entry {number}"
        if not isinstance(entry, dict):
            raise ReferenceDataError(path, f"{where} must be a table")
        extra = sorted(set(entry) - {"id", "title", "intro"})
        if extra:
            raise ReferenceDataError(path, f"{where}: unknown key(s): {', '.join(extra)}")
        for key in ("id", "title", "intro"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise ReferenceDataError(path, f"{where}: missing '{key}'")
        if not SLUG.match(entry["id"]):
            raise ReferenceDataError(path, f"{where}: id must use only a-z, 0-9 and hyphens")
        if entry["id"] in seen:
            raise ReferenceDataError(path, f"group '{entry['id']}' is listed twice")
        seen.add(entry["id"])
        out.append(entry)
    return out


def load_reference(tokens_path, copy_path, utilities, legacy):
    """Everything the reference pages show. utilities and legacy come from tools/theme_css.py."""
    tokens_path, copy_path = Path(tokens_path), Path(copy_path)
    try:
        data = json.loads(tokens_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReferenceDataError(tokens_path, f"cannot read the tokens ({error})") from None
    groups = {key: value for key, value in data.items() if not key.startswith("$")}
    table = {name: token["$value"] for group in groups.values() for name, token in group.items()
             if not name.startswith("$")}
    for needed in (WHITE_TOKEN, INK_TOKEN):
        if needed not in table:
            raise ReferenceDataError(tokens_path, f"the reference pages need a {needed} token")
    entries = _read_copy(copy_path)
    described = [entry["id"] for entry in entries]
    missing = [key for key in groups if key not in described]
    if missing:
        raise ReferenceDataError(copy_path, f"no entry for token group(s): {', '.join(missing)}; "
                                            "add one to guide/reference.toml")
    unknown = [key for key in described if key not in groups]
    if unknown:
        raise ReferenceDataError(copy_path, f"entry for token group(s) that tokens.json does not have: "
                                            f"{', '.join(unknown)}")
    palette, other = [], []
    for entry in entries:
        tokens = []
        for name, token in groups[entry["id"]].items():
            if name.startswith("$"):
                continue
            resolved, alias = _resolve(name, table, tokens_path)
            tokens.append(Token(name, token["$value"], resolved, alias, token.get("$description", "")))
        group = Group(entry["id"], entry["title"], entry["intro"], tuple(tokens))
        (palette if all(HEX.match(t.resolved) for t in tokens) else other).append(group)
    return Reference(
        palette=tuple(palette), tokens=tuple(other),
        utilities=tuple((heading, guidance, tuple(sorted(rows, key=lambda row: _natural(row[0]))))
                        for heading, guidance, rows in utilities),
        legacy=tuple(legacy), white=_resolve(WHITE_TOKEN, table, tokens_path)[0],
        ink=_resolve(INK_TOKEN, table, tokens_path)[0])
```

- [ ] **Step 4: Write the copy file**

Each intro uses only what the token file, `THEMING-GUIDE.md` and the build tools already say.

`guide/reference.toml`:

```toml
# Author-facing titles and intros for the reference pages. Every token group in
# tokens/tokens.json needs an entry here, in the order the groups should appear.
# Colour groups appear on the Colours page; every other group appears on the
# Type, space and shape page. The id must match the group's key in tokens.json.

[[groups]]
id = "primary"
title = "Primary colours"
intro = "Cardiff red, white and black. These three make up the theme's primary palette."

[[groups]]
id = "red-tones"
title = "Error red"
intro = "A darker tone of brand red, used for error text. It is a recorded deviation from the design system."

[[groups]]
id = "greys"
title = "Greys"
intro = "Greys in 10% steps from black."

[[groups]]
id = "accents"
title = "Accent colours"
intro = "Use accents sparingly and with the Design team's permission."

[[groups]]
id = "roles"
title = "Colour roles"
intro = "A role names a colour by its job, such as text or background, so a rule asks for ink rather than black. Most roles point at a palette colour; the table shows which."

[[groups]]
id = "callouts"
title = "Callout colours"
intro = "The rule and icon disc colour for each callout variant, and the colour of the icon on the disc. The title carries the meaning; colour and icon support it."

[[groups]]
id = "font-families"
title = "Font families"
intro = "Headings use Franklin Gothic with a system fallback. Body text uses the system font stack. No web fonts are fetched."

[[groups]]
id = "font-sizes"
title = "Font sizes"
intro = "Sizes by role. Body copy is 18px."

[[groups]]
id = "font-weights"
title = "Weights, leading and tracking"
intro = "Font weight, line height (leading) and letter spacing (tracking), by role."

[[groups]]
id = "space"
title = "Spacing"
intro = "A 4px base. The number in each name is the multiple of 4."

[[groups]]
id = "shape"
title = "Shape and motion"
intro = "The logo width, the corner radius for controls, and animation timing. Structural panels stay square."

[[groups]]
id = "shadows"
title = "Shadows"
intro = "Components stay flat. The small and medium shadows are none; the large and extra-large ones are for overlays only: dropdowns, popovers and modals."
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add tools/guidelib/reference.py guide/reference.toml tests/test_reference.py
git commit -m "feat(cardiffuniversity): read the tokens and utility classes for the reference pages"
```

---

### Task 5: Reference pages

Four pages, written when `write_site` is given reference data: an overview, Colours, Type, space and shape, and Utility classes.

**Files:**
- Modify: `tools/guidelib/records.py` (menu page), `tools/guidelib/pages.py`, `guide/assets/guide.css`
- Modify: `tests/guide_fixture.py`, `tests/test_pages.py`

**Interfaces:**
- Consumes: `reference.Reference`, `Group`, `Token`, `contrast`, `ratio_text`, `passes_aa`; `mdsubset.slugify`.
- Produces: `records.MENU_PAGES` includes `"reference"`. `pages.TOP_PATHS["reference"]`. `pages.write_site(out, site, content, template_path, updated=None, ref=None)` also writes `reference/index.html`, `reference/colours.html`, `reference/tokens.html` and `reference/utilities.html` when `ref` is given. Fixture: `guide_fixture.SITE_WITH_REFERENCE`.

- [ ] **Step 1: Write the failing tests**

**Edit `tests/guide_fixture.py`:** replace

```python
TASK_B = TASK.replace(
```

with

```python
SITE_WITH_REFERENCE = SITE + """
[[menu]]
page = "reference"
title = "Reference"
"""

TASK_B = TASK.replace(
```

**Edit `tests/test_pages.py`:** replace

```python
from guidelib import pages, records
```

with

```python
from guidelib import pages, records, reference
```

**Edit `tests/test_pages.py`:** replace

```python
class UntestedEvidenceTest(unittest.TestCase):
```

with

```python
REF = reference.Reference(
    palette=(
        reference.Group("primary", "Primary colours", "Red, white and black.", (
            reference.Token("cu-white", "#FFFFFF", "#FFFFFF", None, ""),
            reference.Token("cu-black", "#000000", "#000000", None, ""),
            reference.Token("cu-grey-aa", "#767676", "#767676", None, ""),
            reference.Token("cu-grey-low", "#777777", "#777777", None, ""))),
        reference.Group("roles", "Colour roles", "Named by job.", (
            reference.Token("cu-bg", "{cu-white}", "#FFFFFF", "cu-white", "page background"),))),
    tokens=(reference.Group("space", "Spacing", "A 4px base.", (
        reference.Token("cu-space-1", "4px", "4px", None, ""),
        reference.Token("cu-logo-width", "clamp(60px,17vw,80px)", "clamp(60px,17vw,80px)", None, "logo minimums"))),
        reference.Group("font-sizes", "Font sizes", "Sizes by role.", (
            reference.Token("cu-text-body", "18px", "18px", None, ""),))),
    utilities=(("Spacing", "Margin and padding.", (("mt-4", "margin-top: 16px"),)),
               ("Text size", "Sizes.", (("text-lg", "font-size: 20px"),))),
    legacy=(("c10", "Legacy System 2 column width."),),
    white="#FFFFFF", ink="#121212")
REFERENCE_PAGES = ["reference/colours.html", "reference/index.html", "reference/tokens.html", "reference/utilities.html"]


class ReferencePagesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        guide = fx.write_guide(cls.tmp.name, SITE=fx.SITE_WITH_REFERENCE)
        cls.out = Path(cls.tmp.name) / "site"
        cls.written = pages.write_site(cls.out, records.load_site(guide / "site.toml"),
                                       records.load_content(guide / "content"),
                                       support.GUIDE / "templates" / "base.html", ref=REF)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def page(self, relative):
        return parse((self.out / relative).read_text(encoding="utf-8"))

    def section(self, page, heading):
        for section in page.find_all(cls="g-section"):
            if section.find_all("h2") and section.find("h2").text() == heading:
                return section
        raise AssertionError(f"no section headed {heading!r}")

    def rows(self, relative, heading):
        return self.section(self.page(relative), heading).find("tbody").find_all("tr")

    def test_reference_pages_are_written(self):
        self.assertEqual([w for w in self.written if w.startswith("reference/")], REFERENCE_PAGES)

    def test_colour_contrast_cells(self):
        by_token = {row.find("code").text(): row for row in self.rows("reference/colours.html", "Primary colours")}
        cells = {name: [td.text() for td in row.find_all("td")] for name, row in by_token.items()}
        self.assertEqual(cells["--cu-black"][3], "21.0:1 passes AA")
        self.assertEqual(cells["--cu-grey-aa"][3], "4.5:1 passes AA")
        self.assertEqual(cells["--cu-grey-low"][3], "4.4:1 fails AA")
        self.assertEqual(cells["--cu-white"][4], "18.7:1 passes AA")

    def test_colour_swatch_shows_the_colour(self):
        row = self.rows("reference/colours.html", "Primary colours")[2]
        self.assertEqual(row.find(cls="g-swatch").attrs["style"], "background:#767676")
        self.assertEqual(row.find(cls="g-swatch").attrs["aria-hidden"], "true")

    def test_alias_and_note_are_shown(self):
        row = self.rows("reference/colours.html", "Colour roles")[0]
        self.assertEqual([c.text() for c in row.find_all(cls="g-token-note")], ["page background", "same as --cu-white"])
        self.assertEqual(row.find_all("td")[2].find("code").text(), "#FFFFFF")

    def test_colours_page_explains_the_ratios(self):
        text = self.page("reference/colours.html").find(cls="g-main").text()
        self.assertIn("WCAG AA needs 4.5:1 for body text", text)
        self.assertIn("the same whichever", text)

    def test_tokens_page_rows(self):
        rows = self.rows("reference/tokens.html", "Spacing")
        self.assertEqual([[td.text() for td in row.find_all("td")] for row in rows],
                         [["--cu-space-1", "4px", ""],
                          ["--cu-logo-width", "clamp(60px,17vw,80px)", "logo minimums"]])

    def test_tokens_page_shows_a_notes_column_only_when_a_group_has_notes(self):
        page = self.page("reference/tokens.html")
        self.assertEqual([th.text() for th in self.section(page, "Spacing").find_all("th")], ["Token", "Value", "Notes"])
        self.assertEqual([th.text() for th in self.section(page, "Font sizes").find_all("th")], ["Token", "Value"])

    def test_utilities_page_has_a_table_per_family_and_the_legacy_classes(self):
        page = self.page("reference/utilities.html")
        self.assertEqual([[td.text() for td in row.find_all("td")]
                          for row in self.rows("reference/utilities.html", "Spacing")], [[".mt-4", "margin-top: 16px"]])
        self.assertIn("Do not use them in new content", self.section(page, "Legacy classes").text())
        self.assertEqual([[td.text() for td in row.find_all("td")]
                          for row in self.rows("reference/utilities.html", "Legacy classes")],
                         [[".c10", "Legacy System 2 column width."]])

    def test_on_this_page_lists_the_groups_and_they_exist(self):
        for relative, expected in (("reference/colours.html", ["primary", "roles"]),
                                   ("reference/tokens.html", ["space", "font-sizes"]),
                                   ("reference/utilities.html", ["spacing", "text-size", "legacy-classes"])):
            page = self.page(relative)
            ids = {e.attrs["id"] for e in page.iter() if "id" in e.attrs}
            targets = [a.attrs["href"][1:] for a in page.find(cls="g-toc").find_all("a")]
            self.assertEqual(targets, expected, relative)
            self.assertLessEqual(set(targets), ids)

    def test_wide_tables_scroll_inside_their_own_region(self):
        for relative in ("reference/colours.html", "reference/tokens.html", "reference/utilities.html"):
            wraps = self.page(relative).find_all(cls="g-table-scroll")
            self.assertTrue(wraps, relative)
            for wrap in wraps:
                self.assertEqual(wrap.attrs.get("tabindex"), "0")
                self.assertEqual(wrap.attrs.get("role"), "region")
                self.assertTrue(wrap.attrs.get("aria-label"))
                self.assertEqual(len(wrap.find_all("table")), 1)

    def test_reference_menu_marks_the_current_page(self):
        side = self.page("reference/colours.html").find(cls="g-side")
        self.assertEqual([a.text() for a in side.find_all("a")], ["Overview", "Colours", "Type, space and shape", "Utility classes"])
        self.assertEqual(side.find("a", aria_current="page").text(), "Colours")
        self.assertEqual(self.page("reference/index.html").find(cls="g-side").find("a", aria_current="page").text(), "Overview")

    def test_top_menu_marks_reference(self):
        menu = self.page("reference/utilities.html").find(cls="g-top")
        self.assertEqual(menu.find("a", aria_current="page").text(), "Reference")
        self.assertEqual(menu.find("a", aria_current="page").attrs["href"], "../reference/index.html")

    def test_overview_links_to_every_reference_page(self):
        cards = self.page("reference/index.html").find_all(cls="g-card")
        self.assertEqual([c.find("a").attrs["href"] for c in cards], ["colours.html", "tokens.html", "utilities.html"])

    def test_every_reference_page_has_one_main_and_one_h1(self):
        for relative in REFERENCE_PAGES:
            page = self.page(relative)
            self.assertEqual(len(page.find_all(id="main")), 1, relative)
            self.assertEqual(len(page.find_all("h1")), 1, relative)

    def test_reference_links_resolve(self):
        for relative in REFERENCE_PAGES:
            for element in self.page(relative).iter():
                target = element.attrs.get("href") or ""
                if element.tag != "a" or not target or target.startswith(("#", "http:", "https:", "mailto:")):
                    continue
                path = (self.out / relative).parent / target.split("#")[0]
                self.assertTrue(path.resolve().is_file(), f"{relative} links to missing {target}")


class UntestedEvidenceTest(unittest.TestCase):
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_pages.py" 2>&1 | grep -E "^(FAIL|ERROR):|Error|^Ran|FAILED" | head -4`
Expected: `ERROR: setUpClass (test_pages.ReferencePagesTest)` with `TypeError: write_site() got an unexpected keyword argument 'ref'`, or a `RecordError` for the unknown menu page `reference`.

- [ ] **Step 3: Allow the `reference` menu page and share the side navigation**

**Edit `tools/guidelib/records.py`:** replace

```python
MENU_PAGES = ("home", "getting-started", "tasks", "components")
```

with

```python
MENU_PAGES = ("home", "getting-started", "tasks", "components", "reference")
```

**Edit `tools/guidelib/pages.py`:** replace

```python
from guidelib import assets
from guidelib.mdsubset import code_block

TOP_PATHS = {"home": "index.html", "getting-started": "getting-started.html",
             "tasks": "tasks/index.html", "components": "components/index.html"}
```

with

```python
from guidelib import assets, reference
from guidelib.mdsubset import code_block, slugify

TOP_PATHS = {"home": "index.html", "getting-started": "getting-started.html",
             "tasks": "tasks/index.html", "components": "components/index.html",
             "reference": "reference/index.html"}
# (file name, title, what the overview says about it)
REFERENCE_PAGES = (
    ("colours", "Colours", "Every colour in the theme, with its value and its contrast with white and ink."),
    ("tokens", "Type, space and shape", "Font, size, spacing, shape, motion and shadow values."),
    ("utilities", "Utility classes", "Single-purpose classes for spacing, text, layout and more, read from the compiled theme."),
)
COLOUR_HEADERS = ("Colour", "Token", "Value", "Against white", "Against ink")
```

**Edit `tools/guidelib/pages.py`:** replace

```python
def side_menu(ctx, root, active):
    blocks = []
    for title, members in ordered_components(ctx):
        items = "".join(f'<li><a href="{root}components/{c.name}.html"{_current(c.name == active)}>{esc(c.title)}</a></li>'
                        for c in members)
        blocks.append(f"<h2>{esc(title)}</h2><ul>{items}</ul>")
    return ('<nav class="g-side" aria-label="Components">'
            '<button class="g-side-toggle" type="button" aria-expanded="true" aria-controls="g-side-list" hidden>'
            'Components menu</button>'
            f'<div class="g-side-list" id="g-side-list">{"".join(blocks)}</div></nav>')
```

with

```python
def side_nav(label, inner, toggle):
    """The side menu's frame: the nav, the phone-width button and the list guide.js collapses."""
    return (f'<nav class="g-side" aria-label="{esc(label)}">'
            '<button class="g-side-toggle" type="button" aria-expanded="true" aria-controls="g-side-list" hidden>'
            f'{esc(toggle)}</button>'
            f'<div class="g-side-list" id="g-side-list">{inner}</div></nav>')


def side_menu(ctx, root, active):
    blocks = []
    for title, members in ordered_components(ctx):
        items = "".join(f'<li><a href="{root}components/{c.name}.html"{_current(c.name == active)}>{esc(c.title)}</a></li>'
                        for c in members)
        blocks.append(f"<h2>{esc(title)}</h2><ul>{items}</ul>")
    return side_nav("Components", "".join(blocks), "Components menu")
```

- [ ] **Step 4: Render the four reference pages**

**Edit `tools/guidelib/pages.py`:** replace

```python
def write_site(out, site, content, template_path, updated=None):
    """updated, if given, maps a record's path to the date it last changed (or None)."""
    ctx = Ctx(site, content, Template(template_path.read_text(encoding="utf-8")), updated or _unknown)
    rendered = {"index.html": home_page(ctx, content.pages["index"]),
                "components/index.html": components_index(ctx), "tasks/index.html": tasks_index(ctx)}
```

with

```python
def scroll_table(headers, rows, label, extra=""):
    """A table in a box that scrolls sideways on a narrow screen, so the page itself does not."""
    return (f'<div class="g-table-scroll" tabindex="0" role="region" aria-label="{esc(label)}">'
            f'{table(headers, rows, extra)}</div>')


def reference_menu(root, active):
    items = f'<li><a href="{root}reference/index.html"{_current(active == "index")}>Overview</a></li>'
    items += "".join(f'<li><a href="{root}reference/{slug}.html"{_current(slug == active)}>{esc(title)}</a></li>'
                     for slug, title, _ in REFERENCE_PAGES)
    return side_nav("Reference", f"<h2>Reference</h2><ul>{items}</ul>", "Reference menu")


def reference_page(ctx, *, slug, title, lead, sections, intro=""):
    """One generated reference page: side menu, a section per group, and an on this page list."""
    root = "../"
    blocks = "".join(f'<div class="g-section" aria-labelledby="{sid}" role="region"><h2 id="{sid}">{esc(heading)}</h2>{body}</div>'
                     for sid, heading, body in sections)
    body = (f'<div class="g-shell">{reference_menu(root, slug)}<main id="main" class="g-main">'
            f'<p class="g-crumb"><a href="index.html">Reference</a> &rsaquo; {esc(title)}</p>'
            f'<h1>{esc(title)}</h1><p class="g-lead">{esc(lead)}</p>{intro}{blocks}</main>'
            f'{on_this_page([(sid, heading) for sid, heading, _ in sections])}</div>')
    return page_shell(ctx, title=title, root=root, active="reference", body=body)


def reference_index(ctx):
    root = "../"
    cards = "".join(f'<li class="g-card"><a href="{slug}.html">{esc(title)}</a><p>{esc(summary)}</p></li>'
                    for slug, title, summary in REFERENCE_PAGES)
    body = (f'<div class="g-shell g-shell-two">{reference_menu(root, "index")}<main id="main" class="g-main">'
            '<h1>Reference</h1><p class="g-lead">Facts about the theme, generated from the theme itself, so they '
            f'are always current.</p><ul class="g-cards">{cards}</ul></main></div>')
    return page_shell(ctx, title="Reference", root=root, active="reference", body=body)


def swatch(colour):
    return f'<span class="g-swatch" style="background:{colour}" aria-hidden="true"></span>'


def contrast_cell(first, second):
    ratio = reference.contrast(first, second)
    return f"<td>{reference.ratio_text(ratio)} {'passes' if reference.passes_aa(ratio) else 'fails'} AA</td>"


def colour_row(token, ref):
    note = f'<span class="g-token-note">{esc(token.note)}</span>' if token.note else ""
    alias = (f'<span class="g-token-note">same as <code>--{esc(token.alias_of)}</code></span>'
             if token.alias_of else "")
    colour = token.resolved
    return (f"<tr><td>{swatch(colour)}</td><td><code>--{esc(token.name)}</code>{note}</td>"
            f"<td><code>{esc(colour)}</code>{alias}</td>"
            f"{contrast_cell(colour, ref.white)}{contrast_cell(colour, ref.ink)}</tr>")


def colours_page(ctx, ref):
    sections = [(group.id, group.title,
                 f"<p>{esc(group.intro)}</p>"
                 + scroll_table(COLOUR_HEADERS, "".join(colour_row(t, ref) for t in group.tokens),
                                f"{group.title}: colours", "g-table-colours"))
                for group in ref.palette]
    intro = ("<p>Each ratio is the contrast between the colour and white, or the colour and ink, and is the same "
             "whichever of the two is the text. WCAG AA needs 4.5:1 for body text, and 3:1 for large text, icons "
             "and borders. Ratios are rounded down.</p>")
    return reference_page(ctx, slug="colours", title="Colours", sections=sections, intro=intro,
                          lead="Every colour token in the theme, with its value and its contrast with white and ink.")


def tokens_page(ctx, ref):
    sections = []
    for group in ref.tokens:
        notes = any(t.note for t in group.tokens)  # a Notes column only where some token has a note
        rows = "".join(f"<tr><td><code>--{esc(t.name)}</code></td><td><code>{esc(t.value)}</code></td>"
                       + (f"<td>{esc(t.note)}</td>" if notes else "") + "</tr>" for t in group.tokens)
        headers = ("Token", "Value", "Notes") if notes else ("Token", "Value")
        sections.append((group.id, group.title,
                         f"<p>{esc(group.intro)}</p>" + scroll_table(headers, rows, group.title)))
    return reference_page(ctx, slug="tokens", title="Type, space and shape", sections=sections,
                          lead="Typography, spacing, corner radius, motion and shadow values. Colours are on the Colours page.")


def utilities_page(ctx, ref):
    sections = []
    for heading, guidance, rows in ref.utilities:
        body = "".join(f"<tr><td><code>.{esc(cls)}</code></td><td>{esc(value)}</td></tr>" for cls, value in rows)
        sections.append((slugify(heading), heading,
                         f"<p>{esc(guidance)}</p>" + scroll_table(("Class", "What it sets"), body, f"{heading} classes")))
    legacy = "".join(f"<tr><td><code>.{esc(cls)}</code></td><td>{esc(why)}</td></tr>" for cls, why in ref.legacy)
    sections.append(("legacy-classes", "Legacy classes",
                     "<p>These classes remain so older resources keep working. Do not use them in new content.</p>"
                     + scroll_table(("Class", "Why it is here"), legacy, "Legacy classes")))
    return reference_page(ctx, slug="utilities", title="Utility classes", sections=sections,
                          lead="Single-purpose classes. Add one or more to an element's class attribute.")


def write_site(out, site, content, template_path, updated=None, ref=None):
    """updated, if given, maps a record's path to the date it last changed (or None).
    ref, if given, is a reference.Reference and adds the reference pages."""
    ctx = Ctx(site, content, Template(template_path.read_text(encoding="utf-8")), updated or _unknown)
    rendered = {"index.html": home_page(ctx, content.pages["index"]),
                "components/index.html": components_index(ctx), "tasks/index.html": tasks_index(ctx)}
    if ref:
        rendered["reference/index.html"] = reference_index(ctx)
        rendered["reference/colours.html"] = colours_page(ctx, ref)
        rendered["reference/tokens.html"] = tokens_page(ctx, ref)
        rendered["reference/utilities.html"] = utilities_page(ctx, ref)
```

- [ ] **Step 5: Style the swatches, the scrolling tables and the notes**

**Edit `guide/assets/guide.css`:** replace

```css
@media (max-width: 1100px) {
```

with

```css
/* Reference pages: colour swatches, notes under a token, and tables that scroll inside their own box. */
.g-swatch { display: inline-block; width: 40px; height: 40px; border: 1px solid var(--cu-grey-80); vertical-align: middle; }
.g-table-scroll { overflow-x: auto; }
.g-table-scroll:focus-visible { outline: 3px solid var(--cu-ink); outline-offset: 2px; }
.g-table-colours { min-width: 640px; }
.g-token-note { display: block; color: var(--cu-grey-80); font-size: 16px; }
.g-table code { overflow-wrap: anywhere; }

@media (max-width: 1100px) {
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3`
Expected: `OK`

- [ ] **Step 7: Commit**

```bash
git add tools/guidelib/records.py tools/guidelib/pages.py guide/assets/guide.css tests/guide_fixture.py tests/test_pages.py
git commit -m "feat(cardiffuniversity): render the colour, token and utility class reference pages"
```

---

### Task 6: Wire the reference pages into the build

The real build loads the real tokens and utility classes, writes the four pages, adds the menu entry, and gives check 2 the utility classes the pages now cover.

**Files:**
- Modify: `tools/build-guide.py`, `guide/site.toml`
- Modify: `tests/guide_fixture.py`, `tests/test_guide_content.py`, `tests/check_guide.py`
- Modify: `docs/design-notes/2026-10-06-author-guide.md`, `THEMING-GUIDE.md`, `MIGRATION.md`

**Interfaces:**
- Consumes: `reference.load_reference`, `pages.write_site(..., ref=...)`, `theme_css.utility_groups`, `theme_css.utilities`, `theme_css.LEGACY`.
- Produces: `./build.sh guide` writes `site/reference/*.html`. A `ReferenceDataError` stops the build with an `ERROR` line. `tests/check_guide.py` has 5 more checks.

- [ ] **Step 1: Write the failing tests**

**Edit `tests/test_guide_content.py`:** replace

```python
import contextlib
import io
import subprocess
import sys
import unittest

import support
```

with

```python
import contextlib
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import support
from html_tree import parse
```

**Edit `tests/test_guide_content.py`:** replace

```python
    def test_build_runs_from_the_repo_root(self):
```

with

```python
    def test_check_2_counts_only_what_records_must_still_cover(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            build_guide.build(check_only=True)
        match = re.search(r"(\d+) author-facing classes are not covered yet", out.getvalue())
        self.assertIsNotNone(match, out.getvalue())
        # 355 author-facing classes, 259 shown in the utility tables, so at most 96 are left for records.
        self.assertLessEqual(int(match.group(1)), 96)

    def test_built_reference_pages_list_every_token(self):
        tokens = json.loads((support.THEME / "tokens" / "tokens.json").read_text(encoding="utf-8"))
        expected = {name for group, members in tokens.items() if not group.startswith("$")
                    for name in members if not name.startswith("$")}
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            with contextlib.redirect_stdout(io.StringIO()) as printed:
                code = build_guide.build(out=out)
            self.assertEqual(code, 0, printed.getvalue())
            shown = set()
            for name in ("colours", "tokens"):
                tree = parse((out / "reference" / f"{name}.html").read_text(encoding="utf-8"))
                shown |= {c.text()[2:] for c in tree.find_all("code") if c.text().startswith("--cu-")}
            utilities = parse((out / "reference" / "utilities.html").read_text(encoding="utf-8"))
        self.assertEqual(shown, expected)
        self.assertIn("mt-4", {c.text()[1:] for c in utilities.find_all("code")})

    def test_build_runs_from_the_repo_root(self):
```

**Edit `tests/check_guide.py`:** replace

```python
    ("index.html", 1280, "task tiles show their Font Awesome icon",
```

with

```python
    ("reference/colours.html", 1280, "colour swatches are visible",
     "document.querySelector('.g-swatch').getBoundingClientRect().width >= 24"),
    ("reference/colours.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("reference/colours.html", 485, "the colour table scrolls inside its own box",
     "(function () { var b = document.querySelector('.g-table-scroll'); return b.scrollWidth > b.clientWidth; })()"),
    ("reference/utilities.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("reference/index.html", 485, "no sideways scroll", NO_SIDEWAYS_SCROLL),
    ("index.html", 1280, "task tiles show their Font Awesome icon",
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests -p "test_guide_content.py" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|FAILED"; python3 tests/check_guide.py 2>&1 | grep -E "FAIL|passed"`
Expected: `ERROR: test_built_reference_pages_list_every_token` (`FileNotFoundError` for `reference/colours.html`), `FAIL: test_check_2_counts_only_what_records_must_still_cover`, and the five new browser checks fail.

- [ ] **Step 3: Load the reference data in the build**

**Edit `tools/build-guide.py`:** replace

```python
from guidelib import assets, checks, pages, records  # noqa: E402
```

with

```python
from guidelib import assets, checks, pages, records, reference  # noqa: E402
```

**Edit `tools/build-guide.py`:** replace

```python
    last_changed = last_changed or checks.git_last_changed(theme_css.THEME)
    findings = checks.run_all(
        content, site, theme_dir=theme_css.THEME, known=theme_css.stack_classes(),
        author_facing=theme_css.author_facing_classes(), tables=set(), last_changed=last_changed)
```

with

```python
    try:
        ref = reference.load_reference(
            theme_css.THEME / "tokens" / "tokens.json", guide_dir / "reference.toml",
            theme_css.utility_groups(theme_css.utilities()), tuple(sorted(theme_css.LEGACY.items())))
    except reference.ReferenceDataError as error:
        print(f"ERROR {error}")
        return 1
    # The utility tables on the reference pages cover these classes, so check 2 need not ask for records.
    tables = {cls for _, _, rows in ref.utilities for cls, _ in rows}
    last_changed = last_changed or checks.git_last_changed(theme_css.THEME)
    findings = checks.run_all(
        content, site, theme_dir=theme_css.THEME, known=theme_css.stack_classes(),
        author_facing=theme_css.author_facing_classes(), tables=tables, last_changed=last_changed)
```

**Edit `tools/build-guide.py`:** replace

```python
        written = pages.write_site(out, site, content, guide_dir / "templates" / "base.html",
                                   updated=lambda path: last_changed(str(path)))
```

with

```python
        written = pages.write_site(out, site, content, guide_dir / "templates" / "base.html",
                                   updated=lambda path: last_changed(str(path)), ref=ref)
```

**Edit `tests/guide_fixture.py`:** replace

```python
    for folder in ("templates", "assets"):
        real = support.GUIDE / folder
        if real.exists():
            shutil.copytree(real, guide / folder)
    return guide
```

with

```python
    for folder in ("templates", "assets"):
        real = support.GUIDE / folder
        if real.exists():
            shutil.copytree(real, guide / folder)
    if (support.GUIDE / "reference.toml").exists():
        shutil.copy(support.GUIDE / "reference.toml", guide / "reference.toml")
    return guide
```

**Edit `guide/site.toml`:** replace

```toml
[[menu]]
page = "components"
title = "Components"
```

with

```toml
[[menu]]
page = "components"
title = "Components"

[[menu]]
page = "reference"
title = "Reference"
```

- [ ] **Step 4: Update the docs**

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
| Reference | Colours, tokens, utility classes, mostly generated | generated | none (phase 2) |
````

with

````markdown
| Reference | An overview, Colours, Type, space and shape, and Utility classes, all generated from the theme | generated | 2a |
````

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
- The top menu has Home, Getting started, Tasks, Components, Colours and type, and Accessibility.
````

with

````markdown
- The top menu has Home, Getting started, Tasks, Components and Reference. An Accessibility entry
  joins when that page exists. (The Reference entry replaces "Colours and type": the section holds
  colours, type and spacing, and utility classes.)
````

**Edit `docs/design-notes/2026-10-06-author-guide.md`:** replace

````markdown
2. **Phase 2.** The reference pages (colours, tokens, utility classes), buttons, cards, tables,
   alerts, images, layout and typography, and two or three more task pages.
````

with

````markdown
2. **Phase 2**, in three plans so each batch can be reviewed:
   - **2a.** The foundations and the reference pages: optional editor evidence ("Not tested in the
     Xerte editor yet"), one source for task and component links, a check for unbalanced example
     HTML, and the Colours, Type, space and shape, and Utility classes pages.
   - **2b.** Buttons, cards, tables, alerts, images, layout and typography, in small batches.
   - **2c.** Two or three more task pages.
````

**Edit `THEMING-GUIDE.md`:** replace

````markdown
written: a component page finds its tasks from the task files, and a component record that has a
`tasks` field is rejected.
````

with

````markdown
written: a component page finds its tasks from the task files, and a component record that has a
`tasks` field is rejected.

The reference pages are generated. `guide/reference.toml` gives each token group in
`tokens/tokens.json` an author-facing title and intro; when you add a token group, add an entry
there too, or the build stops and names the group.
````

**Edit `MIGRATION.md`:** replace

````markdown
It is not published. Phase 2 adds the reference pages and seven more components.
````

with

````markdown
It is not published. Phase 2a adds the reference pages (colours, type and spacing, utility
classes), an honest "Not tested in the Xerte editor yet" state for component records, one source
for task and component links, and a check for unbalanced example HTML. Phase 2b adds seven more
components and phase 2c more task pages.
````

- [ ] **Step 5: Run everything**

Run: `python3 -m unittest discover -s tests -p "test_*.py" 2>&1 | tail -3 && python3 tests/check_guide.py 2>&1 | tail -1 && ./build.sh guide 2>&1 | tail -3 | cut -c1-140 && git diff --check && echo whitespace-ok`
Expected: `OK`; `27 passed, 0 failed` (the 22 existing browser checks plus 5 new); the build prints the check 2 warning with a smaller count than 345 and ends `Built .../site (10 pages, 2 warning(s)).`; `whitespace-ok`.

- [ ] **Step 6: Look at the pages**

Run: `open site/reference/colours.html` and read the Colours page. Confirm by eye that the swatches match their hex values, the "Against white" and "Against ink" columns read as ratios with "passes AA" or "fails AA", and the side menu lists Overview, Colours, Type, space and shape, and Utility classes.

- [ ] **Step 7: Commit**

```bash
git add tools/build-guide.py guide/site.toml tests/guide_fixture.py tests/test_guide_content.py tests/check_guide.py docs/design-notes/2026-10-06-author-guide.md THEMING-GUIDE.md MIGRATION.md
git commit -m "feat(cardiffuniversity): build the reference pages and add them to the menu"
```

---

## Self-review

**Spec coverage.**

| Requirement | Task |
| --- | --- |
| Optional `[editor]`, "Not tested in the Xerte editor yet" (Nan's decision, 7 October) | 1 |
| Phase 1 weak spot 1: task and component links in two places | 2 |
| Phase 1 weak spot 2: unbalanced example HTML | 3 |
| Reference pages: colours, tokens, utility classes (spec phase 2) | 4, 5, 6 |
| Check 2 stops asking records to cover classes the utility tables show | 6 |
| Reference entry in the top menu | 5, 6 |
| Spec and maintainer docs stay true | 1, 2, 3, 6 |

Not in 2a, by design: the seven component records (2b), more task pages (2c), the other deferred phase 1 findings, publishing, and an Accessibility page.

**Manual checks after Task 6 (Nan):** read the Colours page and the Type, space and shape page for wording (the intros in `guide/reference.toml` are written from the token descriptions and `THEMING-GUIDE.md`); check the phone layout of the colour table; decide whether to run a Docker Xerte test round so component records can gain an `[editor]` table.

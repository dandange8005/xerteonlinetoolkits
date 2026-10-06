"""A small, valid author guide for tests. write_guide() writes it into a temporary folder."""
import shutil
from pathlib import Path

import support

SITE = """\
title = "Test guide"
coverage = "warn"
tasks = ["draw-attention"]

[[groups]]
id = "emphasis"
title = "Emphasis"

[[menu]]
page = "home"
title = "Home"

[[menu]]
page = "getting-started"
title = "Getting started"

[[menu]]
page = "tasks"
title = "Tasks"

[[menu]]
page = "components"
title = "Components"
"""

CALLOUT = """\
+++
name = "callout"
title = "Callouts"
lead = "Pull one key idea out of the page."
group = "emphasis"
status = "current"
since = "v1.4"
tasks = ["draw-attention"]
related = []
scss = ["scss/components/_callout.scss"]

[editor]
survives = true
checked = 2026-09-20
xerte = "3.14"

[parts]
cu-callout = "The container."
cu-callout-title = "The short bold title."
cu-callout-icon = "Only for the older fa-stack markup."

[[examples]]
class = "cu-callout-tip"
label = "Tip"
purpose = "A shortcut or recommendation"
html = '''
<div class="cu-callout cu-callout-tip">
  <strong class="cu-callout-title">Tip</strong>
  <p>Fish &amp; chips.</p>
</div>
'''

[[examples]]
class = "cu-callout-warning"
label = "Warning"
purpose = "A risk the reader must avoid"
html = '''
<div class="cu-callout cu-callout-warning">
  <strong class="cu-callout-title">Warning</strong>
  <p>A risk.</p>
</div>
'''
+++

## When to use it

Use a callout for one idea.

### Do

- Name the variant in the title.

### Don't

- Stack more than two.

## Accessibility

The title says the variant in words.
"""

TASK = """\
+++
name = "draw-attention"
title = "Draw attention to something"
summary = "Make sure readers notice a tip or a warning."
icon = "fa-lightbulb"
components = ["callout"]

[example]
label = "An upload reminder"
purpose = "A paragraph with one Important callout."
html = '''
<p>Upload your file.</p>
<div class="cu-callout cu-callout-important">
  <strong class="cu-callout-title">Important</strong>
  <p>Check that the upload has finished.</p>
</div>
'''
+++

## Goal

Make one point stand out.

## Checklist

- The title names the variant.
"""

INDEX = """\
+++
name = "index"
title = "What do you want to do with your page?"
lead = "Pick a task."
new_steps = ["Choose the theme.", "Paste a callout."]

[[how]]
title = "Choose"
text = "Pick a component."

[[how]]
title = "Check"
text = "Run the checklist."
+++
"""

GETTING_STARTED = """\
+++
name = "getting-started"
title = "Getting started"
lead = "Switch a project to the theme."
+++

## Choose the theme

1. Open the project's properties.
2. Set **Theme** to Cardiff University Theme.

## Brand colours

```css
:root { --color-brand-primary: #00703C; }
```
"""

FILES = {
    "SITE": "site.toml",
    "CALLOUT": "content/components/callout.md",
    "TASK": "content/tasks/draw-attention.md",
    "INDEX": "content/pages/index.md",
    "GETTING_STARTED": "content/pages/getting-started.md",
}


def write_guide(root, **overrides):
    """Write the fixture guide into root/guide. A keyword such as CALLOUT="..." replaces that file;
    CALLOUT=None leaves the file out."""
    guide = Path(root) / "guide"
    texts = {"SITE": SITE, "CALLOUT": CALLOUT, "TASK": TASK, "INDEX": INDEX, "GETTING_STARTED": GETTING_STARTED}
    texts.update(overrides)
    for key, relative in FILES.items():
        if texts[key] is None:
            continue
        path = guide / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(texts[key], encoding="utf-8", newline="")
    for folder in ("templates", "assets"):
        real = support.GUIDE / folder
        if real.exists():
            shutil.copytree(real, guide / folder)
    return guide

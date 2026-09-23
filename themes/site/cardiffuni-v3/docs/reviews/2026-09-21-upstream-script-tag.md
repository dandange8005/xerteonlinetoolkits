# Draft upstream issue: missing closing angle bracket in site theme script tag

Status: prepared locally, not submitted. Source inspected 21 September 2026.

## Problem

In `modules/site/parent_templates/site/common/js/application.js`, `cssSetUp('theme')`
constructs the theme script element as:

```js
$('head').append('<script src="'+ themePath + theme + '/'+ theme+ '.js"' + '</script>');
```

The opening tag has no `>` after its quoted `src` value. The Phase 1 test record reports
that jQuery still fetches and executes the theme script, so this is a malformed-markup
correction rather than a claim that script loading always fails.

## Proposed correction

```js
$('head').append('<script src="'+ themePath + theme + '/'+ theme+ '.js">' + '</script>');
```

## Validation requested

Confirm that a theme script still loads once in editor preview, normal playback and a
standalone export. Preserve the existing ordering relative to theme CSS and player setup.
This report has not changed or tested the upstream player code.

# Xerte integration — Cardiff Learning Resource UI v1

17 September 2026. Read alongside [[Assessment Menu - Xerte Build Guide (Home Page, Option C)]]. This package does not modify the local or live Xerte project.

## Feasibility

The conversation can be implemented as a small custom component in a Bootstrap project. It needs three pieces: HTML Code for the structure/content, project Styles for the visual system, and project Script for navigation and temporary notes. No framework, API or backend is needed.

This is supported by the current [Xerte Bootstrap documentation](https://www.xerte.org.uk/wiki/doku.php?id=bootstrap), which describes the custom Script property, stylesheets and advanced HTML Code elements. The [Styles and Script documentation](https://www.xerte.org.uk/wiki/doku.php?id=styles_and_script) explains the CSS/JavaScript extension points.

The local source at `/Users/nanzhang/Projects/xerteonlinetoolkits/modules/site/parent_templates/site/common/js/application.js`, read on 17 September, provides stronger detail for this installation:

| Lines | Observed behaviour | Consequence |
| --- | --- | --- |
| 1440–1443 | Project script is inserted before content loads. | Do not initialise by querying once and assuming the component exists. |
| 2094 and 2110 | Sections are appended to `#mainContent`, then jQuery `contentLoaded` is triggered. | Initialise when this event fires; repeat safely on return visits. |
| 2238–2247 | A `markup` element appends its text, or loads its URL. | Use HTML Code for form fields and component structure. |

The existing project guide records Bootstrap 2 and the `cardiffuni-v2` theme. The portable package uses its own scoped CSS grid and native controls, so it does not rely on Bootstrap 3/4 class names.

## Files and where they go

| File | Destination |
| --- | --- |
| `conversation.html` | Home section → Advanced Options → HTML Code. Paste the fragment including the `.cu-resource` wrapper. |
| `tokens.css`, followed by `components.css` | Project Styles. Paste both in this order, without `<style>` tags. Alternatively host both in an approved stylesheet location. |
| `components.js` | Project Script. Paste once, without `<script>` tags. |
| `discovery.html` | Optional separate HTML Code element for testing discovery. **Adapt every entry URL to the actual Xerte Page/Section IDs before use.** Its supplied links target the local HTML prototype. |

Keep Xerte's own header, navigation and footer. The CSS is scoped to `.cu-resource`, and does not globally restyle the player. This means the component may need contextual spacing adjustments once viewed with the actual Cardiff theme; it is not a drop-in replacement for the whole theme.

For native Bootstrap links, use the local player’s page/section form, for example `#written|essay`, **only after checking the configured IDs**. The standalone prototype's `#page/written/essay` format is not Xerte's native route syntax.

## How the question component behaves

- Initialises on DOM ready and on jQuery `contentLoaded`.
- Installs one event handler set per component node. Repeated events do not advance twice.
- Keeps a small in-memory state keyed by `data-cu-conversation="assessment-design-v1"`.
- Restores the selected question and typed notes when Xerte removes and recreates the component during navigation.
- Copies all six questions and notes. If clipboard access is denied or unavailable, exposes a selected textarea for manual copying.
- Uses native buttons and labelled textareas. Deliberate step navigation focuses the newly displayed question heading.
- Does not call a server, use AI, store local/session storage, or send notes to Xerte tracking.
- On full player reload or close, state is cleared. On reopening, fields start empty.
- Without JavaScript, all six questions remain visible and the enhancement controls stay hidden. Users can read the questions and manually select their notes.

Keep the same key for the same question set on return visits. Use a different key if another component has different questions. If the question count or ordering changes, version the key so old in-memory positions are not misapplied.

## What authors can change

Question text, explanatory paragraphs, hints and labels are in the HTML. The script contains behaviour, not a separate hidden copy of the six questions. Keep `data-cu-*` attributes and the surrounding structure intact. This is easier to maintain than a complete standalone HTML page, but still needs someone comfortable with source markup.

The supplied fragments and visual component guide are **English specimens**. Translation and language review remain required. The earlier bilingual prototypes are preserved in this Codex folder as draft references. Do not add a language button that only translates a subset of the component.

## Effort and alternatives

| Approach | Benefit | Trade-off |
| --- | --- | --- |
| Custom component (recommended to prototype) | Preserves the reviewed interaction, notes and export. | A maintained HTML/CSS/JS component; test player lifecycle and theme integration. |
| Native accordion | Easier routine content editing and no custom note-state logic. | Does not reproduce the focused conversation, persistent-in-player notes or combined export. |
| Embed the standalone page | Keeps the exact standalone implementation. | Separate hosting/content copy, iframe height/focus and clipboard-context checks. |

The source code makes the custom route technically plausible; it does not establish that the current editor/theme combination has passed integration testing. No time estimate is implied.

## Integration check before adoption

1. Paste the HTML, styles and script into a test copy of the Bootstrap project.
2. Save, close and reopen the editor. Confirm buttons, textareas and `data-cu-*` attributes survive.
3. Preview. Use all six questions by keyboard; check focus is visible and only the current question is shown.
4. Type a note, visit another Xerte page, return and confirm the note and current step survive.
5. Repeat navigation; confirm each click advances only once. Open another copy of the player and confirm notes are not shared between windows.
6. Test copy on the actual published origin and the manual-copy path when permission is denied, including an embedded/LMS context if that is how the resource is delivered.
7. Test narrow screens, Welsh text expansion, zoom and the Cardiff theme’s form styling.
8. Check all 17 entry links against the configured Page/Section IDs.
9. Keep D1 visibly proposed until agreed and complete language review before publication.

## Validation boundary

The component's standalone layout, state retention, reinsertion lifecycle, repeat initialisation and export fallback are checked separately in the companion validation record. It has **not** been pasted into the Xerte editor or tested in the production Cardiff player during this task.

# Audio Player Component — Design Spec
**Date:** 2026-03-12
**Project:** Inclusive Prehabilitation for People with Cancer
**Status:** Approved

---

## Overview

A self-contained HTML snippet that renders a single audio file as a horizontal card. Page authors paste the snippet into the Xerte HTML editor and swap out three values: the audio file path, the display title, and the file size string.

---

## Context and Constraints

- **Platform:** Xerte Online Toolkits (XOT1 / Modern Nottingham theme)
- **Delivery:** Raw HTML pasted into the Xerte page HTML editor
- **Design system:** Uses tokens and utility classes from `custom.css` — no additional stylesheet required
- **Icon library:** Font Awesome 5 Free (already loaded by Xerte)
- **Audio files:** MP3 only, hosted on the same server, referenced by relative path. No fallback format required — all target browsers support MP3 natively
- **Scope:** One audio file per component instance; one instance per page

---

## Component Design

### Layout

Horizontal flex card (`flex-direction: row`, the default), three sections left to right. The layout remains horizontal at all viewport widths — the Xerte reading column is always wide enough to accommodate it.

| Section | Content |
|---|---|
| Icon | `fa-headphones fa-2x`, coloured `--color-primary` |
| Info | Title stacked above file size; fills available space between icon and button |
| Button | Circular 44×44px play/pause toggle |

### CSS — class names vs inline styles

All class names below are verbatim utility classes defined in `custom.css`. Properties that have no matching utility class are set via inline `style` attributes — these are called out explicitly.

**Card container element (`<div>`):**

Classes: `.flex .items-center .gap-md .bg-surface .border .rounded-lg .shadow-card .p-md`

No inline styles needed on the card.

**Icon wrapper (`<div>`):**

Classes: `.flex-center`

No fixed width — the wrapper sizes to the icon. No inline styles needed.

**Icon element:**

```html
<i class="fas fa-headphones fa-2x" aria-hidden="true" style="color: var(--color-primary);"></i>
```

`fa-2x` renders at 2em (~32px). Colour is set via inline `style` because no colour-specific utility class maps to `--color-primary` for arbitrary elements.

**Info wrapper (`<div>`):**

Classes: `.flex .flex-col`
Inline style: `style="flex: 1;"` — no utility class for `flex-grow: 1`

**Title (`<span>`):**

Classes: `.font-semibold .text-heading`

**File size (`<span>`):**

Classes: `.text-sm .text-muted`

Optional field: the author may leave the text content blank or delete the element entirely. An empty `<span class="text-sm text-muted"></span>` renders invisibly — no JS handling required either way.

**Play/pause button (`<button>`):**

- `id="xot-audio-btn"` — required so the `onended` handler can locate and reset the button icon
- Classes: `.rounded-full .bg-primary .text-on-dark .flex-center`
- Inline style: `style="width: 44px; height: 44px; border: none; cursor: pointer;"` — no utility classes cover fixed dimensions
- Focus state: `style` also includes no explicit focus override; the developer must add `:focus-visible` via a `<style>` block in the snippet (see Focus section below)
- `aria-label="Play audio"` — updated dynamically

Icon inside button:

```html
<i class="fas fa-play" aria-hidden="true"></i>
```

No `id` on the icon — it is reached via `document.querySelector('#xot-audio-btn i')`.

**Audio element:**

```html
<audio id="xot-audio-player" src="..." preload="none" hidden
       onended="document.querySelector('#xot-audio-btn i').className='fas fa-play'; document.getElementById('xot-audio-btn').setAttribute('aria-label','Play audio');"></audio>
```

The `<audio>` element sits as the last child inside the card `<div>`. The `hidden` attribute hides it from all users including assistive technology.

---

### Behaviour

**Button onclick handler (inline):**

```javascript
(function(btn) {
  var audio = document.getElementById('xot-audio-player');
  var icon  = btn.querySelector('i');
  if (audio.paused) {
    audio.play();
    icon.className = 'fas fa-pause';
    btn.setAttribute('aria-label', 'Pause audio');
  } else {
    audio.pause();
    icon.className = 'fas fa-play';
    btn.setAttribute('aria-label', 'Play audio');
  }
})(this)
```

This is written as an IIFE using `this` (the button element) to avoid global variable pollution.

**Audio `onended` handler (inline on the `<audio>` element):**

```javascript
document.querySelector('#xot-audio-btn i').className='fas fa-play';
document.getElementById('xot-audio-btn').setAttribute('aria-label','Play audio');
```

When playback ends naturally, the button icon resets to `fa-play` and the `aria-label` reverts to `"Play audio"`.

---

### Focus state

Since this is a healthcare project with WCAG requirements, the button must have a visible focus ring. Because the button's background (`--color-primary`) may conflict with the browser's default outline colour, add a scoped `<style>` block at the top of the snippet:

```html
<style>
  #xot-audio-btn:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 3px;
  }
</style>
```

---

### Author-editable values

Authors change exactly three things in the snippet:

1. `src` on the `<audio>` element — relative path to the MP3 (e.g. `media/audio/intro.mp3`)
2. Title text inside the title `<span>`
3. File size string inside the file size `<span>` (e.g. `3.2 MB`) — optional, may be left blank or the element deleted

---

## Accessibility

- Button is a native `<button>` element — Space and Enter trigger click by default; no additional keyboard handling needed
- `aria-label="Play audio"` on the button, updated to `"Pause audio"` when playing, reset to `"Play audio"` on ended
- `aria-controls` is explicitly out of scope for this component
- All decorative icon elements carry `aria-hidden="true"`
- Focus ring specified via `#xot-audio-btn:focus-visible` (see Focus state section)

---

## Complete Snippet Structure

```
<style> … focus-visible rule … </style>

<div class="flex items-center gap-md bg-surface border rounded-lg shadow-card p-md">

  <!-- Icon -->
  <div class="flex-center">
    <i class="fas fa-headphones fa-2x" aria-hidden="true"
       style="color: var(--color-primary);"></i>
  </div>

  <!-- Info -->
  <div class="flex flex-col" style="flex: 1;">
    <span class="font-semibold text-heading">EDIT: title</span>
    <span class="text-sm text-muted">EDIT: file size (optional)</span>
  </div>

  <!-- Play/pause button -->
  <button id="xot-audio-btn"
          class="rounded-full bg-primary text-on-dark flex-center"
          style="width: 44px; height: 44px; border: none; cursor: pointer;"
          aria-label="Play audio"
          onclick="(function(btn){ … })(this)">
    <i class="fas fa-play" aria-hidden="true"></i>
  </button>

  <!-- Hidden audio element — EDIT: src path -->
  <audio id="xot-audio-player" src="EDIT.mp3" preload="none" hidden
         onended="…"></audio>

</div>
```

---

## Out of Scope

- Progress bar / scrubber
- Volume control
- Multiple audio files / playlist
- Dynamic data loading
- `aria-controls` on the button
- Audio format fallback (MP3 only)
- Responsive layout collapse (horizontal layout held at all widths)
- Multiple instances per page (static IDs are sufficient for single-instance use)

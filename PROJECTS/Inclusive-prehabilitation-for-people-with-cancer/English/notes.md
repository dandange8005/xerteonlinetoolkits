## Background

I have delivered and completed the project and handed over to Shea. 

Shea made some edits to some of the pages in Xerte and had broken some of the custom code that I had written. 

Shea then asked me to help to fix the issues.

## The issues

I hope you had a good break. There have been a few edits from the version you copied across from HEIW, so it is only the following issues and pages that need to be resolved. No problem about doing this next week.
 
English version 24238
https://xerte.cardiff.ac.uk/play_24238#page19 – the interactive cards and associated links to the audio files are not functioning. The content is visible within the editor but not on the published version.
https://xerte.cardiff.ac.uk/play_24238#page36 – the links to the audio files are not functioning.
https://xerte.cardiff.ac.uk/play_24238#page43 – the links to the audio files are not functioning.
https://xerte.cardiff.ac.uk/play_24238#page50 – the link to the audio file is not functioning
https://xerte.cardiff.ac.uk/play_24238#page51 – the link to the audio file is not functioning. Not sure if the cards are formatted as they were previously.
https://xerte.cardiff.ac.uk/play_24238#page52 – the link to the audio file is not functioning. Not sure if the cards are formatted as they were previously.
https://xerte.cardiff.ac.uk/play_24238#page53 – the links to the audio files are not functioning. Not sure if the cards are formatted as they were previously.
https://xerte.cardiff.ac.uk/play_24238#page60 – the links to the audio files are not functioning.
https://xerte.cardiff.ac.uk/play_24238#page61 - – the links to the audio files are not functioning.
 
Welsh version 24449
https://xerte.cardiff.ac.uk/play_24449#page8 – the links to the audio files are not functioning (these will be the same English audio files as in the English version 24238 – we do not have Welsh audio files)
https://xerte.cardiff.ac.uk/play_24449#page25 – the interactive cards are not functioning as they do on the English version, although the content is visible on the published version.
All other issues identified in the English version above are replicated in the Welsh version
 
Thanks again and apologies for messing up – it all looked fine in the editor but only when looking at the published version did I see that it had messed these up.
 
Best wishes

## The solution

Went through the issues page by page, worked out what had actually broken, and rebuilt each broken page as a local `.html` file (`English/pageN.html`, `Welsh/pageN.html`) ready to paste into the Xerte editor. `custom.js` was **not** touched — every fix works within the script exactly as it already is.

### What actually went wrong

Both the audio players and the cards are built by `custom.js` reading specific HTML structure out of the page (see `custom.js` and `docs/2026-03-12-audio-player-component-design.md`). The player, in particular, is strict about shape:

```html
<div class="ippc-audio-player">
  <span class="ippc-audio-title">…</span>
  <audio class="ippc-audio" src="…" preload="none" hidden></audio>
</div>
```

`buildPlayer()` in `custom.js` does `card.insertBefore(infoWrapper, titleEl)` and `card.insertBefore(btn, audio)` — both assume the title and the `<audio>` are direct children of `.ippc-audio-player`. Editing the page in a way that changes that shape breaks the player silently: it looks fine in the editor (custom JS/CSS only runs on the published page — noted in `docs/dev-summary.md`), and only shows as broken once published.

Two ways this happened, both consistent with selecting text that spans a player and applying formatting (a font size, or a paste from Word/a doc):

1. **Wrapped, not moved** (English pages 43, 50, 51, 52, 53, 60, 61; most Welsh pages): the title and `<audio>` got wrapped in an extra `<span style="font-size:22px;">`, so they were no longer direct children of `.ippc-audio-player`. `buildPlayer()` threw (`NotFoundError` / `TypeError`) and the player never rendered — 0 players built, matching what Shea saw.
2. **Title pulled out** (English pages 19, 36; the Welsh page 8/19/36 equivalents were similar): the "Click the play icon…" text was pulled out of the player entirely into its own paragraph, leaving an empty, title-less player. Same result — `buildPlayer()` had nothing to work with and threw.

The same font-size wrapping also explains the card questions on pages 51/52/53: the cards themselves weren't structurally broken, but a `font-size:22px` span around each heading/paragraph was overriding the sizes the cards are meant to use from `custom.css`, so they didn't look like the other cards on the site.

**For future edits:** don't apply formatting (font size, paste from Word) across text that includes one of `.ippc-audio-player`, `.ippc-card`, `.ippc-banner-card` or `.ippc-slider` — it's easy to wrap or move the elements `custom.js` depends on. Edit the surrounding paragraph text on its own, or copy a fresh snippet from `components/*.html` for a new instance.

### How each page was fixed

For every broken page: removed the stray font-size spans, rebuilt each audio player back into the exact shape `custom.js` needs, and matched clips to quotes by downloading each `.mp3` from the Xerte media library and transcribing it (`whisperkit-cli`) to check it against the quote text. Verified against a headless simulation of the real `custom.js` (no errors, correct player/slider count) before saving each file, and confirmed every audio/image link resolves in the target project's media folder.

**English** (`English/pageN.html`) — 9 pages:

| Page | Title | Fault | Fix |
|---|---|---|---|
| 19 | Factors affecting an individual's access and adherence to prehab | Audio prompts pulled into the sliders' quote slides; only 3 title-less players left over. Not the original layout — HEIW has each slider followed by a separate list of players. | Rebuilt as 3 sliders (6/6/5 slides, no audio inside) each followed by its own list of players — 20 in total, titles/sizes matched from the HEIW screenshot. |
| 36 | Health behaviour change techniques | 5 audio prompts pulled out (3 inside the quotes grid); 1 title-less player left with no audio title. | Restored the quotes grid to just its 4 quotes; added 2 separate player lists (4 after the grid, 1 after the speech-bubble image), matching HEIW order. |
| 43 | Support from family and friends | Both players wrapped in a font-size span → `NotFoundError`, 0/2 built. | Rebuilt both players in place, after their quotes (matching HEIW). |
| 50 | Introducing Prehab | 1 player wrapped → 0/1 built. | Rebuilt in place. |
| 51 | The perceived need and potential benefits of prehabilitation | 1 player wrapped → 0/1 built; card text/heading sizes overridden by font-size spans. | Rebuilt the player; removed the font-size spans from all 4 cards. |
| 52 | Providing acceptable cancer prehabilitation interventions | Same as 51, plus a stray empty `<p>` inside card 3 acting as an extra flex item and skewing its layout. | Rebuilt the player; removed the font-size spans; removed the stray paragraph. |
| 53 | Approaches to follow-up | Both players wrapped → 0/2 built; same card sizing issue on all 4 cards. | Rebuilt both players; removed the font-size spans from the cards. |
| 60 | How resources are delivered | Both players wrapped → 0/2 built; same sizing issue on both banner cards. | Rebuilt both players; removed the font-size spans from the banner cards. |
| 61 | Adapting resources to individuals' daily lives | Both players wrapped → 0/2 built. | Rebuilt both players in place. |

**Welsh** (`Welsh/pageN.html`) — 11 pages. Same faults as the English pages, replicated as Shea's email said, plus two pages that are Welsh-only:

| Page | Title | Fault | Fix |
|---|---|---|---|
| 8 | Beth mae gwaith ymchwil blaenorol yn ei ddweud? | All 17 players had an empty title span with the Welsh prompt text loose beside it, wrapped in a font-size span. | Rebuilt all 17 in place; also found and removed a corrupted `aptos=""` attribute (a Word-paste artefact, not an audio fault) on 3 quotes. |
| 19 | Ffactorau sy'n effeithio ar fynediad unigolyn… | Same as English 19. | Same fix; titles use the Welsh half of the HEIW bilingual titles. |
| 25 | Dyma rai cwestiynau i'ch helpu i ddeall yr unigolyn | Welsh-only fault: "Cyfle" and "Cymhelliant" had become headings *inside* the "Gallu" slide instead of starting their own slides — the slider had 2 slides instead of 4. | Split into 4 slides, matching the English page. No audio on this page. |
| 36 | Technegau newid ymddygiad iechyd | Welsh-only: the audio had been lost entirely, and the "Hunan-fonitro:" heading had been turned into an empty, audio-less player. | Restored the heading; added the same 5-player layout as English page 36, titled from the page's own Welsh wording (HEIW had no Welsh titles for this page). |
| 43, 50–53, 60, 61 | (as English) | Same wrapped-title fault as their English equivalents. | Same fix as the English pages, including the card cleanup on 51–53 and 60. |

### Media links

Audio and image `src` attributes went through two forms while fixing this:

1. First, Xerte's own relative form — `src="FileLocation + 'media/…'"`, the same form stored in `data.xml` — so one page could be pasted unchanged into the English (24238), Welsh (24449) or dev (25056) project.
2. Per a later request, converted to direct absolute links scoped to each project: English pages now link straight to `https://xerte.cardiff.ac.uk/USER-FILES/24238-sopnz-Nottingham/media/…`, Welsh pages to `https://xerte.cardiff.ac.uk/USER-FILES/24449-sopnz-Nottingham/media/…`. Every link was checked (HTTP 200) against its project's media folder before being written in. This means each set of pages is now scoped to its own project and won't resolve unmodified if pasted into a different one (including the dev project).

### Outstanding — none of this is pasted into Xerte yet

Everything above exists only as local files under `English/` and `Welsh/`. Still to do:

- Paste each page into its project (dev project first for a sanity check, then 24238/24449) and confirm in the real editor/player — everything above was checked with a simulated version of `custom.js`, not the live site.
- After saving, each page's clips should show as "in use" in Xerte's media list.

Content questions for Shea, left alone rather than guessed at:

- **English 19** — 3 quotes have no matching recording (Technology, both Isolation quotes); 2 clips (M2Q1PT, M2Q3PT) aren't used by any quote on the current page.
- **English 36** — HEIW labels the 2nd player "pacing", but the clip plays the "permission" quote; labelled by what it actually plays instead.
- **English 51/52** — card 4 (page 51) and card 3 (page 52) repeat a sentence that doesn't fit their heading — looks like a copy-paste slip from Shea's edit.
- **Welsh 19** — slide order and a couple of merged quotes differ slightly from the English page.
- **Welsh 52** — missing a "Click here" link and has an English-language heading, where the English page has both.
- **Welsh 8/61** — still carry some leftover Word-paste formatting (line-height/font-family spans) beyond the `aptos=""` fix; harmless but not cleaned up.


## The dev project

https://xerte.cardiff.ac.uk/play_25056


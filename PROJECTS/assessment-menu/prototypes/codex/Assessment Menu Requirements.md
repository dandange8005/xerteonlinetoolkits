# Assessment Menu — project requirements

Apply the shared [[🎨 Cardiff University Design System/design-system/DESIGN|Cardiff Resource Design System]]. These requirements belong to this project, not to the generic system:

- Retain the exact six design questions and guidance-not-policy framing.
- Retain discovery of all 17 assessment types and links to the wider guidance.
- Keep D1 wording visibly proposed until agreed.
- Welsh translation needs language review.
- Retain the conversation pattern with temporary notes and copy fallback for further Xerte testing.
- The final combined landing-page composition and list/grid default remain open.
- Lane colours and labels are project-specific extensions; do not add them to the shared core tokens.

The existing `design-system/v1/` package remains the original assessment implementation. Its Xerte integration still requires testing inside the actual editor/player. New generic components use `CUResourceUI`; the old package uses `CUAssessmentUI`. Avoid double-enhancing the same markup.

Source: [[2026-09-17 Assessment Menu Design Review]]. The subsequent request to generalise the design language is captured in [[🎨 Cardiff University Design System/design-system/README|the shared system index]].

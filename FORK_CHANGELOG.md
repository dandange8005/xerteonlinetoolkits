# Fork Changelog - Cardiff University / DigEd Customizations

> **Maintainer:** Dan Dange ([@dandange8005](https://github.com/dandange8005))
> **Fork of:** [thexerteproject/xerteonlinetoolkits](https://github.com/thexerteproject/xerteonlinetoolkits)
> **Purpose:** Custom themes and templates for Cardiff University Digital Education
> **Note:** This fork is for internal use only and will not submit pull requests to the upstream repository.

This changelog tracks all customizations made to this fork that differ from the upstream Xerte Online Toolkits repository.

---

## Overview

This fork maintains custom themes for Cardiff University's Digital Education team while staying in sync with upstream Xerte releases.

### Custom Assets (Not in Upstream)

| Asset | Location | Description |
|-------|----------|-------------|
| Cardiff Uni Theme | `themes/site/cardiffuni/` | Full theme with SCSS architecture, design tokens, and custom components |
| DigEd Bootstrap Theme | `themes/site/diged/` | Modern Bootstrap-based theme with modular SCSS |
| CKEditor Styles | `editor/js/vendor/ckeditor/styles.js` | Custom editor styles for Cardiff branding |
| Project Docs | `CLAUDE.md` | AI assistant context for development |

---

## Changelog

### [Unreleased]

#### Added
- DigEd Bootstrap theme (`themes/site/diged/`)
  - Modular SCSS architecture with abstract, base, components, layouts, utility layers
  - Custom properties system for runtime theming
  - Responsive breakpoint system
  - Print styles support

#### Notes
- Featherlight lightbox applies `overflow:hidden` to html, which causes scroll reset - needs investigation

---

### [2026-01-22] - Fork Sync & AI Features Setup

#### Changed
- Synced fork with upstream `develop` branch (994 new commits)
- Major upstream additions include:
  - AI integration (OpenAI, Anthropic, Mistral support)
  - Security fixes (RCE vulnerability #1505, SSRF bypass #1504)
  - Interactive Video improvements (#1513, #1510)
  - Graph library for analytics
  - Quiz/MCQ button display options
  - Accessibility improvements (#922 Bullets page)

#### Added
- `vendor_config.php` - AI vendor API key configuration
  - Configured OpenAI API keys for:
    - AI content generation (GPT)
    - Transcription (Whisper)
    - Embeddings/RAG (OpenAI encoding)
    - Image generation (DALL-E 2, DALL-E 3, GPT Image 1)

#### Database
- Ran `upgrade.php` to create AI-related tables:
  - `management_helper` - Stores AI vendor settings and preferences
  - `ai_request_logs` - Tracks AI API usage and costs

#### Configuration
- Enabled AI vendors in Management → AI Settings admin panel

---

### [2024-11-23] - Fork Sync & DigEd Theme

#### Changed
- Rebased fork onto upstream `develop` branch
- Resolved `.gitignore` conflict (merged upstream's `openai_config.php` ignores with local `.DS_Store`)

#### Added
- `themes/site/diged/` - New DigEd Bootstrap theme
- OKLCH color documentation for improved color scales

---

### [2024-10-12] - Cardiff University Theme v2.0

#### Added
- Modular component system with 10 custom components:
  - Boxes, Buttons, Callout, Cards, Details
  - Do's & Don'ts lists, Language toggle, Links, Project Info, Quotes
- Design token system (`scss/_tokens.scss`)
- CSS custom properties for runtime customization
- Component showcase page
- Flexbox utility system
- CKEditor custom styles

#### Changed
- Migrated from monolithic CSS to modular SCSS architecture
- Updated all components to use Cardiff design tokens
- Restructured theme documentation

#### Documentation
- `CARDIFF_THEME_GUIDE.md` - Complete theming guide
- `Components.md` - Component catalog and usage
- `DevLog.md` - Development decisions log
- `THEMING-GUIDE.md` - Customization instructions

---

### [2024-09] - Initial Cardiff Theme

#### Added
- `themes/site/cardiffuni/` - Initial Cardiff University theme
- Custom SCSS variables for Cardiff branding
- Base editor styles integration

---

## Syncing with Upstream

To sync this fork with the latest upstream changes:

```bash
# Fetch upstream
git fetch upstream

# Rebase onto upstream/develop
git rebase upstream/develop

# Resolve any conflicts, then force push
git push --force-with-lease origin develop
```

## File Inventory

### Files Modified from Upstream
- `.gitignore` - Added `.DS_Store`
- `editor/js/vendor/ckeditor/styles.js` - Custom editor styles

### Files Added (Not in Upstream)
```
CLAUDE.md
FORK_CHANGELOG.md (this file)
.vscode/settings.json
vendor_config.php          (AI API keys - do not commit to public repos)
themes/site/cardiffuni/    (entire directory)
themes/site/diged/         (entire directory)
```

---

## Contact

For questions about these customizations:
- GitHub: [@dandange8005](https://github.com/dandange8005)
- Organisation: Cardiff University Digital Education

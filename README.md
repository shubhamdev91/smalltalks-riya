# Small Talk

Small Talk is a premium press-on nail brand from India. Seven nail sets, each tied to a small moment where she
naturally shows her hand, sold through a Shopify store (`0nev20-vn.myshopify.com`, INR).

This repository holds the store's source and working materials: the Shopify theme, the backend for "the talks"
community board, artwork, design specs, copy, SEO strategy, policies and QA records.

AI agents and new contributors: start with [AGENTS.md](AGENTS.md).

## Repository layout

| Path | Contents |
|---|---|
| `theme-build/src/` | Shopify theme (Horizon 4.1.5 base + Small Talk layer): `assets/`, `blocks/`, `config/`, `layout/`, `locales/`, `sections/`, `snippets/`, `templates/` |
| `theme-build/pristine/`, `theme-build/ref/` | Stock Horizon and reference copies, for diffs |
| `theme-build/tools/` | Python checks and helpers (Liquid lint, md5 readback, page checks) |
| `talks/backend/` | "the talks" backend: Python standard-library WSGI app, deployed on Vercel |
| `talks/` | Talks design, owner setup guide, staged theme files, seed data |
| `motion/` | Home hero motion: contract, script, styles, lab |
| `artwork/` | Artwork sources, processed web and HD exports, packaging; `manifest.json` indexes processed assets |
| `spec/` | Design spec: tokens, type, fonts (OFL), layout geometry |
| `copy/` | Copy register (every shopper-visible string has an ID), `FACTS.md`, policy drafts |
| `seo/` | SEO and AEO strategy |
| `policies/` | Store policy texts |
| `owner-plan/` | Source of the owner's launch plan page |
| `qa/` | Acceptance criteria and QA records |
| `backup/` | Snapshot of an earlier theme and the campaign metaobjects |
| `archive/` | Project history: session transcripts and coordination notes (reference only) |
| `Small-Talk-Claude-Implementation-Checklist.md` | Work plan and current status (see **RESUME HERE**) |
| `build-log-foundation.md` | Theme build log |

## Live systems

| System | Where it runs | Notes |
|---|---|---|
| Storefront theme | Shopify | Work happens on the build theme `186651934933`; the live theme is a published copy of it |
| Theme editor settings | Shopify | `config/settings_data.json` is edited in the theme editor; the copy here is not authoritative |
| Products, pages, menus, metaobjects, policies | Shopify admin | Store data is not stored in this repo |
| Talks backend | Vercel project `small-talk-talks-backend` | Reached through the Shopify App Proxy `/apps/talks`; health check at `/api/talks` |

Secrets (Shopify app credentials, salts, provider keys) are kept in Vercel and provider dashboards, never in this repository.

## Working with the code

Requirements: Python 3.12+. No third-party packages.

Run the talks backend tests:

```bash
cd talks/backend
python -m unittest discover -s tests
```

Lint Liquid before uploading theme files:

```bash
python -I theme-build/tools/liquid_lint.py theme-build/src/sections/<file>.liquid
```

Theme changes are uploaded to the build theme only, one writer at a time; see [AGENTS.md](AGENTS.md) for the rules.

## Not tracked

Bulk screenshot runs from QA and the motion lab (`qa/desktop`, `qa/fidelity`, `qa/foundation`, `qa/sonnet`,
`qa/motion`, `theme-build/lab/shots`) are excluded by `.gitignore`.

## Ownership

Proprietary. © Small Talk. All rights reserved. Fonts in `spec/fonts/` and `theme-build/fonts/` are under the SIL Open
Font License (see each folder's `OFL.txt`).

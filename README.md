# Small Talk — project backup

Everything needed to rebuild the Small Talk store work if this laptop is lost. **Agents: start with [AGENTS.md](AGENTS.md).**

| Folder | What it is | Where the live copy runs |
|---|---|---|
| `theme-build/src/` | Shopify theme source (Horizon-based "Claude build") | Shopify — theme 186651934933 is the build; the live store is whichever theme is **MAIN** (owner publishes a copy) |
| `theme-build/pristine/` | Untouched Horizon theme, for diffs | — |
| `talks/backend/` | Talks backend (Python, `app.py`) | Vercel project `small-talk-talks-backend`, deployed via v0 |
| `talks/` (rest) | Talks design, owner setup, staged theme files, seed data | — |
| `artwork/` | All artwork: sources, HD, web exports, packaging | Web exports are uploaded into the theme's `assets/` |
| `spec/`, `copy/`, `seo/`, `policies/`, `motion/`, `owner-plan/` | Specs, copy, SEO, policies, hero motion, owner plan | — |
| `qa/` | QA notes and small screenshot sets (bulk screenshot runs are not committed) | — |
| `backup/` | Snapshot of an earlier Shopify theme | — |

## Not in this repo

- **Secrets.** The talks app's Shopify Client ID/secret and salt live only in Vercel environment variables.
- **Store data.** Products, metaobjects (talks), pages, menus and theme editor settings live in Shopify.
  `theme-build/src/config/settings_data.json` here is an old copy; the owner edits the real one in the theme editor.
- **Bulk QA screenshots** (`qa/desktop`, `qa/fidelity`, `qa/foundation`, `qa/sonnet`, `qa/motion`, `theme-build/lab/shots`) — regenerable.

## Keeping it current

This repo does not sync itself. After a work session:

```bash
git add -A
git commit -m "Describe what changed"
git push
```

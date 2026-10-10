# AGENTS.md — Small Talk

Repository: https://github.com/shubhamdev91/smalltalks-riya (private). The owner's working copy is
`C:\Users\SSTS\Desktop\Riya`. Paths below are relative to the repository root.

Small Talk is a premium press-on nail brand (India, INR) selling on Shopify store `0nev20-vn.myshopify.com`.
Owner: Riya. Shubham runs the build with Claude sessions.

## Read first, in this order

1. `Small-Talk-Claude-Implementation-Checklist.md` → the **RESUME HERE** block is the current truth.
   Where any other file (including this one) disagrees, the checklist wins.
2. The launch plan page, tab **For AI agents**: https://claude.ai/artifact/GLWcdxYnCWEXUMDQJyRshF
   (themes, store data, talks, design system, team, decisions, open items, start-here prompt).
3. `spec/INDEX.md` + `spec/tokens.css` (design), `copy/00-register.md` + `copy/FACTS.md` (words and facts),
   `qa/FINAL-ACCEPTANCE.md` (what "done" means), then whatever your task touches.

## Map

| Path | What it is |
|---|---|
| `theme-build/src/` | Shopify theme source (Horizon 4.1.5 + Small Talk layer). Mirrors build theme **186651934933** |
| `theme-build/pristine/`, `theme-build/ref/` | Stock Horizon and reference copies, for diffs |
| `theme-build/tools/` | Python helpers: `liquid_lint.py`, `md5check.py`, checks and lab scripts |
| `theme-build/copy-map.json` | Locale keys → copy register IDs |
| `talks/` | "the talks" anonymous board: `DESIGN.md`, `OWNER-SETUP.md`, `staged/` theme files, `seed/` |
| `talks/backend/` | Talks backend (`app.py`, stdlib WSGI, tests in `tests/`). Live on Vercel project `small-talk-talks-backend` |
| `motion/` | Hero motion: `CONTRACT.md`, `st-hero-motion.js`, `st-hero.css`, `lab/` |
| `artwork/` | All art. `manifest.json` = processed asset index. `chatgpt/`, `chatgpt-refs/` = owner sources; `hd/` = HD exports |
| `spec/` | Board spec, tokens, type, fonts (OFL), joins/beelines JSON |
| `copy/` | Copy register (every shopper-visible string has an ID), `FACTS.md`, policy drafts |
| `seo/` | `STRATEGY.md`, SEO review |
| `policies/` | Policy source texts |
| `owner-plan/` | Source of the launch-plan page (the published page may be newer) |
| `qa/` | Acceptance notes and small screenshot sets |
| `backup/` | Snapshot of deleted theme 186649313493 and campaign metaobjects |
| `build-log-foundation.md` | Theme build log |

## Live systems

The repository is source and records; these systems hold the live state.

- **Shopify themes.** The build theme 186651934933 is the only theme agents write, and only while holding the
  orchestrator's write lock. The live store is whichever theme is **MAIN**; the owner updates it by duplicating
  the build and publishing the copy. Never write the MAIN theme. Check which theme is MAIN before acting.
- **Theme editor settings.** `config/settings_data.json` is edited by the owner in the theme editor. The copy in
  `theme-build/src/config/` is not authoritative; never upload it.
- **Store data.** Products, metaobjects (campaign + talks), pages, menus, policies live in Shopify. Changes go as a
  proposal to the orchestrator and need the owner's approval.
- **Talks backend.** Deployed from the v0 chat to Vercel. The health check
  `https://small-talk-talks-backend.vercel.app/api/talks` reports the `build` hash = first 12 hex of md5(`app.py`).

## Rules

- Never ask for, read or store secrets. Vercel holds the talks app's Client ID/secret and salt.
- Every shopper-visible word comes from the copy register (st-copy). Don't write UI text yourself.
- Brand: "Diet Cherry" (never "Cherry Repeat"); Brainwave = "Haan, mera idea hai."; no campus/college references;
  no fake reviews, ratings or counts; no medical claims; agents don't generate new artwork.
- Shopify file upserts can fail silently: lint Liquid (`theme-build/tools/liquid_lint.py`) and read back md5s.
- Commit with a clear message and push when a piece of work is finished.

## History (search only when needed)

`archive/` holds past session transcripts and coordination notes. It is large and not required reading; see
`archive/README.md` and search it for a specific decision or event rather than reading it end to end.

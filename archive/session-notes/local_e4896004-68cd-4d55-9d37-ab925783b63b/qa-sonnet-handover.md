# Operational QA (Sonnet checker) — hand-over

Report: `C:\Users\SSTS\Desktop\Riya\qa\sonnet\QA-REPORT.md` (raw JSON in `qa\sonnet\raw\`, scripts in `qa\sonnet\scripts\`).
Run: 2026-10-10, theme 186651934933 (unpublished, t/8 assets), Chrome 154 + Playwright; Lighthouse NOT run (no Node on this machine) — perf = CDP-throttled lab data, clearly labelled.

Failures by check: 1 HTML = 1 (Low, favicon 404) · 2 Structured data = 0 · 3 Links = 1 (Medium, /pages/the-talks orphan + duplicate title/H1 of /blogs/the-talks; 0 broken links; 0 refund-policy links) · 4 A11y = 8 axe rules (1 critical, 4 serious, 2 moderate, 1 minor) · 5 Perf = 2 (High: home mobile LCP 8.2–9.1 s lab; Medium: TBT proxy 1.4–3.0 s, INP proxy 464 ms on home).

Nothing was changed on the store. Cart add/remove was done and reverted (cart back to 0 items). Checkout never opened.

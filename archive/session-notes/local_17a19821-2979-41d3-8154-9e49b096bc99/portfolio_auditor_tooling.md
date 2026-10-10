# Portfolio auditor — tooling notes (2026-10-08)

**Coordinator (updated 2026-10-08):** send all portfolio-audit reports to the Hiring orchestrator, local_005b980d-e89c-4928-ac49-71d710be22f2. The old coordinator, local_17a19821-2979-41d3-8154-9e49b096bc99, is retired. This overrides the coordinator id in portfolio_audit_instructions.md.
Status: queue empty, 53 audits done, waiting for "resume audits".

- The GitHub REST API is unauthenticated: 60 requests/hour, shared by every session on this machine. `tools\gh_fetch.py` and its HTML fallback both return 429 once that runs out.
- Fallback that works: the public commits Atom feed, `https://github.com/<owner>/<repo>/commits/HEAD.atom?page=N`, which gives 20 entries per page with date, author and message. Helper script (read-only, stdlib only): `C:\Users\SSTS\AppData\Local\Temp\claude\C--Users-SSTS-Desktop-Hiring\e564b034-d387-49e2-971b-5548ce794421\scratchpad\commits_atom.py owner/repo [pages]`. Run it with python -I.
- Built-in browser: `navigate` fails when no tab is open. `mcp__Claude_Browser__preview_start {url}` opens a new tab and returns a tabId; pass that to get_page_text and close it afterwards.
- Long-term fix: put a no-scope GitHub token in `.secrets\github_token.txt`. That raises the limit to 5000 requests/hour for everyone.
- Audit verdicts are in `portfolio_audits/` and `progress/portfolio_audit.csv`.

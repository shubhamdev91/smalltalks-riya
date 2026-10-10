# Case-study assessor — status 10 Oct 2026
- Started. Procedure: case_study_assessor_instructions.md (static review only, never run candidate code).
- Heartbeat: session cron "53 */6 * * *" (job b67d3714, session-only, auto-expires after 7 days, about 17 Oct). It dies if this session exits; QUEUE.md stays the fallback.
- tools/cs_similarity.py is ready and self-tested on synthetic fixtures: `python -I tools\cs_similarity.py <id>` compares the latest submission against all others (`--json` and `--threshold` are available). Note: SQL similarity runs high because everyone starts from the DDL we handed out, so weigh the go/ts columns.
- Queue at start: empty. case_study_scores.csv not created yet; it gets created on the first assessment.

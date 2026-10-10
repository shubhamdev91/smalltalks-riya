# Owner plan artifact (10 Oct 2026)

Artifact: https://claude.ai/artifact/GLWcdxYnCWEXUMDQJyRshF ("Small Talk Launch Plan", private to the owner account; capability db).
- Tab 1 "Riya's plan": 12 sections / 76 tasks, "Do this next" card, check-offs in db doc `progress/plan` ({done: {taskId: ISO time}}), localStorage fallback when the viewer can't write.
- Tab 2 "Project context (for AI agents)": themes, store data, talks, brand, design system, team, files, decisions, open items, start-here prompt.

Source: C:\Users\SSTS\Desktop\Riya\owner-plan\src\
- parts/10-head.html (title, CSS, tab-1 shell), 20–23 data JS (sections), 25-tools.js (video tools), 30-context.html (Tab 2), 40-app.js (logic, START_PROMPT, PRODUCTS).
- build.sh concatenates into small-talk-plan.html (publish that file, NOT owner-plan/small-talk-plan.html which is a skeleton-wrapped local test copy).
- link-research.md = verified URLs/admin paths/tool prices as of 10 Oct.

To update Tab 2 from another session: edit parts/30-context.html (or 40-app.js for products/start prompt), run build.sh, then Artifact action "read" on the URL first and publish with `url` set. Never write `progress/*` docs (owner's ticks).
Open questions sent to orchestrator (unanswered at publish): which SD items are already done; whether Riya or the lock holder flips "Refund policy text verified"; phone line in the shipping policy vs D10.

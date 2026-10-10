# Harvest-skill improvements spotted on job 4470290173 (from crm-harvest session, 10 Oct 2026)
These are suggestions only; the skill file itself was not edited (it is shared with the engineer hire).
1. Visibility: if `document.visibilityState` is "hidden" the LinkedIn panel renders late or not at all ("panel not loaded"). Check it in preflight; Chrome must really be the visible window.
2. Identity guard before download: wait until the panel header (right pane, x > 1045 CSS px) shows the candidate's name AND the Resume/Shortlist buttons exist, then grab. Prevents a stale panel saving the wrong CV. A "no resume" answer should be confirmed twice.
3. Short lists (about 5 cards): `__prepW`'s 1400 px padding stretches the layout and pushes the panel header off-screen. Click the cards where they sit instead (set `window.__cur={id,name}` first, compute the click point right before each click, because cards shift after every selection).
4. Click maths: screenshot x/y = CSS px * 1568 / innerWidth (window size changed between 1920x919 and 1920x863 in one session).
5. Card text can carry accessibility suffixes ("X, new applicant", "X is open to work, new applicant"): strip them before building file names, or the name check flags them.
6. Rating menu: a plain coordinate click on a menu item can miss; `find` the menuitem and click by ref. URL values: rating=GOOD_FIT, MAYBE, NOT_A_FIT.
7. Card headline, location and screening answers are readable without any extra page load; the panel's "Screening question responses" section is the last block of the panel text.

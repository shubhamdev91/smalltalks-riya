# Board spec index (st-boardspec, worked by st-artwork)

All coordinates are CSS px at a 390 px viewport. Acceptance is a side-by-side match with the board frame at 390.

| Step | File | Status |
|---|---|---|
| 1 | tokens.css: colours, hero glows, type picks with runners-up | done |
| 1 | type/compare-*.png: candidate sheets; fonts/<family>/ with OFL.txt | done |
| 2 | hero.md: board 2, all 7 states; crops/hero-*@390(-grid).png; hero-colours.json | done |
| 3 | landing.md: board 3, 13 sections, joins (SVG), beelines, sparkles, nail rows; crops/landing-col*; landing-geometry.json, landing-beelines.json, landing-colours.json | done |
| 4 | gallery (tiles) / teasers / FAQ / footer: in landing.md | done |
| 5 | shop.md, product.md, bag.md, checkout.md (reference), nail-guide.md; crops/<frame>@390(-grid).png | done |
| 6 | journal.md, journal-story.md, our-story.md, talks.md, conversation.md, help.md; crops/<frame>@390(-grid).png | done |
| 3b | joins.json: per landing section top edge + curve height, beeline segment with x_in/x_out chained, dash offset, clear zones + art zones, verified (crops/joins-check.png); single-section screens: straight joins, no beeline | done |
| - | TEXT-DIFFS.md (T1 resolved, T2-T91) | done |

Tools are in `spec/tools/`: frames.py, samples.py, typecompare.py, arc.py, herocolors.py, getfonts.py.



Open owner decisions raised by the spec: hero/landing Diet Coke can (hero.md flag 1, landing F1); Brainwave props strip (landing F2); On Me receipt hand (F3); journal-story machinery image; missing product, guide and journal photos (G11).


| - | name-highlight.md: chapter product-name marker swipe (CSS) + tokens; mock artwork/tests/name-highlight-mock.png | done |

# Landing redesign: staged to st-fable's final rules, not written (st-foundation, 10 Oct 2026)

Rules: `qa/fidelity/OWNER-LANDING-CHANGE-1.md` (including its addendum), plus the orchestrator's final values. Nothing has been written to theme 186651934933. **Ready; requesting the lock.**

## Fit rule as built
- **Chapter height:** `max(calc(100svh - var(--st-header-h)), content minimum)`.
  - It sets `height`, not just `min-height`.
  - `contain-intrinsic-size` uses the same height.
  - Only svh is used: no vh, lvh or fixed px.
- **Text stack:** hangs from the top.
  - Body → slogan → nails → name → pill, with visible ink gaps of 12 / 12 / 10 / 10.
  - The note hangs from its bottom, so the 16 px floor makes it grow upward and the gap holds.
- **Art:**
  - Absolute against the section bottom; its cut edge is at the section edge.
  - It may sit behind the nails, name and pill, never behind the slogan.
  - Never upscaled.
- **Content minimum:**
  - `--cmin` = pill bottom (board px), plus 20 px.
  - `--cmin2` = room for the bottom art below the nail row, plus clearance: the beeline's moving parts and bottom-anchored captions stay ≥ 10 board px from every glyph box (≥ 8 px down to 320).
- **Desktop (≥ 990):**
  - The desktop layout is kept (k up to 1.4 px).
  - The fit is `min(100svh − header, 900px)`, with the text stack vertically centred in it (`--dy`).
  - Chapters may run taller where the art needs it. No copy is cut.
- **Beeline:**
  - Each chapter's beeline is a top part (follows the stack), a vertical run and a bottom part (follows the art).
  - A small `{% javascript %}` in `sections/st-chapter.liquid` assembles it for the live height and carries the dash phase down the page.
  - The lab confirms the phase is continuous across every join at every viewport.
  - Without JS, the generated path stays in place, stretched.
- **Joins:** caps over 20 px are drawn at 70%, so the deepest is now 36 (talks 45→31, Brainwave and Green 27→19, Journal 29→20, On Me 36→25, Wild and Pinky 52→36).

## Name highlight (approved)
- **Markup:** st-copy's, as given: `<p class="st-ch__name"><span aria-hidden="true">“</span>{{ set_name | escape }}<span aria-hidden="true">”</span></p>`. The `<p>` is the marker box.
- **Type:**
  - Barlow Semi Condensed 700 at `clamp(22px, 6.7vw, 29px)`, line-height 1.1, nowrap. "Pinky Promise" stays on one line at 320.
  - This is the true Bold: new asset `st-barlow-sc-700.woff2`, 12.3 KB, from the family files in `spec/fonts`.
- **Stroke and glow:**
  - Marker stroke and −1.5° tilt on all 7, with the spec's `--name-hl` / `--name-ink` pairs (tokens synced, `st-tokens.css` = `spec/tokens.css`).
  - The `::after` glow is only on the five dark sets, at `inset: -60% -20%`. No glow on Wild Card or On Me.
  - Forced-colors fallback included. The deep ink is only ever set together with the stroke.

## Per chapter
- **Diet Cherry:** art at the board crops (woman 68, can 37).
- **Brainwave:** the woman stays top-left at 0.82, with the slogan over her chin. The sketchbook (0.82) sits at the bottom. The beeline sweep under the pill is drawn at about half its depth.
- **Green Flag:** woman, phone and hand keep their offsets. The group's bottom 130 px are cropped, so her face sits below the pill at 390×664. Ticks beside the slogan.
- **Shaadi Shift:** the sari sweep as on the board.
- **On Me (option D, st-fable to confirm):** the pill moves left, and the caption sits beside it on the right at board size. Woman at 0.62; receipt hand at 0.5, with all five nails and "On me. xx" visible.
- **Wild Card:** the woman's bottom 180 px are cropped, so her face sits below the pill at 390×664. The cards hand as on the board.
- **Pinky Promise:** the scene's bottom 115 px are cropped (wrists; the interlocked fingers and nails stay). The caption sits top-right above the hands, anchored with the scene. The beeline ends in the scene, as on the board.

## Hero v3.7.3
`assets/st-hero.css` = `motion/st-hero.css` (40804d86). The new `--note-y` values live in the CSS; the CONTRACT (48dde962) lists no Liquid or data change. JS 4a70f913 is unchanged.

## Heights (css px)
In the BEFORE rows, each cell reads body−16 → pill+20 / body → end of art / chapter height. In the AFTER rows, each cell reads body−16 → pill+20 / chapter height. Screen = the viewport minus the header.

BEFORE: preview, `qa/fidelity/before-landing-redesign[-svh]-*.png` and measurements.

| viewport | screen | Diet | Brainwave | Green | Shaadi | On Me | Wild | Pinky |
|---|---|---|---|---|---|---|---|---|
| 440×768 | 699 | 584/691/720 | 609/844/959 | 589/942/976 | 567/779/874 | 566/1073/1204 | 577/914/959 | 526/936/976 |
| 430×744 | 675 | 571/675/703 | 597/825/937 | 576/921/954 | 555/762/854 | 554/1049/1176 | 564/893/937 | 515/915/954 |
| 390×664 | 595 | 521/612/638 | 544/748/850 | 526/835/865 | 507/691/775 | 506/951/1067 | 515/810/850 | 471/830/865 |
| 440×956 | 887 | 584/691/720 | 609/844/959 | 589/942/976 | 567/779/874 | 566/1073/1204 | 577/914/959 | 526/936/976 |
| 430×932 | 863 | 571/675/703 | 597/825/937 | 576/921/954 | 555/762/854 | 554/1049/1176 | 564/893/937 | 515/915/954 |
| 390×844 | 775 | 521/612/638 | 544/748/850 | 526/835/865 | 507/691/775 | 506/951/1067 | 515/810/850 | 471/830/865 |
| 320×568 | 499 | 441/503/523 | 460/614/697 | 444/685/710 | 429/567/636 | 428/781/875 | 435/665/697 | 399/681/710 |
| 1280×800 | 724 | 715/857/893 | 748/1048/1190 | 722/1169/1211 | 695/967/1085 | 694/1332/1494 | 707/1134/1190 | 644/1161/1211 |

AFTER: lab render of the staged files, `qa/fidelity/staged-landing-final-lab-*.png` and measurements.

| viewport | screen | Diet | Brainwave | Green | Shaadi | On Me | Wild | Pinky |
|---|---|---|---|---|---|---|---|---|
| 440×768 | 699 | 494/699 | 484/699 | 473/699 | 463/699 | 452/699 | 458/699 | 457/699 |
| 430×744 | 675 | 483/675 | 474/675 | 463/675 | 453/675 | 443/675 | 448/675 | 447/675 |
| 390×664 | 595 | 442/595 | 433/595 | 423/595 | 415/595 | 405/595 | 410/595 | 409/595 |
| 440×956 | 887 | 494/887 | 484/887 | 473/887 | 463/887 | 452/887 | 458/887 | 457/887 |
| 430×932 | 863 | 483/863 | 474/863 | 463/863 | 453/863 | 443/863 | 448/863 | 447/863 |
| 390×844 | 775 | 442/775 | 433/775 | 423/775 | 415/775 | 405/775 | 410/775 | 409/775 |
| 320×568 | 499 | 375/499 | 376/499 | 360/499 | 354/499 | 348/499 | 353/499 | 350/499 |
| 1280×800 | 731* | 604/755 | 592/830 | 578/882 | 566/868 | 552/873 | 560/830 | 558/892 |

\* The lab header is 69 px at 1280; the theme's is 76, so the real screen is 724.

All 56 cases pass:
- **Phones (every viewport, including 320×568):** each chapter is exactly one screen.
- **Spacing:** the note sits ≥ 16 px from the top, and bottom art stays below the nail row.
- **Captions:** inside the screen, ≥ 8 px from the pill.
- **Beeline:** ≥ 8 px from every glyph box, with the dash phase continuous.
- **1280:** the stack fits and is centred in the first screen, and the art extends below it (1.04–1.23 screens).

## Files to write (remote now → staged)
| file | remote | staged |
|---|---|---|
| assets/st-landing.css | 1ad7daea | 1f512fd6 |
| snippets/st-landing-map.liquid | b3dc808e | f390e2e8 |
| snippets/st-landing-join.liquid | fbff7731 | 4827d0a4 |
| sections/st-chapter.liquid | 320248ea | 80d0fb4c |
| snippets/st-fonts.liquid | 3e70db6b | 027e719c (adds only the 700 face) |
| assets/st-barlow-sc-700.woff2 | (new) | 11ecef9f |
| assets/st-tokens.css | b3e9719f | 8236b819 (= spec/tokens.css) |
| assets/st-hero.css | 2d344ccf | 40804d86 (= motion v3.7.3) |

Still separate: `snippets/st-logo-mark.liquid` af19ebc8 (the header logo without `fetchpriority`). It is staged from the earlier window; the write was denied.

## Open
- **st-fable:** confirm On Me option D (pill left, caption beside it). Fallback C: On Me runs about 1.25 screens at 390×664.
- **Writes:** my last theme write was refused by the Claude Code auto-mode classifier with the reason [Modify Shared Resources]. A grant can only be used if the user allows the Shopify `graphql_mutation` tool.

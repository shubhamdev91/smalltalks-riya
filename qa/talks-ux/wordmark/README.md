# "the talks" wordmark: 3 options (st-fable, 10 Oct 2026)

The owner disliked the current wordmark's font (Caveat 600).

**Intention:** gossip and "tea"; candid; young Indian women; warm and a bit cheeky; inviting, not shouty; readable at
header size (about 24 px); sits beside the blue "small talk" logo (Source Serif 900, stacked) without fighting it.
Typographic only. OFL fonts already in the repo (`spec/fonts/`); nothing downloaded.

**Sheets:** `options-sheet.png` and `options-1536-header-2x.png` (the 1536 header at real size, 2× device pixels, with ink heights).
- In the first, `options-sheet.png`: Rows: NOW, A, B, C. In each row: the site header on phone 390 and desktop 1536, then the
talks hub title on phone and desktop. The fonts were injected into the build preview (lab only, no theme write).
Script: `render_wordmark.py`. Specimen of the fonts considered: `specimen.png`.

| Option | Type | Why it fits | Risk |
|---|---|---|---|
| **A: soft serif** | Fraunces, SOFT 100 / WONK 1, weight 650, opsz 144, −0.025em | The warm, wonky serif of the hero headlines, so it's on-brand and very readable small | A second bold serif beside the bold blue logo: it can read as plain text and compete with the logo |
| **B: marker** | Gochi Hand | A friendly felt-tip note: the most candid and youthful, and clearly more legible than Caveat at 24 px | Still "a handwriting font", which is close to what the owner rejected |
| **C: masthead** (recommended) | "the" in Caveat Brush + "talks" in Source Serif 4 Italic 800 (0.9 em, opsz 60, −0.02em). Two lockups: **header** "the" 1.02 em, −6°; **hub title** "the" 0.74 em, −6° | A gossip-column masthead: the scribbled "the" is the cheeky aside, and "talks" in the logo's own serif family (italic, ink) sits with "small talk" as a sibling, not a rival | Two fonts in one mark, so it must ship as a fixed lockup (see Build), never set as live text |

**Header legibility fix (v2):**
- The orchestrator found the scribbled "the" too small in the 1536 header (it read as a smudge). The header lockup now
  sets "the" at 1.02 em; it was 0.74 em.
- At 1536 the whole mark's ink height is 17.5 px, against today's Caveat at 16 px, so it stays within the −30 % header budget.
  "the" is as tall as "talks" and reads clearly.
- The hub title keeps the smaller 0.74 em "the" (the masthead effect), which is legible at 40 / 52 px.

**Recommendation: C.** In one line: it keeps a candid, handwritten wink while the serif "talks" ties the board to the
"small talk" logo, and it stays legible at 24 px.

## Build (after the owner picks; st-foundation / st-talks)
- **Ship the wordmark as an outlined inline SVG** (text converted to paths from the OFL fonts), with
  `<span class="visually-hidden">the talks</span>` or `aria-label`. No new web font loads. The lockup can't drift
  (rotation, spacing), and it renders identically on every device.
- **Header:** the link keeps its 44 px target and vertical centring. Height of the mark: the visual size of today's
  23.8 px wordmark (x-height about 11 px); on phone, 19.5 px at 320 as now.
- **Hub title:** the same SVG at 40 px (phone) / 52 px (desktop), with the tagline under it as now. Colour ink #0d0b10
  (a burgundy #820622 variant is possible on the hub if wanted).
- **OFL:** keep `OFL.txt` for Caveat Brush and Source Serif 4 with the theme's font licences, since outlines are
  derivative glyphs.

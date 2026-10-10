# Small Talk — ChatGPT artwork pack (v2, HD, board-exact)

## Why the current art looks soft
- The women came from one ChatGPT image with all seven side by side, so each woman is only about 300 px wide. Phones show her at 400–600 px, so she gets stretched.
- The nails and the finger are about 200–300 px wide, but the hero shows them at 2–3 times that.
- Several board pieces were never made as separate files (receipt hand, rotary phone, sketchbook, safety-pin fabric, cards hand), so the build uses stand-ins with hard fade edges.
- Files sent through WhatsApp are compressed again.

## The four HD rules (follow every time)
1. **One subject per image.** Never ask for several sets in one picture. The subject should fill the frame.
2. **Largest size.** Ask for the tall size (1024 × 1536) for people and nails, square (1024 × 1024) for product photos, wide (1536 × 1024) for props.
3. **Download the original.** Open the image in ChatGPT, use the download button, save the PNG. Never screenshot, never pass it through WhatsApp.
4. **Transparent background** for everything marked "cutout". If ChatGPT gives a background anyway, reply: "Same image, transparent background, change nothing else. If you can't, use a flat pure #00FF00 background." If it still fails, accept a flat plain background in pure green #00FF00 (Green Flag: magenta #FF00FF; Wild Card: cyan #00FFFF); we cut it out. Never use the set colour as the background for a cutout.

## How to run it
- **One ChatGPT chat per set** (seven chats), plus one chat for the shared images. Staying in one chat per set keeps that woman and her nails consistent.
- At the start of each set chat, attach the five files from `artwork/chatgpt-refs/<set>/`:
  `1-board-chapter.png`, `2-board-hero.png`, `3-same-woman-reference.png`, `4-exact-nail-designs.png`, `5-packaging.png`.
  Also attach `artwork/chatgpt-refs/_shared/character-sheet.png`.
- Paste the **MASTER PROMPT** first, then the numbered prompts for that set one by one.
- Check every image against the nail table at the bottom. Reject wrong nails with: "Fix the nails only: <correct design>. Change nothing else."
- Save to `C:\Users\SSTS\Desktop\Riya\artwork\chatgpt\<set>\` using the file names given. The artwork session cleans, sizes and installs them.

Priority if you are short on time: **P1** (fixes the blur on the home page) → **P2** (product page gallery) → **P3** (optional packaging re-render).

---

## MASTER PROMPT (paste first in every set chat)

> I'm making artwork for my press-on nail brand's website. The attached board images are the approved design; match them exactly. File 1 is a section of the home page, file 2 is the hero screen, file 3 shows the woman for this set, file 4 shows the exact nail designs (left to right: signature nail, accent nail, extra accent), file 5 is the product box, and the character sheet shows the illustration style.
>
> For every illustration in this chat: bold comic-ink Indian pop illustration exactly like the boards — thick confident black ink outlines, flat saturated colour with soft cel shading, glossy highlights, winged eyeliner, bindi, gold jewellery, dense curly black hair. Hands have exactly five fingers with natural joints. Nails are long almond press-ons, glossy, matching file 4 exactly in colour and pattern.
>
> For every realistic photo in this chat: high-end beauty product photography, soft studio light, crisp focus on the nails, natural medium-brown Indian skin with real texture.
>
> Always: one subject per image, filling the frame, the largest image size you can make, PNG. No text, no logos, no watermark, no border, unless I ask for specific text. When I say "cutout", the background must be transparent.
>
> Reply "ready" and wait for my first request.

---

## Per-set prompts

Each set has the same structure. Replace nothing; the prompts are written out in full.

### ON ME (`chatgpt-refs/on-me/`)
**P1 · on-me-woman.png** (tall, cutout)
> Cutout. The On Me woman exactly as she peeks in on the left of file 1: head and shoulders, three-quarter view facing right, eyes glancing sideways with a calm, confident look, bindi, gold hoop earrings, red top, long curly black hair. Draw the whole head and shoulders, not cropped, so I can crop it myself.

**P1 · on-me-receipt-hand.png** (tall, cutout)
> Cutout. The hand from file 1 entering from the right, holding a restaurant receipt upright between thumb and fingers. Handwritten on the receipt in black pen: "On me. xx". Fingers wear gold rings. Nails, almond: burgundy, mottled amber tortoiseshell and metallic gold, as in file 4. Comic-ink style like the board.

**P1 · on-me-nail-1.png, on-me-nail-2.png, on-me-nail-3.png** (tall, cutout, three separate requests)
> Cutout. One single press-on nail, photorealistic 3D render, exactly like the <first / second / third> nail in file 4: <burgundy glossy / metallic gold / amber tortoiseshell>. Almond shape, pointing straight up, the base edge at the bottom, viewed straight on, glossy studio highlight down the left side like the board. The nail fills 90% of the image height.

**P2 · product page (square, realistic photos, not cutout)**
> on-me-pdp-flatlay.png: A neat fan of this set's press-on nails (burgundy, tortoiseshell, gold, as in file 4) laid on a mustard-yellow (#FFB900) surface, top-down, soft shadow, beauty product photography.
>
> on-me-pdp-hand.png: A relaxed woman's hand, back of the hand to camera, all five fingers visible, resting on a mustard-yellow (#FFB900) surface, wearing almond press-ons in this order from index to little finger: tortoiseshell, gold, tortoiseshell, burgundy, with a burgundy thumb nail. Gold rings. Beauty product photography.
>
> on-me-pdp-moment.png: Close-up of the same hand sliding a restaurant bill folder across a café table, burgundy, tortoiseshell and gold nails in focus, warm evening light, background softly blurred.

**P3 · on-me-pdp-packaging.png** (tall)
> Recreate the box in file 5 exactly, as a clean straight-on product shot on a plain light background at the largest size. Same illustration, same colours, same text exactly as printed: "small talk", "Bill idhar.", "ALMOND PRESS-ONS". Do not change, add or remove anything. Sharp edges.

### BRAINWAVE (`chatgpt-refs/brainwave/`)
**P1 · brainwave-woman.png** (tall, cutout)
> Cutout. The Brainwave woman exactly as in files 1 and 2: curly black hair, round tortoiseshell glasses, bindi, red lips, blue and white floral kurta, looking over her glasses with a sly, sure expression. Head and shoulders, three-quarter view facing right. Whole head, not cropped.

**P1 · brainwave-sketchbook.png** (wide, cutout)
> Cutout. The still life at the bottom of file 1: an open spiral sketchbook with pencil sketches of a crescent-shaped handbag (front view, side view, detail of the curve), a real silver crescent handbag resting on it, two small bottles, and a blue ballpoint pen lying diagonally. Comic-ink style like the board.

**P1 · brainwave-nail-1.png, -2.png, -3.png** (tall, cutout, three requests)
> Cutout. One single press-on nail, photorealistic 3D render, exactly like the <first / second / third> nail in file 4: <cobalt blue glossy / pearly white with soft shimmer / mirror silver chrome>. Almond shape, pointing straight up, base edge at the bottom, straight-on view, glossy studio highlight down the left side. Fills 90% of the image height.

**P2 · product page (square, realistic)**
> brainwave-pdp-flatlay.png: A neat fan of this set's press-on nails (cobalt, pearly white, silver chrome) on a cobalt-blue (#073DF1) surface, top-down, beauty product photography.
>
> brainwave-pdp-hand.png: A relaxed hand, back to camera, all five fingers visible, on a cobalt-blue surface, wearing almond press-ons from index to little finger: silver chrome, cobalt, pearly white, cobalt, with a pearly white thumb nail.
>
> brainwave-pdp-moment.png: Close-up of the same hand holding a blue pen over a sketchbook page with a crescent-handbag sketch, nails in focus.

**P3 · brainwave-pdp-packaging.png**: same packaging prompt as On Me, text exactly as printed on file 5: "small talk", "Haan, mera idea tha.", "ALMOND PRESS-ONS".

### DIET CHERRY (`chatgpt-refs/diet-cherry/`)
**P1 · diet-cherry-woman.png** (tall, cutout)
> Cutout. The Diet Cherry woman exactly as she peeks in at the lower left of file 1: half her face, eye glancing sideways with a knowing smile, gold jhumka, black top, curly black hair. Draw the whole head and shoulders, three-quarter view facing right.

**P1 · diet-cherry-can-hand.png** (tall, cutout)
> Cutout. The hand on the right of file 1 holding a cold silver soda can with condensation drops, drawn in the same comic-ink style. Copy the can's label as it appears in file 1. Nails, almond: deep red, plus one blush nail with a pointed red French tip, as in file 4.

**P1 · diet-cherry-nail-1/2/3.png** (tall, cutout, three requests)
> Cutout. One single press-on nail, photorealistic 3D render, exactly like the <first / second / third> nail in file 4: <mirror silver chrome / deep cherry red glossy / blush with a pointed deep red French tip>. Almond shape, pointing straight up, base edge at the bottom, straight-on, glossy highlight down the left side. Fills 90% of the image height.

**P2 · product page (square, realistic)**
> diet-cherry-pdp-flatlay.png: A neat fan of this set's nails (deep red, silver chrome, blush with red French tip) on a cherry-red (#E10019) surface, top-down.
>
> diet-cherry-pdp-hand.png: Relaxed hand, back to camera, five fingers, on a cherry-red surface, almond press-ons from index to little finger: silver chrome, blush with red French tip, deep red, deep red, with a deep red thumb nail.
>
> diet-cherry-pdp-moment.png: Close-up of the same hand holding a plain unbranded silver can on a marble café table, nails in focus.

**P3 · diet-cherry-pdp-packaging.png**: packaging prompt, text exactly as printed: "small talk", "Haan, wohi wali.", "ALMOND PRESS-ONS".

### GREEN FLAG (`chatgpt-refs/green-flag/`)
**P1 · green-flag-woman.png** (tall, cutout)
> Cutout. The Green Flag woman exactly as at the bottom right of file 1: holding the pink receiver of a vintage phone to her ear, eyes looking up and to the side, warm smile, gold rings, emerald green kurta, curly black hair. Whole head, shoulders and hand.

**P1 · green-flag-phone.png** (square, cutout)
> Cutout. The pink vintage rotary dial telephone at the bottom left of file 1, three-quarter view, gold dial centre, black numbers, coiled pink cord. Comic-ink style.

**P1 · green-flag-nail-1/2.png** (tall, cutout, two requests)
> Cutout. One single press-on nail, photorealistic 3D render, exactly like the <first / second> nail in file 4: <blush with a pointed emerald French tip / emerald green glossy>. Almond shape, pointing straight up, base edge at the bottom, straight-on, glossy highlight down the left. Fills 90% of the image height.

**P2 · product page (square, realistic)**
> green-flag-pdp-flatlay.png: A neat fan of this set's nails (emerald, blush with emerald French tip) on an emerald (#007948) surface, top-down.
>
> green-flag-pdp-hand.png: Relaxed hand, back to camera, five fingers, on an emerald surface, almond press-ons from index to little finger: blush with emerald tip, emerald, blush with emerald tip, emerald, with an emerald thumb nail.
>
> green-flag-pdp-moment.png: Close-up of the same hand holding a pink vintage phone receiver, nails in focus.

**P3 · green-flag-pdp-packaging.png**: packaging prompt, text exactly as printed: "small talk", "Tum aa jao. Main dekh lungi.", "ALMOND PRESS-ONS".

### SHAADI SHIFT (`chatgpt-refs/shaadi-shift/`)
**P1 · shaadi-shift-woman.png** (tall, cutout)
> Cutout. The Shaadi Shift woman exactly as on the left of file 1: red and gold bandhani dupatta draped over her head, gold maang tikka and jhumkas, eyes smiling, one hand lifting the dupatta edge. Whole head, shoulders and hand.

**P1 · shaadi-shift-fabric-pin.png** (wide, cutout)
> Cutout. A fold of red and gold bandhani dupatta fabric with a large gold safety pin fastened through it, as in file 1. Comic-ink style.

**P1 · shaadi-shift-nail-1/2/3.png** (tall, cutout, three requests)
> Cutout. One single press-on nail, photorealistic 3D render, exactly like the <first / second / third> nail in file 4: <soft pink with one small yellow daisy with an orange centre / deep red glossy / soft pink glossy>. Almond shape, pointing straight up, base edge at the bottom, straight-on, glossy highlight down the left. Fills 90% of the image height.

**P2 · product page (square, realistic)**
> shaadi-shift-pdp-flatlay.png: A neat fan of this set's nails (pink, deep red, pink with yellow daisy) on a fuchsia (#FF0078) surface, top-down.
>
> shaadi-shift-pdp-hand.png: Relaxed hand, back to camera, five fingers, on a fuchsia surface, almond press-ons from index to little finger: deep red, pink with yellow daisy, deep red, pink, with a pink thumb nail.
>
> shaadi-shift-pdp-moment.png: Close-up of the same hand fastening a gold safety pin into a red bandhani dupatta, nails in focus.

**P3 · shaadi-shift-pdp-packaging.png**: packaging prompt, text exactly as printed: "small talk", "Dulhan tu. Duty meri.", "ALMOND PRESS-ONS".

### WILD CARD (`chatgpt-refs/wild-card/`)
**P1 · wild-card-woman.png** (tall, cutout)
> Cutout. The Wild Card woman exactly as on the left of file 1: lime and green saree, curly black hair, bindi, a quiet hopeful side glance and small smile. Whole head and shoulders, three-quarter view facing right.

**P1 · wild-card-cards-hand.png** (tall, cutout)
> Cutout. Her hand from file 1 holding a fan of four playing cards close to her chest. The viewer sees only the red patterned card BACKS; the faces point toward her. Gold ring. Exactly five fingers. Nails, almond: acid lime, blush with lime French tip, and one cobalt-and-white checkerboard nail, as in file 4.

**P1 · wild-card-nail-1/2/3.png** (tall, cutout, three requests)
> Cutout. One single press-on nail, photorealistic 3D render, exactly like the <first / second / third> nail in file 4: <cobalt-and-white checkerboard / acid lime glossy / blush with a pointed lime French tip>. Almond shape, pointing straight up, base edge at the bottom, straight-on, glossy highlight down the left. Fills 90% of the image height.

**P2 · product page (square, realistic)**
> wild-card-pdp-flatlay.png: A neat fan of this set's nails (lime, blush with lime tip, cobalt-white checker) on an acid-lime (#B7EF00) surface, top-down.
>
> wild-card-pdp-hand.png: Relaxed hand, back to camera, five fingers, on an acid-lime surface, almond press-ons from index to little finger: blush with lime tip, lime, cobalt-white checker, lime, with a lime thumb nail.
>
> wild-card-pdp-moment.png: Close-up of the same hand holding playing cards face-down against a green felt table, nails in focus.

**P3 · wild-card-pdp-packaging.png**: packaging prompt, text exactly as printed: "small talk", "Achha. Tum pehle.", "ALMOND PRESS-ONS".

### PINKY PROMISE (`chatgpt-refs/pinky-promise/`)
**P1 · pinky-promise-pair.png** (wide, cutout)
> Cutout. The two women exactly as at the bottom of file 1, leaning their heads together, the front woman in a lilac knit sweater. Their hands are clasped in front, fingers interlocked, each wrist clearly connected to its own arm, no extra or fused fingers. Every nail: lilac with a deep burgundy asymmetric pointed tip. Warm, reassuring expressions.

**P1 · pinky-promise-nail-1.png** (tall, cutout)
> Cutout. One single press-on nail, photorealistic 3D render, exactly like the first nail in file 4: lilac with a deep burgundy asymmetric pointed tip sweeping from the right. Almond shape, pointing straight up, base edge at the bottom, straight-on, glossy highlight down the left. Fills 90% of the image height.

**P2 · product page (square, realistic)**
> pinky-promise-pdp-flatlay.png: A neat fan of this set's nails (lilac with burgundy asymmetric tips) on a violet (#6620F2) surface, top-down.
>
> pinky-promise-pdp-hand.png: Relaxed hand, back to camera, five fingers, on a violet surface, every nail lilac with a burgundy asymmetric pointed tip.
>
> pinky-promise-pdp-moment.png: Close-up of two hands linking little fingers in a pinky promise, both wearing the lilac and burgundy nails, soft light.

**P3 · pinky-promise-pdp-packaging.png**: packaging prompt, text exactly as printed: "small talk", "Haath do. Main hoon.", "ALMOND PRESS-ONS".

---

## Shared chat (attach the files in `chatgpt-refs/_shared/`)
Paste the MASTER PROMPT first, replacing "file 1–5" with "the attached files".

**P1 · finger-tone-1.png … finger-tone-4.png** (tall, cutout)
> Cutout. Photoreal: one index finger pointing straight up, exactly like the fingers in finger-tones.png, entering from the bottom edge, bare natural nail with a clean cuticle, centred, filling 90% of the image height. Skin tone <1 light / 2 medium / 3 tan / 4 deep>, matching that column in finger-tones.png.
> After the first one, ask for the others with: "Same image, same pose and size, change only the skin tone to <n>."

**P1 · our-vision-woman.png** (square, background #F6E7D2)
> The close-up in the left tile of board-tiles-our-vision.png: a woman's eye and her hand touching her cheek, burgundy and gold almond nails, gold jhumka, bindi. Comic-ink style.

**P2 · guide-measure.png, guide-apply.png, guide-remove.png** (wide 1536 × 1024, realistic, background #F4EFF0)
> guide-measure: A strip of white paper laid across the widest part of a natural fingernail, a small pen mark on each side.
> guide-apply: A woman pressing a tortoiseshell almond press-on onto her clean natural nail, thumb pressing at the cuticle.
> guide-remove: A woman gently lifting the edge of a burgundy almond press-on with a wooden cuticle stick.

---

## Nail check table (reject anything that doesn't match)
| Set | Set colour (product-photo surface only, never a cutout background) | Five-nail hand, thumb → little finger |
|---|---|---|
| On Me | #FFB900 | burgundy · tortoiseshell · gold · tortoiseshell · burgundy |
| Brainwave | #073DF1 | pearly white · silver chrome · cobalt · pearly white · cobalt (no checkerboard) |
| Diet Cherry | #E10019 | deep red · silver chrome · blush with pointed red French tip · deep red · deep red |
| Green Flag | #007948 | emerald · blush with emerald French tip · emerald · blush with emerald French tip · emerald |
| Shaadi Shift | #FF0078 | pink · deep red · pink with yellow daisy · deep red · pink |
| Wild Card | #B7EF00 | lime · blush with lime French tip · lime · cobalt-white checker · lime |
| Pinky Promise | #6620F2 | lilac with burgundy asymmetric tip on all five |

## Before the product photos go live
The flat-lay photos show a fan of nails. Make sure the number and sizes shown don't contradict what is actually in your kit.

## What you will end up with
| Group | Files | Where it shows |
|---|---|---|
| P1 women and props | 13 | hero half-faces, home page chapters, Journal, Our Story |
| P1 single nails | 18 | hero main nail and accents, chapter nail rows, shop tiles, talks avatars |
| P1 fingers | 4 | hero |
| P1 Our Vision | 1 | home page tile |
| P2 product photos | 21 + 3 guide | product gallery (with the box), Journal tiles, Nail Guide |
| P3 packaging | 7 | product gallery, shop tiles, bag, Our Story |

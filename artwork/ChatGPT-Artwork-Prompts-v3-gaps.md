# Small Talk — what ChatGPT already made, and the prompts for what's still missing (v3)

Source checked: theme "Small Talk — Board corrections / 09 Oct" (186667663573), read only, 10 Oct 2026.
Usable files are copied to `artwork/chatgpt/_from-board-corrections/`. The artwork session processes them from there.

## Assessment of ChatGPT's new art

| File | Size | Verdict | Notes |
|---|---|---|---|
| On Me chapter (woman peeking left + hand with "On me. xx" receipt) | 1200 × 800, transparent | **Use as is** | Matches board 3. Sharp at phone size. Also gives the On Me hero half-face. |
| Green Flag chapter (pink rotary phone + woman on the receiver) | 1536 × 1024, transparent | **Use as is** | Matches board 3. Nails correct (emerald, blush with emerald tips). Also gives the hero half-face. |
| Shaadi Shift chapter (bride's eye under dupatta + gold safety pin) | 1200 × 800, transparent | **Use as is** | Matches board 3. |
| Brainwave sketchbook (crescent-bag sketches + blue pen) | 1536 × 1024, transparent | **Use as is** | Fills the Brainwave props strip. The board also shows a real silver bag and two bottles beside it; minor, not worth a re-run. |
| Journal pair (woman writing with glasses + handbag still life) | 1200 × 800, transparent | **Use as is** | The landing "Small stories. Big feelings." tiles. Split into two. |
| Four-nail preview hand, bare nails | 1349 × 1166, transparent | **Use as is** | 2.6× sharper than ours. The motion code places nails on it, so the nail slots get re-measured. |
| Wild Card chapter | 1536 × 1024, transparent | **Edit** | Good pose and nails, cards face her. But off-board: short bob hair, teal top, blue card backs. The board has long curly hair, a lime/green saree and red card backs. |
| Pinky Promise chapter | 1200 × 800, transparent | **Edit** | Nails and clasped hands are right. The board shows two women leaning together; this shows one woman plus a sleeve. |
| Nail and finger outlines (SVG) | vector | **Not usable** | Only cut-out masks traced from the old low-res atlas. They don't add detail. |
| Diet can in hand (photo) | 1189 × 1323 | **Use for the hero** | Already in our build. Photo style, so it doesn't fit inside the illustrated Diet Cherry chapter. |

Nothing new exists for: the Brainwave woman, the Diet Cherry woman, the Our Vision tile, HD single nails, HD finger tones, product-page photos and Nail Guide photos. The prompts below cover only those, plus the two edits.

## How to run these
- Use one new ChatGPT chat. Attach every file in `artwork/chatgpt-refs/_delta/` at the start, plus `artwork/chatgpt-refs/_shared/character-sheet.png`.
- Paste the master prompt, then the prompts one by one.
- Download each original PNG from ChatGPT. Never screenshot, never send through WhatsApp.
- If an image comes back with a background, reply: "Same image, transparent background, change nothing else. If you can't, use a flat pure #00FF00 background." (Green Flag images: #FF00FF; Wild Card images: #00FFFF.) Never accept the set colour as the background of a cutout.
- Save into `artwork/chatgpt/` with the file name given.

### Master prompt (paste first)
> I'm making artwork for my press-on nail brand's website. The attached files are the approved boards (files starting "board-"), the exact nail designs (files starting "nails-"), and finished artwork from this project (layout-reference, style-reference, edit-me). New illustrations must match the finished artwork exactly in style: bold comic-ink Indian pop illustration, crisp black ink outlines, saturated colour with soft cel shading, glossy highlights, winged eyeliner, bindi, gold jewellery, long dense curly black hair. Hands have exactly five fingers with natural joints. Nails are long glossy almond press-ons matching the "nails-" file for that set exactly. One image per request, the largest size you can make, PNG, transparent background, no text unless I ask, no logos, no watermark, no border. Reply "ready".

## 1 · Edits to ChatGPT's own art (P1)

**wild-card-chapter-v2.png** (attach/point at `edit-me-wild-card-chapter.png`)
> Edit edit-me-wild-card-chapter.png. Keep the pose, the face, the hand, the nails, the ring and the size exactly. Change only: her hair becomes long, dense and curly like the other women; her outfit becomes a lime and green saree with gold border, as in board-wild-card-chapter.png; the card backs become red with a white diamond pattern. Transparent background.

**pinky-promise-chapter-v2.png** (attach/point at `edit-me-pinky-promise-chapter.png`)
> Edit edit-me-pinky-promise-chapter.png. Keep this woman, the clasped hands and every nail exactly. Add the second woman from board-pinky-promise-chapter.png: her face leaning in from the right so their heads nearly touch, smiling, wearing the lilac knit sweater whose sleeve is already in the image. Her arm must connect naturally to the hand already in the clasp. No extra fingers. Transparent background.

## 2 · New chapter art (P1)

**brainwave-chapter.png** (wide)
> Same layout, size and style as layout-reference-on-me-chapter.png. On the left, the Brainwave woman peeking in from the left edge as in board-brainwave-chapter.png and board-brainwave-hero.png: half her face, round tortoiseshell glasses, bindi, red lips, blue and white floral kurta, a sly sure look over her glasses. On the right, her hand holding a blue ballpoint pen. Nails, almond: cobalt blue, pearly white and silver chrome, as in nails-brainwave.png. Leave the middle empty. Transparent background.

**diet-cherry-chapter.png** (wide)
> Same layout, size and style as layout-reference-on-me-chapter.png. On the left, the Diet Cherry woman peeking in from the left edge as in board-diet-cherry-chapter.png: half her face, eye glancing sideways with a knowing smile, gold jhumka, black top. On the right, her hand holding a cold silver soda can with condensation, the label exactly as on the can in board-diet-cherry-chapter.png. Nails, almond: deep cherry red, plus one blush nail with a pointed red French tip, as in nails-diet-cherry.png. Leave the middle empty. Transparent background.

**our-vision-woman.png** (square, background #F6E7D2)
> The left tile of board-our-vision-tile.png at full size: a woman's eye and her hand touching her cheek, burgundy and gold almond nails, gold jhumka, bindi. Same style as the finished artwork.

## 3 · HD nails (P1, fixes the soft hero nail and nail rows)
One request per nail. First paste once:
> For the next requests: one single press-on nail, photorealistic 3D product render, almond shape, pointing straight up with its base edge at the bottom, viewed straight on, glossy studio highlight running down the left side, soft shadow-free edges, transparent background, the nail filling 90% of the image height, tall image. Copy the design from the named nails- file exactly.

Then send each line as its own request:
| File name | Request |
|---|---|
| on-me-nail-1.png | Burgundy glossy (attach the On Me nail sheet from `chatgpt-refs/on-me/4-exact-nail-designs.png`). |
| on-me-nail-2.png | Metallic gold. |
| on-me-nail-3.png | Amber tortoiseshell, mottled dark brown spots. |
| brainwave-nail-1.png | Cobalt blue glossy (nails-brainwave.png). |
| brainwave-nail-2.png | Pearly white with a soft shimmer. |
| brainwave-nail-3.png | Mirror silver chrome. |
| diet-cherry-nail-1.png | Mirror silver chrome (nails-diet-cherry.png). |
| diet-cherry-nail-2.png | Deep cherry red glossy. |
| diet-cherry-nail-3.png | Blush with a pointed deep red French tip. |
| green-flag-nail-1.png | Blush with a pointed emerald French tip (`chatgpt-refs/green-flag/4-exact-nail-designs.png`). |
| green-flag-nail-2.png | Emerald green glossy. |
| shaadi-shift-nail-1.png | Soft pink with one small yellow daisy with an orange centre (`chatgpt-refs/shaadi-shift/4-exact-nail-designs.png`). |
| shaadi-shift-nail-2.png | Deep red glossy. |
| shaadi-shift-nail-3.png | Soft pink glossy. |
| wild-card-nail-1.png | Cobalt-and-white checkerboard (nails-wild-card.png). |
| wild-card-nail-2.png | Acid lime glossy. |
| wild-card-nail-3.png | Blush with a pointed lime French tip. |
| pinky-promise-nail-1.png | Lilac with a deep burgundy asymmetric pointed tip sweeping from the right (nails-pinky-promise.png). |

Reject any nail whose shape or angle differs from the first one you accept; ask "Same shape and angle as the previous nail, only change the design."

## 4 · HD finger tones (P1)
Attach `chatgpt-refs/_shared/finger-tones.png`.
> finger-tone-1.png: Photoreal, one index finger pointing straight up exactly like the first finger in finger-tones.png, entering from the bottom edge, bare natural nail with a clean cuticle, centred, filling 90% of the image height, tall image, transparent background.
> Then: "Same image, same pose and size, change only the skin tone to match finger 2 / 3 / 4 in finger-tones.png", saved as finger-tone-2.png, -3.png, -4.png.

## 5 · Product page and Nail Guide photos (P2)
Unchanged from v2: run section "P2 · product page" for each set and the "guide" prompts in the shared chat of [ChatGPT-Artwork-Prompts.md](ChatGPT-Artwork-Prompts.md). Nothing for these exists in ChatGPT's theme.

## Count
| Group | Files |
|---|---|
| Edits | 2 |
| New chapter art + Our Vision | 3 |
| HD nails | 18 |
| HD finger tones | 4 |
| Product + guide photos (v2 file) | 21 + 3 |

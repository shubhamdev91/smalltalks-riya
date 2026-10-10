# Small Talk rebuild — orchestrator protocol (9 Oct 2026)

Orchestrator: `local_e4896004-68cd-4d55-9d37-ab925783b63b` (Opus). Owns `C:\Users\SSTS\Desktop\Riya\Small-Talk-Claude-Implementation-Checklist.md`. Workers do NOT edit the checklist; report to the orchestrator instead.

## Reporting
- When you finish a package or hit a blocker, SendMessage `local_e4896004-68cd-4d55-9d37-ab925783b63b`: one-line summary first, then: files/theme assets changed, evidence (readback, preview URL, screenshot path), open defects.
- Large evidence goes in this folder as `<worker>-<topic>.md`, not in the message.

## Model/effort rule (owner, 9 Oct)
- All Opus sessions run at xhigh effort; any new Opus session is started at xhigh.
- Sonnet only for purely operational checks (rendered HTML, schema validation, Lighthouse, link checks, automated a11y scans). Never judgement, never copy.
- Never start a Fable session. The parent Fable session handles only the hero motion controller, SEO/AEO strategy sign-off and final acceptance.

## Artwork rule (owner, 9 Oct)
- No new artwork is generated. The ChatGPT art already in Shopify Files is approved; the four boards are the spec. Claude Design / Board 1 is not a gate.
- Allowed: masks, crops, feathering, composites, WebP derivatives. Never redraw, recolour or upscale.
- 10 Oct exception (owner request): st-artwork may draw two small SVG playing cards (ace + king) for Wild Card in the boards' ink style; if the style doesn't match, a ChatGPT prompt goes to the owner instead.
- 10 Oct: the owner is generating a full-face Shaadi Shift woman in ChatGPT (batch E → artwork/chatgpt/E/). Owner-supplied art is approved art; st-artwork masks it and checks fidelity, and it ships as a follow-up swap.
- 10 Oct: owner delivered HD packaging (all 7 accepted; Brainwave + Shaadi confirmed by owner later on 10 Oct) and the official logo (artwork/chatgpt/D). The ≤380 css px packaging cap is lifted for all 7 sets once the HD window lands.

## Phase 2: board fidelity (owner, 9 Oct; supersedes conflicting rules above)
- Acceptance = side-by-side match with the board frame at 390 px (st-fable, qa/fidelity/). Boards win, except: no fake reviews/counts, accessibility minimums, commerce draft-safety.
- Exact board colours (burgundy headings, red pills, blue handwriting on commerce/editorial boards). The blue/ink/plum chrome is retired. Header = landing/hero board.
- The Diet Cherry hero uses the hand-with-Diet-Coke-can art (owner accepted the mark). Other board corrections still stand (Diet Cherry name, "hai").
- Spec lives in C:\Users\SSTS\Desktop\Riya\spec\ (st-artwork as st-boardspec). Build only from spec.

## Theme write lock
- Only theme 186651934933 is ever written. Lock holder now: FREE (fourth publish + v12.1e installed; publish-worthy sent 10 Oct ~20:25Z). Next: talks window (UX + posting-ON) after owner approval; then Tier B. settings_data carries owner edits; never overwrite it.
- A message sent while you held an earlier grant is never a grant for a later window. Write only after a grant that arrives after your last release.
- The orchestrator grants/revokes the lock by message. Release it explicitly ("lock released") when you stop writing.
- Never touch 186699514069 (the LIVE theme since 10 Oct 17:18Z, "Store v1.1", a copy of the build), 186695155925 and 186687553749 (previous lives), 186547241173, 186573160661, 186572636373, 162461974741, 186649313493, 186667663573.
- Live workflow (10 Oct): write only to the build 186651934933 (unpublished). The owner duplicates the build and publishes the copy after each accepted batch. Theme settings such as "Refund policy text verified" are set in the build and reach live through the re-publish.

## Shared data
- Products, prices, stock, pages, blog posts, menus, metaobjects, policies, SEO fields: proposal only. Send proposals to the orchestrator (current value → proposed value → surfaces → reason).
- Theme-local templates/settings: free (lock holder only).
- Talks kill switch (10 Oct 19:37Z): talk_settings/main (gid://shopify/Metaobject/616028176597) posting_open = "false". Only st-talks flips it to "true", in its granted posting-ON window and after the E2E passes; it reverts to "false" on failure. Nobody else touches it.
- Talks moderation (owner, 10 Oct): no owner review queue. Posts and replies publish immediately and hold_all stays "false". Risky content is refused at submit and nothing is saved. The only automatic removal is auto-hide at 3 distinct reports. Topics: plot twists · tiny wins · second opinions · just venting · nail talk ("something else" is the hidden home of "your own" posts).
- Publish plan (owner, 10 Oct): one combined duplicate + publish once the talks rework is on the build and has passed its E2E.

## Board-vs-brief conflicts (brief wins)
- "Diet Cherry", never "Cherry Repeat". Brainwave = "Haan, mera idea hai." everywhere, including the HD packaging (owner 10 Oct: real box says "hai"); only the product handle keeps "tha".
- No "Diet Coke" or any beverage brand in art/copy.
- No red headings/chrome; header "the talks" = thin black handwritten.
- Brainwave art = crescent-handbag sketch in notebook + blue pen, not machinery.
- The Talks examples labelled as examples; no fabricated activity.

## Copy
- Every shopper-visible string comes from st-copy's register in `C:\Users\SSTS\Desktop\Riya\copy\`. Builders use placeholders keyed to register IDs until copy lands.

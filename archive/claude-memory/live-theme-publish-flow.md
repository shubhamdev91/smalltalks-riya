---
name: live-theme-publish-flow
description: How Small Talk changes reach the live store — owner duplicates the build theme and publishes the copy; nobody writes to the live theme
metadata:
  node_type: memory
  type: project
  originSessionId: 01e61cb4-b351-4d98-a557-f8818be4c4e7
  modified: 2026-10-10T17:48:59.630Z
---

All agent theme work goes only to the unpublished build 186651934933 "Small Talk — Claude build (Horizon)". The live store gets it only when the owner duplicates that build and publishes the copy (Themes → ⋯ → Duplicate → Publish). Each re-publish creates a new live theme ID, so re-check `themes { role }` before assuming which theme is live. History: 186687553749 (09:14Z copy) → 186695155925 "Store v1 Small Talk — Claude build (Horizon)" published 10 Oct 2026 14:12Z; that copy missed st-foundation's 14:27Z install (laptop hero v3.8, Pinky clasp row, height fixes). → 186699514069 "Store v1.1 …" published 17:18Z with the accepted desktop batch. The owner views on 1536×703 and 1920-wide browsers, so QA should cover both. To check what a publish caught, compare `checksumMd5` of key files (st-hero.css, st-landing.css, st-landing-map.liquid) between the build and MAIN.

**Why:** the Shopify tool blocks writes to MAIN, and edits made in the live theme editor are lost at the next re-publish.

**Never write (st-foundation's list, 10 Oct 17:20Z):** 186699514069 (MAIN since 17:18Z), 186695155925, 186687553749, 186547241173, 186573160661, 186572636373, 162461974741, 186649313493, and any future published copy. Only 186651934933 is ever written.

**How to apply:** never write to the live theme or advise editing it. After each accepted batch (landing redesign, talks posting on, Instagram footer), remind the user to duplicate and publish. Settings that live in theme files (e.g. "Refund policy text verified", social links) must be set in the build. Related: [[theme-write-lock-protocol]].

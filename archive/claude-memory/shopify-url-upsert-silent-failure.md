---
name: shopify-url-upsert-silent-failure
description: "themeFilesUpsert with URL bodies drops invalid Liquid silently (job done, no userErrors); lint Liquid tag balance + schema before upload and always read back md5s"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 84af96b7-cadf-4ec1-a2eb-81c8910c84b9
  modified: 2026-10-10T16:39:23.349Z
---

A themeFilesUpsert whose body is type URL (staged upload) runs as an async job. If the file is invalid Liquid (e.g. unbalanced if/case/endif), Shopify rejects it silently: the job reports done, userErrors is empty, and the remote file keeps its old checksum. JSON templates saved in the same batch are reformatted, and any settings that the (old, still-live) section schema doesn't define are dropped.

**Why:** on 10 Oct 2026, st-teaser.liquid had a broken case/if structure from a patch script that cut at the wrong `{%- else -%}`. An 8-space pattern matched inside a 12-space line. The landing lab renders its own HTML mirror, so it didn't catch it. The upsert "succeeded", but st-teaser stayed old, and index.json lost three new settings. Only the md5 readback revealed it, and the corrected file needed a fresh OK from the orchestrator.

**How to apply:**
- Before uploading any Liquid, lint it: block tags balanced (if/unless/for/case/capture) with comments stripped, and the `{% schema %}` JSON parses.
- When patching Liquid by text, anchor cuts on whole lines including the newline and the next line's content, never on an indented substring.
- After every upsert, read back each file's checksumMd5. JSON templates come back reformatted, so compare their parsed content instead.
- Upload a section before (or with) any template that uses its new settings, and re-upload the template if the section changed late.

Related: [[theme-write-lock-protocol]].

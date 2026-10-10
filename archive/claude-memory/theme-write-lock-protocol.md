---
name: theme-write-lock-protocol
description: Small Talk build — only write to the Shopify theme after an explicit lock grant that arrives AFTER my last release
metadata:
  node_type: memory
  type: feedback
  originSessionId: 84af96b7-cadf-4ec1-a2eb-81c8910c84b9
  modified: 2026-10-10T12:57:31.996Z
---

Write to the Small Talk theme (186651934933) only after the orchestrator sends an explicit lock grant that arrives after my most recent "lock released". A grant that was sent before or crossed with my release does not count; if the order is unclear, ask the orchestrator before writing.

**Why:** on 10 Oct 2026 messages crossed — I used a re-grant that the orchestrator had already superseded by granting st-talks, so two sessions briefly held write rights (no file overlap, but the orchestrator asked for this rule).

It happened again the same day in the other direction (st-talks wrote on a stale grant while st-foundation held the lock). No damage only because st-talks re-fetched remote checksums and did an insert-only locale check.

**Live theme:** never written; it changes with each owner publish (see [[live-theme-publish-flow]]).

**How to apply:** before any themeFilesUpsert, check the latest lock message is a grant newer than my last release; prepare and stage changes locally while waiting (see [[small-talk-build-log]] for where work is recorded). Right before writing, re-fetch the remote checksum of every file and diff it against what I last uploaded. For locales/en.default.json, prove every line outside my own namespace is byte-identical to the current remote.

A third crossing on 10 Oct: a session wrote under a conditional grant that the orchestrator had already declared stale (it had released without using it, and the lock had gone to another session). No file overlap, but two sessions held write rights. Rule: a grant the orchestrator calls stale or superseded is void even if it is the newest grant you have read; when messages may have crossed, ask "is my grant still valid?" before writing.

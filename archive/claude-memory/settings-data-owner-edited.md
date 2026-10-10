---
name: settings-data-owner-edited
description: "Small Talk build theme's config/settings_data.json is owner-edited in the theme editor; never upload the local copy"
metadata:
  node_type: memory
  type: project
  originSessionId: 84af96b7-cadf-4ec1-a2eb-81c8910c84b9
  modified: 2026-10-10T14:16:58.094Z
---

The build theme's (186651934933) `config/settings_data.json` is changed by the owner in the theme editor (10 Oct 2026: "Refund policy text verified" ON, remote md5 3674b780). The local `theme-build/src/config/settings_data.json` is stale and must never be uploaded as-is.

**Why:** the orchestrator ruled it so (10 Oct). Also, the Claude Code auto-mode classifier refuses edits to it ([Modify Shared Resources]), and the Admin API returns it re-formatted (no byte-exact copy possible).

**How to apply:** if a future change touches settings_data:
1. Re-fetch the remote.
2. Merge only the needed key, checked semantically (parsed JSON differs by that key only).
3. Propose it to the orchestrator first.

Otherwise leave it alone. Related: [[theme-write-lock-protocol]].

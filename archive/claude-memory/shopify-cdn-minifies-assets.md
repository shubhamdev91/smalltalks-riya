---
name: shopify-cdn-minifies-assets
description: "The storefront CDN serves Shopify-minified JS, so a served file's md5 never matches the theme checksum; verify by Admin checksumMd5 plus content markers"
metadata:
  node_type: memory
  type: reference
  originSessionId: 84af96b7-cadf-4ec1-a2eb-81c8910c84b9
  modified: 2026-10-10T19:53:21.311Z
---

On the Small Talk store, `//<shop>/cdn/shop/t/<n>/assets/*.js` returns Shopify's minified copy. Its md5 differs from the theme file's `checksumMd5` and can differ between fetches. Seen 10 Oct 2026 with st-hero-motion.js: Admin 57b4cad4, served 915640da / 1448d6de.

**How to apply:** treat the Admin API `checksumMd5` read-back as proof of the write. To confirm the preview runs the new code, grep the served file for strings only the new version has (or lacks), and test the behaviour. Never report a served-bytes md5 mismatch as a failed install. Related: [[shopify-url-upsert-silent-failure]].

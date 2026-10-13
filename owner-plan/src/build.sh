#!/bin/sh
cd "$(dirname "$0")"
{
cat parts/10-head.html
cat parts/30-context.html
printf '</main>\n<div class="toast" id="toast" role="status" aria-live="polite"></div>\n<script>\n'
cat parts/20-data-a.js parts/21-data-b.js parts/22-data-c.js parts/23-data-d.js parts/24-structure.js
if [ -f parts/25-tools.js ]; then cat parts/25-tools.js parts/26-priority.js parts/27-deps.js parts/28-walkthrough.js; else echo "const TOOLS_HTML = '<p>Tools table coming.</p>';"; fi
cat parts/40-app.js
printf '</script>\n'
} > small-talk-plan.html

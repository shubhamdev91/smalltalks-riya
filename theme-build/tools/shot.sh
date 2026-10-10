#!/bin/sh
# usage: shot.sh <path-with-query-after-host> <width> <height> <outfile>
URL="https://0nev20-vn.myshopify.com$1"
case "$URL" in *\?*) URL="$URL&preview_theme_id=186651934933";; *) URL="$URL?preview_theme_id=186651934933";; esac
PROFILE="$(cygpath -w /c/Users/SSTS/AppData/Local/Temp/claude/C--Users-SSTS-Desktop-Riya/84af96b7-cadf-4ec1-a2eb-81c8910c84b9/scratchpad/edgeprof)"
OUT="$(cygpath -w "$4")"
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$PROFILE" --window-size=$2,$3 --virtual-time-budget=8000 --screenshot="$OUT" "$URL" 2>/dev/null
ls -la "$4"

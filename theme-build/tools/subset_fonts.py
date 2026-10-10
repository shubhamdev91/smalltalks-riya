"""Subset the theme's woff2 fonts to the characters the copy actually uses (hero v3.7.1 load plan, item 6).
Source: fonts/out/<name>.woff2 (the Basic Latin + Latin-1 subsets); output: src/assets/<name>.woff2.
Kept: Basic Latin (U+0020-007E), NBSP and the non-ASCII characters found in the copy register, locales and templates
(© ° · × é – — ‘ ’ “ ” • … ‹ › ₹ ← → ↗ −), every OpenType layout feature, and variation axes (Caveat, DM Sans).
The logo face (st-source-serif-logo-900) is already cut to the wordmark and is left alone.
Usage: python -I tools/subset_fonts.py"""
import hashlib, pathlib
from fontTools import subset
from fontTools.ttLib import TTFont

TB = pathlib.Path(__file__).resolve().parents[1]
SRC = TB / 'fonts/out'
OUT = TB / 'src/assets'
UNICODES = list(range(0x20, 0x7F)) + [0xA0, 0xA9, 0xB0, 0xB7, 0xD7, 0xE9, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D,
                                       0x2022, 0x2026, 0x2039, 0x203A, 0x20B9, 0x2190, 0x2192, 0x2197, 0x2212]
SKIP = {'st-source-serif-logo-900.woff2'}

total_before = total_after = 0
for src in sorted(SRC.glob('st-*.woff2')):
    if src.name in SKIP:
        continue
    before = src.stat().st_size
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['*']
    opts.notdef_outline = True
    opts.name_IDs = ['*']
    opts.name_languages = ['*']
    font = TTFont(src)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=UNICODES)
    sub.subset(font)
    out = OUT / src.name
    font.flavor = 'woff2'
    font.save(out)
    after = out.stat().st_size
    total_before += before
    total_after += after
    missing = [f'U+{u:04X}' for u in UNICODES if u not in TTFont(src).getBestCmap()]
    print(f'{src.name:34} {before:7} -> {after:7} ({after / before:5.1%})  md5 {hashlib.md5(out.read_bytes()).hexdigest()[:8]}'
          + (f'  (source lacks {", ".join(missing)})' if missing else ''))
print(f'total {total_before} -> {total_after} ({total_after / total_before:.1%})')

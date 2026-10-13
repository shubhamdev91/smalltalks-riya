"""st-fable: Small Talk logo v2 concepts: precise vector letterform edits on the official traced logo (base.svg,
viewBox 0 0 1336 818, colour #001df9). Each variant = the original path under a mask (removes the edited letter part
and cuts knockouts) + new letterform parts, all one colour (currentColor), so it reverses cleanly.
Writes v2-<key>.svg (fill set per use) and a monogram SVG per variant."""
import pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
BASE_D = re.search(r' d="([^"]+)"', (HERE / 'base.svg').read_text(encoding='utf-8')).group(1)
VB = '0 0 1336 818'

# ---------------- Direction A: the final "l" of "small" becomes an almond press-on nail ----------------
# stem x 1196–1296 (centre 1246), cap height y≈5, x-height ≈ 155. The ascender IS the nail: convex almond sides and a
# soft point leaning a touch right. Where nail meets "finger", two small side notches (silhouette only, no inner line,
# so it never reads as an i-dot or a smile). A slim gloss crescent sits on the upper left.
A = {
    'remove': ['M1166 0 H1318 V232 H1166 Z'],
    'add': [
        'M1196 240 C1190 180 1188 128 1196 88 C1206 46 1228 14 1254 4 C1278 12 1296 44 1302 88 '
        'C1308 130 1304 182 1296 240 Z',
    ],
    'knock': [
        # side notches at the nail base
        'M1186 214 L1206 228 L1186 242 Z',
        'M1306 214 L1286 228 L1306 242 Z',
        # gloss crescent
        'M1214 186 C1208 142 1212 96 1230 56 C1224 96 1222 142 1228 186 Z',
    ],
}

# ---------------- Direction B: the "k" leg becomes a polish-brush stroke that tapers off ----------------
# k stem x 870–966. The leg is a band ≈ 91 px thick, at y 700 spanning x 968–1077, slope dx/dy ≈ 0.68.
# Below y 700 it becomes one brush swipe that swells a little, then draws out to a fine flicked tip.
B = {
    'remove': ['M968 700 H1200 V818 H982 V782 L968 774 Z'],
    'add': [
        'M966 690 L1074 690 C1088 712 1104 734 1124 754 C1146 776 1170 794 1200 808 '
        'C1160 812 1118 804 1080 786 C1040 768 1004 740 980 716 C974 710 968 702 966 690 Z',
    ],
    'knock': [
        'M1104 772 C1128 788 1150 798 1176 805 L1172 809 C1146 803 1124 793 1100 777 Z',
        'M1088 756 C1110 774 1132 786 1154 794 L1151 798 C1128 791 1106 779 1086 761 Z',
    ],
}

# ---------------- Direction C: the "k" arm ends in a bead of polish (a teardrop terminal) ----------------
# The thin diagonal arm (≈ 34 px across, at 45°) runs on from y 618 and swells into a round drop (r 29) instead of the
# flag serif: a teardrop terminal like the logo's "a" already has. Type first, a bead of polish second.
C = {
    'remove': ['M1000 540 H1162 V614 H1000 Z'],
    'add': ['M1017.0 618.0 C1041.0 594.0 1057.4 553.6 1071.5 539.5 A29 29 0 0 1 1112.5 580.5 C1098.4 594.6 1075.0 594.0 1051.0 618.0 Z'],
    'knock': ['M1074.0 562.0 C1074.0 545.5 1086.2 539.1 1097.2 538.5 C1086.8 545.5 1081.6 554.2 1080.4 562.0 Z'],
}
VARS = {'A': A, 'B': B, 'C': C}
_N = 0


def svg(v=None, fill='currentColor', extra=''):
    if v is None:
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" {extra}><path fill="{fill}" fill-rule="evenodd" d="{BASE_D}"/></svg>'
    rm = ''.join(f'<path d="{d}" fill="#000"/>' for d in v['remove'])
    kn = ''.join(f'<path d="{d}" fill="#000"/>' for d in v['knock'])
    add = ''.join(f'<path d="{d}"/>' for d in v['add'])
    global _N
    _N += 1
    uid = f'{_N}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" {extra}><defs>'
            f'<mask id="r{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1336" height="818"><rect width="1336" height="818" fill="#fff"/>{rm}{kn}</mask>'
            f'<mask id="k{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1336" height="818"><rect width="1336" height="818" fill="#fff"/>{kn}</mask></defs>'
            f'<g fill="{fill}"><path fill-rule="evenodd" mask="url(#r{uid})" d="{BASE_D}"/><g mask="url(#k{uid})">{add}</g></g></svg>')


if __name__ == '__main__':
    (HERE / 'v2-current.svg').write_text(svg(None, '#001df9'), encoding='utf-8')
    for k, v in VARS.items():
        (HERE / f'v2-{k}.svg').write_text(svg(v, '#001df9'), encoding='utf-8')
    print('ok')

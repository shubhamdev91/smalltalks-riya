"""WCAG contrast for every text token on its real ground; find passing replacements by darkening along the same hue."""
import colorsys


def L(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def cr(a, b):
    la, lb = L(a), L(b); return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def darken_to(fg, bg, target=4.5):
    h = fg.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    while ll > 0:
        c = "#%02x%02x%02x" % tuple(round(v * 255) for v in colorsys.hls_to_rgb(hh, ll, ss))
        if cr(c, bg) >= target:
            return c
        ll -= 0.005
    return "#000000"


PAIRS = [
    ("--st-muted (footer, helper)", "#9698ab", "#fdfdfc"),
    ("--st-body", "#6e7184", "#fdfdfc"),
    ("--st-hand-blue", "#3653c7", "#fdfdfc"),
    ("--st-red", "#a31a33", "#fdfdfc"),
    ("--st-burgundy", "#820622", "#fdfdfc"),
    ("--st-price", "#0b0b2e", "#fdfdfc"),
    ("--st-pill-ink on --st-pill", "#ffffff", "#920324"),
    ("--st-logo-blue", "#1412d5", "#fdfdfc"),
    ("--st-talks-ink", "#0d0b10", "#fdfdfc"),
    ("--st-navy on cream", "#14168f", "#fdf6e9"),
    ("--st-landing-red on cream", "#bc0a1e", "#fdf6e9"),
    ("outline-pill red text on cream", "#ce3e46", "#fdf6e9"),
    ("tile label red on cream", "#c6292d", "#fdf6e9"),
    ("hand-blue on bag pink panel", "#3653c7", "#fee2ed"),
    ("view-set blue", "#4e6dcd", "#fdfdfc"),
    ("PDP desc navy-blue", "#373f8b", "#fdfdfc"),
    ("talks bubble text", "#3b3ba8", "#e3e0fe"),
    ("field placeholder", "#b0b0bd", "#ffffff"),
    ("chip text", "#1a1a2e", "#fcfcfd"),
    ("hero pill on-me white on", "#ffffff", "#9c0219"),
    ("hero pill brainwave ink", "#0f0bcd", "#ffffff"),
    ("hero pill diet-cherry ink", "#d6171a", "#ffffff"),
    ("hero pill green-flag ink", "#107247", "#ffffff"),
    ("hero pill shaadi white on", "#ffffff", "#9b021a"),
    ("hero pill wild-card ink", "#0f0cce", "#ffffff"),
    ("hero pill pinky ink", "#d6181b", "#ffffff"),
    ("chapter pill red ink", "#cc2f36", "#ffffff"),
    ("hero headline on-me ink on ground", "#180e0b", "#f5a908"),
    ("hero white on brainwave ground", "#ffffff", "#0444d9"),
    ("hero white on diet-cherry ground", "#ffffff", "#b70a09"),
    ("hero white on green-flag ground", "#ffffff", "#04673c"),
    ("hero ink on shaadi ground", "#180e0b", "#f61d6d"),
    ("hero ink on wild-card ground", "#0f0b5c", "#b4f50a"),
    ("hero white on pinky ground", "#ffffff", "#621dec"),
    ("landing white on shaadi #f30b5e", "#ffffff", "#f30b5e"),
    ("landing white on diet-cherry #d40319", "#ffffff", "#d40319"),
    ("landing white on pinky #6919f9", "#ffffff", "#6919f9"),
    ("landing black on wild #aee60d", "#000602", "#aee60d"),
    ("landing black on on-me #fbbe10", "#2b0f00", "#fbbe10"),
]

if __name__ == "__main__":
    for n, a, b in PAIRS:
        r = cr(a, b)
        fix = "" if r >= 4.5 else f"  -> FAIL 4.5; large-text(>=24px/19px bold) {'ok' if r >= 3 else 'FAIL'}; passing: {darken_to(a, b)}"
        print(f"{n:40s} {a} on {b}: {r:5.2f}{fix}")

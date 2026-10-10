"""Official-logo deliverables (owner-D-1): raster ladder, brand files, favicon set (logo-derived), social share image,
contact sheets, manifest entries with md5s. Composites/crops of the official wordmark only."""
import hashlib, io, json, os
import numpy as np
from PIL import Image, ImageDraw
import logo_favicon as LF

ART = LF.ART
LOGO = os.path.join(ART, "hd", "logo")
FAV = os.path.join(ART, "hd", "favicon-logo")
TESTS = os.path.join(ART, "tests", "hd")
PAPER = (253, 253, 252)


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def rec(p):
    return {"path": os.path.relpath(p, ART).replace("\\", "/"), "bytes": os.path.getsize(p), "md5": md5(p), "px": list(Image.open(p).size) if not p.endswith(".svg") else None}


def resize(im, w):
    h = round(im.height * w / im.width)
    r = im.convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")
    a = np.array(r); a[a[..., 3] == 0, :3] = 0
    return Image.fromarray(a)


def main():
    out = {}
    trim = Image.open(os.path.join(LOGO, "small-talk-logo-trim.png")).convert("RGBA")
    tr = json.load(open(os.path.join(LOGO, "_trace.json")))
    out["svg"] = {**rec(os.path.join(LOGO, "small-talk-logo.svg")), "fill": tr["colour"], "viewBox": f"0 0 {tr['size'][0]} {tr['size'][1]}",
                  "verify": tr["verify"], "note": "potrace of the cleaned alpha at 2x; single fill, even-odd; max boundary deviation 0.75 src px vs the raster at 4x; 6/6 components, 2/2 counters"}
    out["raster_master"] = {**rec(os.path.join(LOGO, "small-talk-logo-trim.png")), "note": f"official wordmark trimmed (+4 px pad) from source box {tr['trim_box_in_source']}; colour snapped to the source's own flat fill {tr['colour']}; alpha noise <=8 removed, interior 251-254 -> 255"}
    # raster ladder for header/footer fallbacks (SVG preferred): widths in px
    lad = {}
    for w in (168, 252, 220, 330, 480, 640):
        im = resize(trim, w)
        p = os.path.join(LOGO, f"small-talk-logo-{w}.png"); im.save(p, optimize=True)
        pw = os.path.join(LOGO, f"small-talk-logo-{w}.webp"); b = io.BytesIO(); im.save(b, "WEBP", lossless=True, method=6); open(pw, "wb").write(b.getvalue())
        lad[w] = {"png": rec(p), "webp": rec(pw)}
    out["raster_ladder"] = {"note": "header ~84 css wide -> 168 (2x) / 252 (3x); footer ~110 css -> 220 / 330; 480/640 for large uses. Prefer the SVG.", "files": lad}
    # brand settings files (owner steps: Settings > Brand, checkout logo)
    os.makedirs(os.path.join(LOGO, "brand"), exist_ok=True)
    p1 = os.path.join(LOGO, "brand", "small-talk-logo-transparent-1336.png"); trim.save(p1, optimize=True)
    sq = Image.new("RGBA", (1200, 1200), (255, 255, 255, 255)); lg = resize(trim, 900); sq.alpha_composite(lg, ((1200 - lg.width) // 2, (1200 - lg.height) // 2))
    p2 = os.path.join(LOGO, "brand", "small-talk-logo-square-1200.png"); sq.convert("RGB").save(p2, optimize=True)
    out["brand_files"] = {"transparent": rec(p1), "square_on_white": rec(p2), "note": "owner uploads: Settings > Brand (logo + square logo) and checkout logo"}
    # social share 1200x630, logo on site paper, >=15% safe margin
    so = Image.new("RGBA", (1200, 630), PAPER + (255,)); lg = resize(trim, 720)
    so.alpha_composite(lg, ((1200 - lg.width) // 2, (630 - lg.height) // 2))
    p3 = os.path.join(LOGO, "social-share-1200x630.png"); so.convert("RGB").save(p3, optimize=True)
    p3j = os.path.join(LOGO, "social-share-1200x630.jpg"); so.convert("RGB").save(p3j, quality=92, optimize=True)
    out["social_share"] = {"png": rec(p3), "jpg": rec(p3j), "ground": "#fdfdfc (--st-paper)",
                           "logo_box_px": [lg.width, lg.height], "margin_pct": {"x": round((1200 - lg.width) / 2 / 1200 * 100, 1), "y": round((630 - lg.height) / 2 / 630 * 100, 1)}}
    # favicon set: tab sizes = 's' glyph; home-screen / apple = full stacked wordmark
    os.makedirs(FAV, exist_ok=True)
    s_ic = LF.compose(LF.variant("s"), LF.FILLS["s"])
    wm_r = LF.compose(LF.variant("wordmark"), LF.FILLS["wordmark"])
    wm_sq = LF.compose(LF.variant("wordmark"), LF.FILLS["wordmark"], rounded=False)
    s_sq = LF.compose(LF.variant("s"), LF.FILLS["s"], rounded=False)
    files = {}
    for name, im, n in (("favicon-16.png", s_ic, 16), ("favicon-32.png", s_ic, 32), ("favicon-48.png", s_ic, 48),
                        ("favicon-192.png", wm_r, 192), ("favicon-512.png", wm_r, 512)):
        p = os.path.join(FAV, name); LF.down(im, n).save(p, optimize=True); files[name] = p
    p = os.path.join(FAV, "apple-touch-icon-180.png"); LF.down(wm_sq, 180).convert("RGB").save(p, optimize=True); files["apple-touch-icon-180.png"] = p
    p = os.path.join(FAV, "favicon.ico"); LF.down(s_ic, 48).save(p, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)]); files["favicon.ico"] = p
    # alternates: 's' at the large sizes too (if st-fable prefers one mark everywhere)
    for name, im, n in (("alt-s-192.png", s_ic, 192), ("alt-s-512.png", s_ic, 512)):
        p = os.path.join(FAV, name); LF.down(im, n).save(p, optimize=True); files[name] = p
    p = os.path.join(FAV, "alt-s-apple-touch-icon-180.png"); LF.down(s_sq, 180).convert("RGB").save(p, optimize=True); files["alt-s-apple-touch-icon-180.png"] = p
    out["favicon"] = {"recommendation": "logo-derived: the wordmark's own 's' glyph (crop of the official logo, exact #001df9 on paper #fdfdfc) for the tab sizes 16/32/48 + .ico; the full stacked wordmark for 180 (apple) / 192 / 512, where it is legible. The full wordmark is illegible at 16 and only borderline at 32; 'st' is muddy at 16.",
                      "files": {k: rec(v) for k, v in files.items()},
                      "candidates_sheet": "tests/hd/contact-favicon-logo-candidates.png", "vs_nail_sheet": "tests/hd/contact-favicon-logo-final.png",
                      "html": ['<link rel="icon" href="{{ \'favicon.ico\' | asset_url }}" sizes="48x48">',
                               '<link rel="icon" type="image/png" sizes="32x32" href="{{ \'favicon-32.png\' | asset_url }}">',
                               '<link rel="icon" type="image/png" sizes="192x192" href="{{ \'favicon-192.png\' | asset_url }}">',
                               '<link rel="apple-touch-icon" sizes="180x180" href="{{ \'apple-touch-icon-180.png\' | asset_url }}">'],
                      "supersedes": "hd/favicon (nail) once st-fable picks; nail set stays as fallback"}
    # sheets: final favicon set vs nail on light/dark; logo on light/dark + 4x trace overlay crop; social
    nail = {16: Image.open(os.path.join(ART, "hd", "favicon", "favicon-16.png")).convert("RGBA"),
            32: Image.open(os.path.join(ART, "hd", "favicon", "favicon-32.png")).convert("RGBA"),
            180: Image.open(os.path.join(ART, "hd", "favicon", "apple-touch-icon-180.png")).convert("RGBA")}
    new = {16: Image.open(files["favicon-16.png"]).convert("RGBA"), 32: Image.open(files["favicon-32.png"]).convert("RGBA"),
           180: Image.open(files["apple-touch-icon-180.png"]).convert("RGBA")}
    rows = []
    for g in ((242, 242, 242), (35, 35, 40)):
        row = Image.new("RGB", (900, 230), g); d = ImageDraw.Draw(row); x = 10
        for lbl, st in (("logo set (recommended)", new), ("nail set (current)", nail)):
            d.text((x, 6), lbl, fill=(140, 140, 140))
            row.paste(st[16], (x, 30), st[16]); row.paste(st[32], (x + 26, 30), st[32])
            z = st[16].resize((64, 64), Image.NEAREST); row.paste(z, (x, 76), z)
            z = st[32].resize((64, 64), Image.NEAREST); row.paste(z, (x + 70, 76), z)
            row.paste(st[180], (x + 150, 30), st[180]); x += 440
        rows.append(row)
    s = Image.new("RGB", (900, 460), "white"); s.paste(rows[0], (0, 0)); s.paste(rows[1], (0, 230))
    s.save(os.path.join(TESTS, "contact-favicon-logo-final.png"))
    ov = Image.open(os.path.join(TESTS, "logo-trace-overlay-4x.png"))
    lg = resize(trim, 600); sheet = Image.new("RGB", (1240, 1060), "white")
    a = Image.new("RGBA", (620, 400), PAPER + (255,)); a.alpha_composite(lg, (10, (400 - lg.height) // 2)); sheet.paste(a.convert("RGB"), (0, 0))
    b = Image.new("RGBA", (620, 400), (17, 17, 20, 255)); b.alpha_composite(lg, (10, (400 - lg.height) // 2)); sheet.paste(b.convert("RGB"), (620, 0))
    sheet.paste(ov.crop((800, 180, 1420, 800)), (0, 420))       # 4x around the 'a' counter of "small"
    sheet.paste(ov.crop((2950, 1900, 3570, 2520)), (620, 420))  # 4x 'k' of "talk"
    ImageDraw.Draw(sheet).text((4, 404), "4x trace overlay: blue = both, red = raster only, cyan = SVG only (max dev 0.75 src px)", fill="black")
    sheet.save(os.path.join(TESTS, "contact-logo.png"))
    mp = os.path.join(ART, "manifest.json"); m = json.load(open(mp, encoding="utf-8"))
    m["hd"]["batches"].setdefault("owner-D-1", {})["logo"] = {"source": "chatgpt/D/Royal-blue stacked small talk wordmark-1.png (fallback -9 not needed)", **out,
                                                               "sheets": ["tests/hd/contact-logo.png", "tests/hd/contact-favicon-logo-candidates.png", "tests/hd/contact-favicon-logo-final.png"]}
    json.dump(m, open(mp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(json.dumps({k: (v.get("md5") if isinstance(v, dict) and "md5" in v else None) for k, v in out.items()}))


if __name__ == "__main__":
    main()

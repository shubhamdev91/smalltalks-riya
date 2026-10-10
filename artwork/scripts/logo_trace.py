"""Official logo: clean + trim the raster master, potrace it to a single-fill SVG, verify the trace against the
raster at 4x (boundary deviation in source px), write raster exports + brand files."""
import hashlib, io, json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
import potrace

ART = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ART, "chatgpt", "D", "Royal-blue stacked small talk wordmark-1.png")
OUT = os.path.join(ART, "hd", "logo")
TESTS = os.path.join(ART, "tests", "hd")
UP = 2          # trace on a 2x alpha (sub-pixel accuracy), coordinates divided back
PAD = 4


def clean():
    a = np.array(Image.open(SRC).convert("RGBA")).astype(float)
    al = a[..., 3]
    al = np.clip((al - 8) * 255.0 / (240 - 8), 0, 255)       # snap: <=8 -> 0 (noise), >=240 -> 255 (interior 251-254)
    solid = al >= 255
    colour = np.median(a[solid][:, :3], 0).round().astype(int)
    out = np.zeros_like(a)
    out[..., :3] = colour; out[..., 3] = al
    out[al == 0, :3] = 0
    ys, xs = np.nonzero(al > 0)
    bb = (int(xs.min()) - PAD, int(ys.min()) - PAD, int(xs.max()) + 1 + PAD, int(ys.max()) + 1 + PAD)
    return np.round(out[bb[1]:bb[3], bb[0]:bb[2]]).astype(np.uint8), tuple(int(c) for c in colour), bb


def trace(alpha):
    H, W = alpha.shape
    big = np.array(Image.fromarray(alpha).resize((W * UP, H * UP), Image.BICUBIC))
    bm = potrace.Bitmap(big < 128)   # potracer traces False as ink
    plist = bm.trace(turdsize=4, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.2)
    d = []
    polys = []   # flattened polylines for verification
    for curve in plist:
        sx, sy = curve.start_point.x / UP, curve.start_point.y / UP
        d.append(f"M{sx:.2f} {sy:.2f}")
        pts = [(sx, sy)]; cur = (sx, sy)
        for seg in curve.segments:
            if seg.is_corner:
                c, e = seg.c, seg.end_point
                d.append(f"L{c.x / UP:.2f} {c.y / UP:.2f}L{e.x / UP:.2f} {e.y / UP:.2f}")
                pts += [(c.x / UP, c.y / UP), (e.x / UP, e.y / UP)]; cur = pts[-1]
            else:
                c1, c2, e = seg.c1, seg.c2, seg.end_point
                d.append(f"C{c1.x / UP:.2f} {c1.y / UP:.2f} {c2.x / UP:.2f} {c2.y / UP:.2f} {e.x / UP:.2f} {e.y / UP:.2f}")
                p0 = np.array(cur); p1 = np.array([c1.x, c1.y]) / UP; p2 = np.array([c2.x, c2.y]) / UP; p3 = np.array([e.x, e.y]) / UP
                for t in np.linspace(0, 1, 16)[1:]:
                    u = 1 - t; pts.append(tuple(u ** 3 * p0 + 3 * u * u * t * p1 + 3 * u * t * t * p2 + t ** 3 * p3))
                cur = tuple(p3)
        d.append("Z")
        polys.append(pts)
    return "".join(d), polys, len(plist)


def raster_polys(polys, W, H, k):
    acc = np.zeros((H * k, W * k), bool)
    for pts in polys:
        m = Image.new("1", (W * k, H * k), 0)
        ImageDraw.Draw(m).polygon([(x * k, y * k) for x, y in pts], fill=1)
        acc ^= np.array(m)          # even-odd
    return acc


def verify(alpha, polys, k=4):
    H, W = alpha.shape
    ref = np.array(Image.fromarray(alpha).resize((W * k, H * k), Image.BICUBIC)) >= 128
    tr = raster_polys(polys, W, H, k)
    diff = ref ^ tr
    edge = ref ^ ndimage.binary_erosion(ref)
    dist = ndimage.distance_transform_edt(~edge) / k        # source px from the raster boundary
    dev = dist[diff]
    # counters: hole count per letter component must match
    holes_ref = ndimage.label(ndimage.binary_fill_holes(ref) & ~ref)[1]
    holes_tr = ndimage.label(ndimage.binary_fill_holes(tr) & ~tr)[1]
    comps_ref = ndimage.label(ref)[1]; comps_tr = ndimage.label(tr)[1]
    res = {"diff_px_at_4x": int(diff.sum()), "max_dev_src_px": round(float(dev.max()) if dev.size else 0, 3),
           "p99_dev_src_px": round(float(np.percentile(dev, 99)) if dev.size else 0, 3),
           "iou": round(float((ref & tr).sum() / (ref | tr).sum()), 5),
           "components": [comps_ref, comps_tr], "counters": [holes_ref, holes_tr]}
    # overlay: red = raster only, cyan = trace only
    ov = np.full(ref.shape + (3,), 255, np.uint8)
    ov[ref & tr] = (0, 29, 249); ov[ref & ~tr] = (255, 0, 0); ov[tr & ~ref] = (0, 220, 220)
    return res, ov


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    os.makedirs(OUT, exist_ok=True)
    cut, colour, bb = clean()
    hexc = "#%02x%02x%02x" % colour
    H, W = cut.shape[:2]
    d, polys, n = trace(cut[..., 3])
    res, ov = verify(cut[..., 3], polys)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="small talk">'
           f'<path fill="{hexc}" fill-rule="evenodd" d="{d}"/></svg>\n')
    sp = os.path.join(OUT, "small-talk-logo.svg"); open(sp, "w").write(svg)
    Image.fromarray(cut).save(os.path.join(OUT, "small-talk-logo-trim.png"), optimize=True)
    # overlay crops at 4x around the 'a' counters and 'k'
    Image.fromarray(ov).save(os.path.join(TESTS, "logo-trace-overlay-4x.png"))
    print(json.dumps({"colour": hexc, "trim_box_in_source": bb, "size": [W, H], "subpaths": n, **res, "svg_bytes": os.path.getsize(sp)}))
    json.dump({"colour": hexc, "trim_box_in_source": list(bb), "size": [W, H], "subpaths": n, "verify": res, "svg_bytes": os.path.getsize(sp)},
              open(os.path.join(OUT, "_trace.json"), "w"), indent=1)


if __name__ == "__main__":
    main()

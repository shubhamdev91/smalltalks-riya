import re
p='typecompare.py'; s=open(p,encoding='utf-8').read()
start=s.index('def render('); end=s.index('def main():')
new='''def draw(text, f, track):
    """Draw text char by char with extra tracking (px). Returns L mask image (tight)."""
    lines = text.split("\\n")
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 0.95)
    widths = [sum(f.getlength(c) + track for c in ln) for ln in lines]
    W = int(max(widths) + abs(track) * 4 + f.size); H = lh * len(lines) + f.size
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = f.size // 2
        for c in ln:
            d.text((x, f.size // 2 + i * lh), c, font=f, fill=255)
            x += f.getlength(c) + track
    return im


def tight(im, angle):
    if angle:
        im = im.rotate(-angle, resample=Image.BICUBIC, expand=True)
    m = np.array(im) > 127
    ys, xs = np.nonzero(m)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def render(text, fpath, axes, target_h, target_w, fg, bg, shape, origin, angle=0):
    track_em = 0.0
    for _ in range(3):
        lo, hi = 4, 800
        while lo < hi:
            s = (lo + hi) // 2
            f = font(fpath, s, **axes)
            if tight(draw(text, f, track_em * s), angle).height < target_h:
                lo = s + 1
            else:
                hi = s
        s = lo; f = font(fpath, s, **axes)
        n = max(len(max(text.split("\\n"), key=len)) - 1, 1)
        a_, b_ = -0.25, 0.25
        for _ in range(20):
            m_ = (a_ + b_) / 2
            if tight(draw(text, f, m_ * s), angle).width < target_w:
                a_ = m_
            else:
                b_ = m_
        track_em = (a_ + b_) / 2
    layer = tight(draw(text, f, track_em * s), angle)
    canvas = Image.new("RGB", shape, tuple(int(v) for v in bg))
    col = Image.new("RGB", layer.size, tuple(int(v) for v in fg))
    canvas.paste(col, origin, layer)
    full = Image.new("L", shape, 0)
    full.paste(layer, origin)
    return canvas, np.array(full) > 127, s, track_em


'''
s=s[:start]+new+s[end:]
s=s.replace('img, cm, size = render(text, path, axes, th, 40, fg, bg, crop.size, origin, ANGLE.get(role, 0))','tw = xs.max() - xs.min() + 1\n            img, cm, size, tr = render(text, path, axes, th, tw, fg, bg, crop.size, origin, ANGLE.get(role, 0))')
s=s.replace('scored.append((name, iou))','scored.append((name, iou, round(size / K, 1), round(tr, 3)))')
s=s.replace("(~{size / K:.0f}px at board scale)\", img, iou))","(~{size / K:.0f}px at board scale, tracking {tr:+.3f}em)\", img, iou))")
s=s.replace('SCORE = {"pill", "talks", "shop-heading", "ui-sub"}','SCORE = {"pill", "talks", "shop-heading", "ui-sub", "headline"}')
open(p,'w',encoding='utf-8').write(s)

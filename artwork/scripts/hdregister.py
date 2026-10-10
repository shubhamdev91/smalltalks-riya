"""Masked NCC registration of an HD piece against a board crop (finds css scale + offset).

register(piece_rgba, board_rgb, search_box, scales) -> best {scale, left, top, ncc}
Works on gradient-magnitude images (robust to colour drift between the board render and the new art).
Masked normalised cross-correlation via FFT (Padfield 2012 form).
"""
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.signal import fftconvolve


def grad(g):
    g = ndimage.gaussian_filter(g, 1.0)
    return np.hypot(ndimage.sobel(g, 0), ndimage.sobel(g, 1))


def masked_ncc(I, T, M):
    """I image, T template, M binary mask (same shape as T). Returns NCC map over valid offsets."""
    T = T * M
    n = M.sum()
    Tm = T[M > 0].mean()
    Tz = (T - Tm) * M
    Ts = np.sqrt((Tz ** 2).sum())
    f = lambda a, b: fftconvolve(a, b[::-1, ::-1], mode="valid")
    num = f(I, Tz)
    sI = f(I, M)
    sI2 = f(I * I, M)
    var = sI2 - sI ** 2 / n
    den = Ts * np.sqrt(np.maximum(var, 1e-6))
    return num / den


def register(piece, board, search, scales, use_grad=True):
    """piece RGBA uint8 (source px); board RGB uint8 at css scale; search=(x0,y0,x1,y1) board region the
    piece may occupy (may extend past board edges -> padded). Returns best dict."""
    x0, y0, x1, y1 = search
    pad = 400
    B = np.pad(board.astype(float).mean(-1), pad, mode="edge")
    Bs = B[y0 + pad:y1 + pad, x0 + pad:x1 + pad]
    Bg = grad(Bs) if use_grad else Bs
    best = None
    for s in scales:
        w, h = max(4, round(piece.shape[1] * s)), max(4, round(piece.shape[0] * s))
        if w >= Bg.shape[1] or h >= Bg.shape[0]:
            continue
        p = np.array(Image.fromarray(piece).convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")).astype(float)
        M = (p[..., 3] > 200).astype(float)
        M = ndimage.binary_erosion(M, iterations=2).astype(float)
        if M.sum() < 200:
            continue
        T = p[..., :3].mean(-1)
        Tg = grad(T) if use_grad else T
        ncc = masked_ncc(Bg, Tg, M)
        iy, ix = np.unravel_index(np.argmax(ncc), ncc.shape)
        v = float(ncc[iy, ix])
        if best is None or v > best["ncc"]:
            best = {"scale": float(s), "left": int(x0 + ix), "top": int(y0 + iy), "ncc": round(v, 3), "w": w, "h": h}
    return best


def refine(piece, board, best, span=0.06, steps=13, margin=40):
    s0 = best["scale"]
    scales = np.linspace(s0 * (1 - span), s0 * (1 + span), steps)
    srch = (best["left"] - margin, best["top"] - margin, best["left"] + best["w"] + margin, best["top"] + best["h"] + margin)
    return register(piece, board, srch, scales)

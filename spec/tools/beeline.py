"""Chain detected dashes into beeline paths per column; render overlay for checking."""
import json, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.sparse.csgraph import connected_components
from scipy.spatial.distance import cdist

ROOT = os.path.join(os.path.dirname(__file__), "..")
C = os.path.join(ROOT, "crops")
G = json.load(open(os.path.join(ROOT, "landing-geometry.json")))


def order_chain(P):
    """Greedy nearest-neighbour ordering starting from the topmost end."""
    D = cdist(P, P)
    start = int(np.argmin(P[:, 1]))
    seq = [start]; left = set(range(len(P))) - {start}
    while left:
        cur = seq[-1]
        nxt = min(left, key=lambda j: D[cur, j])
        if D[cur, nxt] > 60:
            break
        seq.append(nxt); left.remove(nxt)
    return P[seq]


def smooth_path(P):
    if len(P) < 3:
        return None
    # resample every ~3 points, Catmull-Rom -> cubic
    Q = P[::2] if len(P) > 8 else P
    d = f"M{Q[0][0]:.0f},{Q[0][1]:.0f}"
    for i in range(len(Q) - 1):
        p0 = Q[i - 1] if i else Q[i]; p1 = Q[i]; p2 = Q[i + 1]; p3 = Q[i + 2] if i + 2 < len(Q) else p2
        c1 = p1 + (p2 - p0) / 6; c2 = p2 - (p3 - p1) / 6
        d += f" C{c1[0]:.0f},{c1[1]:.0f} {c2[0]:.0f},{c2[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}"
    return d


def main():
    out = {}
    for col in range(1, 5):
        im = Image.open(os.path.join(C, f"landing-col{col}@390.png")).convert("RGB")
        vis = im.copy(); d = ImageDraw.Draw(vis)
        for mode, colr in (("white", (255, 0, 255)), ("red", (0, 160, 255))):
            ds = np.array(G["dashes"][f"col{col}-{mode}"]) if G["dashes"][f"col{col}-{mode}"] else np.zeros((0, 4))
            if len(ds) < 4:
                continue
            P = ds[:, :2]
            A = (cdist(P, P) < 34).astype(int)
            n, lab = connected_components(A, directed=False)
            k = 0
            for c in range(n):
                idx = np.nonzero(lab == c)[0]
                if len(idx) < 5:
                    continue
                pts = order_chain(P[idx])
                if len(pts) < 5:
                    continue
                span = np.ptp(pts, 0)
                if max(span) < 70:
                    continue  # text clusters are compact
                gaps = np.linalg.norm(np.diff(pts, axis=0), axis=1)
                path = smooth_path(pts)
                k += 1
                key = f"col{col}-{mode}-{k}"
                out[key] = {"colour": "#ffffff" if mode == "white" else "#c8102e", "points": len(pts),
                            "y_range_in_col": [round(float(pts[:, 1].min())), round(float(pts[:, 1].max()))],
                            "dash_len_px": round(float(np.median(ds[idx, 2])), 1),
                            "pitch_px": round(float(np.median(gaps)), 1), "path": path}
                d.line([tuple(p) for p in pts], fill=colr, width=3)
                d.text(tuple(pts[0] + [6, 0]), key, fill=(0, 0, 0))
        vis.save(os.path.join(C, f"landing-col{col}-beeline.png"))
    json.dump(out, open(os.path.join(ROOT, "landing-beelines.json"), "w"), indent=1)
    for k, v in out.items():
        print(k, v["y_range_in_col"], v["points"], v["dash_len_px"], v["pitch_px"])


if __name__ == "__main__":
    main()

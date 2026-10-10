"""Download OFL font candidates + licence files from github.com/google/fonts into spec/fonts/<family>/."""
import json, os, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "fonts")
DIRS = ["librecaslontext", "sourceserif4", "youngserif"] or ["fraunces", "caprasimo", "corben", "kalam", "caveatbrush", "gochihand",
        "barlowsemicondensed", "robotocondensed", "ibmplexsanscondensed",
        "nanumpenscript", "reeniebeanie", "caveat", "playfairdisplay", "dmserifdisplay",
        "abrilfatface", "dmsans", "patrickhand", "shadowsintolighttwo"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "spec-fonts"})
    return urllib.request.urlopen(req, timeout=60).read()


for d in DIRS:
    try:
        items = json.loads(get(f"https://api.github.com/repos/google/fonts/contents/ofl/{d}"))
    except Exception as e:
        print("FAIL", d, e); continue
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for it in items:
        n = it["name"]
        if n.endswith(".ttf") and "Italic" not in n or n == "OFL.txt":
            if n.endswith(".ttf") and not any(k in n for k in ("[", "Regular", "Bold", "SemiBold", "Black", "-")) and d not in ("reeniebeanie",):
                pass
            open(os.path.join(OUT, d, n), "wb").write(get(it["download_url"]))
            print(d, n)


import json, os, glob
R='..'
n=json.load(open(f'{R}/nails/manifest.json')); f=json.load(open(f'{R}/fingers/manifest.json')); h=json.load(open(f'{R}/hand/preview-hand.json'))
f['main_nail_on_finger']={"cell_scale":0.76,"placement":"nail cell anchor (0.5,0.925) on nail_bed_anchor; nail width = 1.08x natural plate (~130 px)","overflow":"nail tip extends ~70 px above the finger canvas top at this scale; container must not clip (overflow: visible)"}
json.dump(f,open(f'{R}/fingers/manifest.json','w'),indent=2)
files={}
for p in sorted(glob.glob(f'{R}/nails/*.webp')+glob.glob(f'{R}/fingers/*.webp')+glob.glob(f'{R}/hand/*.webp')+glob.glob(f'{R}/nails/web/*.webp')+glob.glob(f'{R}/fingers/web/*.webp')+glob.glob(f'{R}/hand/web/*.webp')):
    rel=os.path.relpath(p,R).replace('\\','/'); kb=os.path.getsize(p)/1000
    files[rel]={"bytes":os.path.getsize(p),"budget_kb":200 if 'hand' in rel else 120,"within_budget":kb<=(200 if 'hand' in rel else 120)}
m={"package":"Small Talk hero artwork - Phase 1","generated":"2026-10-09","nails":n,"fingers":f,"preview_hand":h,"files":files,
   "tests":sorted(os.path.relpath(p,R).replace('\\','/') for p in glob.glob(f'{R}/tests/*.png')),
   "total_bytes":sum(v["bytes"] for v in files.values()),
   "variants":{"master":"nails/*.webp, fingers/*.webp: lossless, RGB on opaque pixels bit-identical to the source atlas (scripts/verify.py; extra-accent column is resampled 0.64x so not comparable pixel-for-pixel). Over the 120 KB budget: nails 118-156 KB, fingers 201-214 KB.","web":"nails/web/*.webp, fingers/web/*.webp: WebP q100, 41-80 KB, alpha identical, RGB delta on opaque mean ~1.0-1.5, p99 6-25 (see derivatives.json). Orchestrator chooses which set ships."},
   "derivatives":json.load(open(f'{R}/derivatives.json')),
   "contact_sheets":sorted(os.path.relpath(p,R).replace(chr(92),'/') for p in glob.glob(f'{R}/tests/contact-*.png'))}
for k in n["sets"]: n["sets"][k]["web"]=f"nails/web/{k}.webp"
for t in f["tones"]: t["web"]=t["file"].replace("fingers/","fingers/web/")
h["web"]="hand/web/preview-hand.webp"
m["ships"]="web paths (q100) ship in the theme; lossless masters stay here as source of truth (orchestrator decision 2026-10-09)"
m["preview_slots"]={"order":"index, middle, ring, little (lowest/leftmost first)","keyed_by":"the set whose nails are SHOWN on the preview hand (the next set)","source":"orchestrator decision from board 2, 2026-10-09",
  "on-me":[0,2,1,0],"brainwave":[0,1,2,0],"diet-cherry":[1,0,2,1],"green-flag":[1,0,1,0],"shaadi-shift":[2,1,0,2],"wild-card":[1,2,0,1],"pinky-promise":[0,0,0,0]}
m["preview_hand_display"]={"css_width_px_at_390_scene":146,"rule":"scale with scene width and clamp; tuned by Fable against the rendered hero"}
m["distinct_accents"]={"meaning":"columns that are visibly different designs; never fly between two columns in the same equivalence group",
  "method":"mean |dRGB| over the alpha union (premultiplied on grey) + visual check, scripts/diffcols.py; < 30 = candidate duplicate",
  "on-me":{"distinct":[0,1,2],"equivalent":[]},
  "brainwave":{"distinct":[0,1,2],"equivalent":[]},
  "diet-cherry":{"distinct":[0,1,2],"equivalent":[]},
  "green-flag":{"distinct":[0,1],"equivalent":[[1,2]],"note":"accent and extra_accent are both solid emerald (mean d 16.2); col2 only differs in shape/highlight"},
  "shaadi-shift":{"distinct":[0,1,2],"equivalent":[],"note":"col0 vs col2 mean d 17.1 but the yellow flower is the whole design difference; counts as distinct"},
  "wild-card":{"distinct":[0,1,2],"equivalent":[]},
  "pinky-promise":{"distinct":[0],"equivalent":[[0,1,2]],"note":"one design: lilac with burgundy tip; col0 tip right, col1 mirrored tip left, col2 symmetric V (mean d 18-28); near-identical at preview size"}}
p2=json.load(open(f'{R}/phase2.json'))
m["phase2"]={"package":"readjustment of approved art (no generation/redraw/recolour), 2026-10-09","checks":json.load(open(f'{R}/phase2-checks.json',encoding='utf-8-sig')),**p2}
S={"characters":{"status":"accepted","display":"150 css px wide at a 390 scene, bleed/anchor as listed","known_deviations":["same woman in all 7 cells","brainwave: no crescent-bag sketch visible","pinky-promise: clasped hands, one solid burgundy + one tipless lilac nail","hair-smudge at feathered cuts"]},
 "chapters":{"status":"accepted: ship the -fade variants only (fade_variant.web)","display":"max 180 css px wide (>=1.5x density); never wider","raw_variant":"not shipped","known_deviations":["ground colour delta vs metaobject (hidden by fade)","on-me: no bill","pinky-promise: no hands","brainwave: no blue pen","shaadi-shift: safety pin unclear","no nails visible in scenes"]},
 "guide":{"status":"accepted: guide/web/nail-guide.webp","as_is":"not shipped"},
 "shop_lifestyle":{"status":"accepted","label":"must be labelled as illustration wherever shown"},
 "shop_finger_states":{"status":"not shipped - design mismatch","reason":"shaadi-shift shows two white-centred flowers; pinky-promise tip is crimson; shipping 5 of 7 is inconsistent"},
 "packaging":{"status":"accepted as final source; render <=380 css px; srcset 370/480 only","note":"owner: no hi-res exists; the seven approved PNGs are final. Shadow is applied in CSS."},
 "diet_can":{"status":"not used anywhere; crop proposal rejected","note":"character and chapter cans are unbranded"}}
for k,v in S.items(): m["phase2"][k]={"_status":v,"items":m["phase2"][k]}
m["phase2"]["status_decided_by"]="orchestrator, 2026-10-09"
m["contact_sheets"]=sorted(os.path.relpath(p,R).replace(chr(92),'/') for p in glob.glob(f'{R}/tests/contact-*.png'))
json.dump(m,open(f'{R}/manifest.json','w'),indent=2)
print(m['total_bytes']); [print(k,v['bytes'],v['within_budget']) for k,v in files.items()]








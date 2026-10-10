"""Builds motion/lab/index.html (a reference DOM for the hero motion controller) from artwork/manifest.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
m = json.load(open(ROOT / 'artwork/manifest.json', encoding='utf-8'))
camp = json.load(open(ROOT / 'backup/theme-186649313493/campaign-metaobjects.json', encoding='utf-8'))['entries']
order = ['on-me', 'brainwave', 'diet-cherry', 'green-flag', 'shaadi-shift', 'wild-card', 'pinky-promise']
by = {c['handle']: c for c in camp}
SWATCHES = ['#efa67d', '#d7895d', '#9f5a3a', '#713f2c']


def flight_cols(h):
    return [c for c in m['distinct_accents'][h]['distinct'] if c != 0]


HD = m['hd']['batches']['board-corrections-1']['assets']
HERO_HD = {'on-me': ['on-me-woman'], 'green-flag': ['green-flag-woman-hero'], 'shaadi-shift': ['shaadi-shift-pin-hero'],
           'wild-card': ['wild-card-woman-hero', 'wild-card-cards-hand-hero'], 'pinky-promise': ['pinky-promise-face-hero']}


def hd_img(key):
    a = HD[key]
    return {'src': '../../artwork/' + a['web'], 'width': a['web_px'][0], 'height': a['web_px'][1]}


def hero_character(h):
    """v3.4: HD board-correction pieces where they exist (placement is CSS); Wild Card has a second part."""
    if h == 'diet-cherry':
        return {'src': '../../artwork/_source/desi-diet-can-v1.webp', 'width': 1189, 'height': 1323, 'anchor': {'x': 0, 'y': 0.5}, 'bleed': ['left'], 'widthAt390': 220}
    if h in HERO_HD:
        keys = HERO_HD[h]
        ch = {**hd_img(keys[0]), 'bleed': ['left'] if h != 'green-flag' else ['right']}
        if len(keys) > 1:
            ch['parts'] = [hd_img(k) for k in keys[1:]]
        return ch
    ch = m['phase2']['characters']['items'][h]
    return {'src': '../../artwork/' + ch['web'], 'width': ch['width'], 'height': ch['height'],
            'anchor': ch['anchor'], 'bleed': ch['bleed_edges'], 'widthAt390': ch['css_width_at_390']}


campaigns = []
for h in order:
    c = by[h]
    cta_ink = '#09195d' if h == 'wild-card' else c['cta_foreground']  # theme-local contrast guard
    campaigns.append({
        'key': h, 'name': c['name'], 'headline': c['headline'], 'note': c['note'], 'index': c['motion_index'],
        'colors': {'scene': c['background'], 'ink': c['foreground'], 'ctaBackground': c['cta_background'], 'ctaForeground': cta_ink},
        'url': '/products/' + c['product_handle'], 'ctaLabel': 'Shop “' + c['name'] + '”',
        'sprite': '../../artwork/' + m['nails']['sets'][h]['web'],
        'previewSlots': m['preview_slots'][h], 'flightColumns': flight_cols(h),
        'live': True,
        'altText': c['name'] + ' nail design: ' + c['short_description'],
        **({'sampleColumns': [1, 0]} if h == 'green-flag' else {}),
        'character': hero_character(h),
    })

data = {
    'version': 2, 'autoplay': True, 'defaultTone': 2,
    'tones': [{'index': t['index'], 'swatch': s, 'src': '../../artwork/' + t['web']} for t, s in zip(m['fingers']['tones'], SWATCHES)],
    'finger': {'width': 310, 'height': 840, 'anchor': {'x': m['fingers']['nail_bed_anchor']['x'], 'y': m['fingers']['nail_bed_anchor']['y']}, 'nailCellScale': 0.76},
    'nailCell': {'width': 204, 'height': 354, 'anchor': {'x': 0.5, 'y': 0.925}},
    'previewHand': (lambda ph: {'src': '../../artwork/' + ph['web'], 'width': ph['web_px'][0], 'height': ph['web_px'][1],
                    'slots': [{'cuticle': s['cuticle'], 'rotation': s['rotation_deg'], 'cellWidthFrac': s['cell_width_frac_of_hand']} for s in ph['slots']]})(m['hd']['batches']['board-corrections-1']['preview_hand']),
    'labels': {'pause': 'Pause', 'play': 'Play', 'replay': 'Play again', 'next': 'Next set: {name}',
               'tone': 'Skin tone, Skin tone {n} of {count}', 'announce': '{name}. {headline}', 'hold': 'Press and hold to pause.'},
    'campaigns': campaigns,
}

first, nxt = campaigns[0], campaigns[1]
slots = nxt['previewSlots']
pn = ''.join(
    f'<span class="st-nail" data-st-hero-preview-nail="{i}" style="--st-nails:url(\'{nxt["sprite"]}\');--col:{slots[i]}"></span>'
    for i in range(4))

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Small Talk hero - motion lab</title>
<link rel="preload" as="image" href="{first['sprite']}">
<link rel="stylesheet" href="../st-hero.css">
<style>
 @font-face{{font-family:'Fraunces';src:url('../../spec/fonts/fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf') format('truetype');font-weight:100 900;font-display:swap}}
 @font-face{{font-family:'Caveat';src:url('../../spec/fonts/caveat/Caveat[wght].ttf') format('truetype');font-weight:400 700;font-display:swap}}
 @font-face{{font-family:'Barlow Semi Condensed';src:url('../../spec/fonts/barlowsemicondensed/BarlowSemiCondensed-SemiBold.ttf') format('truetype');font-weight:600;font-display:swap}}
 :root{{--st-header-h:69px}}
 body{{margin:0;font-family:system-ui,sans-serif;background:#fdfdfc}}
 .st-pen{{font-family:'Segoe Script','Comic Sans MS',cursive;font-weight:300}}
 .st-display{{font-family:Georgia,serif;font-weight:900;letter-spacing:-.04em}}
 .lab-header{{height:69px;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;padding:0 1rem;color:#1013b3;font-weight:800}}
 .lab-below{{height:120vh;padding:2rem;color:#272332}}
 .visually-hidden{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
</style></head><body>
<div class="lab-header"><span>&#9776;</span><span>small talk</span><span class="st-pen">the talks</span><span>bag</span></div>
<section class="st-hero" data-st-hero data-active-key="{first['key']}" data-active-index="0" data-next-key="{nxt['key']}" data-tone="2" data-tone-count="4" data-autoplay="true" aria-label="Nail sets"
 style="--st-scene:{first['colors']['scene']};--st-scene-ink:{first['colors']['ink']};--st-cta-bg:{first['colors']['ctaBackground']};--st-cta-ink:{first['colors']['ctaForeground']};--st-tone-swatch:#d7895d">
 <div class="st-hero__scene" data-st-hero-scene aria-hidden="true"></div>
 <div class="st-hero__halo" aria-hidden="true"></div>
 <div class="st-hero__character" data-st-hero-character aria-hidden="true" data-bleed="{' '.join(first['character']['bleed'])}"><img data-st-hero-character-img src="{first['character']['src']}" width="{first['character']['width']}" height="{first['character']['height']}" alt="" fetchpriority="low"></div>
 <button type="button" class="st-hero__preview" data-st-hero-preview data-key="{nxt['key']}" aria-label="Next set: {nxt['name']}" aria-disabled="true">
  <img class="st-hero__hand" src="{data['previewHand']['src']}" width="{data['previewHand']['width']}" height="{data['previewHand']['height']}" alt="" loading="lazy">{pn}
 </button>
 <div class="st-hero__copy"><p class="st-hero__note" data-st-hero-note>{first['note']}</p><h1 class="st-hero__headline" data-st-hero-headline>{first['headline']}</h1></div>
 <div class="st-hero__accent st-hero__accent--2" aria-hidden="true"><span class="st-nail" data-st-hero-accent="2" style="--st-nails:url('{first['sprite']}');--col:2"></span></div>
 <div class="st-hero__accent st-hero__accent--1" aria-hidden="true"><span class="st-nail" data-st-hero-accent="1" style="--st-nails:url('{first['sprite']}');--col:1"></span></div>
 <div class="st-hero__finger" data-st-hero-finger aria-hidden="true">
  <img class="st-hero__tone" data-st-hero-tone-sprite src="{data['tones'][1]['src']}" width="310" height="840" alt="" fetchpriority="high">
  <button type="button" class="st-hero__main" data-st-hero-main aria-label="Hold to pause" aria-description="Press and hold to pause." aria-disabled="true"><span class="st-nail" data-st-hero-main-nail style="--st-nails:url('{first['sprite']}');--col:0"></span></button>
 </div>
 <div class="st-hero__flyers" data-st-hero-flyers aria-hidden="true"></div>
 <div class="st-hero__controls">
  <button type="button" class="st-hero__control st-hero__control--pause" data-st-hero-pause aria-pressed="false" aria-disabled="true" aria-label="Pause">
   <svg class="st-hero__icon-pause" width="14" height="16" viewBox="0 0 14 16" aria-hidden="true"><rect x="1" y="1" width="4" height="14" rx="1" fill="currentColor"/><rect x="9" y="1" width="4" height="14" rx="1" fill="currentColor"/></svg>
   <svg class="st-hero__icon-play" width="14" height="16" viewBox="0 0 14 16" aria-hidden="true"><path d="M2 1l11 7-11 7z" fill="currentColor"/></svg>
  </button>
  <button type="button" class="st-hero__control st-hero__control--tone" data-st-hero-tone aria-disabled="true" aria-label="Skin tone, Skin tone 2 of 4"><span class="st-hero__swatch" aria-hidden="true"></span></button>
 </div>
 <p class="visually-hidden" data-st-hero-main-desc id="st-hero-main-desc">{first['altText']}</p>
 <a class="st-hero__cta" href="{first['url']}" data-st-hero-cta>{first['ctaLabel']}<span class="st-arrow" aria-hidden="true">&#8599;</span></a>
 <p class="visually-hidden" aria-live="polite" data-st-hero-status></p>
 <script type="application/json" data-st-hero-data>{json.dumps(data)}</script>
</section>
<div class="lab-below"><p>Page content below the hero. Scroll should always move the page.</p></div>
<script src="../st-hero-motion.js" defer></script>
</body></html>'''

(ROOT / 'motion/lab').mkdir(parents=True, exist_ok=True)
(ROOT / 'motion/lab/index.html').write_text(html, encoding='utf-8')
(ROOT / 'motion/lab/data.json').write_text(json.dumps(data, indent=1), encoding='utf-8')
(ROOT / '.claude').mkdir(exist_ok=True)
json.dump({"version": "0.0.1", "configurations": [{"name": "motion-lab", "runtimeExecutable": "python",
           "runtimeArgs": ["-m", "http.server", "8765", "--bind", "127.0.0.1"], "port": 8765},
          {"name": "motion-lab-2", "runtimeExecutable": "python",
           "runtimeArgs": ["-m", "http.server", "8766", "--bind", "127.0.0.1"], "port": 8766}]},
          open(ROOT / '.claude/launch.json', 'w'), indent=1)
print('ok', len(html))

"""Prepare (locally, no upload) TLK-154 + the single posting switch snippet st-talk-live. Run from theme-build/src."""
import json

READ_FLAG = """{%- capture live_flag -%}{%- render 'st-talk-live' -%}{%- endcapture -%}
{%- liquid
  assign live = false
  if live_flag == 'on'
    assign live = true
  endif
-%}
"""


def edit(p, pairs):
    s = open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:70])
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


# Hub / topic list
edit('sections/st-talks-list.liquid', [
    ("""{%- liquid
  assign is_talks = false
  assign feed = nil""", READ_FLAG + """{%- liquid
  assign is_talks = false
  assign feed = nil"""),
    ("""id: section.id, live: section.settings.posting_live -%}""", """id: section.id, live: live -%}"""),
    ("""{%- if is_talks and section.settings.posting_live -%}""", """{%- if is_talks and live -%}"""),
    ("""    { "type": "checkbox", "id": "posting_live", "label": "Posting live", "default": false, "info": "Turn on once the talks backend is set up (talks/OWNER-SETUP.md). Off: the composer shows the pre-launch note (TLK-153)." },
""", ""),
])
# Thread
edit('sections/st-talks-thread.liquid', [
    ("""{%- liquid
  assign thread = nil
  assign moved = nil""", READ_FLAG + """{%- liquid
  assign thread = nil
  assign moved = nil"""),
    ("""    assign form_id = 'StReply-' | append: section.id
    assign live = section.settings.posting_live
""", """    assign form_id = 'StReply-' | append: section.id
"""),
    ("""    { "type": "checkbox", "id": "posting_live", "label": "Posting live", "default": false, "info": "Turn on once the talks backend is set up (talks/OWNER-SETUP.md). Off: replies and reports show the pre-launch note (TLK-153)." },
""", ""),
])
# Start-a-talk panel
edit('sections/st-talks-start.liquid', [
    ("""{%- liquid
  assign is_talks = false
  if metaobject and metaobject.system.type == 'talk_thread'""", READ_FLAG + """{%- liquid
  assign is_talks = false
  if metaobject and metaobject.system.type == 'talk_thread'"""),
    ("""id: section.id, live: section.settings.posting_live -%}""", """id: section.id, live: live -%}"""),
    ("""    { "type": "checkbox", "id": "posting_live", "label": "Posting live", "default": false, "info": "Same switch as on the hub and the thread." },
""", ""),
])
# House rules: TLK-075 when live, TLK-154 before launch (same switch)
edit('sections/st-talks-rules.liquid', [
    ("""{%- liquid
  assign is_talks = false
  if blog.handle == section.settings.blog_handle and article == blank""", READ_FLAG + """{%- liquid
  assign is_talks = false
  if blog.handle == section.settings.blog_handle and article == blank"""),
    ("""    {%- if section.settings.moderation != blank -%}
      <p>{{ section.settings.moderation | escape }}</p>
    {%- endif -%}""", """    {%- liquid
      assign moderation = section.settings.moderation
      unless live
        assign moderation = section.settings.moderation_prelaunch | default: section.settings.moderation
      endunless
    -%}
    {%- if moderation != blank -%}
      <p>{{ moderation | escape }}</p>
    {%- endif -%}"""),
    ("""    { "type": "textarea", "id": "moderation", "label": "Moderation (TLK-075)",""",
     """    { "type": "textarea", "id": "moderation_prelaunch", "label": "Moderation before posting opens (TLK-154)", "info": "Shown instead of TLK-075 while the talks posting switch (snippet st-talk-live) is off.", "default": "Once posting opens, talks and replies go live straight away. Anything that might name a real person is held for a quick check first, and we take down whatever breaks these rules." },
    { "type": "textarea", "id": "moderation", "label": "Moderation (TLK-075)","""),
])
# Templates: drop the old per-section switch, add TLK-154 to the rules settings
TLK154 = ("Once posting opens, talks and replies go live straight away. Anything that might name a real person is held "
          "for a quick check first, and we take down whatever breaks these rules.")
for path, keys in {'templates/blog.json': ['main'], 'templates/metaobject/talk_topic.json': ['main'],
                   'templates/metaobject/talk_thread.json': ['main', 'start']}.items():
    d = json.load(open(path, encoding='utf-8'))
    for k in keys:
        d['sections'][k]['settings'].pop('posting_live', None)
    r = d['sections']['rules']['settings']
    order = list(r.keys())
    r['moderation_prelaunch'] = TLK154
    order.insert(order.index('moderation'), 'moderation_prelaunch')
    d['sections']['rules']['settings'] = {k: r[k] for k in order}
    open(path, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('prepared')

"""Apply st-copy v1.4 talks wording to the theme-local talks files (run from theme-build/src)."""


def edit(p, pairs):
    s = open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:70])
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


edit('snippets/st-talk-config.liquid', [
    ("""          {{ k | json }}: {{ key | t | json }}{% unless forloop.last %},{% endunless %}""",
     """          {{ k | json }}: {{ key | t: max: '__max__' | json }}{% unless forloop.last %},{% endunless %}"""),
])
edit('snippets/st-talk-composer.liquid', [
    ("""  @param {boolean} [live] - Posting is switched on (section setting "Posting live"). Off: a quiet "Posting opens
    soon" note renders instead of the form (TLK-148), so nobody meets a box that can't post yet.""",
     """  @param {boolean} [live] - Posting is switched on (section setting "Posting live"). Off: a quiet pre-launch note
    renders instead of the form (TLK-153), so nobody meets a box that can't post yet."""),
    ("""    <p class="st-compose__soon">{{ 'small_talk.talks.live.soon' | t }}</p>""",
     """    <p class="st-compose__soon">{{ 'small_talk.talks.live.prelaunch' | t }}</p>"""),
])
edit('sections/st-talks-thread.liquid', [
    ("""      <p class="st-reply__soon">{{ 'small_talk.talks.live.soon' | t }}</p>""",
     """      <p class="st-reply__soon">{{ 'small_talk.talks.live.prelaunch' | t }}</p>"""),
    ("""      <p class="st-thread__meta">
        {{- t_alias | escape -}}
        {%- if topic_label != blank -%}
          {{ ' · ' }}
          {%- if topic -%}
            <a href="{{ topic.system.url }}">{{ topic_label | escape }}</a>
          {%- else -%}
            {{- topic_label | escape -}}
          {%- endif -%}
        {%- endif -%}
        {%- if thread.posted_at.value != blank -%}""",
     """      <p class="st-thread__meta">
        {{- t_alias | escape -}}
        {%- if thread.posted_at.value != blank -%}"""),
    ("""  - "Back to the talks" (TLK-020), the set-nail avatar, "{alias} · {topic} · {date}" (TLK-021), the title (H1), the""",
     """  - "Back to the talks" (TLK-020), the set-nail avatar, "{alias} · {date}" (TLK-008/021), the title (H1), the"""),
    ("""    assign topic = thread.topic.value
    assign topic_label = thread.topic_label.value | default: topic.label.value
""", ""),
    ("""Off: replies and reports show \\"Posting opens soon\\"." },""",
     """Off: replies and reports show the pre-launch note (TLK-153)." },"""),
])
edit('sections/st-talks-list.liquid', [
    ("""          {%- else -%}
            <p class="st-talks__empty" data-st-empty>{{ 'small_talk.talks.hub.empty' | t }}</p>
          {%- endif -%}
        {%- endif -%}
        {%- if paginate.previous or paginate.next -%}""",
     """          {%- else -%}
            <p class="st-talks__empty" data-st-empty>{{ 'small_talk.talks.live.empty' | t }}</p>
          {%- endif -%}
        {%- endif -%}
        {%- if paginate.previous or paginate.next -%}"""),
    ("""      {%- else -%}
        <p class="st-talks__empty" data-st-empty>{{ 'small_talk.talks.hub.empty' | t }}</p>
      {%- endif -%}
    {%- endif -%}""",
     """      {%- else -%}
        <p class="st-talks__empty" data-st-empty>{{ 'small_talk.talks.live.empty' | t }}</p>
      {%- endif -%}
    {%- endif -%}"""),
    ("""Off: the composer shows \\"Posting opens soon\\"." },""",
     """Off: the composer shows the pre-launch note (TLK-153)." },"""),
])
edit('snippets/st-talk-alias.liquid', [
    ("""  <button type="button" class="st-alias__link" data-st-alias-toggle aria-expanded="false" aria-controls="{{ id }}-alias">""",
     """  <button
    type="button"
    class="st-alias__link"
    data-st-alias-toggle
    aria-expanded="false"
    aria-controls="{{ id }}-alias"
    aria-label="{{ 'small_talk.talks.live.change_label' | t | escape }}"
  >"""),
    ("""    <button type="button" class="st-alias__ghost" data-st-alias-shuffle>{{ 'small_talk.talks.live.alias_shuffle' | t }}</button>""",
     """    <button type="button" class="st-alias__ghost" data-st-alias-shuffle aria-label="{{ 'small_talk.talks.live.shuffle_label' | t | escape }}">
      {{- 'small_talk.talks.live.alias_shuffle' | t -}}
    </button>"""),
])
edit('sections/st-talks-rules.liquid', [
    ("""    {%- if section.settings.moderation != blank -%}
      <p>{{ section.settings.moderation | escape }}</p>""",
     """    {%- if section.settings.privacy != blank -%}
      <p>{{ section.settings.privacy | escape }}</p>
    {%- endif -%}
    {%- if section.settings.moderation != blank -%}
      <p>{{ section.settings.moderation | escape }}</p>"""),
    ("""    { "type": "text", "id": "rule_2", "label": "Rule 2 (TLK-072)", "default": "No real names, no handles, no screenshots, nothing that could identify anyone." },
    { "type": "text", "id": "rule_3", "label": "Rule 3 (TLK-073)", "default": "No hate, harassment or bullying. No selling, no links." },
    { "type": "text", "id": "rule_4", "label": "Rule 4 (TLK-074)", "default": "Your alias is the only name anyone sees. No email, no account." },""",
     """    { "type": "text", "id": "rule_2", "label": "Rule 2 (TLK-072)", "default": "No real names, numbers, handles or links. Nothing that could identify anyone." },
    { "type": "text", "id": "rule_3", "label": "Rule 3 (TLK-073)", "default": "No hate, harassment or bullying. No selling." },
    { "type": "text", "id": "rule_4", "label": "Rule 4 (TLK-074)", "default": "Your alias is the only name anyone sees. We don’t ask for a name, email or account." },
    { "type": "textarea", "id": "privacy", "label": "Privacy line (TLK-148)", "default": "To stop spam, we keep a scrambled code for your device and network, never the details themselves, and delete it within 30 days." },"""),
    ("""    { "type": "textarea", "id": "moderation", "label": "Moderation (TLK-075)", "default": "Talks and replies go live straight away. Our filter holds anything that might name someone for a quick check, and we take down what breaks these rules." },
    { "type": "textarea", "id": "report", "label": "How to report (TLK-076)", "info": "{email} becomes a link to the store's contact email.", "default": "Tap Report on anything that breaks these rules. Three reports and it’s hidden until we’ve checked. Something about you? Email {email} and we’ll take it down." },""",
     """    { "type": "textarea", "id": "moderation", "label": "Moderation (TLK-075)", "default": "Talks and replies go live straight away. Anything that might name a real person is held for a quick check first, and we take down whatever breaks these rules." },
    { "type": "textarea", "id": "report", "label": "How to report (TLK-076)", "info": "{email} becomes a link to the store's contact email.", "default": "Tap Report on anything that breaks these rules. Three reports from different people and it’s hidden until we’ve checked it. Something here about you? Email {email} with the link and we’ll take it down." },"""),
])
edit('assets/st-talks.js', [
    ("""  const fmt = (text, vars = {}) =>
    String(text ?? '')
      .replace('__alias__', vars.alias ?? '')
      .replace('__n__', vars.n ?? '');""",
     """  const fmt = (text, vars = {}) =>
    String(text ?? '')
      .replace('__alias__', vars.alias ?? '')
      .replace('__n__', vars.n ?? '')
      .replace('__max__', vars.max ?? '');"""),
    ("""    const showError = (code, field) => {
      say(status, E[code] ?? E.server, 'error');""",
     """    const showError = (code, field) => {
      say(status, fmt(E[code] ?? E.server, { max: cfg.max.thread.toLocaleString('en-IN') }), 'error');"""),
    ("""      if (text.length > cfg.max.reply) return say(status, E.too_long, 'error'), ta.focus();""",
     """      if (text.length > cfg.max.reply) return say(status, fmt(E.too_long, { max: cfg.max.reply }), 'error'), ta.focus();"""),
    ("""          say(status, E[error.code] ?? E.server, 'error');
          ta.setAttribute('aria-invalid', 'true');""",
     """          say(status, fmt(E[error.code] ?? E.server, { max: cfg.max.reply }), 'error');
          ta.setAttribute('aria-invalid', 'true');"""),
])
print('ok')

"""House-rules section settings = st-copy v1.4 (TLK-070…077 + TLK-148) in the talks templates (run from theme-build/src)."""
import json

RULES = {
    "rule_2": "No real names, numbers, handles or links. Nothing that could identify anyone.",
    "rule_3": "No hate, harassment or bullying. No selling.",
    "rule_4": "Your alias is the only name anyone sees. We don’t ask for a name, email or account.",
    "privacy": "To stop spam, we keep a scrambled code for your device and network, never the details themselves, and delete it within 30 days.",
    "moderation": "Talks and replies go live straight away. Anything that might name a real person is held for a quick check first, and we take down whatever breaks these rules.",
    "report": "Tap Report on anything that breaks these rules. Three reports from different people and it’s hidden until we’ve checked it. Something here about you? Email {email} with the link and we’ll take it down.",
}
ORDER = ["blog_handle", "heading", "rule_1", "rule_2", "rule_3", "rule_4", "privacy", "moderation", "report", "support",
         "support_tel_1", "support_tel_2"]
for path in ('templates/blog.json', 'templates/metaobject/talk_topic.json', 'templates/metaobject/talk_thread.json'):
    d = json.load(open(path, encoding='utf-8'))
    s = d['sections']['rules']['settings']
    s.update(RULES)
    d['sections']['rules']['settings'] = {k: s[k] for k in ORDER if k in s}
    open(path, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    print(path, 'ok')

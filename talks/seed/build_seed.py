"""Builds metaobjectCreate variables for the 9 seed threads from the-talks articles (read 9 Oct via Admin API)."""
import json, re, sys
TOPIC = {"Plot twists": "gid://shopify/Metaobject/616028242133", "Tiny wins": "gid://shopify/Metaobject/616028274901", "Nail talk": "gid://shopify/Metaobject/616028307669"}
A = json.load(open('articles.json', encoding='utf-8'))
out = {}
for i, a in enumerate(sorted(A, key=lambda a: a['publishedAt'], reverse=True)):
    topic = next(t for t in a['tags'] if t in TOPIC)
    sset = next(t.split(':', 1)[1] for t in a['tags'] if t.startswith('set:'))
    body = re.sub(r'<[^>]+>', '', a['body']).strip()
    out[f"t{i}"] = {"type": "talk_thread", "handle": a['handle'], "capabilities": {"publishable": {"status": "ACTIVE"}},
        "fields": [{"key": "title", "value": a['title']}, {"key": "body", "value": body},
                   {"key": "topic", "value": TOPIC[topic]}, {"key": "alias", "value": "small talk"},
                   {"key": "avatar", "value": sset}, {"key": "by_brand", "value": "true"},
                   {"key": "posted_at", "value": a['publishedAt']}, {"key": "reply_count", "value": "0"},
                   {"key": "report_count", "value": "0"}, {"key": "source", "value": "seed: " + a['id']}]}
json.dump(out, open('seed_vars.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False))

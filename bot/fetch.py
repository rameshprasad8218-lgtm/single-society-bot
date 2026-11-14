import re, html, feedparser
from .config import FEEDS


def clean(t):
    t = html.unescape(re.sub(r"<[^>]+>", " ", t or ""))
    return re.sub(r"\s+", " ", t).strip()


def fetch(feed_keys, seen):
    items, titles = [], set()
    for k in feed_keys:
        d = feedparser.parse(FEEDS[k])
        for e in d.entries[:25]:
            title = clean(e.get("title"))
            src = clean(e.get("source", {}).get("title", "")) if e.get("source") else ""
            if " - " in title and not src:
                title, src = title.rsplit(" - ", 1)
            elif src and title.endswith(" - " + src):
                title = title[: -len(src) - 3]
            key = title.lower()[:60]
            if not title or key in titles or e.get("link") in seen or key in seen:
                continue
            titles.add(key)
            items.append({
                "title": title,
                "source": src,
                "link": e.get("link", ""),
                "published": e.get("published", ""),
                "summary": clean(e.get("summary"))[:300],
            })
    return items

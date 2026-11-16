"""Run one slot: fetch -> AI write -> render poster -> save -> (publish).

Usage: python -m bot.main [--slot 1030] [--series cricket] [--no-publish]
"""
import argparse, csv, datetime as dt, json, os, subprocess, sys
from pathlib import Path
from .config import SERIES, SLOTS
from .fetch import fetch
from .write import write
from .render import render
from . import publish as ig
from . import telegram as tg

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "posted.json"
LOG = ROOT / "data" / "log.csv"
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def nearest_slot(now):
    # GitHub cron runs 40-55 min late, so round DOWN to the hour slot (nearest-slot made two
    # posts land in slot 2100 and skipped subah/neta series entirely).
    hm = now.hour * 60 + now.minute
    past = [s for s in SLOTS if int(s[:2]) * 60 + int(s[2:]) <= hm]
    return max(past) if past else min(SLOTS)


def _toks(t):
    import re
    return {w[:6] for w in re.findall(r"[a-z0-9]{5,}", t.lower())}


def same_story(title, recent):
    # same news in different words/sources (e.g. Amitabh firing story posted twice): >=2 shared long words
    t = _toks(title)
    return any(len(t & _toks(r)) >= 2 for r in recent[-40:])


def git(*a):
    subprocess.run(["git", *a], cwd=ROOT, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot"); ap.add_argument("--series"); ap.add_argument("--no-publish", action="store_true")
    a = ap.parse_args()
    now = dt.datetime.now(IST)
    slot = a.slot or nearest_slot(now)
    rot = SLOTS[slot]
    series_key = a.series or rot[now.timetuple().tm_yday % len(rot)]
    name, tag, feeds = SERIES[series_key]

    state = json.loads(STATE.read_text()) if STATE.exists() else {"seen": [], "recent": []}
    day = now.strftime("%Y-%m-%d")
    done = state.get("slots_done", {})
    if not a.slot and slot in done.get(day, []):
        print("Slot", slot, "already posted today"); return
    items = fetch(feeds, set(state["seen"]))
    items = [i for i in items if not same_story(i["title"], state["recent"])]
    if not items:
        print("No fresh news for", series_key); return
    data, item = write(name, items, state["recent"])
    if not data:
        print("AI skipped: nothing suitable"); return
    if not data.get("serious") and not data.get("tag"):
        data["tag"] = tag

    out = ROOT / "posters" / day
    out.mkdir(parents=True, exist_ok=True)
    stem = f"{now.strftime('%H%M')}_{series_key}"
    png = out / f"{stem}.png"
    render(data, str(png))
    caption = data["caption"].strip() + "\n\n" + " ".join(data["hashtags"])
    (out / f"{stem}.txt").write_text(caption + f"\n\nNews link: {item['link']}\n", encoding="utf-8")
    (out / f"{stem}.json").write_text(json.dumps({"data": data, "item": item}, ensure_ascii=False, indent=1), encoding="utf-8")

    state["seen"] = (state["seen"] + [item["link"], item["title"].lower()[:60]])[-600:]
    state["recent"] = (state["recent"] + [item["title"]])[-40:]
    state["slots_done"] = {day: done.get(day, []) + [slot]}
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    media_id, status = "", "saved"
    in_ci = os.getenv("GITHUB_ACTIONS") == "true"
    if in_ci:
        git("add", "-A"); git("commit", "-m", f"poster {day} {stem}"); git("push")
    if ig.ready() and not a.no_publish:
        repo = os.environ.get("GITHUB_REPOSITORY")
        url = f"https://raw.githubusercontent.com/{repo}/main/posters/{day}/{stem}.png"
        try:
            media_id = ig.publish(url, caption); status = "posted"
        except Exception as e:
            status = f"publish_failed: {e}"[:200]
            print(status, file=sys.stderr)

    hook = os.getenv("MAKE_WEBHOOK_URL")
    if hook and not a.no_publish and status != "posted":
        import requests
        repo = os.environ.get("GITHUB_REPOSITORY")
        url = f"https://raw.githubusercontent.com/{repo}/main/posters/{day}/{stem}.png"
        try:
            r = requests.post(hook, json={"image_url": url, "caption": caption, "series": series_key}, timeout=60)
            status = "sent_to_make" if r.ok else f"make_failed_{r.status_code}"
        except Exception as e:
            status = f"make_failed: {e}"[:120]

    if tg.ready():
        try:
            tg.send(str(png), caption); status += "+telegram"
        except Exception as e:
            status += f"+telegram_failed: {e}"[:120]
            print(status, file=sys.stderr)

    new = not LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time_ist", "series", "serious", "headline", "source", "media_id", "status"])
        w.writerow([now.strftime("%Y-%m-%d %H:%M"), series_key, data.get("serious", False),
                    f"{data.get('line1','')} {data.get('line2','')} {data.get('line3','')}", item["source"], media_id, status])
    if in_ci:
        git("add", "-A"); git("commit", "-m", f"log {stem} {status}"); git("push")
    print(status, png)


if __name__ == "__main__":
    main()

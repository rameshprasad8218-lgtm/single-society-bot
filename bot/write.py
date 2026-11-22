import json, os, time, requests
from .config import GEMINI_MODEL, MAX_ITEMS_TO_AI, PAGE_HASHTAG

PROMPT = """Tum "Single Society" naam ke Instagram news page ke head writer ho.
Page ka style: har khabar funny aur ekdum aasan Hinglish (Roman Hindi) mein, taaki 10 second mein samajh aa jaye.
Series: {series}

Neeche aaj ki khabrein hain (title, source, summary). Inme se SIRF EK chuno jo:
- India mein sabse zyada log share karenge (paisa, students, cricket, filmein, desh ki badi khabar)
- Pichhli posts se alag ho: {recent}

KADE NIYAM:
1. Sirf wahi facts aur numbers likho jo neeche diye text mein hain. Koi number apne se mat banao.
2. Maut, hadsa, aatank, aparadh, aapda, beemari -> "serious": true, aur koi mazaak nahi (chat aur joke khaali chhodo).
3. Dharm, jaati, aurat, kisi neta/celebrity par personal mazaak kabhi nahi. Mazaak sirf situation par.
3c. Shabd galat mat badlo: "tareef" (praise) ka matlab tariff NAHI hai, aur "tariff" ka matlab tareef nahi. Headline mein sirf wahi likho jo news kehti hai (jaise Trump ne India ki TAREEF ki, tariff nahi lagaya). Agar headline se khabar ka matlab ulta ho sakta hai, to skip karo.
3b. Serious post (maut/hadsa/aatank): caption mein "like banta hai", emoji-bhari hype ya engagement-bait nahi; sirf shant, izzat wali line. Masjid/mandir/church jaisi dharmik jagah ka naam mat likho. Har shabd ki spelling dobara check karo (jaise "lashkar", "masjid").
4. Politics mein kisi party ka paksh mat lo.
5. Agar koi bhi khabar inme fit na ho to {{"skip": true}} do.
6. SAARA text (line1, line2, line3, sub, stats, chat, asar) sirf Roman Hinglish (English letters) mein likho. Devanagari ya Gurmukhi/Punjabi akshar kabhi nahi, aur ek line mein do script mix mat karo.
7. Wahi film/insaan/ghatna dobara mat chuno jo pichhli posts mein aa chuki hai (naam ya topic same ho to alag khabar lo).
8. Stats mein sirf asli number/tareekh jo text mein hai ("9ve din" jaisa filler ya "Kiya naya record" jaisa khaali matlab nahi). Number na ho to sirf 2 stats do.
9. Caption ka aakhri sawaal aisa ho ki log share/save karein ya dost ko tag karein. CTA har baar alag likho (sirf "tag karo" baar-baar nahi): "Save kar lo, baad mein kaam aayega", "Story pe share karo", "Comment mein batao: aapki ray?", ya "Dost ko tag karo jo...". Paisa/exam/job posts par "Save kar lo" best hai (saves reach badhate hain).

Sirf yeh JSON do:
{{
 "pick": <chuni khabar ka index number>,
 "serious": false,
 "tag": "<2-3 shabd, CAPS, jaise DOODH MEHENGA>",
 "line1": "<headline ka chhota hissa, max 22 akshar>",
 "line2": "<sabse bada punch, CAPS, max 12 akshar>",
 "line3": "<headline ka ant, CAPS, max 18 akshar>",
 "sub": "<ek line mein asli khabar, max 60 akshar>",
 "stats": [{{"n": "<number ya chhota fact, max 7 akshar>", "t": "<matlab, max 22 akshar>"}}],  // 2 se 4, sirf text mein diye facts
 "chat": [{{"who": "<BETA/MUMMY/STUDENT/BOSS etc>", "say": "<max 48 akshar>"}}, {{"who": "...", "say": "..."}}],
 "asar_label": "TUMPE ASAR",
 "asar": "<aam aadmi par asar ya funny takeaway, max 52 akshar>",
 "icon": "<ek: milk, money, cricket, film, exam, mic, city, fuel, phone, plane, alert>",
 "caption": "<Instagram caption: hook line, 3-5 emoji bullets mein facts, ek funny line, ek sawaal jisse log comment/tag karein>",
 "hashtags": ["<5 hashtags, aakhri {page_tag} ho>"]
}}

KHABREIN:
{items}
"""


def write(series_name, items, recent_titles):
    key = os.environ["GEMINI_API_KEY"]
    items = items[:MAX_ITEMS_TO_AI]
    listing = "\n".join(
        f"[{i}] {it['title']} | {it['source']} | {it['summary']}" for i, it in enumerate(items)
    )
    prompt = PROMPT.format(
        series=series_name,
        recent="; ".join(recent_titles[-15:]) or "koi nahi",
        page_tag=PAGE_HASHTAG,
        items=listing,
    )
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "responseMimeType": "application/json"},
    }
    text, last_err = None, None
    for model in [GEMINI_MODEL, "gemini-flash-lite-latest", "gemini-flash-latest"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        for attempt in range(2):
            try:
                r = requests.post(url, params={"key": key}, json=body, timeout=240)
                if r.status_code in (404, 400):
                    last_err = f"{model}: {r.status_code} {r.text[:200]}"; break
                r.raise_for_status()
                text = r.json()["candidates"][0]["content"]["parts"][-1]["text"]
                print("AI model used:", model)
                break
            except Exception as e:
                last_err = f"{model}: {e}"
                time.sleep(10)
        if text:
            break
    if not text:
        raise RuntimeError(f"Gemini failed: {last_err}")
    data = json.loads(text)
    if data.get("skip"):
        return None, None
    blob = json.dumps({k: data.get(k) for k in ("line1", "line2", "line3", "sub", "stats", "chat", "asar")}, ensure_ascii=False)
    if any("\u0900" <= ch <= "\u097f" or "\u0a00" <= ch <= "\u0a7f" for ch in blob):  # Devanagari/Gurmukhi glitch: font renders badly, Roman only
        print("AI output had Devanagari/Gurmukhi text: skipping slot"); return None, None
    item = items[int(data["pick"])]
    data["stats"] = (data.get("stats") or [])[:4]
    data["chat"] = (data.get("chat") or [])[:2]
    tags = [t if t.startswith("#") else "#" + t for t in data.get("hashtags", [])][:5]
    if PAGE_HASHTAG not in tags:
        tags = tags[:4] + [PAGE_HASHTAG]
    data["hashtags"] = tags
    data["source_text"] = f"Source: {item['source'] or 'Google News'}"
    return data, item

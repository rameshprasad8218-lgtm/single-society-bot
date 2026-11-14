# Single Society: Auto News Poster Bot

Ye bot roz 14 baar (har ghante, subah 8 se raat 9 baje tak) trending khabar uthata hai, Gemini AI se funny Hinglish poster aur caption likhwata hai, poster banata hai aur Instagram pe post karta hai. Ye GitHub Actions pe chalta hai, poori tarah free.

Dukh wali khabar (maut, hadsa, aparadh) aaye to bot apne aap **serious dark design** use karta hai, usme koi mazaak nahi hota.

---

## Setup (ek baar, ~20 minute)

### Step 1: Gemini API key (free)
1. https://aistudio.google.com/apikey kholo, Google account se login karo
2. **Create API key** dabao, key copy karo
3. Ye key chat mein kisi ko mat bhejna

### Step 2: Instagram token
1. Instagram app mein jaao: Settings → Account type and tools → **Switch to professional account** → **Creator**
2. Computer pe https://developers.facebook.com kholo → **Get Started** (Facebook se login, developer account ban jayega)
3. **My Apps → Create App**, naam `Single Society Bot` rakho
4. Use case mein **"Manage messaging & content on Instagram"** chuno → Create
5. Left menu: **Instagram → API setup with Instagram login**
6. **"Generate access tokens" → Add account** → apna Single Society Instagram login karo → Allow
7. Account ke saamne **Generate token** dabao, lambi token copy karo (ye 60 din chalti hai)
8. Wahin **App roles → Roles** mein khud ko *Instagram Tester* bana do agar maange, phir Instagram app mein Settings → Website permissions → Apps → Tester invite **Accept** karo

### Step 3: Keys GitHub mein daalo
Repo kholo → **Settings → Secrets and variables → Actions → New repository secret**

| Name | Value |
|---|---|
| `GEMINI_API_KEY` | Step 1 wali key |
| `IG_ACCESS_TOKEN` | Step 2 wali token |

### Step 4: Test
1. Repo mein **Actions** tab → agar poochhe to **Enable workflows** dabao
2. **Single Society poster → Run workflow** → `publish` mein `no` likho → Run
3. 2-3 minute baad `posters/` folder mein poster aur caption dikhega
4. Poster theek lage to dobara Run karo `publish = yes` ke saath, Instagram pe post ho jayega

Iske baad bot apne aap roz chalega.

---

## Agar Instagram token nahi daala
Bot phir bhi har slot pe poster + caption (`posters/<date>/*.png` aur `.txt`) bana dega. Tum wahan se download karke khud post kar sakte ho.

## Badlav kaise karein
- Time / series: `bot/config.py` → `SLOTS`, `SERIES`
- Writing ka style aur niyam: `bot/write.py` → `PROMPT`
- Design: `bot/render.py`
- Roz ka record: `data/log.csv`

## Har 50 din pe
Instagram token 60 din mein expire hoti hai. Step 2.7 se nayi token bana ke `IG_ACCESS_TOKEN` secret update kar do.

import os
import html as H
from .config import PAGE_NAME, PAGE_TAGLINE

E = lambda s: H.escape(str(s or ""))

_S = 'stroke="#111" stroke-width="7" stroke-linejoin="round"'
ICONS = {
 "milk": f'<path d="M80 90 L250 90 L268 380 Q165 398 62 380 Z" fill="#fff" {_S}/><path d="M80 90 L110 40 L220 40 L250 90 Z" fill="#fff" {_S}/><path d="M72 200 Q120 175 165 200 T260 200 L268 380 Q165 398 62 380 Z" fill="#2F7BFF" {_S}/><text x="165" y="160" text-anchor="middle" font-weight="800" font-size="46">DOODH</text>',
 "money": f'<circle cx="165" cy="215" r="150" fill="#FFB800" {_S}/><circle cx="165" cy="215" r="112" fill="#FFD84D" {_S}/><text x="165" y="275" text-anchor="middle" font-weight="800" font-size="170">₹</text>',
 "fuel": f'<rect x="70" y="80" width="160" height="290" rx="18" fill="#FF2E3B" {_S}/><rect x="100" y="115" width="100" height="80" rx="8" fill="#fff" {_S}/><path d="M230 140 L275 170 L275 320 Q275 345 252 345" fill="none" {_S}/><rect x="55" y="365" width="190" height="28" rx="8" fill="#111"/>',
 "cricket": f'<rect x="135" y="40" width="58" height="250" rx="26" fill="#F2C58A" {_S} transform="rotate(25 165 200)"/><rect x="150" y="270" width="28" height="100" rx="10" fill="#8B5A2B" {_S} transform="rotate(25 165 200)"/><circle cx="90" cy="320" r="48" fill="#E8262C" {_S}/><path d="M60 300 Q90 320 120 300 M60 340 Q90 320 120 340" fill="none" stroke="#fff" stroke-width="5"/>',
 "film": f'<rect x="40" y="150" width="250" height="210" rx="16" fill="#111" {_S}/><g transform="rotate(-14 40 150)"><rect x="40" y="90" width="250" height="60" rx="8" fill="#fff" {_S}/><path d="M80 90 L60 150 M140 90 L120 150 M200 90 L180 150 M260 90 L240 150" stroke="#111" stroke-width="14"/></g><text x="165" y="285" text-anchor="middle" font-weight="800" font-size="70" fill="#FFD400">ACTION</text>',
 "exam": f'<rect x="20" y="40" width="290" height="340" rx="26" fill="#fff" {_S}/><path d="M20 66 a26 26 0 0 1 26 -26 h238 a26 26 0 0 1 26 26 v60 h-290z" fill="#FF2E3B" {_S}/><text x="165" y="110" text-anchor="middle" font-weight="800" font-size="40" fill="#fff">EXAM</text><path d="M80 200 h170 M80 250 h170 M80 300 h110" stroke="#111" stroke-width="12" stroke-linecap="round"/>',
 "mic": f'<rect x="115" y="40" width="100" height="190" rx="50" fill="#FF2E3B" {_S}/><path d="M80 170 Q80 280 165 280 Q250 280 250 170" fill="none" {_S}/><path d="M165 280 V350 M110 360 H220" {_S} fill="none"/>',
 "city": f'<rect x="30" y="160" width="90" height="220" fill="#2F7BFF" {_S}/><rect x="120" y="70" width="100" height="310" fill="#fff" {_S}/><rect x="220" y="200" width="80" height="180" fill="#FF2E3B" {_S}/><path d="M150 110 h40 M150 160 h40 M150 210 h40 M150 260 h40" stroke="#111" stroke-width="12"/>',
 "phone": f'<rect x="85" y="30" width="160" height="350" rx="30" fill="#111" {_S}/><rect x="103" y="70" width="124" height="250" rx="10" fill="#2F7BFF"/><circle cx="165" cy="350" r="12" fill="#fff"/>',
 "alert": f'<path d="M165 40 L310 360 H20 Z" fill="#FFD400" {_S}/><rect x="150" y="140" width="30" height="130" rx="12" fill="#111"/><circle cx="165" cy="315" r="20" fill="#111"/>',
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Poppins',sans-serif;overflow:hidden;position:relative;background:var(--bg);color:var(--ink)}
.dots{position:absolute;inset:0;background-image:radial-gradient(var(--dot) 2.2px,transparent 2.4px);background-size:26px 26px}
.top,.foot{position:absolute;left:0;right:0;height:96px;background:#111;display:flex;align-items:center;justify-content:space-between;padding:0 54px;color:#fff}
.top{top:0}.foot{bottom:0;font-size:24px}
.brand{color:var(--acc);font-weight:800;font-size:34px;letter-spacing:2px}
.live{display:flex;align-items:center;gap:12px;font-weight:700;font-size:24px;letter-spacing:3px}
.live i{width:16px;height:16px;border-radius:50%;background:#FF2E3B;box-shadow:0 0 0 6px rgba(255,46,59,.3)}
.tag{position:absolute;top:140px;left:54px;background:#FF2E3B;color:#fff;font-weight:800;font-size:26px;letter-spacing:4px;padding:12px 24px;transform:rotate(-2deg);box-shadow:6px 6px 0 #111}
.head{position:absolute;top:220px;left:54px;width:650px;font-weight:800;line-height:1.05;letter-spacing:-1.5px}
.head div{white-space:nowrap}[data-fit]{display:inline-block;white-space:nowrap}
.l1{font-size:62px}
.l2{font-size:104px;color:#fff;-webkit-text-stroke:4px #111;paint-order:stroke fill;text-shadow:7px 7px 0 #111}
.l3{font-size:62px;margin-top:8px}.l3 b{background:#111;color:var(--acc);padding:0 14px}
.icon{position:absolute;top:160px;right:60px;width:300px;transform:rotate(5deg)}
.sub{position:absolute;top:585px;left:54px;right:54px;font-size:34px;font-weight:700;white-space:nowrap}
.stats{position:absolute;top:665px;left:54px;right:54px;display:flex;gap:18px}
.st{flex:1;background:#fff;color:#111;border:4px solid #111;box-shadow:7px 7px 0 #111;padding:20px 12px;text-align:center;border-radius:14px}
.st .n{font-size:44px;font-weight:800;line-height:1;white-space:nowrap}
.st .t{font-size:19px;font-weight:600;margin-top:8px;color:#333;line-height:1.2}
.st:first-child{background:#FF2E3B;color:#fff}.st:first-child .t{color:#fff}
.chat{position:absolute;top:850px;left:54px;right:54px}
.b{font-size:28px;font-weight:600;padding:14px 26px;border-radius:26px;border:4px solid #111;max-width:820px;margin-bottom:14px;line-height:1.25}
.b small{display:block;font-size:20px;font-weight:800;letter-spacing:2px;margin-bottom:4px;opacity:.7}
.b1{background:#fff;color:#111;border-bottom-left-radius:4px}
.b2{background:#111;color:#fff;margin-left:auto;border-bottom-right-radius:4px}.b2 small{color:var(--acc);opacity:1}
.foot b{color:var(--acc);font-weight:800;font-size:28px}.src{font-size:20px;opacity:.75}
/* serious */
.serious .l2{color:var(--acc);-webkit-text-stroke:0;text-shadow:none}
.serious .tag{background:#fff;color:#111;box-shadow:none;transform:none}
.serious .st{background:#1d1d1d;color:#fff;border-color:#444;box-shadow:none}.serious .st .t{color:#ccc}
.serious .st:first-child{background:#fff;color:#111}.serious .st:first-child .t{color:#333}
.serious .b1{background:#1d1d1d;color:#fff;border-color:#444}
"""




def build_html(d):
    serious = bool(d.get("serious"))
    theme = ("--bg:#121212;--ink:#fff;--acc:#FFD400;--dot:rgba(255,255,255,.05)" if serious
             else "--bg:#FFD400;--ink:#111;--acc:#FFD400;--dot:rgba(0,0,0,.09)")
    stats = "".join(
        f'<div class="st"><div class="n" data-fit>{E(s.get("n"))}</div><div class="t">{E(s.get("t"))}</div></div>'
        for s in d.get("stats", [])
    )
    bubbles = ""
    if not serious:
        for i, c in enumerate(d.get("chat", [])):
            bubbles += f'<div class="b {"b1" if i % 2 == 0 else "b2"}"><small>{E(c.get("who"))}</small>"{E(c.get("say"))}"</div>'
    if d.get("asar"):
        bubbles += f'<div class="b b1"><small>{E(d.get("asar_label") or "TUMPE ASAR")}</small>{E(d["asar"])}</div>'
    icon = ICONS.get(d.get("icon"), ICONS["alert"])
    chat_top = 850 if not serious else 870
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body class="{'serious' if serious else 'fun'}" style="{theme}">
<div class="dots"></div>
<div class="top"><div class="brand">{E(PAGE_NAME)}</div><div class="live"><i></i>{'UPDATE' if serious else 'BREAKING'}</div></div>
<div class="tag">{E(d.get('tag'))}</div>
<div class="head"><div class="l1"><span data-fit="640">{E(d.get('line1'))}</span></div><div class="l2"><span data-fit="640">{E(d.get('line2'))}</span></div><div class="l3"><b data-fit="620">{E(d.get('line3'))}</b></div></div>
<svg class="icon" viewBox="0 0 330 400" font-family="Poppins">{icon}</svg>
<div class="sub"><span data-fit="972">{E(d.get('sub'))}</span></div>
<div class="stats">{stats}</div>
<div class="chat" style="top:{chat_top}px">{bubbles}</div>
<div class="foot"><div><b>Follow karo</b> &nbsp;{E(PAGE_TAGLINE)}</div><div class="src">{E(d.get('source_text'))}</div></div>
</body></html>"""


def render(d, out_png):
    from playwright.sync_api import sync_playwright
    html = build_html(d)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.getenv("CHROME_PATH") or None)
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.set_content(html, wait_until="networkidle")
        pg.wait_for_timeout(600)
        pg.evaluate("""document.querySelectorAll('[data-fit]').forEach(el=>{
  const max = el.dataset.fit ? +el.dataset.fit : el.closest('.st').clientWidth-24;
  let fs = parseFloat(getComputedStyle(el).fontSize);
  while (el.getBoundingClientRect().width > max && fs > 14) { fs -= 2; el.style.fontSize = fs + 'px'; }
})""")
        pg.screenshot(path=out_png)
        b.close()
    return html

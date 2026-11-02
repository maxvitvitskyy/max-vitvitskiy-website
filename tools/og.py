#!/usr/bin/env python3
"""Render a 1200x630 OG card for every work in data/works.json -> img/works/<slug>/og.jpg.

Left: the artwork at 4:5, as large as the card allows. Right: wordmark, title, one-line subject,
key specs, price from, and an "on sale" badge. Rendered with headless Chrome in the site's own fonts.

Run from the repo root:  python3 tools/og.py [slug ...]
"""
import html, json, os, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
e = lambda t: html.escape(str(t), quote=True)
U = lambda p: 'file://' + os.path.join(ROOT, p)

CSS = '''
@font-face{font-family:"Moniqa";src:url("%(f)s/Moniqa-MediumDisplay.woff2")}
@font-face{font-family:"Moniqa Head";src:url("%(f)s/Moniqa-MediumHeading.woff2")}
@font-face{font-family:"Raleway";src:url("%(f)s/Raleway-cyrillic.woff2");unicode-range:U+0400-045F,U+0490-0491,U+2116}
@font-face{font-family:"Raleway";src:url("%(f)s/Raleway-latin.woff2");unicode-range:U+0000-00FF,U+2000-206F,U+20AC,U+2122,U+2190-21FF,U+00D7}
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;position:relative;color:#F1E0C5;font-family:"Raleway",sans-serif;
  background:radial-gradient(70%% 90%% at 22%% 50%%,rgba(255,166,48,.16),transparent 70%%),#0d0d0c}
.art{position:absolute;left:44px;top:40px;width:440px;height:550px;border-radius:6px;overflow:hidden;
  box-shadow:0 30px 70px rgba(0,0,0,.65),0 0 0 1px rgba(241,224,197,.08)}
.art img{width:100%%;height:100%%;object-fit:cover;display:block}
.tx{position:absolute;left:548px;right:56px;top:52px;bottom:48px;display:flex;flex-direction:column}
.logo{height:26px;width:auto;align-self:flex-start;opacity:.95}
h1{font-family:"Moniqa Head","Moniqa",serif;font-weight:400;text-transform:uppercase;line-height:.98;letter-spacing:.01em;
  margin-top:auto;font-size:%(fs)dpx;text-wrap:balance}
.sub{margin-top:16px;font-size:21px;line-height:1.4;color:rgba(241,224,197,.72);text-wrap:balance}
ul{list-style:none;margin-top:26px;display:flex;flex-direction:column;gap:9px;font-size:18px;letter-spacing:.02em;color:rgba(241,224,197,.86)}
li{display:flex;gap:12px;align-items:center}li::before{content:"";width:18px;height:1px;background:#FFA630}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:18px}
.badge{display:inline-flex;align-items:center;gap:10px;height:46px;padding:0 22px;border-radius:99px;background:#FFA630;color:#01110A;
  font-size:15px;font-weight:500;letter-spacing:.16em;text-transform:uppercase}
.badge i{width:8px;height:8px;border-radius:50%%;background:#01110A}
.pr{font-family:"Moniqa",serif;font-size:34px;color:#F1E0C5}.pr small{font-family:"Raleway",sans-serif;font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:rgba(241,224,197,.6);margin-right:10px}
'''


def card(w):
    t = w['title']
    fs = 66 if len(t) <= 16 else 56 if len(t) <= 24 else 48
    prices = [v for z in w['sizes'] for x in z['p'].values() for v in (x.values() if isinstance(x, dict) else [x])]
    sub = w.get('seo') or ''
    sub = sub[:1].upper() + sub[1:]
    year = f' · {w["year"]}' if w.get('year') else ''
    return f'''<!doctype html><meta charset="utf-8"><style>{CSS % {"f": U("fonts"), "fs": fs}}</style>
<div class="art"><img src="{U(w['imgs'][0])}"></div>
<div class="tx">
  <img class="logo" src="{U('img/wordmark.svg')}">
  <h1>{e(t)}</h1>
  <p class="sub">{e(sub)}</p>
  <ul><li>Музейне полотно · тираж 10{year}</li><li>40×60 — 80×120 см, рама з масиву</li><li>Підпис і сертифікат автентичності</li></ul>
  <div class="foot"><span class="badge"><i></i>У продажу</span><span class="pr"><small>від</small>${min(prices):,}</span></div>
</div>'''


def main():
    W = json.load(open(os.path.join(ROOT, 'data/works.json'), encoding='utf-8'))
    only = set(sys.argv[1:])
    with tempfile.TemporaryDirectory() as tmp:
        for w in W:
            if not w.get('slug') or (only and w['slug'] not in only) or not w.get('sizes'):
                continue
            src = os.path.join(tmp, w['slug'] + '.html')
            png = os.path.join(tmp, w['slug'] + '.png')
            open(src, 'w', encoding='utf-8').write(card(w))
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                            '--force-device-scale-factor=1', '--window-size=1200,630', '--virtual-time-budget=3000',
                            f'--screenshot={png}', 'file://' + src], check=True, capture_output=True)
            out = os.path.join(ROOT, 'img/works', w['slug'], 'og.jpg')
            Image.open(png).convert('RGB').crop((0, 0, 1200, 630)).save(out, 'JPEG', quality=86, optimize=True, progressive=True)
            print(w['slug'], flush=True)


if __name__ == '__main__':
    main()

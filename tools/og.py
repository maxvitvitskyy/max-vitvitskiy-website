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
@font-face{font-family:"BazaART";src:url("%(f)s/BazaART.woff2")}
@font-face{font-family:"Moniqa Head";src:url("%(f)s/Moniqa-MediumHeading.woff2")}
@font-face{font-family:"Raleway";src:url("%(f)s/Raleway-cyrillic.woff2");unicode-range:U+0400-045F,U+0490-0491,U+2116}
@font-face{font-family:"Raleway";src:url("%(f)s/Raleway-latin.woff2");unicode-range:U+0000-00FF,U+2000-206F,U+20AC,U+2122,U+2190-21FF,U+00D7}
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;position:relative;color:#F1E0C5;font-family:"Raleway",sans-serif;
  background:radial-gradient(70%% 90%% at 22%% 50%%,rgba(255,166,48,.16),transparent 70%%),#0d0d0c}
/* thin black frame: a black moulding with a faint lit edge so it reads on the dark ground */
.art{position:absolute;left:44px;top:40px;width:440px;height:550px;padding:9px;background:linear-gradient(145deg,#1d1c1a,#050505 55%%,#111);
  box-shadow:0 30px 70px rgba(0,0,0,.7),0 0 0 1px rgba(241,224,197,.14),inset 0 0 0 1px rgba(255,255,255,.05)}
.art img{width:100%%;height:100%%;object-fit:cover;display:block;box-shadow:inset 0 0 0 1px rgba(0,0,0,.6)}
.word{font-family:"BazaART","Moniqa",serif;font-weight:400;font-size:46px;line-height:.9;white-space:nowrap;padding:.04em .04em .14em;
  color:#FAA719}
.mark{position:absolute;top:40px;right:56px;height:36px;width:auto}
.tx{position:absolute;left:540px;right:56px;top:40px;bottom:40px;display:flex;flex-direction:column;text-align:left}
.body{margin:88px 0 auto}
h1{font-family:"Moniqa Head","Moniqa",serif;font-weight:400;text-transform:uppercase;line-height:.98;letter-spacing:.01em;font-size:%(fs)dpx;text-wrap:balance}
.sub{margin-top:18px;font-size:20px;line-height:1.45;color:rgba(241,224,197,.78);text-wrap:pretty;max-width:560px}
ul{list-style:none;padding:0;margin-top:26px;display:flex;flex-direction:column;gap:11px;font-size:18px;letter-spacing:.01em;color:rgba(241,224,197,.9)}
li{display:flex;gap:12px;align-items:center}
li svg{flex:none;width:20px;height:20px}
.foot{display:flex;align-items:center;justify-content:space-between;gap:22px}
.badge{display:inline-flex;align-items:center;gap:10px;height:46px;padding:0 22px;border-radius:99px;background:#FFA630;color:#01110A;
  font-size:15px;font-weight:500;letter-spacing:.16em;text-transform:uppercase}
.badge i{width:8px;height:8px;border-radius:50%%;background:#01110A}
.ed{font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:rgba(241,224,197,.75)}.ed b{font-family:"Moniqa",serif;font-weight:400;font-size:30px;letter-spacing:0;color:#F1E0C5;margin:0 9px;vertical-align:-3px}
'''

CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="9.25" fill="none" stroke="#FFA630" stroke-opacity=".55" stroke-width="1.2"/><path d="M6 10.4l2.6 2.6L14.2 7.3" fill="none" stroke="#FFA630" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def card(w):
    t = w['title']
    fs = 66 if len(t) <= 16 else 56 if len(t) <= 24 else 48
    sub = w.get('meaning') or w.get('seo') or ''
    sub = sub[:1].upper() + sub[1:]
    year = f' · {w["year"]}' if w.get('year') else ''
    items = ['Тираж 10 примірників', f'Музейне полотно, архівні чорнила{year}', '40×60 — 80×120 см, рама з масиву дерева', 'Підпис і сертифікат автентичності']
    lis = ''.join(f'<li>{CHECK}{e(x)}</li>' for x in items)
    return f'''<!doctype html><meta charset="utf-8"><style>{CSS % {"f": U("fonts"), "fs": fs}}</style>
<div class="art"><img src="{U(w['imgs'][0])}"></div>
<img class="mark" src="{U('img/logo-mark.png')}">
<div class="tx">
  <div class="body"><h1>{e(t)}</h1><p class="sub">{e(sub)}</p><ul>{lis}</ul></div>
  <div class="foot"><span class="badge"><i></i>У продажу</span><span class="word">Max Vitvitskiy</span></div>
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

#!/usr/bin/env python3
"""Build the gallery from data/works.json.

- works.html: refreshes the W data, the catalog cards and the JSON-LD
- works/<slug>/index.html: a static, indexable page for every work that has a slug
- sitemap.xml: home, catalog and every work page with its images

Run from the repo root:  python3 tools/build.py
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://maxvitvitskyy.github.io/max-vitvitskiy-website/'
CAT = 'works.html'


def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()


def write(p, s):
    p = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def e(t):
    return html.escape(str(t), quote=True)


def strip(t):
    return re.sub(r'<[^>]+>', '', t)


def prices(w):
    out = []
    for z in w['sizes']:
        for v in z['p'].values():
            out += list(v.values()) if isinstance(v, dict) else [v]
    return out


def tags(w):
    return [t for b in w.get('info', []) if b.get('tags') for t in b['tags']]


def ld(w):
    pr = prices(w)
    return {
        '@type': 'VisualArtwork', 'name': w['title'], 'url': SITE + 'works/' + w['slug'] + '/',
        'creator': {'@type': 'Person', 'name': 'Max Vitvitskiy', 'url': SITE},
        'artform': 'Digital painting', 'artMedium': 'Canvas print', 'artEdition': '10',
        'image': [SITE + x for x in w['imgs']], 'inLanguage': 'uk',
        'description': w['lead'] + ' ' + ' '.join(strip(p) for p in w['story']),
        'keywords': ', '.join(tags(w)),
        'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'USD', 'lowPrice': min(pr), 'highPrice': max(pr),
                   'offerCount': len(pr), 'availability': 'https://schema.org/LimitedAvailability'},
    }


def card(i, w):
    alt = (w.get('alts') or [''])[0]
    sold = '1' if w['status'] == 'Продана' else '0'
    st = '<span class="st sold">' if sold == '1' else '<span class="st">'
    inner = (f'\n      <span class="ph"><img src="{e(w["img"])}" alt="{e(alt)}" width="840" height="1050" loading="{"eager" if i < 3 else "lazy"}"></span>'
             f'\n      <span class="cap"><span class="row"><span class="ttl">{e(w["title"])}</span><span class="n">{w["n"]:02d}</span></span>'
             f'<span class="row">{st}{e(w["status"])}</span><span class="ed">{e(w["edition"])}</span></span></span>\n    ')
    attrs = f'data-i="{i}" data-cat="{e(w["cat"])}" data-sold="{sold}" aria-label="{e(w["title"])}"'
    if w.get('slug'):
        return f'    <a class="w" href="works/{w["slug"]}/" {attrs}>{inner}</a>'
    return f'    <button class="w" type="button" {attrs}>{inner}</button>'


def dialog(w, n, total):
    """Pre-rendered work view, identical to what the catalog's JS draws, so the page reads without JS."""
    thumbs = ''.join(f'<button type="button" data-src="{e(s)}" aria-label="Варіація {k + 1}"{" aria-current=\"true\"" if k == 0 else ""}><img src="{e(s)}" alt=""></button>'
                     for k, s in enumerate(w['imgs']))
    desc = ('<p>' + e(w['lead']) + '</p>' if w.get('lead') else '') + ''.join('<p>' + p + '</p>' for p in w['story'])
    opts = lambda xs: ''.join(f'<option value="{e(x["id"])}">{e(x["label"])}</option>' for x in xs)
    fin = next(f for f in w['fins'] if f['id'] == 'framed')
    p0 = w['sizes'][0]['p']['framed'][w['frames'][0]['id']]
    info = ''.join('<details><summary>' + e(b['t']) + '</summary>'
                   + ('<ul class="tags">' + ''.join('<li>' + e(t) + '</li>' for t in b['tags']) + '</ul>' if b.get('tags') else '')
                   + ('<ul>' + ''.join('<li>' + e(t) + '</li>' for t in b['l']) + '</ul>' if b.get('l') else '')
                   + '</details>' for b in w.get('info', []))
    sold = ' sold' if w['status'] == 'Продана' else ''
    return f'''<div class="dv open solo" id="dv" aria-labelledby="dv-t">
  <button class="x" type="button" aria-label="До каталогу"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <div class="art"><div class="stage"><button class="nav prev" type="button" aria-label="Попередній кадр"><i class="ar" aria-hidden="true"></i></button><img class="main" src="{e(w['imgs'][0])}" alt="{e(w['alts'][0])}" width="1600" height="1600"><button class="nav next" type="button" aria-label="Наступний кадр"><i class="ar" aria-hidden="true"></i></button></div><div class="thumbs" role="group" aria-label="Кадри роботи">{thumbs}</div></div>
  <div class="tx">
    <div class="wn"><button class="wb wp" type="button" aria-label="Попередня робота"><i class="ar" aria-hidden="true"></i></button><span class="count">{n} / {total}</span><button class="wb wx" type="button" aria-label="Наступна робота"><i class="ar" aria-hidden="true"></i></button></div>
    <h1 id="dv-t">{e(w['title'])}</h1>
    <p class="meta"><span class="st-v{sold}">{e(w['status'])}</span><span class="sep" aria-hidden="true"></span><span class="ed-v">{e(w['edition'])}</span></p>
    <div class="dsc"><div class="desc">{desc}</div><button class="rm" type="button" aria-expanded="false">Читати повністю</button></div>
    <form class="cf" onsubmit="return false">
      <label>Розмір<select id="cf-size">{opts(w['sizes'])}</select></label>
      <label>Виконання<select id="cf-fin">{opts(w['fins'])}</select></label>
      <label class="fr">Колір рами<select id="cf-frame">{opts(w['frames'])}</select></label>
    </form>
    <div class="buy"><div class="pr"><span class="pv">${p0:,}</span><small class="pn">{e(fin['note'])} Ціна в USD, без доставки.</small></div><a class="ask" href="mailto:hello@maxvitvitskiy.com?subject={e('Artwork: ' + w['title'])}">Запитати про роботу<i class="ar" aria-hidden="true"></i></a></div>
    <dl><dt>Техніка</dt><dd>Фотографія, цифрова композиція</dd><dt>Документи</dt><dd>Сертифікат автентичності</dd></dl>
    <div class="inf">{info}</div>
  </div>
</div>'''


def page(src, w, i, n, total):
    style = re.search(r'<style>.*?</style>', src, re.S).group(0)
    script = re.search(r'\n<script>\n.*?</script>', src, re.S).group(0)
    url = SITE + 'works/' + w['slug'] + '/'
    title = f'{w["title"]} — Max Vitvitskiy'
    desc = w['lead']
    og = SITE + w['imgs'][0]
    head = f'''<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<base href="../../">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(', '.join(tags(w)))}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0d0d0c">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="product">
<meta property="og:site_name" content="Max Vitvitskiy">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1600">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
<link rel="apple-touch-icon" href="img/icon-180.png">
<script type="application/ld+json">{json.dumps({'@context': 'https://schema.org', **ld(w)}, ensure_ascii=False)}</script>
{style}
</head>
<body>
'''
    return head + dialog(w, n, total) + f'\n<script>window.SOLO={i};</script>' + script.replace('\n<script>\n', '\n<script>\n', 1) + '\n</body>\n</html>\n'


def main():
    W = json.loads(read('data/works.json'))
    src = read(CAT)
    # data the catalog's JS reads (pages keep their own copy via the same script)
    src = re.sub(r'^const W=\[.*?\];\n', lambda m: 'const W=' + json.dumps(W, ensure_ascii=False) + ';\n', src, count=1, flags=re.M | re.S)
    # catalog cards
    cards = '\n'.join(card(i, w) for i, w in enumerate(W))
    src = re.sub(r'(<div class="wall">\n).*?(\n  </div>\n</main>)', lambda m: m.group(1) + cards + m.group(2), src, count=1, flags=re.S)
    # catalog structured data
    graph = [ld(w) for w in W if w.get('slug')]
    src = re.sub(r'<script type="application/ld\+json">.*?</script>',
                 lambda m: '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>',
                 src, count=1, flags=re.S)
    write(CAT, src)

    real = [i for i, w in enumerate(W) if w.get('slug')]
    for k, i in enumerate(real):
        write(f'works/{W[i]["slug"]}/index.html', page(src, W[i], i, k + 1, len(real)))

    # the catalog stays noindex while it still holds placeholder cards, so it is not listed
    urls = [(SITE, [])] + [(SITE + 'works/' + W[i]['slug'] + '/', [SITE + x for x in W[i]['imgs']]) for i in real]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u, ims in urls:
        sm.append('  <url><loc>' + e(u) + '</loc>' + ''.join('<image:image><image:loc>' + e(x) + '</image:loc></image:image>' for x in ims) + '</url>')
    sm.append('</urlset>\n')
    write('sitemap.xml', '\n'.join(sm))
    print(f'catalog: {len(W)} cards, pages: {len(real)}, sitemap: {len(urls)} urls')


if __name__ == '__main__':
    main()

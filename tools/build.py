#!/usr/bin/env python3
"""Build the gallery from data/works.json.

- works.html: refreshes the W data, the catalog cards and the JSON-LD
- works/<slug>/index.html: a static, indexable page for every work that has a slug
- sitemap.xml: home, catalog and every work page with its images

Run from the repo root:  python3 tools/build.py
"""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://maxvitvitskiy.com/'
CAT = 'works.html'
# catalog filters: (id, label), in display order; a work lists its ids in "themes" (data/works.json)
THEMES = [('portraits', 'Портрети'), ('animals', 'Тварини'), ('birds', 'Птахи'), ('butterflies', 'Метелики'), ('flowers', 'Квіти'), ('ocean', 'Океан'),
          ('faith', 'Віра'), ('ukraine', 'Україна'), ('love', 'Любов'), ('self', 'Самопізнання'), ('transformation', 'Перетворення')]
# Google Analytics 4 (enhanced measurement counts the catalog's pushState work views as page views)
GA = ('<script async src="https://www.googletagmanager.com/gtag/js?id=G-0TL5BZW0QP"></script>\n'
      '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag(\'js\',new Date());gtag(\'config\',\'G-0TL5BZW0QP\');</script>\n')


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


def ver(p):
    """image path with a content hash, so a replaced cover is never served from a stale cache"""
    import hashlib
    try:
        with open(os.path.join(ROOT, p), 'rb') as f:
            return p + '?v=' + hashlib.md5(f.read()).hexdigest()[:8]
    except OSError:
        return p


def thumb(s):
    return re.sub(r'/(\d)\.jpg$', r'/t\1.jpg', s)


def clip(t, n=158):
    t = strip(t)
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0].rstrip(',;:—–-') + '…'


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


def purl(w, lang='uk'):
    return SITE + ('en/' if lang == 'en' else '') + 'works/' + w['slug'] + '/'


def ld(w, lang='uk'):
    pr = prices(w)
    return {
        '@type': 'VisualArtwork', 'name': w['title'], 'url': purl(w, lang),
        'creator': {'@type': 'Person', 'name': 'Max Vitvitskiy', 'url': SITE},
        'artform': 'Digital painting', 'artMedium': 'Canvas print', 'artEdition': '10',
        'image': [SITE + x for x in w['imgs']], 'thumbnailUrl': SITE + w['img'], 'inLanguage': lang,
        **({'dateCreated': str(w['year'])} if w.get('year') else {}),
        'description': w['lead'] + ' ' + ' '.join(strip(p) for p in w['story']),
        'keywords': ', '.join(tags(w)),
        'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'USD', 'lowPrice': min(pr), 'highPrice': max(pr),
                   'offerCount': len(pr), 'availability': 'https://schema.org/LimitedAvailability', 'url': purl(w, lang)},
    }


def card(i, w, lang='uk'):
    alt = w.get('cardAlt') or (w.get('alts') or [''])[0]
    sold = '1' if w['status'] in ('Продана', 'Sold') else '0'
    st = '<span class="st sold">' if sold == '1' else '<span class="st">'
    inner = (f'\n      <span class="ph"><img src="{e(ver(w["img"]))}" alt="{e(alt)}" width="840" height="1050" loading="{"eager" if i < 3 else "lazy"}"></span>'
             f'\n      <span class="cap"><span class="row"><span class="ttl">{e(w["title"])}</span><span class="n">{w["n"]:03d}</span></span>'
             f'<span class="row">{st}{e(w["status"])}</span><span class="ed">{e(w["edition"])}</span></span></span>\n    ')
    attrs = f'data-i="{i}" data-cat="{e(' '.join(w['themes']))}" data-sold="{sold}" aria-label="{e(w["title"])}"'
    if w.get('slug'):
        return f'    <a class="w" href="{"en/" if lang == "en" else ""}works/{w["slug"]}/" {attrs}>{inner}</a>'
    return f'    <button class="w" type="button" {attrs}>{inner}</button>'


THEME_LABELS = {'uk': dict(THEMES), 'en': i18n.THEMES_EN}


def tr_static(h, lang):
    """Ukrainian static markup -> English (the dialog pre-render shares the catalog's UI strings)"""
    if lang != 'en':
        return h
    for ua, en in i18n.UI:
        h = h.replace(ua, en)
    h = h.replace(' Ціна в USD, без доставки.', ' Price in USD, shipping not included.').replace('aria-label="До каталогу"', 'aria-label="To the gallery"')
    h = h.replace('<label class="fr">Колір рами', '<label class="fr">Frame colour')
    return re.sub(r'aria-label="Кадр (\d+)"', r'aria-label="Frame \1"', h)


def dialog(w, n, total, lang='uk', W=None):
    """Pre-rendered work view, identical to what the catalog's JS draws, so the page reads without JS."""
    thumbs = ''.join(f'<button type="button" data-src="{e(s)}" aria-label="Кадр {k + 1}"{" aria-current=\"true\"" if k == 0 else ""}><img src="{e(thumb(s))}" alt="" loading="lazy"></button>'
                     for k, s in enumerate(w['imgs']))
    desc = ('<p>' + e(w['lead']) + '</p>' if w.get('lead') else '') + ''.join('<p>' + p + '</p>' for p in w['story'])
    opts = lambda xs: ''.join(f'<option value="{e(x["id"])}">{e(x["label"])}</option>' for x in xs)
    fin = next(f for f in w['fins'] if f['id'] == 'framed')
    p0 = w['sizes'][0]['p']['framed'][w['frames'][0]['id']]
    info = ''.join('<details><summary>' + e(b['t']) + '</summary>'
                   + ('<ul class="tags">' + ''.join('<li>' + e(t) + '</li>' for t in b['tags']) + '</ul>' if b.get('tags') else '')
                   + ('<ul>' + ''.join('<li>' + e(t) + '</li>' for t in b['l']) + '</ul>' if b.get('l') else '')
                   + '</details>' for b in w.get('info', []))
    sold = ' sold' if w['status'] in ('Продана', 'Sold') else ''
    en = lang == 'en'
    pre = 'en/' if en else ''
    other = (SITE + 'works/' + w['slug'] + '/') if en else (SITE + 'en/works/' + w['slug'] + '/')
    lng = f'<a class="lng" href="{"works" if en else "en/works"}/{w["slug"]}/" hreflang="{"uk" if en else "en"}" lang="{"uk" if en else "en"}">{"UA" if en else "EN"}</a>'
    thl = THEME_LABELS[lang]
    themes = ('<nav class="th" aria-label="' + ('Themes' if en else 'Теми') + '"><span>' + ('Themes' if en else 'Теми') + '</span>'
              + ''.join(f'<a href="{pre}works{"/" if en else ".html"}#cat-{t}">{e(thl[t])}</a>' for t in w['themes']) + '</nav>')
    rel = ''
    if W is not None and w.get('rel'):
        rel = ('<nav class="rel" aria-labelledby="rel-t"><h2 id="rel-t">' + ('Related works' if en else 'Схожі роботи') + '</h2><div class="rg">'
               + ''.join(f'<a href="{pre}works/{W[k]["slug"]}/"><img src="{e(thumb(W[k]["imgs"][0]))}" alt="{e(W[k]["alts"][0])}" width="320" height="400" loading="lazy"><span>{e(W[k]["title"])}</span></a>' for k in w['rel'])
              + '</div></nav>')
    out = f'''<div class="dv open solo" id="dv" aria-labelledby="dv-t">
  <button class="x" type="button" aria-label="До каталогу"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <div class="art"><div class="stage"><button class="nav prev" type="button" aria-label="Попередній кадр"><i class="ar" aria-hidden="true"></i></button><img class="main" src="{e(w['imgs'][0])}" alt="{e(w['alts'][0])}" width="1280" height="1600"><button class="nav next" type="button" aria-label="Наступний кадр"><i class="ar" aria-hidden="true"></i></button></div><div class="thumbs" role="group" aria-label="Кадри роботи"{" hidden" if len(w['imgs']) < 2 else ""}>{thumbs}</div></div>
  <div class="tx">
    <div class="wn"><button class="wb wp" type="button" aria-label="Попередня робота"><i class="ar" aria-hidden="true"></i></button><span class="count">{n} / {total}</span><button class="wb wx" type="button" aria-label="Наступна робота"><i class="ar" aria-hidden="true"></i></button>{lng}</div>
    <h1 id="dv-t">{e(w['title'])}</h1>
    <p class="meta"><span class="st-v{sold}">{e(w['status'])}</span><span class="sep" aria-hidden="true"></span><span class="ed-v">{e(w['edition'])}</span></p>
    <div class="dsc"><div class="desc">{desc}</div><button class="rm" type="button" aria-expanded="false">Читати повністю</button></div>
    <form class="cf" onsubmit="return false">
      <label>Розмір<select id="cf-size">{opts(w['sizes'])}</select></label>
      <label>Виконання<select id="cf-fin">{opts(w['fins'])}</select></label>
      <label class="fr">Колір рами<select id="cf-frame">{opts(w['frames'])}</select></label>
    </form>
    <div class="buy"><div class="pr"><span class="pv">${p0:,}</span><small class="pn">{e(fin['note'])} Ціна в USD, без доставки.</small></div><a class="ask" href="mailto:maxim.vitvitskiy@gmail.com?subject={e('Artwork: ' + w['title'])}">Запитати про роботу<i class="ar" aria-hidden="true"></i></a></div>
    <dl><dt>Техніка</dt><dd>Фотографія, цифрова композиція</dd><dt>Документи</dt><dd>Сертифікат автентичності</dd></dl>
    <div class="inf">{info}</div>
    <div id="tn">{themes}{rel}</div>
  </div>
</div>'''
    return tr_static(out, lang)


def alternates(path_uk, path_en):
    return (f'<link rel="alternate" hreflang="uk" href="{SITE}{path_uk}">\n<link rel="alternate" hreflang="en" href="{SITE}{path_en}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{SITE}{path_uk}">\n')


def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': k + 1, 'name': n, 'item': u} for k, (n, u) in enumerate(items)]}


def lang_script(lang):
    return "<script>try{localStorage.setItem('lang','" + lang + "')}catch(e){}</script>\n"


def page(src, w, i, n, total, lang='uk', W=None):
    en = lang == 'en'
    style = re.search(r'<style>.*?</style>', src, re.S).group(0)
    script = re.search(r'\n<script>\n.*?</script>', src, re.S).group(0)
    path = ('en/' if en else '') + 'works/' + w['slug'] + '/'
    url = SITE + path
    if en:
        title = f'{w["title"]} — Surreal Wall Art Print | Max Vitvitskiy'
        ogalt = f'{w["title"]} — {w["seo"]}; artwork by Max Vitvitskiy, edition of 10, available'
        og = SITE + f'img/works/{w["slug"]}/og-en.jpg'
    else:
        title = f'{w["title"]} — сюрреалістична картина | Max Vitvitskiy'
        ogalt = f'{w["title"]} — картина Max Vitvitskiy, тираж 10, у продажу'
        og = SITE + (w.get('og') or w['imgs'][0])
    desc = clip(w['lead'])
    cat_url = SITE + ('en/works/' if en else 'works.html')
    graph = [{'@context': 'https://schema.org', **ld(w, lang)},
             {'@context': 'https://schema.org', **crumbs([('Home', SITE + ('en/' if en else '')), ('Gallery' if en else 'Галерея', cat_url), (w['title'], url)])}]
    head = (f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<base href="{"../../../" if en else "../../"}">\n<title>{e(title)}</title>\n'
            f'<meta name="description" content="{e(desc)}">\n<meta name="keywords" content="{e(", ".join(tags(w)))}">\n'
            f'<link rel="canonical" href="{url}">\n{alternates("works/" + w["slug"] + "/", "en/works/" + w["slug"] + "/")}{GA}'
            '<meta name="theme-color" content="#0d0d0c">\n<meta name="color-scheme" content="dark">\n'
            '<meta property="og:type" content="product">\n<meta property="og:site_name" content="Max Vitvitskiy">\n'
            f'<meta property="og:locale" content="{"en_US" if en else "uk_UA"}">\n<meta property="og:locale:alternate" content="{"uk_UA" if en else "en_US"}">\n'
            f'<meta property="og:title" content="{e(title)}">\n<meta property="og:description" content="{e(desc)}">\n'
            f'<meta property="og:image" content="{og}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{e(ogalt)}">\n<meta property="og:url" content="{url}">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">\n<link rel="apple-touch-icon" href="img/icon-180.png">\n'
            f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>\n{lang_script(lang)}{style}\n</head>\n<body>\n')
    return head + dialog(w, n, total, lang, W) + f'\n<script>window.SOLO={i};</script>' + script + '\n</body>\n</html>\n'


from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class _Spans(HTMLParser):
    """finds elements carrying data-uk: (start-tag start, inner start, inner end)"""
    def __init__(s, src):
        super().__init__(convert_charrefs=False)
        s.ls = [0] + [m.end() for m in re.finditer('\n', src)]
        s.stack, s.out = [], []
        s.feed(src)

    def off(s):
        l, c = s.getpos()
        return s.ls[l - 1] + c

    def handle_starttag(s, tag, attrs):
        if tag in VOID:
            return
        st = s.off()
        s.stack.append((tag, st, st + len(s.get_starttag_text()), any(k == 'data-uk' for k, _ in attrs)))

    def handle_startendtag(s, tag, attrs):
        pass

    def handle_endtag(s, tag):
        while s.stack:
            t = s.stack.pop()
            if t[0] == tag:
                if t[3]:
                    s.out.append((t[1], t[2], s.off()))
                break


def to_uk(src):
    """English-default markup (data-uk = Ukrainian) -> Ukrainian-default markup (data-en = English)"""
    spans, last = [], -1
    for st, a, b in sorted(_Spans(src).out):
        if st >= last:          # outermost only
            spans.append((st, a, b))
            last = b
    for st, a, b in reversed(spans):
        tag = src[st:a]
        uk = html.unescape(re.search(r'data-uk="([^"]*)"', tag).group(1))
        en_inner = src[a:b].replace('&', '&amp;').replace('"', '&quot;')
        src = src[:st] + tag[:-1] + f' data-en="{en_inner}">' + uk + src[b:]
    return src


HOME = {
    'uk': dict(title='Max Vitvitskiy — художник, дизайнер вражень, ментор креативності',
               desc='Я створюю мистецтво, проєктую досвіди, що об’єднують людей, і допомагаю розкривати творчий потенціал.', og='img/og-uk.jpg'),
    'en': dict(title='Max Vitvitskiy — Artist · Experience Designer · Creative Mentor',
               desc='I create art, design experiences that bring people together, and help unlock creative potential.', og='img/og.jpg'),
}


def home(W, WE):
    """Home pages: index.html (Ukrainian markup) and en/index.html (English markup) from tools/home.src.html.
    Both keep the language toggle; it now switches between the two URLs."""
    tpl = read('tools/home.src.html')
    for lang, WL in (('uk', W), ('en', WE)):
        en = lang == 'en'
        rows = []
        for w in WL[:15]:
            u = f'works/{w["slug"]}/'
            rows.append(f'    <a class="work" href="{u}" data-href-uk="{u}" data-href-en="en/{u}"><div class="ph"><img src="{e(ver(w["img"]))}" alt="{e(w.get("cardAlt") or w["title"])}" width="840" height="1050" loading="lazy"></div>'
                        f'<div class="cap"><span class="row"><span class="ttl">{e(w["title"])}</span><span class="n">{w["n"]:03d}</span></span>'
                        f'<span class="row"><span class="st" data-uk="Доступна">Available</span><span class="ed" data-uk="Тираж 10">Edition of 10</span></span></div></a>')
        src, n = re.subn(r'(<div class="gallery rv">\n)(?:    <a class="work"[^>]*href="[^"]*"[^>]*>.*?</a>\n)+(    <a class="work all")', lambda m: m.group(1) + '\n'.join(rows) + '\n' + m.group(2), tpl, count=1, flags=re.S)
        assert n == 1, 'homepage gallery not found'
        src = re.sub(r'href="works\.html"(?! data-href)', 'href="works.html" data-href-uk="works.html" data-href-en="en/works/"', src)
        H = HOME[lang]
        url = SITE + ('en/' if en else '')
        # head
        src = re.sub(r'<html lang="en">', f'<html lang="{lang}">', src, count=1)
        src = re.sub(r'<title>.*?</title>', lambda m: '<title>' + e(H['title']) + '</title>', src, count=1)
        src = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + e(H['desc']) + '"', src, count=1)
        src = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + e(H['title']) + '"', src, count=1)
        src = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + e(H['desc']) + '"', src, count=1)
        src = src.replace('https://maxvitvitskiy.com/img/og.jpg', SITE + H['og'])
        src = re.sub(r'<link rel="canonical" href="[^"]*">', lambda m: f'<link rel="canonical" href="{url}">\n' + alternates('', 'en/').rstrip('\n'), src, count=1)
        src = re.sub(r'<meta property="og:url" content="[^"]*">', lambda m: f'<meta property="og:url" content="{url}">\n<meta property="og:locale" content="{"en_US" if en else "uk_UA"}">\n<meta property="og:locale:alternate" content="{"uk_UA" if en else "en_US"}">', src, count=1)
        person = {'@context': 'https://schema.org', '@type': 'Person', 'name': 'Max Vitvitskiy', 'url': SITE, 'image': SITE + 'img/about.jpg',
                  'jobTitle': ['Artist', 'Experience Designer', 'Creative Mentor'] if en else ['Художник', 'Дизайнер вражень', 'Ментор креативності'],
                  'sameAs': ['https://www.instagram.com/maxvitvitskiy/', 'https://www.youtube.com/@MaxVitvitskiy', 'https://www.tiktok.com/@maxvitvitskiy', 'https://t.me/maxvitvitskiy']}
        src = src.replace('<script>document.documentElement.classList.add("js")</script>', '<script type="application/ld+json">' + json.dumps(person, ensure_ascii=False) + '</script>\n<script>document.documentElement.classList.add("js")</script>', 1)
        # language handling in the page script: the language is the page's own; the toggle moves between the two URLs
        old = 'L.forEach(e=>e.dataset.en=e.innerHTML)'
        assert old in src
        src = src.replace(old, 'L.forEach(e=>{if(e.dataset.en===undefined)e.dataset.en=e.innerHTML})', 1)
        src, k = re.subn(r"document\.querySelectorAll\('\.lang button'\)\.forEach\(b=>b\.onclick=\(\)=>\{.*?\n\s*setTimeout\(\(\)=>\{setLang\(l\);.*?\},210\)\}\);\n",
                         lambda m: "document.querySelectorAll('.lang button').forEach(b=>b.onclick=()=>{const l=b.dataset.l;if(l===document.documentElement.lang)return;try{localStorage.setItem('lang',l)}catch(e){}location.href=(l==='en'?'/en/':'/')+location.hash});\n", src, count=1, flags=re.S)
        assert k == 1, 'language toggle handler not found'
        src, k = re.subn(r"let sl=null;try\{sl=localStorage\.getItem\('lang'\)\}catch\(e\)\{\}\nsetLang\(sl\|\|.*?\);\n",
                         lambda m: ("let sl=null;try{sl=localStorage.getItem('lang')}catch(e){}\n"
                                    + ("setLang('en');\n" if en else "if(sl==='en')location.replace('/en/'+location.hash);else setLang('uk');\n")), src, count=1, flags=re.S)
        assert k == 1, 'language init not found'
        if en:
            # English raw links and root-absolute assets (the page lives one level down)
            def hr(m):
                t = m.group(0)
                y = re.search(r'data-href-en="([^"]*)"', t).group(1)
                return re.sub(r'href="[^"]*"', 'href="' + (y if y.startswith('http') else '/' + y) + '"', t, count=1)
            src = re.sub(r'<a [^>]*data-href-en="[^"]*"[^>]*>', hr, src)
            src = re.sub(r'(data-href-(?:uk|en)=")(?!http)([^"]*)', lambda m: m.group(1) + '/' + m.group(2), src)
            src = re.sub(r'(?<=["\'(,\s])(img|fonts|video|reels|js)/', r'/\1/', src)
        else:
            src = to_uk(src)
        write('en/index.html' if en else 'index.html', src)


def card_frame(W):
    """index of the gallery frame that is the card picture itself (-1 if none), so card slides never repeat it"""
    import hashlib
    h = lambda p: hashlib.md5(open(os.path.join(ROOT, p), 'rb').read()).hexdigest()
    for w in W:
        if w.get('slug'):
            c = h(w['img'])
            w['ci'] = next((k for k, x in enumerate(w['imgs']) if h(x) == c), -1)


def related(W, k=4):
    """for each work: the k closest by shared themes (Jaccard), then by catalog proximity"""
    real = [i for i, w in enumerate(W) if w.get('slug')]
    for i in real:
        a = set(W[i]['themes'])
        sc = []
        for j in real:
            if j == i:
                continue
            b = set(W[j]['themes'])
            sc.append((-(len(a & b) / (len(a | b) or 1)), abs(i - j), j))
        W[i]['rel'] = [j for _, _, j in sorted(sc)[:k]]


def catalog(tpl, W, lang):
    """the catalog page (works.html for uk, en/works/index.html for en) from the shared template"""
    en = lang == 'en'
    src = tpl
    if en:
        for ua, e_ in i18n.UI:
            assert ua in src, 'UI string missing in template: ' + ua
            src = src.replace(ua, e_)
        src = src.replace('<a class="logo" href="index.html"', '<a class="logo" href="en/"').replace('<a class="back" href="index.html"', '<a class="back" href="en/"')
    th = i18n.THEMES_EN if en else dict(THEMES)
    # data the catalog's JS reads (pages keep their own copy via the same script) + labels for the themes/related blocks
    lb = {'rel': 'Related works' if en else 'Схожі роботи', 'th': 'Themes' if en else 'Теми', 'cat': 'en/works/' if en else 'works.html', 'pre': 'en/' if en else ''}
    data = 'const W=' + json.dumps(W, ensure_ascii=False) + ';\nconst TH=' + json.dumps(th, ensure_ascii=False) + ',LB=' + json.dumps(lb, ensure_ascii=False) + ';\n'
    src = re.sub(r'^const W=\[.*?\];\n(?:const TH=.*?;\n)?', lambda m: data, src, count=1, flags=re.M | re.S)
    used = {t for w in W for t in w['themes']}
    btn = lambda k, l, p='false': f'<button type="button" data-f="{k}" aria-pressed="{p}">{l}</button>'
    chips = [btn('all', 'All' if en else 'Усі', 'true')] + [btn(k, th[k]) for k, _ in THEMES if k in used] + [btn('available', 'Available' if en else 'Доступні')]
    rows = '<div class="frow">' + ''.join(chips[:7]) + '</div><div class="frow">' + ''.join(chips[7:]) + '</div>'
    src = re.sub(r'(<div class="filters"[^>]*>\n    ).*?(\n  </div>)', lambda m: m.group(1) + rows + m.group(2), src, count=1, flags=re.S)
    cards = '\n'.join(card(i, w, lang) for i, w in enumerate(W))
    src = re.sub(r'(<div class="wall">\n).*?(\n  </div>\n</main>)', lambda m: m.group(1) + cards + m.group(2), src, count=1, flags=re.S)
    real = [w for w in W if w.get('slug')]
    cat_url = SITE + ('en/works/' if en else 'works.html')
    graph = [ld(w, lang) for w in real]
    graph.append({'@type': 'CollectionPage', 'name': 'Max Vitvitskiy — artworks' if en else 'Картини Max Vitvitskiy', 'url': cat_url, 'inLanguage': lang,
                  'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(real),
                                 'itemListElement': [{'@type': 'ListItem', 'position': k + 1, 'url': purl(w, lang), 'name': w['title']} for k, w in enumerate(real)]}})
    graph.append(crumbs([('Home', SITE + ('en/' if en else '')), ('Gallery' if en else 'Галерея', cat_url)]))
    src = re.sub(r'<script type="application/ld\+json">.*?</script>',
                 lambda m: '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>',
                 src, count=1, flags=re.S)
    # head: language, base, canonical, hreflang, social tags
    if en:
        H = i18n.HEAD_EN
        src = re.sub(r'<base href="[^"]*">', '<base href="../../">', src, count=1)
        src = re.sub(r'<title>.*?</title>', lambda m: '<title>' + e(H['title']) + '</title>', src, count=1)
        src = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + e(H['desc']) + '"', src, count=1)
        src = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + e(H['ogtitle']) + '"', src, count=1)
        src = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + e(H['ogdesc']) + '"', src, count=1)
        src = src.replace('img/og-uk.jpg', 'img/og.jpg')
    src = re.sub(r'<link rel="canonical" href="[^"]*">(\n<link rel="alternate" hreflang="[^"]*" href="[^"]*">)*',
                 lambda m: f'<link rel="canonical" href="{cat_url}">\n' + alternates('works.html', 'en/works/').rstrip('\n'), src, count=1)
    src = re.sub(r'<meta property="og:url" content="[^"]*">(\n<meta property="og:locale[^>]*>)*',
                 lambda m: f'<meta property="og:url" content="{cat_url}">\n<meta property="og:locale" content="{"en_US" if en else "uk_UA"}">\n<meta property="og:locale:alternate" content="{"uk_UA" if en else "en_US"}">', src, count=1)
    src = re.sub(r"<script>try\{localStorage\.setItem\('lang','[a-z]+'\)\}catch\(e\)\{\}</script>\n", '', src)
    src = src.replace('</head>', lang_script(lang) + '</head>', 1)
    # language switch next to the "home" link
    lng = f'<a class="lng" href="{"works.html" if en else "en/works/"}" hreflang="{"uk" if en else "en"}" lang="{"uk" if en else "en"}">{"UA" if en else "EN"}</a>'
    src = re.sub(r'<a class="lng".*?</a>', '', src)
    src = src.replace('<a class="back"', lng + '<a class="back"', 1)
    return src


def main():
    W = json.loads(read('data/works.json'))
    related(W)
    card_frame(W)
    tpl = read(CAT)
    WE = i18n.localize(W)
    for a, b in zip(W, WE):
        b['rel'] = a['rel']
        b['ci'] = a.get('ci', -1)
    real = [i for i, w in enumerate(W) if w.get('slug')]
    for lang, WL in (('uk', W), ('en', WE)):
        src = catalog(tpl, WL, lang)
        write(CAT if lang == 'uk' else 'en/works/index.html', src)
        for k, i in enumerate(real):
            write(('en/' if lang == 'en' else '') + f'works/{WL[i]["slug"]}/index.html', page(src, WL[i], i, k + 1, len(real), lang, WL))
    home(W, WE)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
          ]

    def entry(uk, en, imgs):
        alt = (f'<xhtml:link rel="alternate" hreflang="uk" href="{e(SITE + uk)}"/><xhtml:link rel="alternate" hreflang="en" href="{e(SITE + en)}"/>'
               f'<xhtml:link rel="alternate" hreflang="x-default" href="{e(SITE + uk)}"/>')
        for u in (uk, en):
            sm.append('  <url><loc>' + e(SITE + u) + '</loc>' + alt + ''.join('<image:image><image:loc>' + e(SITE + x) + '</image:loc></image:image>' for x in imgs) + '</url>')

    entry('', 'en/', [])
    entry('works.html', 'en/works/', [])
    for i in real:
        entry('works/' + W[i]['slug'] + '/', 'en/works/' + W[i]['slug'] + '/', W[i]['imgs'])
    sm.append('</urlset>\n')
    write('sitemap.xml', '\n'.join(sm))
    write('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /data/\n\nSitemap: {SITE}sitemap.xml\n')
    print(f'catalog: {len(W)} cards x2 languages, pages: {len(real)}x2, sitemap urls: {4 + 2 * len(real)}')


if __name__ == '__main__':
    main()

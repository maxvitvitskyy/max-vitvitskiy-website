"""English localisation of the gallery data and UI strings (used by build.py and og.py).

The Ukrainian site is the source of truth (data/works.json). English copy for each work lives in
data/works-en.json (lead, story, meaning, seo); everything else is mapped here.
"""
import copy, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THEMES_EN = {'portraits': 'Portraits', 'animals': 'Animals', 'birds': 'Birds', 'butterflies': 'Butterflies', 'flowers': 'Flowers', 'ocean': 'Ocean',
             'faith': 'Faith', 'ukraine': 'Ukraine', 'love': 'Love', 'self': 'Self-discovery', 'transformation': 'Transformation'}

FIN = {'Полотно в тубусі': ('Canvas in a tube', 'Protective tube — if you plan to frame it yourself.'),
       'На підрамнику': ('Stretched canvas', 'Stretched over a wooden bar frame, a clean gallery look.'),
       'У дерев’яній рамі': ('In a wooden frame', 'Solid wooden frame, ready to hang (recommended).')}
FRAME = {'Натуральний': 'Natural', 'Темний дуб': 'Dark oak', 'Чорне дерево': 'Ebony', 'Вугільно-чорний': 'Charcoal black'}

BLOCK = {'Що входить у видання': "What's included", 'Куди пасує': 'Where it fits', 'Доставка й умови': 'Shipping & terms',
         'Теги й характеристики': 'Tags & details'}
LINE = {
    'Підпис автора від руки': 'Hand-signed by the artist',
    'Індивідуальна нумерація (X/10)': 'Individually numbered (X/10)',
    'Фізичний сертифікат автентичності': 'Physical certificate of authenticity',
    'Музейне полотно': 'Museum-quality canvas',
    'Архівні світлостійкі чорнила': 'Archival lightfast inks',
    'Кожна робота ретельно перевіряється перед відправкою': 'Every piece is carefully inspected before shipping',
    'Вітальня, спальня, кабінет, передпокій, кухня й їдальня': 'Living room, bedroom, study, hallway, kitchen and dining room',
    'Офіси, галерейні простори, інтер’єри з акцентом на мистецтво': 'Offices, gallery spaces, art-focused interiors',
    'Подарунок для колекціонера чи любителя мистецтва': 'A gift for a collector or art lover',
    'Нестандартний розмір чи формат — напишіть, обговоримо': 'Custom size or format — write to me and we will discuss it',
    'Виготовлення й підготовка: 5–10 робочих днів': 'Production and preparation: 5–10 business days',
    'Номер відстеження для кожного замовлення, повністю застрахована доставка': 'Tracking number for every order, fully insured shipping',
    'Фото готової роботи перед відправкою — за запитом': 'A photo of the finished piece before shipping — on request',
    'Кур’єр може попросити номер телефону — вкажіть його в замовленні': 'The courier may ask for a phone number — please add it to your order',
    'Мито й імпортні податки сплачує покупець': 'Duties and import taxes are paid by the buyer',
    'Кольори можуть трохи відрізнятися залежно від налаштувань екрана': 'Colours may differ slightly depending on your screen settings',
    'Кожна робота виготовляється на замовлення': 'Every piece is made to order',
    'Орієнтація: вертикальна': 'Orientation: vertical',
}
COLOR = {'чорний': 'black', 'червоний': 'red', 'темно-червоний': 'dark red', 'синій': 'blue', 'помаранчевий': 'orange', 'білий': 'white',
         'темно-бірюзовий': 'dark turquoise', 'теплий золотий': 'warm gold', 'золотий': 'gold', 'смарагдовий': 'emerald',
         'глибокий зелений / бірюзовий': 'deep green / turquoise', 'мідний': 'copper', 'коричневий': 'brown', 'жовтий': 'yellow',
         'теплий помаранчевий': 'warm orange', 'бірюзовий': 'turquoise', 'темно-зелений': 'dark green'}
THEME_WORD = {'люди й портрет': 'people & portrait', 'фентезі': 'fantasy', 'натхнення': 'inspiration', 'тварини': 'animals', 'квіти': 'flowers',
              'природа': 'nature', 'абстракція': 'abstraction', 'надихаючі вислови': 'inspirational quotes', 'люди': 'people',
              'духовність': 'spirituality', 'релігія': 'religion', 'рослини': 'plants', 'класичне мистецтво': 'classical art',
              'пейзаж': 'landscape', 'музика': 'music', 'любов': 'love', 'патріотична': 'patriotic', 'Різдво': 'Christmas',
              'портрет': 'portrait', 'птахи': 'birds', 'самопізнання': 'self-discovery', 'вода': 'water'}
STYLE = {'сучасний': 'modern', 'сюрреалізм': 'surrealism'}


def spec(line):
    if line in LINE:
        return LINE[line]
    k, _, v = line.partition(': ')
    if k == 'Основний колір':
        return 'Primary colour: ' + COLOR[v]
    if k == 'Додатковий колір':
        return 'Secondary colour: ' + COLOR[v]
    if k == 'Рік':
        return 'Year: ' + v
    if k == 'Стиль':
        return 'Style: ' + STYLE[v]
    if k == 'Тематика':
        return 'Theme: ' + ', '.join(THEME_WORD[x] for x in v.split(', '))
    raise KeyError(line)


def alts(w):
    t, seo = w['title'], w.get('_seo_en', '')
    out, seen = [], {}
    for k, a in enumerate(w['alts']):
        if k == 0:
            s = f'{t} — {seo}, artwork by Max Vitvitskiy' if seo else f'{t} — artwork by Max Vitvitskiy'
        elif 'крупний план' in a:
            s = f'{t} — close-up of the museum-quality canvas'
        elif 'порівняння розмірів' in a:
            s = f'{t} — size comparison, 16×24, 24×36 and 32×48 in, above a sofa'
        elif 'деталь' in a:
            s = f'{t} — detail of the framed print: frame corner and canvas texture'
        elif 'на дивані' in a:
            s = f'{t} — framed print on a sofa'
        else:
            s = f'{t} in a room interior — framed artwork by Max Vitvitskiy on the wall'
        seen[s] = seen.get(s, 0) + 1
        out.append(s if seen[s] == 1 else f'{s} (view {seen[s]})')
    return out


def localize(W):
    """English copy of the work list (same order, same slugs, same images)."""
    en = json.load(open(os.path.join(ROOT, 'data/works-en.json'), encoding='utf-8'))
    out = []
    for w in W:
        x = copy.deepcopy(w)
        t = en[w['slug']]
        x['lead'], x['story'], x['meaning'], x['seo'] = t['lead'], t['story'], t['meaning'], t['seo']
        x['_seo_en'] = t['seo']
        x['status'] = {'Доступна': 'Available', 'Продана': 'Sold'}[w['status']]
        x['edition'] = w['edition'].replace('Тираж', 'Edition of')
        x['cardAlt'] = f'{w["title"]} in an interior — wall art by Max Vitvitskiy'
        x['alts'] = alts(x)
        x['desc'] = t['lead']
        for z in x['sizes']:
            z['label'] = z['label'].replace(' см', ' cm')
        for f in x['fins']:
            f['label'], f['note'] = FIN[f['label']]
        for f in x['frames']:
            f['label'] = FRAME[f['label']]
        for b in x.get('info', []):
            b['t'] = BLOCK[b['t']]
            if b.get('l'):
                b['l'] = [spec(l) for l in b['l']]
        out.append(x)
    return out


# UI strings in the catalog template (works.html): Ukrainian -> English. Every key must occur in the template.
UI = [
    ('  <section class="close" aria-labelledby="cl-t">\n    <h2 id="cl-t"><span class="ln">Деякі образи</span><span class="ln"><i>залишаються</i></span><span class="ln">з нами.</span></h2>\n    <p class="cl-s">Можливо, один із них — <b>саме твій.</b></p>\n    <div class="cl-rule" aria-hidden="true"></div>\n    <p class="cl-b">Кожна робота має власну історію та сенс. Якщо певний образ відгукнувся тобі, можливо, саме час зробити його частиною свого простору.</p>\n    <p class="cl-c">Обери роботу, яка тобі близька.</p>\n    <a class="cl-btn" href="mailto:maxim.vitvitskiy@gmail.com?subject=%D0%94%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BD%D1%96%D1%81%D1%82%D1%8C%20%D1%80%D0%BE%D0%B1%D0%BE%D1%82%D0%B8">Запитати про доступність роботи<i class="ar" aria-hidden="true"></i></a>\n  </section>\n',
     '  <section class="close" aria-labelledby="cl-t">\n    <h2 id="cl-t"><span class="ln">Some images</span><span class="ln"><i>stay</i></span><span class="ln">with us.</span></h2>\n    <p class="cl-s">Perhaps one of them is <b>yours.</b></p>\n    <div class="cl-rule" aria-hidden="true"></div>\n    <p class="cl-b">Every work has its own story and meaning. If an image speaks to you, maybe it is time to make it part of your space.</p>\n    <p class="cl-c">Choose the work that feels close to you.</p>\n    <a class="cl-btn" href="mailto:maxim.vitvitskiy@gmail.com?subject=Artwork%20availability">Ask about availability<i class="ar" aria-hidden="true"></i></a>\n  </section>\n'),
    ('<html lang="uk">', '<html lang="en">'),
    ('class="dlogo" href="/"', 'class="dlogo" href="/en/"'),
    ('aria-label="Закрити"', 'aria-label="Close"'),
    ('aria-label="Попередній кадр"', 'aria-label="Previous frame"'),
    ('aria-label="Наступний кадр"', 'aria-label="Next frame"'),
    ('aria-label="Кадри роботи"', 'aria-label="Frames of the work"'),
    ('aria-label="Попередня робота"', 'aria-label="Previous work"'),
    ('aria-label="Наступна робота"', 'aria-label="Next work"'),
    ('aria-label="Фільтр робіт"', 'aria-label="Filter works"'),
    ('На головну</a>', 'Home</a>'),
    ('<span class="k">Галерея · 2021–2026</span><h1>Нові <i>роботи</i></h1>', '<span class="k">Gallery · 2021–2026</span><h1>New <i>works</i></h1>'),
    ('<p><span>Я створюю образи, що поєднують реальність, уяву та символізм. У кожній роботі закладена історія, думка або відчуття — про те, що ми переживаємо, у що віримо та що відкриваємо в собі.</span> <span>Це мистецтво про внутрішній світ людини, красу життя та сенси, які не завжди можна передати словами.</span></p>',
     '<p><span>I create images that combine reality, imagination and symbolism. Every work holds a story, a thought or a feeling — about what we live through, what we believe in and what we discover within ourselves.</span> <span>This is art about the inner world of a person, the beauty of life and meanings that cannot always be put into words.</span></p>'),
    ('Створюй · Надихай · Проживай', 'Create · Inspire · Experience'),
    ('Читати повністю</button>', 'Read more</button>'),
    ('<label>Розмір<select', '<label>Size<select'),
    ('<label>Виконання<select', '<label>Finish<select'),
    ('<label class="fr" hidden>Колір рами<select', '<label class="fr" hidden>Frame colour<select'),
    ('Запитати про роботу<i', 'Ask about this work<i'),
    ('<dt>Техніка</dt><dd>Фотографія, цифрова композиція</dd><dt>Документи</dt><dd>Сертифікат автентичності</dd>',
     '<dt>Medium</dt><dd>Photography, digital composition</dd><dt>Documents</dt><dd>Certificate of authenticity</dd>'),
    ("'<button type=\"button\" data-src=\"'+s+'\" aria-label=\"Кадр '", "'<button type=\"button\" data-src=\"'+s+'\" aria-label=\"Frame '"),
    ("sv.classList.toggle('sold',w.status==='Продана')", "sv.classList.toggle('sold',w.status==='Sold')"),
    ("rm.textContent='Читати повністю'", "rm.textContent='Read more'"),
    ("rm.textContent=o?'Згорнути':'Читати повністю'", "rm.textContent=o?'Collapse':'Read more'"),
    ("' Ціна в USD, без доставки.'", "' Price in USD, shipping not included.'"),
    ("let body='Робота: '+w.title", "let body='Artwork: '+w.title"),
    ("'\\nРозмір: '", "'\\nSize: '"),
    ("'\\nВиконання: '", "'\\nFinish: '"),
    ("'\\nКолір рами: '", "'\\nFrame colour: '"),
    ("'\\nЦіна: $'", "'\\nPrice: $'"),
    ("new URL('works.html',document.baseURI).href", "new URL('en/works/',document.baseURI).href"),
    ("new URL('works/'+w.slug+'/',document.baseURI).href", "new URL('en/works/'+w.slug+'/',document.baseURI).href"),
]

CHIP = {'Усі': 'All', 'Доступні': 'Available'}

HEAD_EN = dict(
    title='Max Vitvitskiy Art Gallery — Surreal Wall Art, Limited Editions of 10',
    desc="Browse Max Vitvitskiy's symbolic, surreal artworks on museum-quality canvas: signed editions of 10 with a certificate of authenticity. Sizes 16×24 to 32×48 in, solid wood frames.",
    ogtitle='Max Vitvitskiy — surreal wall art, editions of 10',
    ogdesc='Symbolic surreal artworks on museum-quality canvas: edition of 10, signed, with a certificate of authenticity.',
)

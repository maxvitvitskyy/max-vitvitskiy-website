"""Privacy policy (privacy/, en/privacy/) and the site-wide 404.html.
Run from tools/build.py; standalone: python3 tools/legal.py"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://maxvitvitskiy.com/'
MAIL = 'maxim.vitvitskiy@gmail.com'
UPDATED = {'uk': '9 листопада 2026', 'en': '9 November 2026'}

FONTS = '''@font-face{font-family:"Moniqa Head";src:url("/fonts/Moniqa-MediumHeading.woff2") format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Raleway";src:url("/fonts/Raleway-cyrillic.woff2") format("woff2");font-weight:300 500;font-display:swap;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}
@font-face{font-family:"Raleway";src:url("/fonts/Raleway-latin.woff2") format("woff2");font-weight:300 500;font-display:swap;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}'''

BASE = FONTS + '''
:root{--coal:#0d0d0c;--ink:#01110A;--amber:#FFA630;--cream:#F1E0C5;--sand:#FCDE9C;--muted:rgba(241,224,197,.66);--line:rgba(241,224,197,.14);
  --gut:clamp(20px,5vw,72px);--head:"Moniqa Head",serif;--display:"Moniqa",serif;--body:"Raleway","Helvetica Neue",Arial,sans-serif;--ease:cubic-bezier(.16,1,.3,1);
  --arrow:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='33 -513 581 348'><path transform='scale(1,-1)' fill='black' d='M417 165 401 183 566 328H33V350H566L401 496L417 513L614 339Z'/></svg>")}
*{box-sizing:border-box;margin:0;padding:0}
html{color-scheme:dark;-webkit-text-size-adjust:100%}
body{background:var(--coal);color:var(--cream);font-family:var(--body);-webkit-font-smoothing:antialiased;min-height:100svh}
a{color:inherit}
::selection{background:rgba(255,166,48,.35);color:#fff}
:focus-visible{outline:2px solid rgba(255,166,48,.75);outline-offset:3px;border-radius:4px}
.top{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:max(18px,env(safe-area-inset-top)) var(--gut) 18px}
.top .logo img{display:block;height:30px;width:auto}
.top nav{display:flex;gap:6px}
.top nav a{padding:10px 14px;border-radius:99px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;text-decoration:none;color:var(--muted);transition:color .3s,background .3s}
.top nav a:hover{color:var(--cream);background:rgba(241,224,197,.06)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:12px;min-height:52px;padding:0 26px;border-radius:99px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;text-decoration:none;transition:background .3s,color .3s,border-color .3s,transform .2s}
.btn .ar{width:1.25em;height:.7em;background:currentColor;-webkit-mask:var(--arrow) center/contain no-repeat;mask:var(--arrow) center/contain no-repeat;transition:transform .4s var(--ease)}
.btn:hover .ar{transform:translateX(4px)}
.btn.fill{background:var(--amber);color:var(--ink)}.btn.fill:hover{background:var(--sand)}
.btn.line{border:1px solid rgba(241,224,197,.22);color:var(--cream)}.btn.line:hover{border-color:var(--amber);color:var(--amber)}
footer{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 24px;padding:28px var(--gut) calc(28px + env(safe-area-inset-bottom));border-top:1px solid var(--line);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
footer a{text-decoration:none}footer a:hover{color:var(--cream)}
@media(prefers-reduced-motion:reduce){*{transition-duration:.01ms!important;animation-duration:.01ms!important}}
'''


def logo(lang):
    return f'<a class="logo" href="{"/en/" if lang == "en" else "/"}" aria-label="Max Vitvitskiy"><img src="/img/logo-mark.png" alt="" width="600" height="255"></a>'


# ---------------------------------------------------------------- privacy
P = {
 'uk': dict(
  title='Політика конфіденційності — Max Vitvitskiy',
  desc='Які дані збирає сайт maxvitvitskiy.com, навіщо, де вони зберігаються і як їх видалити.',
  h1='Політика конфіденційності', lead='Коротко: я збираю лише те, що потрібно, щоб відповісти вам і доставити роботу. Нічого не продаю і не передаю для реклами.',
  upd='Оновлено', nav=[('Галерея', '/works.html'), ('Контакти', '/#contact')], other=('EN', '/en/privacy/'),
  foot='Створюй · Надихай · Проживай',
  sections=[
   ('Хто відповідає за дані', [
     f'Max Vitvitskiy, власник сайту maxvitvitskiy.com. З будь-яких питань щодо ваших даних пишіть на <a href="mailto:{MAIL}">{MAIL}</a>.']),
   ('Що я збираю', [
     '<b>Замовлення картини.</b> Ім’я, email, телефон, країна й місто, адреса або відділення Нової пошти, спосіб оплати, коментар, а для подарунка — текст листівки. А також обрана робота, розмір, рама й ціна.',
     '<b>Повідомлення з форми.</b> Ім’я, email або Telegram, тема й текст повідомлення.',
     '<b>Статистика.</b> Google Analytics збирає знеособлені дані про відвідування: які сторінки відкриті, тип пристрою й браузера, приблизне місце (країна чи місто). Для цього Google використовує cookie.']),
   ('Навіщо', [
     'Щоб підтвердити наявність роботи, розрахувати й організувати доставку, надіслати посилання на оплату, відповісти на ваше повідомлення. Статистика допомагає зрозуміти, що на сайті працює добре, а що варто покращити.']),
   ('Де зберігаються дані', [
     'Замовлення й повідомлення потрапляють у мою Google Таблицю (Google Workspace), а сповіщення про них приходять мені на пошту Gmail і в особистий Telegram-бот. Доступ до них маю лише я.',
     'Для доставки адресу й телефон я передаю службі доставки (Нова пошта або міжнародний перевізник), а для оплати — платіжному сервісу, через який ви платите. Лише те, що потрібно для цього.']),
   ('Скільки зберігаються', [
     'Дані замовлення — стільки, скільки потрібно для його виконання, гарантійних питань і обліку. Повідомлення — поки триває наше спілкування. На ваш запит я видалю їх раніше, якщо закон не вимагає зберігати.']),
   ('Що зберігається на вашому пристрої', [
     'Ваш браузер запам’ятовує обрану мову сайту і контакти, введені у вікні замовлення, щоб наступного разу не вводити їх знову. Це зберігається лише у вашому браузері (localStorage), мені не надсилається, і ви можете очистити це в налаштуваннях браузера.',
     'Відео з YouTube завантажуються лише після того, як ви натиснете на ролик, у режимі youtube-nocookie.']),
   ('Ваші права', [
     f'Ви можете попросити показати, виправити або видалити ваші дані, а також відмовитися від подальшого зв’язку. Напишіть на <a href="mailto:{MAIL}">{MAIL}</a>, і я відповім протягом 30 днів.',
     'Відмовитися від статистики Google Analytics можна, заблокувавши cookie в браузері або встановивши офіційне розширення Google Analytics Opt-out.']),
  ]),
 'en': dict(
  title='Privacy Policy — Max Vitvitskiy',
  desc='What data maxvitvitskiy.com collects, why, where it is kept and how to have it deleted.',
  h1='Privacy Policy', lead='In short: I collect only what I need to reply to you and deliver your artwork. Nothing is sold or shared for advertising.',
  upd='Updated', nav=[('Gallery', '/en/works/'), ('Contact', '/en/#contact')], other=('UA', '/privacy/'),
  foot='Create · Inspire · Experience',
  sections=[
   ('Who is responsible', [
     f'Max Vitvitskiy, owner of maxvitvitskiy.com. For any question about your data, write to <a href="mailto:{MAIL}">{MAIL}</a>.']),
   ('What I collect', [
     '<b>Artwork orders.</b> Name, e-mail, phone, country and city, delivery address or Nova Poshta branch, payment method, comment and, for a gift, the card text. Also the chosen work, size, frame and price.',
     '<b>Contact form messages.</b> Name, e-mail or Telegram, topic and message.',
     '<b>Statistics.</b> Google Analytics collects anonymised visit data: pages viewed, device and browser type, approximate location (country or city). Google uses cookies for this.']),
   ('Why', [
     'To confirm availability, calculate and arrange delivery, send you a payment link and answer your message. Statistics show me what works on the site and what to improve.']),
   ('Where the data is kept', [
     'Orders and messages are stored in my Google Sheet (Google Workspace); notifications reach my Gmail inbox and a private Telegram bot. Only I have access.',
     'For delivery I pass your address and phone to the carrier (Nova Poshta or an international courier), and for payment to the payment service you pay through — only what each of them needs.']),
   ('How long', [
     'Order data for as long as needed to fulfil the order, handle any warranty question and keep accounts. Messages for as long as our conversation lasts. On request I delete them sooner, unless the law requires keeping them.']),
   ('What stays on your device', [
     'Your browser remembers the site language and the contact details you typed into the order window, so you do not have to type them again. This stays in your browser only (localStorage), is never sent to me, and you can clear it in your browser settings.',
     'YouTube videos load only after you click a reel, in youtube-nocookie mode.']),
   ('Your rights', [
     f'You can ask to see, correct or delete your data, or to stop any further contact. Write to <a href="mailto:{MAIL}">{MAIL}</a> and I will reply within 30 days.',
     'To opt out of Google Analytics, block its cookies in your browser or install Google’s official Analytics Opt-out add-on.']),
  ]),
}

PRIV_CSS = '''
main{width:min(760px,100% - 2*var(--gut));margin:clamp(28px,6vw,80px) auto clamp(60px,9vw,120px)}
h1{font-family:var(--head);font-weight:400;text-transform:uppercase;font-size:clamp(46px,7.4vw,96px);line-height:.9;letter-spacing:-.005em;text-wrap:balance}
.lead{margin-top:22px;font-size:clamp(17px,1.6vw,20px);line-height:1.6;color:var(--cream);max-width:40ch;text-wrap:pretty}
.upd{margin-top:16px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.toc{margin-top:40px;padding:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px}
.toc a{padding:8px 14px;border-radius:99px;border:1px solid var(--line);font-size:13px;text-decoration:none;color:var(--muted);transition:color .3s,border-color .3s}
.toc a:hover{color:var(--amber);border-color:rgba(255,166,48,.5)}
section{display:grid;grid-template-columns:minmax(0,13rem) minmax(0,1fr);gap:8px 40px;padding:36px 0;border-bottom:1px solid var(--line);scroll-margin-top:20px}
h2{font-family:var(--head);font-weight:400;text-transform:uppercase;font-size:clamp(24px,2.4vw,30px);line-height:1;color:var(--amber);text-wrap:balance}
section p{font-size:16px;line-height:1.75;color:var(--muted);max-width:62ch;text-wrap:pretty}
section p+p{margin-top:14px}
section p b{color:var(--cream);font-weight:500}
section a{color:var(--cream);text-decoration-color:rgba(255,166,48,.6);text-underline-offset:3px}
section a:hover{color:var(--amber)}
.ask{margin-top:44px;display:flex;flex-wrap:wrap;gap:12px}
@media(max-width:699px){section{grid-template-columns:1fr;gap:14px;padding:28px 0}.top nav a{padding:10px}}
'''


def privacy(lang):
    t = P[lang]
    en = lang == 'en'
    path = ('en/' if en else '') + 'privacy/'
    ids = [f's{i + 1}' for i in range(len(t['sections']))]
    secs = ''.join(f'<section id="{ids[i]}" aria-labelledby="{ids[i]}-h"><h2 id="{ids[i]}-h">{html.escape(h)}</h2><div>' + ''.join(f'<p>{p}</p>' for p in ps) + '</div></section>'
                   for i, (h, ps) in enumerate(t['sections']))
    toc = ''.join(f'<a href="#{ids[i]}">{html.escape(h)}</a>' for i, (h, _) in enumerate(t['sections']))
    nav = ''.join(f'<a href="{u}">{html.escape(n)}</a>' for n, u in t['nav']) + f'<a href="{t["other"][1]}" hreflang="{"uk" if en else "en"}" lang="{"uk" if en else "en"}">{t["other"][0]}</a>'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t["title"])}</title>
<meta name="description" content="{html.escape(t["desc"])}">
<link rel="canonical" href="{SITE}{path}">
<link rel="alternate" hreflang="uk" href="{SITE}privacy/">
<link rel="alternate" hreflang="en" href="{SITE}en/privacy/">
<meta name="theme-color" content="#0d0d0c">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<style>{BASE}{PRIV_CSS}</style>
</head>
<body>
<header class="top">{logo(lang)}<nav aria-label="{"Site" if en else "Сайт"}">{nav}</nav></header>
<main>
<h1>{html.escape(t["h1"])}</h1>
<p class="lead">{html.escape(t["lead"])}</p>
<p class="upd">{t["upd"]} · {UPDATED[lang]}</p>
<nav class="toc" aria-label="{"Contents" if en else "Зміст"}">{toc}</nav>
{secs}
<div class="ask"><a class="btn fill" href="mailto:{MAIL}">{"Write to me" if en else "Написати мені"}<i class="ar" aria-hidden="true"></i></a><a class="btn line" href="{"/en/works/" if en else "/works.html"}">{"Back to the gallery" if en else "До галереї"}</a></div>
</main>
<footer><span>© 2026 Max Vitvitskiy</span><span>{t["foot"]}</span></footer>
</body>
</html>
'''


# ---------------------------------------------------------------- 404
NF_CSS = '''
body{display:grid;grid-template-rows:auto 1fr auto}
.nf{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);align-items:center;gap:clamp(28px,6vw,90px);width:min(1180px,100% - 2*var(--gut));margin:0 auto;padding:clamp(20px,5vw,60px) 0}
.code{font-family:var(--head);font-size:clamp(84px,15vw,220px);line-height:.8;letter-spacing:-.01em;color:transparent;background:linear-gradient(0deg,#F5920A 0%,#FFB93D 55%,#FFCE7A 100%);-webkit-background-clip:text;background-clip:text}
h1{margin-top:clamp(14px,2vw,24px);font-family:var(--head);font-weight:400;text-transform:uppercase;font-size:clamp(34px,4.6vw,64px);line-height:.95;text-wrap:balance}
h1 i{font-style:normal;color:transparent;background:linear-gradient(0deg,#F5920A 0%,#FFB93D 55%,#FFCE7A 100%);-webkit-background-clip:text;background-clip:text}
.nf p{margin-top:18px;font-size:16px;line-height:1.7;color:var(--muted);max-width:42ch;text-wrap:pretty}
.acts{margin-top:30px;display:flex;flex-wrap:wrap;gap:12px}
.art{position:relative;justify-self:center;width:min(100%,380px);aspect-ratio:4/5}
.art a{position:absolute;inset:0;display:block;border-radius:6px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.6);transform:rotate(-2deg);transition:transform .7s var(--ease)}
.art a:hover{transform:rotate(0) scale(1.01)}
.art img{width:100%;height:100%;object-fit:cover;display:block}
.art .cap{position:absolute;left:0;right:0;bottom:0;padding:40px 18px 16px;background:linear-gradient(transparent,rgba(0,0,0,.75));font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--cream)}
.art .cap b{display:block;margin-top:4px;font-family:var(--head);font-weight:400;font-size:24px;letter-spacing:0}
@media(max-width:799px){.nf{grid-template-columns:1fr}.art{order:-1;width:min(62%,260px)}}
'''

WORKS = [('introspectum', 'Introspectum'), ('a-thousand-moments-later', 'A Thousand Moments Later'), ('miracle', 'Miracle'),
         ('open-my-eyes', 'Open My Eyes'), ('lion-and-lamb', 'Lion and Lamb'), ('face-the-sun', 'Face the Sun')]


def not_found():
    import json
    works = json.dumps(WORKS)
    return f'''<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Сторінку не знайдено — Max Vitvitskiy</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0d0d0c">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png">
<style>{BASE}{NF_CSS}</style>
</head>
<body>
<header class="top">{logo("uk")}<nav aria-label="Сайт"><a href="/works.html" data-en="/en/works/">Галерея</a><a href="/#contact" data-en="/en/#contact">Контакти</a></nav></header>
<main class="nf">
  <div>
    <div class="code" aria-hidden="true">404</div>
    <h1 data-en="This page <i>is not here</i>">Цієї сторінки <i>тут немає</i></h1>
    <p data-en="Perhaps the link is outdated or the address has a typo. The works themselves are where they always were.">Можливо, посилання застаріло або в адресі описка. Самі роботи — там, де й були.</p>
    <div class="acts"><a class="btn fill" href="/works.html" data-en="/en/works/"><span data-en="To the gallery">До галереї</span><i class="ar" aria-hidden="true"></i></a><a class="btn line" href="/" data-en="/en/"><span data-en="Home">На головну</span></a></div>
  </div>
  <div class="art"><a href="/works.html"><img alt="" width="840" height="1050"><span class="cap"><span data-en="Meanwhile">Поки що</span><b></b></span></a></div>
</main>
<footer><span>© 2026 Max Vitvitskiy</span><span data-en="Create · Inspire · Experience">Створюй · Надихай · Проживай</span></footer>
<script>
(function(){{
  var en=/^\\/en(\\/|$)/.test(location.pathname);
  try{{if(!en&&localStorage.getItem('lang')==='en'&&!/^\\/(works|privacy)/.test(location.pathname))en=true}}catch(e){{}}
  if(en){{document.documentElement.lang='en';document.title='Page not found — Max Vitvitskiy';
    document.querySelectorAll('[data-en]').forEach(function(el){{var v=el.getAttribute('data-en');if(el.tagName==='A')el.setAttribute('href',v);else el.innerHTML=v}});
    document.querySelector('.top nav').setAttribute('aria-label','Site');document.querySelector('.logo').setAttribute('href','/en/')}}
  var W={works},w=W[Math.floor(Math.random()*W.length)],a=document.querySelector('.art a');
  a.href=(en?'/en/':'/')+'works/'+w[0]+'/';var img=a.querySelector('img');img.src='/img/works/'+w[0]+'/card.webp';img.alt=w[1];a.querySelector('b').textContent=w[1];
}})();
</script>
</body>
</html>
'''


def main():
    for lang in ('uk', 'en'):
        p = os.path.join(ROOT, ('en/' if lang == 'en' else '') + 'privacy/index.html')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(privacy(lang))
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(not_found())


if __name__ == '__main__':
    main()

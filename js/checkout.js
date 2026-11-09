/* Checkout: the work you chose on the left, three short steps on the right (contacts, delivery, payment), then a confirmation.
   Orders go to ENDPOINT as JSON when it is set (Formspree / FormSubmit / own worker); without it the order opens as a ready e-mail. */
(function(){
'use strict';
var ENDPOINT='';                       // e.g. 'https://formspree.io/f/xxxx' — leave empty to send the order by e-mail
var MAIL='maxim.vitvitskiy@gmail.com';
var EN=(document.documentElement.lang||'uk').slice(0,2)==='en';
var T=EN?{
  buy:'Order this work',close:'Close',steps:['Contacts','Delivery','Payment'],
  h:['Who is it for?','Where do we send it?','How would you like to pay?'],
  sub:['We will confirm availability and the delivery cost before you pay anything.','We pack every work in a rigid box with corner guards and full insurance.','You will get a secure payment link only after I confirm your order personally.'],
  name:'Full name',email:'E-mail',phone:'Phone',phoneHint:'With country code, for the courier',
  country:'Country',city:'City',np:'Nova Poshta',npBranch:'Branch',npCourier:'Courier to the door',branch:'Branch number',branchPh:'e.g. 12',
  addr:'Street, house, apartment',addr2:'Address line 2 (optional)',region:'Region / state (optional)',zip:'Postal code',
  gift:'This is a gift',giftNote:'No prices in the parcel; I add a hand-signed card.',giftMsg:'Text for the card (optional)',
  pay:[['card','Card online','Visa, Mastercard, Apple Pay, Google Pay'],['paypal','PayPal','Convenient for buyers outside Ukraine'],['iban','Bank transfer','Invoice for companies and sole proprietors']],
  note:'Comment (optional)',notePh:'Room, wall size, delivery wishes…',
  next:'Continue',back:'Back',send:'Send the order',sending:'Sending…',
  fine:'By sending the order you agree that your data is used only to process this order. You pay nothing now.',
  size:'Size',fin:'Finish',frame:'Frame',price:'Work',ship:'Delivery',shipV:'after confirmation',total:'Total',plus:' + delivery',
  ed:'Edition of 10 · signed · certificate of authenticity',edit:'Change',
  req:'Please fill this in',bad:{email:'This doesn’t look like an e-mail — check for a missing @ or dot.',phone:'Add the full number with the country code, e.g. +44…'},
  okH:'Order received',okP:'Thank you! I will personally check the edition, calculate delivery to your address and send you a payment link.',
  okMail:'Your mail app has opened with the order filled in — just press “Send”.',
  okNo:'Order number',okSteps:['I confirm availability and the delivery cost','You pay by the secure link','The work is printed, signed and shipped with tracking'],
  okBack:'Back to the gallery',err:'The order could not be sent. Check your connection and try again — or write to '+MAIL,
  mailSubj:'Order',summary:'Your order'
}:{
  buy:'Придбати картину',close:'Закрити',steps:['Контакти','Доставка','Оплата'],
  h:['Для кого робота?','Куди надіслати?','Як зручно оплатити?'],
  sub:['Спершу я підтверджу наявність і вартість доставки — платити зараз нічого не потрібно.','Кожну роботу пакуємо в жорстку коробку з кутниками й повною страховкою.','Безпечне посилання на оплату ви отримаєте після того, як я особисто підтверджу замовлення.'],
  name:'Ім’я та прізвище',email:'Email',phone:'Телефон',phoneHint:'Для кур’єра чи відділення',
  country:'Країна',city:'Місто',np:'Нова пошта',npBranch:'Відділення',npCourier:'Кур’єр до дверей',branch:'Номер відділення',branchPh:'Наприклад, 12',
  addr:'Вулиця, будинок, квартира',addr2:'Адреса, рядок 2 (необов’язково)',region:'Область / штат (необов’язково)',zip:'Поштовий індекс',
  gift:'Це подарунок',giftNote:'Без цін у посилці, додам підписану від руки листівку.',giftMsg:'Текст для листівки (необов’язково)',
  pay:[['card','Карткою онлайн','Visa, Mastercard, Apple Pay, Google Pay'],['paypal','PayPal','Зручно для покупців з-за кордону'],['iban','Переказ на рахунок','Рахунок для компаній і ФОП']],
  note:'Коментар (необов’язково)',notePh:'Кімната, розмір стіни, побажання до доставки…',
  next:'Далі',back:'Назад',send:'Надіслати замовлення',sending:'Надсилаю…',
  fine:'Надсилаючи замовлення, ви погоджуєтесь, що дані використовуються лише для його оформлення. Зараз ви нічого не платите.',
  size:'Розмір',fin:'Виконання',frame:'Рама',price:'Робота',ship:'Доставка',shipV:'після підтвердження',total:'Разом',plus:' + доставка',
  ed:'Тираж 10 · підпис · сертифікат автентичності',edit:'Змінити',
  req:'Заповніть це поле',bad:{email:'Схоже, в адресі бракує @ або крапки — перевірте, будь ласка.',phone:'Вкажіть повний номер, наприклад +380 67 123 45 67'},
  okH:'Замовлення прийнято',okP:'Дякую! Я особисто перевірю тираж, розрахую доставку на вашу адресу й надішлю посилання на оплату.',
  okMail:'Відкрився лист із готовим замовленням — просто натисніть «Надіслати».',
  okNo:'Номер замовлення',okSteps:['Підтверджую наявність і вартість доставки','Ви оплачуєте за безпечним посиланням','Роботу друкуємо, підписуємо й відправляємо з трекінгом'],
  okBack:'Повернутися до галереї',err:'Не вдалося надіслати замовлення. Перевірте з’єднання й спробуйте ще раз — або напишіть на '+MAIL,
  mailSubj:'Замовлення',summary:'Ваше замовлення'
};
var FRAME={natural:['#d9b58a','#b98d5e','#8a6340'],oak:['#6b4628','#4a2f1a','#2e1c0f'],ebony:['#2a211b','#17110d','#0b0806'],coal:['#4b4a47','#2b2a28','#171615']};
var COUNTRIES='UA PL DE GB US CA FR IT ES NL BE AT CH CZ SK HU RO MD LT LV EE FI SE NO DK IE PT GR BG HR SI IL AE TR GE AU NZ JP KR SG'.split(' ');

var css=`
.co{position:fixed;inset:0;z-index:80;display:grid;place-items:center;padding:clamp(0px,3vw,40px);visibility:hidden;pointer-events:none}
.co.on{visibility:visible;pointer-events:auto}
.co-bg{position:absolute;inset:0;background:rgba(5,4,3,.84);-webkit-backdrop-filter:blur(14px) saturate(.8);backdrop-filter:blur(14px) saturate(.8);opacity:0;transition:opacity .5s var(--ease)}
.co.on .co-bg{opacity:1}
.co-p{position:relative;display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1fr);width:min(1120px,100%);height:min(760px,100%);border-radius:30px;overflow:hidden;
  background:linear-gradient(150deg,#1a1410,#0e0b09 55%,#120d09);box-shadow:0 40px 120px rgba(0,0,0,.7),inset 1px 1px 1px rgba(255,236,214,.06),inset -1px -1px 2px rgba(0,0,0,.4);
  opacity:0;transform:translateY(28px) scale(.985);transition:opacity .5s var(--ease),transform .7s var(--ease)}
.co.on .co-p{opacity:1;transform:none}
.co ::selection{background:rgba(255,166,48,.35);color:#fff}
/* left: the work itself */
.co-s{position:relative;display:flex;flex-direction:column;gap:22px;padding:clamp(28px,3.4vw,48px);background:radial-gradient(120% 80% at 50% 30%,rgba(255,150,40,.10),transparent 60%),#0b0907;border-right:1px solid rgba(255,236,214,.06);overflow:auto;scrollbar-width:none}
.co-s::-webkit-scrollbar{display:none}
.co-wall{flex:1 1 0;min-height:240px;display:grid;place-items:center;container-type:size;margin:6px 0 4px}
.co-art{position:relative;box-sizing:border-box;height:min(100cqh,440px);width:auto;max-width:100cqw;aspect-ratio:var(--ar,2/3);transition:padding .6s var(--ease),box-shadow .6s var(--ease),background .6s}
.co-art img{display:block;width:100%;height:100%;object-fit:cover;border-radius:1px}
.co-art[data-f=framed]{padding:8px;background:linear-gradient(135deg,var(--f1),var(--f2) 45%,var(--f3));box-shadow:0 30px 60px rgba(0,0,0,.6),0 10px 18px rgba(0,0,0,.45),inset 1px 1px 0 rgba(255,255,255,.16),inset -1px -1px 0 rgba(0,0,0,.5),0 0 0 1px rgba(255,236,214,.07)}
.co-art[data-f=framed] img{box-shadow:inset 0 0 0 1px rgba(0,0,0,.4),0 0 0 1px rgba(0,0,0,.35)}
.co-art[data-f=stretched]{box-shadow:0 26px 50px rgba(0,0,0,.6),6px 8px 0 -2px rgba(0,0,0,.35)}
.co-art[data-f=rolled]{box-shadow:0 18px 40px rgba(0,0,0,.5)}
.co-art[data-f=rolled] img{border-radius:2px}
.co-glow{position:absolute;inset:auto 10% -14% 10%;height:30%;background:radial-gradient(closest-side,rgba(255,160,50,.16),transparent);pointer-events:none;z-index:-1}
.co-t{font-family:var(--head);font-weight:400;text-transform:uppercase;font-size:clamp(28px,2.6vw,40px);line-height:.95;color:var(--cream)}
.co-t,.co-ed{text-align:center}
.co-ed{margin-top:8px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.co-rows{display:grid;gap:10px;padding-top:16px;border-top:1px solid rgba(255,236,214,.08);font-size:14px}
.co-rows div{display:flex;justify-content:space-between;gap:16px}
.co-rows dt{color:var(--muted)}.co-rows dd{color:var(--cream);text-align:right}
.co-rows .tot{padding-top:12px;margin-top:4px;border-top:1px solid rgba(255,236,214,.08);align-items:baseline}
.co-rows .tot dd{font-family:var(--head);font-size:30px;color:var(--amber);font-variant-numeric:tabular-nums}
.co-rows .tot small{font-family:var(--body);font-size:13px;color:var(--muted);margin-left:4px}
.co-edit{align-self:flex-start;background:none;border:0;padding:4px 0;color:var(--amber);font:inherit;font-size:12px;letter-spacing:.16em;text-transform:uppercase;border-bottom:1px solid rgba(255,166,48,.4);cursor:pointer;transition:color .3s,border-color .3s}
.co-edit:hover{color:var(--sand);border-color:var(--sand)}
/* right: steps */
.co-f{position:relative;display:grid;grid-template-rows:auto minmax(0,1fr) auto;min-height:0}
.co-top{display:flex;align-items:center;gap:18px;padding:26px clamp(24px,3.4vw,48px) 0}
.co-pr{flex:1;display:flex;gap:6px;list-style:none;margin:0;padding:0;counter-reset:s}
.co-pr li{flex:1;display:grid;gap:9px;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:rgba(241,224,197,.42);transition:color .4s}
.co-pr li::before{content:"";height:3px;border-radius:3px;background:rgba(255,236,214,.09);background-image:linear-gradient(90deg,var(--amber),#ffc46b);background-size:0 100%;background-repeat:no-repeat;transition:background-size .7s var(--ease)}
.co-pr li.on,.co-pr li.done{color:var(--cream)}.co-pr li.on::before,.co-pr li.done::before{background-size:100% 100%}
.co-x{flex:none;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,236,214,.12);background:rgba(0,0,0,.2);color:var(--cream);display:grid;place-items:center;cursor:pointer;transition:border-color .3s,color .3s}
.co-x:hover,.co-x:focus-visible{border-color:var(--amber);color:var(--amber);outline:0}
.co-x svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round}
.co-body{position:relative;overflow:auto;overscroll-behavior:contain;padding:30px clamp(24px,3.4vw,48px) 24px;scrollbar-width:thin;scrollbar-color:rgba(255,166,48,.35) transparent}
.co-step{display:none;flex-direction:column;gap:18px}
.co-step.on{display:flex;animation:coIn .55s var(--ease) both}
.co-step.back{animation-name:coInB}
@keyframes coIn{from{opacity:0;transform:translateX(26px);filter:blur(4px)}}
@keyframes coInB{from{opacity:0;transform:translateX(-26px);filter:blur(4px)}}
.co h3{font-family:var(--head);font-weight:400;text-transform:uppercase;font-size:clamp(30px,3vw,44px);line-height:.95;color:var(--cream);text-wrap:balance}
.co h3:focus,.co-ok:focus{outline:0}
.co-sub{margin-top:-6px;color:var(--muted);font-size:15px;line-height:1.6;max-width:46ch}
.co-g{display:grid;grid-template-columns:1fr 1fr;gap:14px 14px}
.co-g>.w{grid-column:1/-1}
.co-fl{position:relative;display:grid;gap:7px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.co-fl input,.co-fl select,.co-fl textarea{width:100%;min-height:52px;padding:14px 16px;border-radius:14px;border:1px solid rgba(255,236,214,.07);background:rgba(0,0,0,.28);color:var(--cream);font:400 16px/1.4 var(--body);letter-spacing:0;text-transform:none;
  box-shadow:inset 3px 3px 7px rgba(0,0,0,.45),inset -2px -2px 5px rgba(255,236,214,.025);caret-color:var(--amber);transition:border-color .3s,box-shadow .3s,background .3s;-webkit-appearance:none;appearance:none}
.co-fl textarea{min-height:92px;resize:vertical}
.co-fl select{padding-right:44px;background-image:var(--chev);background-repeat:no-repeat;background-position:right 18px center;background-size:8px 13px;cursor:pointer}
.co-fl select option{background:#16110d;color:var(--cream)}
.co-fl input::placeholder,.co-fl textarea::placeholder{color:rgba(241,224,197,.38)}
.co-fl input:focus,.co-fl select:focus,.co-fl textarea:focus{outline:0;border-color:rgba(255,166,48,.6);box-shadow:inset 3px 3px 7px rgba(0,0,0,.45),0 0 0 4px rgba(255,166,48,.12)}
.co-fl.bad input,.co-fl.bad select{border-color:rgba(255,120,90,.7)}
.co-fl .er{min-height:0;font-size:13px;letter-spacing:0;text-transform:none;color:#ff9b7d;line-height:1.4}
.co-fl .er:empty{display:none}
.co-fl .hn{font-size:12px;letter-spacing:0;text-transform:none;color:rgba(241,224,197,.5)}
.co-fl input:-webkit-autofill{-webkit-text-fill-color:var(--cream);-webkit-box-shadow:inset 0 0 0 60px #1a140f;caret-color:var(--amber)}
/* segmented choice + payment cards */
.co-seg{display:grid;grid-template-columns:repeat(var(--n,2),1fr);gap:6px;padding:5px;border-radius:16px;background:rgba(0,0,0,.28);box-shadow:inset 3px 3px 7px rgba(0,0,0,.45)}
.co-seg label{position:relative;display:grid;place-items:center;min-height:44px;padding:8px 10px;border-radius:12px;font-size:14px;color:var(--muted);text-align:center;cursor:pointer;transition:color .3s,background .35s,box-shadow .35s}
.co-seg input,.co-pay input,.co-chk input{position:absolute;opacity:0;pointer-events:none}
.co-seg label:has(input:checked){color:var(--cream);background:linear-gradient(145deg,#2a2018,#1a140f);box-shadow:4px 5px 12px rgba(0,0,0,.45),inset 1px 1px 1px rgba(255,236,214,.07)}
.co-seg label:has(input:focus-visible),.co-pay label:has(input:focus-visible),.co-chk:has(input:focus-visible){outline:2px solid rgba(255,166,48,.7);outline-offset:2px}
.co-pay{display:grid;gap:10px}
.co-pay label{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:16px;padding:16px 18px;border-radius:18px;border:1px solid rgba(255,236,214,.07);background:linear-gradient(145deg,rgba(255,236,214,.035),rgba(255,236,214,.008));cursor:pointer;transition:border-color .35s,background .35s,transform .2s}
.co-pay label:hover{border-color:rgba(255,166,48,.3)}
.co-pay label:has(input:checked){border-color:rgba(255,166,48,.65);background:linear-gradient(145deg,rgba(255,166,48,.09),rgba(255,166,48,.02))}
.co-pay b{display:block;font-weight:500;font-size:16px;color:var(--cream)}
.co-pay small{display:block;margin-top:3px;font-size:13px;color:var(--muted);line-height:1.45}
.co-pay i{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:rgba(0,0,0,.3);box-shadow:inset 2px 2px 5px rgba(0,0,0,.5);color:var(--amber)}
.co-pay i svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.co-pay .rd{width:20px;height:20px;border-radius:50%;border:1.5px solid rgba(255,236,214,.25);transition:border-color .3s,box-shadow .3s}
.co-pay label:has(input:checked) .rd{border-color:var(--amber);box-shadow:inset 0 0 0 4px #1a130c,inset 0 0 0 10px var(--amber)}
.co-chk{position:relative;display:flex;align-items:flex-start;gap:14px;padding:14px 16px;border-radius:16px;background:rgba(0,0,0,.2);cursor:pointer}
.co-chk .bx{flex:none;width:22px;height:22px;margin-top:1px;border-radius:7px;border:1.5px solid rgba(255,236,214,.25);display:grid;place-items:center;transition:background .3s,border-color .3s}
.co-chk .bx svg{width:13px;height:13px;fill:none;stroke:var(--ink);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:20;stroke-dashoffset:20;transition:stroke-dashoffset .35s var(--ease)}
.co-chk:has(input:checked) .bx{background:var(--amber);border-color:var(--amber)}.co-chk:has(input:checked) .bx svg{stroke-dashoffset:0}
.co-chk b{display:block;font-weight:500;color:var(--cream);font-size:15px}.co-chk small{display:block;margin-top:2px;color:var(--muted);font-size:13px;line-height:1.45}
.co-hide{display:grid;grid-template-rows:0fr;transition:grid-template-rows .5s var(--ease),opacity .4s;opacity:0}
.co-hide>div{min-height:0;overflow:hidden}
.co-hide.on{grid-template-rows:1fr;opacity:1}
.co-hide.on>div{overflow:visible}
.co-fine{font-size:13px;line-height:1.55;color:rgba(241,224,197,.5);max-width:52ch}
/* bottom bar */
.co-bar{display:flex;align-items:center;gap:12px;padding:16px clamp(24px,3.4vw,48px) calc(18px + env(safe-area-inset-bottom));border-top:1px solid rgba(255,236,214,.06);background:linear-gradient(180deg,rgba(14,11,9,.6),#0e0b09)}
.co-bk{min-height:52px;padding:0 22px;border-radius:99px;border:1px solid rgba(255,236,214,.12);background:none;color:var(--cream);font:500 13px var(--body);letter-spacing:.16em;text-transform:uppercase;cursor:pointer;transition:border-color .3s,color .3s,opacity .3s}
.co-bk:hover,.co-bk:focus-visible{border-color:var(--amber);color:var(--amber);outline:0}
.co-bk[hidden]{display:none}
.co-go{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:12px;min-height:56px;padding:0 26px;border:0;border-radius:99px;background:linear-gradient(145deg,#ffb24a,#f29a2b);color:var(--ink);font:500 13px var(--body);letter-spacing:.16em;text-transform:uppercase;cursor:pointer;
  box-shadow:0 12px 28px rgba(242,154,43,.22),inset 1px 1px 1px rgba(255,255,255,.35);transition:box-shadow .4s,transform .2s,filter .3s}
.co-go:hover{box-shadow:0 16px 36px rgba(242,154,43,.34),inset 1px 1px 1px rgba(255,255,255,.4)}
.co-go:active{transform:translateY(1px)}
.co-go:focus-visible{outline:2px solid rgba(255,166,48,.8);outline-offset:4px}
.co-go[disabled]{cursor:progress;filter:saturate(.6) brightness(.85)}
.co-go .ar{width:1.25em;height:.7em;background:currentColor;-webkit-mask:var(--arrow) center/contain no-repeat;mask:var(--arrow) center/contain no-repeat;transition:transform .4s var(--ease)}
.co-go:hover .ar{transform:translateX(4px)}
.co-go .sp{width:18px;height:18px;border-radius:50%;border:2px solid rgba(1,17,10,.25);border-top-color:var(--ink);animation:coSp .8s linear infinite}
@keyframes coSp{to{transform:rotate(360deg)}}
.co-msg{color:#ff9b7d;font-size:14px;line-height:1.5}
.co-msg:empty{display:none}
/* done */
.co-ok{display:none;flex-direction:column;gap:20px}
.co-ok.on{display:flex;animation:coIn .6s var(--ease) both}
.co-okh{display:flex;align-items:center;gap:16px}
.co-seal{flex:none;width:.95em;height:.95em;font-size:clamp(30px,3vw,44px);border-radius:50%;display:grid;place-items:center;border:1px solid rgba(255,166,48,.55);background:rgba(255,166,48,.06);box-shadow:inset 0 0 14px rgba(255,166,48,.12)}
.co-seal svg{width:52%;height:52%;fill:none;stroke:var(--amber);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:40;stroke-dashoffset:40;animation:coTick .7s .25s var(--ease) forwards}
@keyframes coTick{to{stroke-dashoffset:0}}
.co-no{display:inline-flex;gap:14px;align-items:baseline;padding:12px 18px;border-radius:14px;background:rgba(0,0,0,.28);box-shadow:inset 3px 3px 7px rgba(0,0,0,.45);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);align-self:flex-start}
.co-no{flex-wrap:wrap;row-gap:4px}.co-no b{white-space:nowrap;font:500 16px var(--body);letter-spacing:.08em;color:var(--amber);font-variant-numeric:tabular-nums}
.co-tl{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:0;counter-reset:t}
.co-tl li{position:relative;display:flex;gap:16px;padding:0 0 18px;color:var(--cream);font-size:15px;line-height:1.5;counter-increment:t}
.co-tl li::before{content:counter(t);flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-size:13px;color:var(--amber);border:1px solid rgba(255,166,48,.45);background:#120d09;position:relative;z-index:1}
.co-tl li:not(:last-child)::after{content:"";position:absolute;left:15px;top:30px;bottom:0;width:1px;background:linear-gradient(rgba(255,166,48,.45),rgba(255,166,48,.08))}
.co-tl li span{padding-top:4px}
/* mini summary (phones) */
.co-mini{display:none}
@media(max-width:899px){
  .co{padding:0;place-items:end stretch}
  .co-p{grid-template-columns:1fr;grid-template-rows:auto minmax(0,1fr);width:100%;height:100%;height:100dvh;border-radius:0;transform:translateY(40px)}
  .co-s{display:none}
  .co-f{grid-row:1/3}
  .co-top{padding:max(14px,env(safe-area-inset-top)) 18px 0}
  .co-mini{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:14px;margin:16px 18px 0;padding:10px 12px 10px 10px;border-radius:18px;background:rgba(0,0,0,.25);box-shadow:inset 3px 3px 7px rgba(0,0,0,.45);text-align:left;border:0;color:inherit;font:inherit;width:calc(100% - 36px)}
  .co-mini img{width:48px;height:60px;object-fit:cover;border-radius:4px}
  .co-mini b{display:block;font-family:var(--head);font-weight:400;text-transform:uppercase;font-size:20px;line-height:1;color:var(--cream)}
  .co-mini small{display:block;margin-top:5px;font-size:12px;color:var(--muted);line-height:1.35}
  .co-mini .pv{font-family:var(--head);font-size:24px;color:var(--amber);font-variant-numeric:tabular-nums}
  .co-body{padding:24px 18px 20px}
  .co-bar{padding:12px 18px calc(12px + env(safe-area-inset-bottom))}
  .co-g{grid-template-columns:1fr}
  .co-pr li{font-size:10px;letter-spacing:.12em}
  .co-go,.co-bk{letter-spacing:.1em;white-space:nowrap}.co-go{padding:0 18px}.co-bk{padding:0 18px}
}
@media(max-width:899px){.co-f{grid-template-rows:auto auto minmax(0,1fr) auto}}
@media(prefers-reduced-motion:reduce){.co *,.co *::before{animation-duration:.01ms!important;transition-duration:.01ms!important}}
`;

var ICON={card:'<svg viewBox="0 0 24 24"><rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3 10h18M7 15h3"/></svg>',
  paypal:'<svg viewBox="0 0 24 24"><path d="M8 20l1.2-7h4.3c3.2 0 5.3-1.8 5.7-4.6.4-2.6-1.4-4.4-4.3-4.4H8.6L6 20"/><path d="M11 13l.7-4h2.2"/></svg>',
  iban:'<svg viewBox="0 0 24 24"><path d="M4 9.5L12 5l8 4.5M5 10v7M9.5 10v7M14.5 10v7M19 10v7M3.5 19.5h17"/></svg>'};
var X='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
var TICK='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7"/></svg>';

var root,st=0,ord=null,lastFocus=null,built=false;
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fld(id,lab,attrs,w,hint){return '<label class="co-fl'+(w?' w':'')+'" data-f="'+id+'">'+lab+'<input id="co-'+id+'" name="'+id+'" '+attrs+'>'+(hint?'<span class="hn">'+hint+'</span>':'')+'<span class="er" aria-live="polite"></span></label>'}
function countryOpts(){var dn=null;try{dn=new Intl.DisplayNames([EN?'en':'uk'],{type:'region'})}catch(e){}
  var n=function(c){return dn?dn.of(c):c};var rest=COUNTRIES.slice(1).sort(function(a,b){return n(a).localeCompare(n(b),EN?'en':'uk')});
  return ['UA'].concat(rest).map(function(c){return '<option value="'+c+'">'+esc(n(c))+'</option>'}).join('')+'<option value="OTHER">'+(EN?'Other country':'Інша країна')+'</option>'}

function build(){
  var s=document.createElement('style');s.textContent=css;document.head.appendChild(s);
  root=document.createElement('div');root.className='co';root.setAttribute('role','dialog');root.setAttribute('aria-modal','true');root.setAttribute('aria-labelledby','co-h');root.hidden=true;
  root.innerHTML='<div class="co-bg"></div><div class="co-p">'
   +'<aside class="co-s" aria-label="'+T.summary+'"><div class="co-wall"><div class="co-art"><img alt=""><span class="co-glow"></span></div></div>'
   +'<div><p class="co-t"></p><p class="co-ed">'+T.ed+'</p></div><dl class="co-rows"></dl><button class="co-edit" type="button">'+T.edit+'</button></aside>'
   +'<div class="co-f"><div class="co-top"><ol class="co-pr">'+T.steps.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ol><button class="co-x" type="button" aria-label="'+T.close+'">'+X+'</button></div>'
   +'<button class="co-mini" type="button" aria-label="'+T.edit+'"><img alt=""><span><b></b><small></small></span><span class="pv"></span></button>'
   +'<form class="co-body" novalidate>'
   // step 1
   +'<section class="co-step" data-s="0"><h3 id="co-h">'+T.h[0]+'</h3><p class="co-sub">'+T.sub[0]+'</p><div class="co-g">'
   +fld('name',T.name,'autocomplete="name" required',1)
   +fld('email',T.email,'type="email" autocomplete="email" inputmode="email" required spellcheck="false"')
   +fld('phone',T.phone,'type="tel" autocomplete="tel" inputmode="tel" required placeholder="+380"',0,T.phoneHint)
   +'</div></section>'
   // step 2
   +'<section class="co-step" data-s="1"><h3>'+T.h[1]+'</h3><p class="co-sub">'+T.sub[1]+'</p><div class="co-g">'
   +'<label class="co-fl w" data-f="country">'+T.country+'<select id="co-country" name="country" autocomplete="country">'+countryOpts()+'</select><span class="er"></span></label>'
   +'<div class="co-hide w" data-when="other"><div>'+fld('countryOther',EN?'Which country?':'Яка країна?','autocomplete="country-name"',1)+'</div></div>'
   +fld('city',T.city,'autocomplete="address-level2" required',1)
   +'<div class="co-hide w on" data-when="ua"><div class="co-g" style="padding-top:2px">'
   +'<div class="co-seg w" role="radiogroup" aria-label="'+T.np+'"><label><input type="radio" name="npType" value="branch" checked>'+T.np+' · '+T.npBranch.toLowerCase()+'</label><label><input type="radio" name="npType" value="courier">'+T.npCourier+'</label></div>'
   +'<div class="co-hide w on" data-when="branch"><div>'+fld('branch',T.branch,'inputmode="numeric" placeholder="'+T.branchPh+'"',1)+'</div></div>'
   +'</div></div>'
   +'<div class="co-hide w" data-when="addr"><div class="co-g" style="padding-top:2px">'
   +fld('addr',T.addr,'autocomplete="address-line1"',1)
   +'<div class="co-hide w" data-when="intl"><div class="co-g">'+fld('addr2',T.addr2,'autocomplete="address-line2"',1)+fld('region',T.region,'autocomplete="address-level1"')+fld('zip',T.zip,'autocomplete="postal-code"')+'</div></div>'
   +'</div></div>'
   +'<label class="co-chk w"><input type="checkbox" name="gift"><span class="bx">'+TICK+'</span><span><b>'+T.gift+'</b><small>'+T.giftNote+'</small></span></label>'
   +'<div class="co-hide w" data-when="gift"><div><label class="co-fl w">'+T.giftMsg+'<textarea name="giftMsg" rows="2"></textarea></label></div></div>'
   +'</div></section>'
   // step 3
   +'<section class="co-step" data-s="2"><h3>'+T.h[2]+'</h3><p class="co-sub">'+T.sub[2]+'</p>'
   +'<div class="co-pay" role="radiogroup" aria-label="'+T.steps[2]+'">'+T.pay.map(function(p,k){return '<label><input type="radio" name="pay" value="'+p[0]+'"'+(k?'':' checked')+'><i>'+ICON[p[0]]+'</i><span><b>'+p[1]+'</b><small>'+p[2]+'</small></span><span class="rd"></span></label>'}).join('')+'</div>'
   +'<label class="co-fl w">'+T.note+'<textarea name="note" rows="3" placeholder="'+T.notePh+'"></textarea></label>'
   +'<p class="co-fine">'+T.fine+'</p></section>'
   // done
   +'<section class="co-ok" tabindex="-1"><div class="co-okh"><span class="co-seal">'+TICK+'</span><h3>'+T.okH+'</h3></div><p class="co-sub co-okp"></p><p class="co-no">'+T.okNo+' <b></b></p><ol class="co-tl">'+T.okSteps.map(function(x){return '<li><span>'+x+'</span></li>'}).join('')+'</ol></section>'
   +'<p class="co-msg" role="alert"></p>'
   +'</form>'
   +'<div class="co-bar"><button class="co-bk" type="button" hidden>'+T.back+'</button><button class="co-go" type="button"><span class="lb">'+T.next+'</span><i class="ar" aria-hidden="true"></i></button></div>'
   +'</div></div>';
  document.body.appendChild(root);
  var f=root.querySelector('form');
  root.querySelector('.co-bg').onclick=close;root.querySelector('.co-x').onclick=close;
  root.querySelector('.co-edit').onclick=close;root.querySelector('.co-mini').onclick=close;
  root.querySelector('.co-bk').onclick=function(){go(st-1)};
  root.querySelector('.co-go').onclick=next;
  f.addEventListener('submit',function(e){e.preventDefault();next()});
  f.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.tagName==='INPUT'){e.preventDefault();next()}});
  f.addEventListener('change',function(e){toggles();save();if(e.target.closest('.co-fl.bad'))check(e.target)});
  f.addEventListener('input',function(e){var l=e.target.closest('.co-fl.bad');if(l)check(e.target);});
  f.addEventListener('focusout',function(e){if(e.target.value)check(e.target)});
  root.addEventListener('keydown',function(e){
    if(e.key==='Escape'){e.stopPropagation();e.preventDefault();close();return}
    if(e.key==='Tab'){var q=[].filter.call(root.querySelectorAll('button,input,select,textarea,[tabindex="0"]'),function(x){return x.offsetParent!==null&&!x.disabled});if(!q.length)return;
      var a=q[0],b=q[q.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();b.focus()}else if(!e.shiftKey&&document.activeElement===b){e.preventDefault();a.focus()}}
  },true);
  restore();toggles();built=true}

function val(n){var f=root.querySelector('form'),e=f.elements[n];if(!e)return '';if(e.length&&!e.tagName){for(var i=0;i<e.length;i++)if(e[i].checked)return e[i].value;return ''}return e.type==='checkbox'?e.checked:String(e.value||'').trim()}
function toggles(){var c=val('country'),ua=c==='UA',cour=val('npType')==='courier';
  var on=function(k,v){var x=root.querySelector('[data-when="'+k+'"]');x.classList.toggle('on',!!v);x.querySelectorAll('input,textarea').forEach(function(i){i.tabIndex=v?0:-1})};
  on('other',c==='OTHER');on('ua',ua);on('branch',ua&&!cour);on('addr',!ua||cour);on('intl',!ua);on('gift',val('gift'));
  // a hidden block inside a shown block keeps its own state
  if(!ua){root.querySelector('[data-when="branch"]').classList.remove('on')}
}
var RULES={name:function(v){return v.length>1},email:function(v){return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)},phone:function(v){return v.replace(/\D/g,'').length>=9}};
function need(n){var c=val('country'),ua=c==='UA',cour=val('npType')==='courier';
  if(n==='branch')return ua&&!cour; if(n==='addr')return !ua||cour; if(n==='zip')return !ua; if(n==='countryOther')return c==='OTHER';
  return ['name','email','phone','city'].indexOf(n)>-1}
function check(inp){var l=inp.closest('.co-fl');if(!l||!l.dataset.f)return true;var n=l.dataset.f,v=String(inp.value||'').trim(),msg='';
  if(!v){if(need(n))msg=T.req}else if(RULES[n]&&!RULES[n](v))msg=T.bad[n]||T.req;
  l.classList.toggle('bad',!!msg);l.querySelector('.er').textContent=msg;inp.setAttribute('aria-invalid',msg?'true':'false');return !msg}
function valid(s){var sec=root.querySelector('.co-step[data-s="'+s+'"]'),ok=true,first=null;
  sec.querySelectorAll('.co-fl[data-f] input').forEach(function(i){if(i.closest('.co-hide:not(.on)'))return;if(!check(i)){ok=false;first=first||i}});
  if(first)first.focus();return ok}
function go(s,dir){var prev=st;st=Math.max(0,Math.min(2,s));var back=st<prev;
  root.querySelectorAll('.co-step').forEach(function(x,k){x.classList.toggle('on',k===st);x.classList.toggle('back',k===st&&back)});
  root.querySelector('.co-ok').classList.remove('on');
  root.querySelectorAll('.co-pr li').forEach(function(x,k){x.classList.toggle('on',k===st);x.classList.toggle('done',k<st);if(k===st)x.setAttribute('aria-current','step');else x.removeAttribute('aria-current')});
  root.querySelector('.co-bk').hidden=st===0;
  root.querySelector('.co-go .lb').textContent=st===2?T.send:T.next;
  root.querySelector('.co-msg').textContent='';
  root.querySelector('.co-body').scrollTop=0;
  if(prev!==st){var h=root.querySelector('.co-step.on h3');h.tabIndex=-1;h.focus({preventScroll:true})}}
function next(){if(root.classList.contains('done')){close();return}
  if(!valid(st))return;if(st<2){go(st+1);return}send()}

function money(n){return '$'+Number(n).toLocaleString('en-US')}
function summary(){var o=ord,a=root.querySelector('.co-art'),fr=FRAME[o.frameId]||FRAME.oak;
  a.dataset.f=o.finId;a.style.setProperty('--f1',fr[0]);a.style.setProperty('--f2',fr[1]);a.style.setProperty('--f3',fr[2]);
  var m=/(\d+)\s*[×x]\s*(\d+)/.exec(o.size||'');a.style.setProperty('--ar','4/5');
  a.querySelector('img').src=o.img;a.querySelector('img').alt=o.title;
  root.querySelector('.co-t').textContent=o.title;
  var rows=[[T.size,o.size],[T.fin,o.fin]];if(o.finId==='framed'&&o.frame)rows.push([T.frame,o.frame]);
  rows.push([T.price,money(o.price)],[T.ship,T.shipV]);
  root.querySelector('.co-rows').innerHTML=rows.map(function(r){return '<div><dt>'+esc(r[0])+'</dt><dd>'+esc(r[1])+'</dd></div>'}).join('')
    +'<div class="tot"><dt>'+T.total+'</dt><dd>'+money(o.price)+'<small>'+T.plus+'</small></dd></div>';
  var mi=root.querySelector('.co-mini');mi.querySelector('img').src=o.thumb||o.img;mi.querySelector('b').textContent=o.title;
  mi.querySelector('small').textContent=[o.size&&o.size.split('(')[0].trim(),o.finId==='framed'?o.frame:o.fin].filter(Boolean).join(' · ');
  mi.querySelector('.pv').textContent=money(o.price)}

var KEY='mv-checkout';
function save(){try{var f=root.querySelector('form'),d={};['name','email','phone','country','countryOther','city','branch','addr','addr2','region','zip','npType'].forEach(function(n){d[n]=val(n)});localStorage.setItem(KEY,JSON.stringify(d))}catch(e){}}
function restore(){try{var d=JSON.parse(localStorage.getItem(KEY)||'null');if(!d)return;var f=root.querySelector('form');
  Object.keys(d).forEach(function(n){var e=f.elements[n];if(!e||!d[n])return;if(e.length&&!e.tagName){[].forEach.call(e,function(r){r.checked=r.value===d[n]})}else e.value=d[n]})}catch(e){}}

function orderNo(){var d=new Date(),p=function(n){return String(n).padStart(2,'0')};return 'MV-'+String(d.getFullYear()).slice(2)+p(d.getMonth()+1)+p(d.getDate())+'-'+Math.random().toString(36).slice(2,6).toUpperCase()}
function payload(no){var c=val('country'),cn=c==='OTHER'?val('countryOther'):(root.querySelector('#co-country').selectedOptions[0]||{}).text;
  var ua=c==='UA',cour=val('npType')==='courier',pay=T.pay.filter(function(p){return p[0]===val('pay')})[0];
  var addr=ua?(cour?(T.npCourier+': '+val('addr')):(T.np+', '+T.npBranch.toLowerCase()+' №'+val('branch'))):[val('addr'),val('addr2'),val('region'),val('zip')].filter(Boolean).join(', ');
  return {order:no,work:ord.title,url:ord.url,size:ord.size,finish:ord.fin,frame:ord.finId==='framed'?ord.frame:'',price_usd:ord.price,
    name:val('name'),email:val('email'),phone:val('phone'),country:cn,city:val('city'),delivery:addr,
    gift:val('gift')?(EN?'yes':'так'):'',gift_message:val('giftMsg'),payment:pay?pay[1]:'',comment:val('note'),lang:EN?'en':'uk'}}
function asText(p){var L=EN?{order:'Order',work:'Work',url:'Link',size:'Size',finish:'Finish',frame:'Frame',price_usd:'Price, USD',name:'Name',email:'E-mail',phone:'Phone',country:'Country',city:'City',delivery:'Delivery',gift:'Gift',gift_message:'Card text',payment:'Payment',comment:'Comment'}
  :{order:'Замовлення',work:'Робота',url:'Посилання',size:'Розмір',finish:'Виконання',frame:'Рама',price_usd:'Ціна, USD',name:'Ім’я',email:'Email',phone:'Телефон',country:'Країна',city:'Місто',delivery:'Доставка',gift:'Подарунок',gift_message:'Текст листівки',payment:'Оплата',comment:'Коментар'};
  return Object.keys(L).filter(function(k){return p[k]}).map(function(k){return L[k]+': '+p[k]}).join('\n')}
function send(){var b=root.querySelector('.co-go'),no=orderNo(),p=payload(no),msg=root.querySelector('.co-msg');msg.textContent='';
  save();
  if(!ENDPOINT){location.href='mailto:'+MAIL+'?subject='+encodeURIComponent(T.mailSubj+' '+no+' — '+p.work)+'&body='+encodeURIComponent(asText(p)+'\n');done(no,true);return}
  b.disabled=true;b.querySelector('.lb').textContent=T.sending;var ar=b.querySelector('.ar');ar.className='sp';
  fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(Object.assign({_subject:T.mailSubj+' '+no+' — '+p.work,_replyto:p.email,message:asText(p)},p))})
   .then(function(r){if(!r.ok)throw 0;done(no,false)})
   .catch(function(){msg.textContent=T.err})
   .then(function(){b.disabled=false;ar.className='ar';if(!root.classList.contains('done'))b.querySelector('.lb').textContent=T.send})}
function done(no,mail){root.classList.add('done');
  root.querySelectorAll('.co-step').forEach(function(x){x.classList.remove('on')});
  root.querySelectorAll('.co-pr li').forEach(function(x){x.classList.remove('on');x.classList.add('done')});
  var ok=root.querySelector('.co-ok');ok.querySelector('.co-okp').textContent=T.okP+(mail?' '+T.okMail:'');ok.querySelector('.co-no b').textContent=no;ok.classList.add('on');
  root.querySelector('.co-bk').hidden=true;root.querySelector('.co-go .lb').textContent=T.okBack;
  root.querySelector('.co-body').scrollTop=0;ok.focus({preventScroll:true});
  var g=root.querySelector('form').elements;['gift','giftMsg','note'].forEach(function(n){if(g[n]){if(g[n].type==='checkbox')g[n].checked=false;else g[n].value=''}})}

function open(o){if(!built)build();ord=o;root.classList.remove('done');summary();toggles();
  root.querySelectorAll('.co-fl.bad').forEach(function(l){l.classList.remove('bad');l.querySelector('.er').textContent=''});
  st=-1;go(0);lastFocus=document.activeElement;root.hidden=false;document.documentElement.style.overflow='hidden';
  requestAnimationFrame(function(){requestAnimationFrame(function(){root.classList.add('on');var f=root.querySelector('#co-name');if(f&&!f.value&&matchMedia('(min-width:900px)').matches)f.focus({preventScroll:true});else root.querySelector('.co-x').focus({preventScroll:true})})})}
function close(){if(!root||!root.classList.contains('on'))return;save();root.classList.remove('on');document.documentElement.style.overflow='';
  setTimeout(function(){if(!root.classList.contains('on'))root.hidden=true},500);if(lastFocus&&lastFocus.focus)lastFocus.focus({preventScroll:true})}

window.Checkout={open:open,close:close,label:T.buy};
})();

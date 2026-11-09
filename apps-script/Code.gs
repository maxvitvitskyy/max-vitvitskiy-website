/**
 * Замовлення й звернення з сайту → Google Таблиця + лист + Telegram.
 * Копія коду з Apps Script проєкту «Orders» (розгортання, версія 7).
 * Редагується в браузері; цей файл — для історії. Опис: apps-script/README.md.
 * Токен бота й chat_id — лише в Script Properties (TG_TOKEN, TG_CHAT_ID), не тут.
 */

var NOTIFY = 'maxim.vitvitskiy@gmail.com';
var SHEET = 'Замовлення';

var COLS = [
  ['received', 'Отримано'], ['order', 'Номер'], ['status', 'Статус'],
  ['work', 'Робота'], ['size', 'Розмір'], ['finish', 'Виконання'], ['frame', 'Рама'], ['price_usd', 'Ціна, USD'],
  ['name', 'Ім’я'], ['email', 'Email'], ['phone', 'Телефон'],
  ['country', 'Країна'], ['city', 'Місто'], ['delivery', 'Доставка'],
  ['gift', 'Подарунок'], ['gift_message', 'Текст листівки'],
  ['payment', 'Оплата'], ['comment', 'Коментар'], ['lang', 'Мова'], ['url', 'Сторінка роботи']
];

var MSG_SHEET = 'Звернення';
var MSG_COLS = [
  ['received', 'Отримано'], ['status', 'Статус'], ['topic', 'Тема'],
  ['name', 'Ім’я'], ['contact', 'Email / Telegram'], ['message', 'Повідомлення'],
  ['lang', 'Мова'], ['url', 'Сторінка']
];

function sheetOf_(name, cols, statuses, statusCol, index) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(name) || ss.insertSheet(name, index);
  if (sh.getLastRow() === 0) {
    sh.appendRow(cols.map(function (c) { return c[1]; }));
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, cols.length).setFontWeight('bold').setBackground('#1a140f').setFontColor('#FFA630');
    sh.getRange(2, statusCol, 999, 1).setDataValidation(SpreadsheetApp.newDataValidation()
      .requireValueInList(statuses, true).build());
  }
  return sh;
}
function sheet_() { return sheetOf_(SHEET, COLS, ['Новий', 'Підтверджено', 'Оплачено', 'Відправлено', 'Скасовано'], 3, 0); }
function msgSheet_() { return sheetOf_(MSG_SHEET, MSG_COLS, ['Новий', 'В роботі', 'Відповів', 'Закрито'], 2, 1); }

function esc_(v) { return String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

function tgSend_(text) {
  try {
    var pr = PropertiesService.getScriptProperties();
    var token = pr.getProperty('TG_TOKEN'), chat = pr.getProperty('TG_CHAT_ID');
    if (!token || !chat) return;
    UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
      method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      payload: JSON.stringify({ chat_id: chat, text: text.slice(0, 4000), parse_mode: 'HTML', disable_web_page_preview: true })
    });
  } catch (err) { console.error('telegram', err); }
}

function tgq_(s) { return '<blockquote>' + esc_(String(s).slice(0, 1500)) + '</blockquote>'; }

function telegram_(kind, d) {
  var g = function (k) { return d[k] == null ? '' : String(d[k]).trim(); };
  var flag = d.lang === 'en' ? ' 🇬🇧' : d.lang === 'uk' ? ' 🇺🇦' : '';
  var SEP = '\n\n──────────\n\n';
  var blocks = [];

  if (kind === 'order') {
    blocks.push('🧾 <b>НОВЕ ЗАМОВЛЕННЯ</b>' + flag + '\n<code>' + esc_(g('order')) + '</code>');

    var w = ['🖼 <b>РОБОТА</b>'];
    if (g('work')) w.push('<b>' + esc_(g('work')) + '</b>');
    if (g('size')) w.push('Розмір: ' + esc_(g('size')));
    if (g('finish')) w.push('Виконання: ' + esc_(g('finish')));
    if (g('frame')) w.push('Рама: ' + esc_(g('frame')));
    if (g('price_usd')) w.push('Ціна: <b>$' + esc_(g('price_usd')) + '</b>');
    blocks.push(w.join('\n'));

    var c = ['👤 <b>КЛІЄНТ</b>'];
    if (g('name')) c.push('<b>' + esc_(g('name')) + '</b>');
    if (g('email')) c.push('✉︎ ' + esc_(g('email')));
    if (g('phone')) c.push('✆ ' + esc_(g('phone')));
    if (c.length > 1) blocks.push(c.join('\n'));

    var dl = ['📦 <b>ДОСТАВКА</b>'];
    var place = [g('city'), g('country')].filter(function (s) { return s; }).join(', ');
    if (place) dl.push(esc_(place));
    if (g('delivery')) dl.push(esc_(g('delivery')));
    var gift = g('gift');
    if ((gift && !/^(ні|no|false|0)$/i.test(gift)) || g('gift_message')) {
      dl.push('\n🎁 <b>Подарунок</b>');
      if (g('gift_message')) dl.push(tgq_(g('gift_message')));
    }
    if (dl.length > 1) blocks.push(dl.join('\n'));

    if (g('payment')) blocks.push('💳 <b>ОПЛАТА</b>\n' + esc_(g('payment')));
    if (g('comment')) blocks.push('💬 <b>КОМЕНТАР</b>\n' + tgq_(g('comment')));
  } else {
    blocks.push('✉️ <b>НОВЕ ЗВЕРНЕННЯ</b>' + flag + (g('topic') ? '\n<i>' + esc_(g('topic')) + '</i>' : ''));
    var f = ['👤 <b>ВІД КОГО</b>'];
    if (g('name')) f.push('<b>' + esc_(g('name')) + '</b>');
    if (g('contact')) f.push(esc_(g('contact')));
    if (f.length > 1) blocks.push(f.join('\n'));
    if (g('message')) blocks.push('💬 <b>ПОВІДОМЛЕННЯ</b>\n' + tgq_(g('message')));
  }

  var links = [];
  if (/^https?:\/\//.test(g('url'))) links.push('🔗 <a href="' + esc_(g('url')).replace(/"/g, '&quot;') + '">Сторінка</a>');
  links.push('📊 <a href="' + SpreadsheetApp.getActiveSpreadsheet().getUrl() + '">Таблиця</a>');

  tgSend_(blocks.join(SEP) + SEP + links.join('   ·   '));
}

function row_(cols, d) {
  return cols.map(function (c) {
    var v = d[c[0]]; v = v == null ? '' : v;
    return typeof v === 'string' && /^[=+\-@]/.test(v) ? "'" + v : v;
  });
}

function contact_(d) {
  if (!d.name || !d.contact || !d.message) return out_({ ok: false, error: 'missing fields' });
  d.received = new Date();
  d.status = 'Новий';
  msgSheet_().appendRow(row_(MSG_COLS, d));
  telegram_('msg', d);
  if (NOTIFY) {
    var mail = { to: NOTIFY, subject: 'Нове звернення — ' + (d.topic || 'без теми') + ' — ' + d.name,
      body: MSG_COLS.filter(function (c) { return d[c[0]] && c[0] !== 'received'; })
        .map(function (c) { return c[1] + ': ' + d[c[0]]; }).join('\n') + '\n\nТаблиця: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl() };
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.contact)) mail.replyTo = d.contact;
    try { MailApp.sendEmail(mail); } catch (err) { console.error('mail', err); }
  }
  return out_({ ok: true });
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (d.website) return out_({ ok: true });
    if (d.type === 'contact') return contact_(d);
    if (!d.order || !d.email || !d.work) return out_({ ok: false, error: 'missing fields' });
    d.received = new Date();
    d.status = 'Новий';
    sheet_().appendRow(row_(COLS, d));
    telegram_('order', d);
    if (NOTIFY) {
      var lines = COLS.filter(function (c) { return d[c[0]] !== '' && d[c[0]] != null && c[0] !== 'received'; })
        .map(function (c) { return c[1] + ': ' + d[c[0]]; });
      try {
        MailApp.sendEmail({
          to: NOTIFY, replyTo: d.email,
          subject: 'Нове замовлення ' + d.order + ' — ' + d.work + ' ($' + d.price_usd + ')',
          body: lines.join('\n') + '\n\nТаблиця: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl()
        });
      } catch (err) { console.error('mail', err); }
    }
    return out_({ ok: true });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function setup() { sheet_(); msgSheet_(); }
function testTelegram() { tgSend_('✅ <b>Бот підключено</b>\n\nСповіщення про замовлення й звернення приходитимуть сюди'); }
function doGet() { return out_({ ok: true, service: 'orders' }); }
function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

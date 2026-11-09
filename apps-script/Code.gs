/**
 * Замовлення картин із сайту → Google Таблиця (+ лист-сповіщення).
 *
 * Як підключити (один раз):
 * 1. Створи нову Google Таблицю, наприклад «Замовлення картин».
 * 2. Розширення → Apps Script. Видали все в редакторі й встав цей файл повністю. Збережи.
 * 3. Розгорнути (Deploy) → Нове розгортання → тип «Вебзастосунок».
 *      Виконувати як: Я.   Хто має доступ: Усі.
 *    Натисни «Розгорнути», дозволь доступ своєму акаунту.
 * 4. Скопіюй URL вебзастосунку (закінчується на /exec) і передай його для сайту.
 *
 * Якщо пізніше зміниш цей код: Розгорнути → Керувати розгортаннями → олівець →
 * Версія: «Нова версія» → Розгорнути. Адреса /exec лишається та сама.
 */

var NOTIFY = 'maxim.vitvitskiy@gmail.com';   // куди надсилати лист про нове замовлення; '' — не надсилати
var SHEET = 'Замовлення';

var COLS = [
  ['received', 'Отримано'], ['order', 'Номер'], ['status', 'Статус'],
  ['work', 'Робота'], ['size', 'Розмір'], ['finish', 'Виконання'], ['frame', 'Рама'], ['price_usd', 'Ціна, USD'],
  ['name', 'Ім’я'], ['email', 'Email'], ['phone', 'Телефон'],
  ['country', 'Країна'], ['city', 'Місто'], ['delivery', 'Доставка'],
  ['gift', 'Подарунок'], ['gift_message', 'Текст листівки'],
  ['payment', 'Оплата'], ['comment', 'Коментар'], ['lang', 'Мова'], ['url', 'Сторінка роботи']
];

// Звернення з форми на головній сторінці — окремий аркуш тієї ж таблиці
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

/* Telegram: токен і chat_id лише в Script Properties (TG_TOKEN, TG_CHAT_ID), не в коді.
   Якщо Telegram не відповів — рядок у таблиці вже записаний, заявка не губиться. */
function esc_(v) { return String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function telegram_(title, cols, d) {
  try {
    var pr = PropertiesService.getScriptProperties();
    var token = pr.getProperty('TG_TOKEN'), chat = pr.getProperty('TG_CHAT_ID');
    if (!token || !chat) return;
    var lines = cols.filter(function (c) { return d[c[0]] !== '' && d[c[0]] != null && ['received', 'status', 'lang'].indexOf(c[0]) < 0; })
      .map(function (c) { return '<b>' + esc_(c[1]) + ':</b> ' + esc_(c[0] === 'price_usd' ? '$' + d[c[0]] : d[c[0]]); });
    var text = '<b>' + esc_(title) + '</b>\n\n' + lines.join('\n') + '\n\n<a href="' + SpreadsheetApp.getActiveSpreadsheet().getUrl() + '">Відкрити таблицю</a>';
    UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
      method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      payload: JSON.stringify({ chat_id: chat, text: text.slice(0, 4000), parse_mode: 'HTML', disable_web_page_preview: true })
    });
  } catch (err) { console.error('telegram', err); }
}

function row_(cols, d) {
  return cols.map(function (c) {
    var v = d[c[0]]; v = v == null ? '' : v;
    return typeof v === 'string' && /^[=+\-@]/.test(v) ? "'" + v : v;   // без формул із форми
  });
}

function contact_(d) {
  if (!d.name || !d.contact || !d.message) return out_({ ok: false, error: 'missing fields' });
  d.received = new Date();
  d.status = 'Новий';
  msgSheet_().appendRow(row_(MSG_COLS, d));
  telegram_('✉️ Нове звернення — ' + (d.topic || 'без теми'), MSG_COLS, d);
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
    if (d.website) return out_({ ok: true });                 // бот заповнив приховане поле
    if (d.type === 'contact') return contact_(d);
    if (!d.order || !d.email || !d.work) return out_({ ok: false, error: 'missing fields' });
    d.received = new Date();
    d.status = 'Новий';
    sheet_().appendRow(row_(COLS, d));
    telegram_('🖼 Нове замовлення ' + d.order + ' — ' + d.work, COLS, d);
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

function setup() { sheet_(); msgSheet_(); }   // один раз: створити аркуші й надати дозволи

// запустити з редактора після того, як TG_TOKEN і TG_CHAT_ID додано у Script Properties
function testTelegram() { telegram_('✅ Бот підключено', [['note', 'Перевірка']], { note: 'сповіщення про замовлення й звернення приходитимуть сюди' }); }

function doGet() { return out_({ ok: true, service: 'orders' }); }

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

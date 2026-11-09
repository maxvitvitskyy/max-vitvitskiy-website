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

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET) || ss.insertSheet(SHEET, 0);
  if (sh.getLastRow() === 0) {
    sh.appendRow(COLS.map(function (c) { return c[1]; }));
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, COLS.length).setFontWeight('bold').setBackground('#1a140f').setFontColor('#FFA630');
    var st = sh.getRange(2, 3, 999, 1);
    st.setDataValidation(SpreadsheetApp.newDataValidation()
      .requireValueInList(['Новий', 'Підтверджено', 'Оплачено', 'Відправлено', 'Скасовано'], true).build());
  }
  return sh;
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (d.website) return out_({ ok: true });                 // бот заповнив приховане поле
    if (!d.order || !d.email || !d.work) return out_({ ok: false, error: 'missing fields' });
    d.received = new Date();
    d.status = 'Новий';
    var row = COLS.map(function (c) {
      var v = d[c[0]];
      v = v == null ? '' : v;
      return typeof v === 'string' && /^[=+\-@]/.test(v) ? "'" + v : v;   // без формул із форми
    });
    sheet_().appendRow(row);
    if (NOTIFY) {
      var lines = COLS.filter(function (c) { return d[c[0]] !== '' && d[c[0]] != null && c[0] !== 'received'; })
        .map(function (c) { return c[1] + ': ' + d[c[0]]; });
      MailApp.sendEmail({
        to: NOTIFY, replyTo: d.email,
        subject: 'Нове замовлення ' + d.order + ' — ' + d.work + ' ($' + d.price_usd + ')',
        body: lines.join('\n') + '\n\nТаблиця: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl()
      });
    }
    return out_({ ok: true });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function doGet() { return out_({ ok: true, service: 'orders' }); }

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

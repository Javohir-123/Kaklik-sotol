// index.js
// Avto Chat Bot — kalit so'zga qarab avtomatik javob beruvchi Telegram bot.
//
// Ishlash tartibi:
// 1) Admin "Kalit so'z" tugmasini bosadi -> keyingi xabari kalit so'z sifatida saqlanadi
// 2) Admin "Javob kiritish" tugmasini bosadi -> keyingi xabari o'sha kalit so'zga javob sifatida saqlanadi
// 3) Oddiy foydalanuvchi botga yozganda, xabari kiritilgan kalit so'zlardan birini
//    o'z ichiga olsa, mos javob avtomatik yuboriladi.

require('dotenv').config();
const { Telegraf, Markup } = require('telegraf');
const { loadData, saveData } = require('./storage');

const BOT_TOKEN = process.env.BOT_TOKEN;
if (!BOT_TOKEN) {
  console.error('XATOLIK: BOT_TOKEN topilmadi. .env fayliga yoki Railway Variables bo\'limiga BOT_TOKEN qo\'shing.');
  process.exit(1);
}

// Vergul bilan ajratilgan admin ID'lar: masalan "111111,222222"
const ADMIN_IDS = (process.env.ADMIN_IDS || '')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean);

const bot = new Telegraf(BOT_TOKEN);

// --- Yordamchi funksiyalar -------------------------------------------------

function isAdmin(ctx) {
  const id = String(ctx.from.id);
  return ADMIN_IDS.length === 0 ? true : ADMIN_IDS.includes(id); // admin ro'yxati bo'sh bo'lsa, hamma admin (test uchun)
}

function mainKeyboard() {
  return Markup.keyboard([
    ['🔑 Kalit so\'z', '📝 Javob kiritish'],
    ['📋 Ro\'yxat', '🗑 O\'chirish'],
    ['🏠 Kabinet', '📊 Statistika'],
  ]).resize();
}

function findAutoReply(data, text) {
  const lower = text.toLowerCase();
  // Xabar ichida kalit so'z uchrasa yetarli (moslashuvchan qidiruv)
  return data.autoReplies.find((item) => lower.includes(item.keyword.toLowerCase()));
}

// Telegram Business xabariga to'g'ri javob yuborish uchun.
// Business xabarlarga oddiy ctx.reply() ishlamaydi — business_connection_id kerak bo'ladi.
async function sendReply(ctx, text) {
  const businessId = ctx.update.business_message?.business_connection_id;
  if (businessId) {
    return ctx.telegram.sendMessage(ctx.chat.id, text, {
      business_connection_id: businessId,
    });
  }
  return ctx.reply(text);
}

function touchUser(data, ctx) {
  const id = String(ctx.from.id);
  const now = new Date().toISOString();
  if (!data.users[id]) {
    data.users[id] = {
      id,
      username: ctx.from.username || '',
      firstName: ctx.from.first_name || '',
      firstSeen: now,
      lastSeen: now,
      messageCount: 0,
    };
  }
  data.users[id].lastSeen = now;
  data.users[id].messageCount += 1;
  data.stats.totalMessages += 1;
}

// --- Buyruqlar ---------------------------------------------------------

bot.start((ctx) => {
  const data = loadData();
  touchUser(data, ctx);
  saveData(data);

  if (isAdmin(ctx)) {
    return ctx.reply(
      'Assalomu alaykum! Avto Chat Bot boshqaruv paneliga xush kelibsiz.\n\n' +
        '🔑 Kalit so\'z — yangi kalit so\'z qo\'shish\n' +
        '📝 Javob kiritish — oxirgi kiritilgan kalit so\'zga javob yozish\n' +
        '📋 Ro\'yxat — barcha kalit so\'z/javoblarni ko\'rish\n' +
        '🗑 O\'chirish — kalit so\'zni o\'chirish\n' +
        '🏠 Kabinet — sozlamalar\n' +
        '📊 Statistika — foydalanuvchilar va xabarlar statistikasi',
      mainKeyboard()
    );
  }
  return ctx.reply('Assalomu alaykum! Savolingizni yozing, imkon qadar tezroq javob beramiz.');
});

bot.hears('🔑 Kalit so\'z', (ctx) => {
  if (!isAdmin(ctx)) return;
  const data = loadData();
  data.pendingKeyword[String(ctx.from.id)] = { stage: 'awaiting_keyword' };
  saveData(data);
  ctx.reply('Yangi kalit so\'zni yuboring!\n(Masalan: "narxi", "ish vaqti", "manzil")');
});

bot.hears('📝 Javob kiritish', (ctx) => {
  if (!isAdmin(ctx)) return;
  const data = loadData();
  const pending = data.pendingKeyword[String(ctx.from.id)];

  if (!pending || !pending.keyword) {
    return ctx.reply(
      '⚠️ Avval "🔑 Kalit so\'z" tugmasi orqali kalit so\'z kiriting, so\'ngra unga javob yozing.'
    );
  }

  data.pendingKeyword[String(ctx.from.id)] = { stage: 'awaiting_answer', keyword: pending.keyword };
  saveData(data);
  ctx.reply(`Kiritilgan "${pending.keyword}" kalit so'ziga yuborilishi kerak bo'lgan javob matnini yuboring!`);
});

bot.hears('📋 Ro\'yxat', (ctx) => {
  if (!isAdmin(ctx)) return;
  const data = loadData();
  if (data.autoReplies.length === 0) {
    return ctx.reply('Hozircha kalit so\'zlar mavjud emas.');
  }
  const list = data.autoReplies
    .map((item, i) => `${i + 1}. 🔑 ${item.keyword}\n   📝 ${item.answer}`)
    .join('\n\n');
  ctx.reply(`Barcha kalit so'z/javoblar:\n\n${list}`);
});

bot.hears('🗑 O\'chirish', (ctx) => {
  if (!isAdmin(ctx)) return;
  const data = loadData();
  if (data.autoReplies.length === 0) {
    return ctx.reply('O\'chirish uchun kalit so\'zlar mavjud emas.');
  }
  const buttons = data.autoReplies.map((item) => [
    Markup.button.callback(`❌ ${item.keyword}`, `delete_${item.id}`),
  ]);
  ctx.reply('O\'chirmoqchi bo\'lgan kalit so\'zni tanlang:', Markup.inlineKeyboard(buttons));
});

bot.action(/delete_(.+)/, (ctx) => {
  if (!isAdmin(ctx)) return ctx.answerCbQuery();
  const id = ctx.match[1];
  const data = loadData();
  const before = data.autoReplies.length;
  data.autoReplies = data.autoReplies.filter((item) => item.id !== id);
  saveData(data);
  ctx.answerCbQuery(before !== data.autoReplies.length ? 'O\'chirildi ✅' : 'Topilmadi');
  ctx.editMessageText('Amal bajarildi. Ro\'yxatni qayta ko\'rish uchun "📋 Ro\'yxat" tugmasini bosing.');
});

bot.hears('🏠 Kabinet', (ctx) => {
  if (!isAdmin(ctx)) return;
  const data = loadData();
  ctx.reply(
    `👤 Kabinet\n\n` +
      `ID: ${ctx.from.id}\n` +
      `Ism: ${ctx.from.first_name || '-'}\n` +
      `Username: @${ctx.from.username || '-'}\n` +
      `Jami kalit so'zlar: ${data.autoReplies.length}\n` +
      `Bot ishga tushgan sana: ${new Date(data.stats.startedAt).toLocaleString('uz-UZ')}`
  );
});

bot.hears('📊 Statistika', (ctx) => {
  if (!isAdmin(ctx)) return;
  const data = loadData();
  const userCount = Object.keys(data.users).length;
  ctx.reply(
    `📊 Statistika\n\n` +
      `👥 Foydalanuvchilar soni: ${userCount}\n` +
      `💬 Jami xabarlar: ${data.stats.totalMessages}\n` +
      `🤖 Avto javob berilgan: ${data.stats.autoRepliedMessages}\n` +
      `🔑 Kalit so'zlar soni: ${data.autoReplies.length}`
  );
});

// --- Oddiy matnli xabarlarni qayta ishlash ------------------------------

bot.on('text', async (ctx) => {
  const data = loadData();
  const text = ctx.message.text.trim();
  const adminId = String(ctx.from.id);
  const isBusiness = Boolean(ctx.update.business_message);

  // Business xabarlarda admin boshqaruv menyusi ishlamaydi (bu shaxsiy akkauntga kelgan mijoz xabari) —
  // to'g'ridan-to'g'ri avto-javob mantig'iga o'tamiz.
  if (!isBusiness) {
    // Admin "kalit so'z / javob kiritish" jarayonida bo'lsa
    const pending = data.pendingKeyword[adminId];
    if (isAdmin(ctx) && pending) {
      if (pending.stage === 'awaiting_keyword') {
        data.pendingKeyword[adminId] = { stage: 'has_keyword', keyword: text };
        saveData(data);
        return ctx.reply(
          `✅ Kalit so'z qo'shildi: "${text}"\n\n` +
            `Endi "📝 Javob kiritish" tugmasini bosib, shu kalit so'zga javob yozing.\n` +
            `Yana yangi kalit so'z qo'shish uchun "🔑 Kalit so'z" tugmasini bosing.`
        );
      }

      if (pending.stage === 'awaiting_answer') {
        const newItem = {
          id: Date.now().toString(),
          keyword: pending.keyword,
          answer: text,
          createdAt: new Date().toISOString(),
        };
        data.autoReplies.push(newItem);
        delete data.pendingKeyword[adminId];
        saveData(data);
        return ctx.reply(`✅ Avto javob muvaffaqiyatli qo'shildi!\n\n🔑 ${newItem.keyword}\n📝 ${newItem.answer}`);
      }
    }

    // Admin panel tugmalari bilan ziddiyat bo'lmasligi uchun, tugma matnlarini o'tkazib yuboramiz
    const menuLabels = ['🔑 Kalit so\'z', '📝 Javob kiritish', '📋 Ro\'yxat', '🗑 O\'chirish', '🏠 Kabinet', '📊 Statistika'];
    if (menuLabels.includes(text)) return;
  }

  // Oddiy foydalanuvchi (yoki Business mijozi) xabari — statistika va avto javob
  touchUser(data, ctx);
  const match = findAutoReply(data, text);
  if (match) {
    data.stats.autoRepliedMessages += 1;
    saveData(data);
    return sendReply(ctx, match.answer);
  }

  saveData(data);
  // Mos kalit so'z topilmasa, hech narsa demaymiz (yoki xohlasangiz standart javob qo'shishingiz mumkin)
});

// --- Telegram Business hodisalari ---------------------------------------
// Business akkaunt botga ulanganda/uzilganda kelgan xabarlar.
// Telegraf yangi versiyalarida bular alohida update turi sifatida keladi,
// lekin matnli xabar tarkibi bot.on('text') orqali ham ushlanadi (yuqorida).
// Shu handlerlar faqat ulanish holatini kuzatib, konsolga yozib qo'yish uchun.

bot.on('business_connection', (ctx) => {
  const conn = ctx.update.business_connection;
  console.log('🔗 Business ulanish yangilandi:', conn?.user_chat_id, 'faol:', conn?.is_enabled);
});

bot.on('deleted_business_messages', (ctx) => {
  console.log('🗑 Business xabar(lar) o\'chirildi.');
});

// --- Xatoliklarni ushlash ------------------------------------------------

bot.catch((err, ctx) => {
  console.error(`Xatolik yuz berdi (${ctx.updateType}):`, err);
});

// --- Botni ishga tushirish -----------------------------------------------

bot.launch({
  allowedUpdates: [
    'message',
    'edited_message',
    'callback_query',
    'business_connection',
    'business_message',
    'edited_business_message',
    'deleted_business_messages',
  ],
}).then(() => {
  console.log('✅ Avto Chat Bot ishga tushdi! (Telegram Business qo\'llab-quvvatlanadi)');
});

// Railway/serverlarda to'g'ri to'xtash uchun
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));

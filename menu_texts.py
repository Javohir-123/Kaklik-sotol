# Asosiy va admin menyusidagi barcha tugma matnlari.
# Bu matnlar har qanday FSM holatida ham "menyu tugmasi" deb tanilishi va
# joriy jarayonni to'xtatib, tegishli bo'limga o'tishi kerak.

MAIN_MENU_TEXTS = {
    "🛒 Sotish",
    "🛍 Sotib olish",
    "🧑‍💼 Ish berish",
    "👷 Ishlash",
    "💳 Balansni to'ldirish",
    "📊 Balans",
    "👨‍💼 Admin bilan bog'lanish",
    "📋 Mening e'lonlarim",
}

ADMIN_MENU_TEXTS = {
    "💰 Pul berish",
    "✉️ Xabar yuborish",
    "📈 Statistika",
    "⬅️ Asosiy menyu",
}

ALL_MENU_TEXTS = MAIN_MENU_TEXTS | ADMIN_MENU_TEXTS | {"/start", "/admin"}

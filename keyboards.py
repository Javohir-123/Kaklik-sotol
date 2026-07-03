from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data_lists import CATEGORIES, GENDERS, JOB_TYPES, REGIONS, DISTRICTS


# ==================== ASOSIY MENYU ====================

def main_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Sotish"), KeyboardButton(text="🛍 Sotib olish")],
            [KeyboardButton(text="🧑‍💼 Ish berish"), KeyboardButton(text="👷 Ishlash")],
            [KeyboardButton(text="💳 Balansni to'ldirish"), KeyboardButton(text="📊 Balans")],
            [KeyboardButton(text="📋 Mening e'lonlarim")],
            [KeyboardButton(text="👨‍💼 Admin bilan bog'lanish")],
        ],
        resize_keyboard=True
    )
    return kb


def admin_reply_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Pul berish"), KeyboardButton(text="✉️ Xabar yuborish")],
            [KeyboardButton(text="📈 Statistika"), KeyboardButton(text="⬅️ Asosiy menyu")],
        ],
        resize_keyboard=True
    )
    return kb


# ==================== KATEGORIYALAR ====================

def categories_kb(action: str):
    """action: 'sell' yoki 'buy' — callback_data ga qo'shiladi"""
    builder = InlineKeyboardBuilder()
    for cat_key, cat_data in CATEGORIES.items():
        builder.button(text=cat_data["title"], callback_data=f"{action}_cat_{cat_key}")
    builder.adjust(2)
    return builder.as_markup()


def items_kb(action: str, cat_key: str):
    builder = InlineKeyboardBuilder()
    items = CATEGORIES[cat_key]["items"]
    for item_key, item_title in items.items():
        builder.button(text=item_title, callback_data=f"{action}_item_{cat_key}_{item_key}")
    builder.button(text="⬅️ Orqaga", callback_data=f"{action}_back_categories")
    builder.adjust(2)
    return builder.as_markup()


# ==================== E'LON YARATISH JARAYONI ====================

def gender_kb():
    builder = InlineKeyboardBuilder()
    for g in GENDERS:
        builder.button(text=g, callback_data=f"gender_{g}")
    builder.adjust(3)
    return builder.as_markup()


def photos_done_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Rasm qo'shishni tugatish", callback_data="photos_done")
    builder.adjust(1)
    return builder.as_markup()


def confirm_listing_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Tasdiqlash va joylash", callback_data="listing_confirm")
    builder.button(text="❌ Bekor qilish", callback_data="listing_cancel")
    builder.adjust(1)
    return builder.as_markup()


# ==================== SOTIB OLISH — E'LONNI KO'RISH ====================

def listing_view_kb(listing_id: int, index: int, total: int):
    builder = InlineKeyboardBuilder()
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"nav_{index-1}"))
    nav_row.append(InlineKeyboardButton(text=f"{index+1}/{total}", callback_data="noop"))
    if index < total - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"nav_{index+1}"))
    builder.row(*nav_row)
    builder.row(InlineKeyboardButton(text="📞 Sotib olish (Egasini ko'rish)", callback_data=f"viewcontact_{listing_id}"))
    return builder.as_markup()


# ==================== ISH E'LONLARI ====================

def region_kb(action: str):
    """action: 'jobpost' yoki 'jobbrowse' — callback_data ga qo'shiladi"""
    builder = InlineKeyboardBuilder()
    for region_key, region_title in REGIONS.items():
        builder.button(text=region_title, callback_data=f"{action}_region_{region_key}")
    builder.adjust(2)
    return builder.as_markup()


def district_kb(action: str, region_key: str):
    """action: 'jobpost' yoki 'jobbrowse'. Tanlangan viloyatning tumanlarini ko'rsatadi."""
    builder = InlineKeyboardBuilder()
    districts = DISTRICTS.get(region_key, [])
    for i, district_name in enumerate(districts):
        builder.button(text=district_name, callback_data=f"{action}_district_{region_key}_{i}")
    builder.button(text="⬅️ Orqaga (viloyatlar)", callback_data=f"{action}_back_regions")
    builder.adjust(2)
    return builder.as_markup()


def job_types_kb():
    builder = InlineKeyboardBuilder()
    for key, title in JOB_TYPES.items():
        builder.button(text=title, callback_data=f"jobtype_{key}")
    builder.adjust(1)
    return builder.as_markup()


def job_view_kb(job_id: int, index: int, total: int):
    builder = InlineKeyboardBuilder()
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"jobnav_{index-1}"))
    nav_row.append(InlineKeyboardButton(text=f"{index+1}/{total}", callback_data="noop"))
    if index < total - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"jobnav_{index+1}"))
    builder.row(*nav_row)
    builder.row(InlineKeyboardButton(text="📞 Bog'lanish (Egasini ko'rish)", callback_data=f"jobcontact_{job_id}"))
    return builder.as_markup()


# ==================== TO'LOV ====================

def cancel_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Bekor qilish", callback_data="cancel_action")
    return builder.as_markup()


def admin_deposit_kb(deposit_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Tasdiqlash", callback_data=f"depapprove_{deposit_id}")
    builder.button(text="❌ Rad etish", callback_data=f"depreject_{deposit_id}")
    builder.adjust(2)
    return builder.as_markup()


# ==================== MENING E'LONLARIM ====================

def my_listing_kb(listing_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 E'lonni o'chirish", callback_data=f"dellisting_{listing_id}")
    builder.adjust(1)
    return builder.as_markup()


def my_job_kb(job_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 E'lonni o'chirish", callback_data=f"deljob_{job_id}")
    builder.adjust(1)
    return builder.as_markup()

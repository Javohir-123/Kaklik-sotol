from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database import db
from keyboards import main_menu_kb
from config import ADMIN_USERNAME

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)

    name = message.from_user.first_name or "Foydalanuvchi"

    await message.answer(
        f"👋 Assalomu alaykum, <b>{name}</b>!\n\n"
        "🐾 <b>Sotuv Bozor</b> botiga xush kelibsiz.\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "Ushbu bot orqali parrandalar, qora mol, qo'y, ot, mashina va boshqa "
        "turdagi mol-mulkni sotish yoki sotib olish mumkin. Shuningdek, "
        "ish e'lonlarini joylashtirish va qidirish imkoniyati mavjud.\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "📋 <b>Bot imkoniyatlari:</b>\n\n"
        "🛒 <b>Sotish</b>\n"
        "Mol-mulkingizni rasm va tavsif bilan e'lon qilib joylashtirasiz. "
        "Birinchi e'lon bepul, keyingi e'lonlar uchun belgilangan to'lov talab qilinadi.\n\n"
        "🛍 <b>Sotib olish</b>\n"
        "Boshqa foydalanuvchilar joylagan e'lonlarni ko'rib chiqasiz. "
        "Tanlangan e'lon egasining aloqa ma'lumotlarini ko'rish uchun "
        "belgilangan to'lov amalga oshiriladi.\n\n"
        "🧑‍💼 <b>Ish berish</b>\n"
        "Xodim talab qilinsa, ushbu bo'limdan e'lon joylashtiriladi.\n\n"
        "👷 <b>Ishlash</b>\n"
        "Viloyat va tuman bo'yicha mavjud ish e'lonlarini ko'rish imkoniyati.\n\n"
        "💳 <b>Balansni to'ldirish</b>\n"
        "Hisobni to'ldirish uchun ushbu bo'limdan foydalaniladi.\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "Quyidagi menyudan kerakli bo'limni tanlang:",
        reply_markup=main_menu_kb()
    )


@router.message(F.text == "⬅️ Asosiy menyu")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Asosiy menyu:", reply_markup=main_menu_kb())


@router.message(F.text == "📊 Balans")
async def show_balance(message: Message):
    user = await db.get_user(message.from_user.id)
    balance = user["balance"] if user else 0
    formatted = f"{balance:,}".replace(",", " ")
    await message.answer(
        "💼 <b>Hisobingiz</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Joriy balans: <b>{formatted} so'm</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "Balansni to'ldirish uchun \"💳 Balansni to'ldirish\" tugmasini bosing.",
        parse_mode="HTML"
    )


@router.message(F.text == "👨‍💼 Admin bilan bog'lanish")
async def contact_admin(message: Message):
    await message.answer(
        "👨‍💻 <b>Admin bilan bog'lanish</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"Telegram: {ADMIN_USERNAME}\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "Savol, taklif yoki muammolar yuzasidan murojaat qilishingiz mumkin.",
        parse_mode="HTML"
    )

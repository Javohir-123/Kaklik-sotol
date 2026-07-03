import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import db
from keyboards import main_menu_kb, cancel_kb, admin_deposit_kb
from states import Deposit
from config import CARD_NUMBER, MIN_DEPOSIT, ADMIN_IDS, ADMIN_USERNAME
from utils.ocr_check import check_receipt

logger = logging.getLogger(__name__)
router = Router()


def fmt(amount: int) -> str:
    """Summani 1 000 000 ko'rinishida formatlaydi"""
    return f"{amount:,}".replace(",", " ")


@router.message(F.text == "💳 Balansni to'ldirish")
async def deposit_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Deposit.entering_amount)
    await message.answer(
        "💳 <b>Balansni to'ldirish</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "Qancha summa kiritmoqchisiz?\n\n"
        f"Minimal summa: <b>{fmt(MIN_DEPOSIT)} so'm</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "Summani faqat raqamlarda kiriting (masalan: <code>5000</code>):",
        reply_markup=cancel_kb(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "cancel_action")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Bekor qilindi.")
    await callback.message.answer("🏠 Asosiy menyu:", reply_markup=main_menu_kb())
    await callback.answer()


@router.message(Deposit.entering_amount)
async def deposit_enter_amount(message: Message, state: FSMContext):
    text = message.text.strip().replace(" ", "").replace(",", "")
    if not text.isdigit():
        await message.answer("⚠️ Iltimos summani faqat raqamlarda kiriting (masalan: 5000):")
        return

    amount = int(text)
    if amount < MIN_DEPOSIT:
        await message.answer(f"⚠️ Minimal summa {fmt(MIN_DEPOSIT)} so'm. Qaytadan kiriting:")
        return

    await state.update_data(amount=amount)
    await state.set_state(Deposit.waiting_receipt)
    await message.answer(
        "💳 <b>To'lov qilish uchun:</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"💳 Karta raqami: <code>{CARD_NUMBER}</code>\n"
        f"💰 Summa: <b>{fmt(amount)} so'm</b>\n"
        f"🆔 Telegram ID: <code>{message.from_user.id}</code>\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "✅ To'lovni amalga oshirgach, chek rasmini (screenshot) yuboring.",
        parse_mode="HTML"
    )


@router.message(Deposit.waiting_receipt, F.photo)
async def deposit_receive_receipt(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    amount = data["amount"]
    user_id = message.from_user.id
    photo_file_id = message.photo[-1].file_id
    full_name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "—"

    deposit_id = await db.create_deposit(user_id, amount, photo_file_id, status="pending")

    await message.answer("⏳ Chekingiz tekshirilmoqda, biroz kuting...")

    try:
        file = await bot.get_file(photo_file_id)
        file_bytes_io = await bot.download_file(file.file_path)
        image_bytes = file_bytes_io.read()
        approved, reason = check_receipt(image_bytes, amount)
    except Exception as e:
        logger.error(f"Chekni yuklab olishda xato: {e}")
        approved, reason = False, "❌ Rasmni tahlil qilishda texnik xatolik yuz berdi."

    total_deposits = await db.count_deposits() + 1

    if approved:
        await db.update_deposit_status(deposit_id, "approved")
        await db.update_balance(user_id, amount)
        await state.clear()
        await message.answer(
            "✅ <b>Chekingiz avtomatik tasdiqlandi!</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Balansingizga <b>{fmt(amount)} so'm</b> qo'shildi.\n"
            "━━━━━━━━━━━━━━━━━━━",
            reply_markup=main_menu_kb(),
            parse_mode="HTML"
        )
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_photo(
                    admin_id,
                    photo_file_id,
                    caption=(
                        "✅ <b>AVTOMATIK TASDIQLANDI</b>\n"
                        "━━━━━━━━━━━━━━━━━━━\n"
                        f"👤 Foydalanuvchi: {full_name}\n"
                        f"🔗 Lichkasi: {username}\n"
                        f"🆔 ID: <code>{user_id}</code>\n"
                        f"💰 Summa: {fmt(amount)} so'm"
                    ),
                    parse_mode="HTML"
                )
            except Exception:
                pass
    else:
        await state.clear()
        await db.update_deposit_status(deposit_id, "pending")
        await message.answer(
            "⚠️ <b>Chek avtomatik tasdiqlanmadi</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"📝 Sabab: {reason}\n\n"
            "👨‍💼 Chekingiz admin tomonidan tekshiriladi.\n"
            "⏳ Bu jarayon 24 soatgacha vaqt olishi mumkin.\n"
            f"🔑 Chek ID: <code>{deposit_id}</code>\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"Tezroq tasdiqlash kerak bo'lsa, admin bilan bog'laning: {ADMIN_USERNAME}",
            reply_markup=main_menu_kb(),
            parse_mode="HTML"
        )

        for admin_id in ADMIN_IDS:
            try:
                await bot.send_photo(
                    admin_id,
                    photo_file_id,
                    caption=(
                        "💳 <b>YANGI CHEK KELDI</b> (avtomatik tekshirilmadi)\n"
                        "━━━━━━━━━━━━━━━━━━━\n"
                        f"👤 Foydalanuvchi: {full_name}\n"
                        f"🔗 Lichkasi: {username}\n"
                        f"🆔 ID: <code>{user_id}</code>\n"
                        f"💰 Kutilgan summa: {fmt(amount)} so'm\n"
                        f"📊 Jami depositlar: {total_deposits} ta\n"
                        f"⚠️ {reason}\n"
                        "━━━━━━━━━━━━━━━━━━━\n"
                        f"🔑 Chek ID: <code>{deposit_id}</code>"
                    ),
                    reply_markup=admin_deposit_kb(deposit_id),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Adminga xabar yuborishda xato: {e}")


@router.message(Deposit.waiting_receipt)
async def deposit_wrong_content(message: Message):
    await message.answer("⚠️ Iltimos chek rasmini (screenshot) yuboring.")


# ==================== ADMIN TOMONIDAN QO'LDA TASDIQLASH ====================

@router.callback_query(F.data.startswith("depapprove_"))
async def admin_approve_deposit(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔ Sizda ruxsat yo'q.", show_alert=True)
        return

    deposit_id = int(callback.data.replace("depapprove_", ""))
    deposit = await db.get_deposit(deposit_id)

    if not deposit or deposit["status"] != "pending":
        await callback.answer("⚠️ Bu chek allaqachon ko'rib chiqilgan.", show_alert=True)
        return

    await db.update_deposit_status(deposit_id, "approved")
    await db.update_balance(deposit["user_id"], deposit["amount"])

    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ <b>ADMIN TOMONIDAN TASDIQLANDI</b>",
        parse_mode="HTML"
    )
    await callback.answer("✅ Tasdiqlandi")

    try:
        await bot.send_message(
            deposit["user_id"],
            "✅ <b>Chekingiz admin tomonidan tasdiqlandi!</b>\n"
            f"💰 Balansingizga <b>{fmt(deposit['amount'])} so'm</b> qo'shildi.",
            parse_mode="HTML"
        )
    except Exception:
        pass


@router.callback_query(F.data.startswith("depreject_"))
async def admin_reject_deposit(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("⛔ Sizda ruxsat yo'q.", show_alert=True)
        return

    deposit_id = int(callback.data.replace("depreject_", ""))
    deposit = await db.get_deposit(deposit_id)

    if not deposit or deposit["status"] != "pending":
        await callback.answer("⚠️ Bu chek allaqachon ko'rib chiqilgan.", show_alert=True)
        return

    await db.update_deposit_status(deposit_id, "rejected")

    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n❌ <b>ADMIN TOMONIDAN RAD ETILDI</b>",
        parse_mode="HTML"
    )
    await callback.answer("❌ Rad etildi")

    try:
        await bot.send_message(
            deposit["user_id"],
            "❌ Chekingiz rad etildi.\n"
            f"Agar bu xato deb hisoblasangiz, admin bilan bog'laning: {ADMIN_USERNAME}"
        )
    except Exception:
        pass

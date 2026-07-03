from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import db
from keyboards import my_listing_kb, my_job_kb
from data_lists import get_category_title, get_item_title

router = Router()


@router.message(F.text == "📋 Mening e'lonlarim")
async def my_listings(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id

    listings = await db.get_user_listings(user_id)
    jobs = await db.get_user_jobs(user_id)

    if not listings and not jobs:
        await message.answer("📭 Sizda hozircha faol e'lonlar yo'q.")
        return

    if listings:
        await message.answer(f"🛒 <b>Sizning sotish e'lonlaringiz</b> ({len(listings)} ta):")
        for listing in listings:
            text = (
                f"{get_item_title(listing['category'], listing['subcategory'])}\n"
                f"💰 Narxi: {listing['price']}\n"
                f"📝 {listing['description']}\n"
                f"🔑 ID: {listing['listing_id']}"
            )
            await message.answer(text, reply_markup=my_listing_kb(listing["listing_id"]))

    if jobs:
        label = "Ish e'lonlaringiz"
        await message.answer(f"🧑‍💼 <b>Sizning {label.lower()}</b> ({len(jobs)} ta):")
        for job in jobs:
            text = (
                f"📌 {job['title']}\n"
                f"💰 {job['salary']}\n"
                f"📍 {job['location']}\n"
                f"🔑 ID: {job['job_id']}"
            )
            await message.answer(text, reply_markup=my_job_kb(job["job_id"]))


@router.callback_query(F.data.startswith("dellisting_"))
async def delete_listing(callback: CallbackQuery):
    listing_id = int(callback.data.replace("dellisting_", ""))
    success = await db.remove_listing(listing_id, callback.from_user.id)

    if success:
        await callback.message.edit_text("🗑 E'lon o'chirildi.")
        await callback.answer("✅ O'chirildi")
    else:
        await callback.answer("⚠️ E'lonni o'chirib bo'lmadi (ehtimol allaqachon o'chirilgan).", show_alert=True)


@router.callback_query(F.data.startswith("deljob_"))
async def delete_job(callback: CallbackQuery):
    job_id = int(callback.data.replace("deljob_", ""))
    success = await db.remove_job(job_id, callback.from_user.id)

    if success:
        await callback.message.edit_text("🗑 E'lon o'chirildi.")
        await callback.answer("✅ O'chirildi")
    else:
        await callback.answer("⚠️ E'lonni o'chirib bo'lmadi (ehtimol allaqachon o'chirilgan).", show_alert=True)

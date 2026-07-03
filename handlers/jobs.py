from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import db
from keyboards import job_view_kb, main_menu_kb, region_kb, district_kb
from data_lists import REGIONS, DISTRICTS
from states import JobPosting, JobBrowsing

router = Router()


# ==================== "Ish berish" -> XODIM KERAK BO'LGAN E'LON JOYLASH ====================

@router.message(F.text == "🧑‍💼 Ish berish")
async def job_post_start(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(job_type="ish_berish")
    await state.set_state(JobPosting.entering_title)
    await message.answer("🧑‍💼 Qanday ishga xodim kerak? Ish nomini/lavozimini kiriting:")


@router.message(JobPosting.entering_title)
async def job_enter_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(JobPosting.entering_description)
    await message.answer("📝 Qo'shimcha ma'lumot kiriting (shartlar, tajriba, talablar va h.k.):")


@router.message(JobPosting.entering_description)
async def job_enter_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(JobPosting.entering_salary)
    await message.answer("💰 Maosh/narxni kiriting (masalan: 3 000 000 so'm yoki \"Kelishiladi\"):")


@router.message(JobPosting.entering_salary)
async def job_enter_salary(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await state.set_state(JobPosting.entering_location)
    await message.answer("📍 Qaysi viloyatda ish beryapsiz? Tanlang:", reply_markup=region_kb("jobpost"))


@router.callback_query(JobPosting.entering_location, F.data.startswith("jobpost_region_"))
async def job_choose_region(callback: CallbackQuery, state: FSMContext):
    region_key = callback.data.replace("jobpost_region_", "")
    await state.update_data(region_key=region_key)
    await callback.message.edit_text(
        f"📍 {REGIONS.get(region_key)} — qaysi tuman/shahar? Tanlang:",
        reply_markup=district_kb("jobpost", region_key)
    )
    await callback.answer()


@router.callback_query(JobPosting.entering_location, F.data == "jobpost_back_regions")
async def job_post_back_regions(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📍 Qaysi viloyatda ish beryapsiz? Tanlang:", reply_markup=region_kb("jobpost"))
    await callback.answer()


@router.callback_query(JobPosting.entering_location, F.data.startswith("jobpost_district_"))
async def job_choose_district(callback: CallbackQuery, state: FSMContext):
    # format: jobpost_district_{region_key}_{index}
    payload = callback.data.replace("jobpost_district_", "")
    region_key, idx_str = payload.rsplit("_", 1)
    idx = int(idx_str)
    district_name = DISTRICTS.get(region_key, [])[idx]
    region_title = REGIONS.get(region_key, region_key)

    full_location = f"{region_title}, {district_name}"
    await state.update_data(location=full_location)
    await state.set_state(JobPosting.entering_contact_username)
    await callback.message.edit_text(
        "👤 Telegram username kiriting (masalan @username), bo'lmasa \"yo'q\" deb yozing:"
    )
    await callback.answer()


@router.message(JobPosting.entering_contact_username)
async def job_enter_username(message: Message, state: FSMContext):
    await state.update_data(contact_username=message.text)
    await state.set_state(JobPosting.entering_contact_phone)
    await message.answer("📞 Telefon raqamingizni kiriting:")


@router.message(JobPosting.entering_contact_phone)
async def job_enter_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    job_id = await db.add_job(
        user_id=message.from_user.id,
        job_type=data["job_type"],
        title=data["title"],
        description=data["description"],
        salary=data["salary"],
        location=data["location"],
        contact_username=data["contact_username"],
        contact_phone=message.text
    )
    await state.clear()
    await message.answer(
        "✅ <b>E'loningiz joylandi!</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🔑 E'lon ID: {job_id}\n"
        f"📌 {data['title']}\n"
        f"📝 {data['description']}\n"
        f"💰 {data['salary']}\n"
        f"📍 {data['location']}\n"
        "━━━━━━━━━━━━━━━━━━━",
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
    )


# ==================== "Ishlash" -> VILOYAT, KEYIN TUMAN, KEYIN E'LONLAR ====================

def _format_job_text(job):
    return (
        f"📌 <b>{job['title']}</b>\n\n"
        f"📝 {job['description']}\n"
        f"💰 Maosh/narx: {job['salary']}\n"
        f"📍 Manzil: {job['location']}\n\n"
        "Bog'lanish uchun pastdagi tugmani bosing."
    )


@router.message(F.text == "👷 Ishlash")
async def job_browse_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(JobBrowsing.choosing_type)
    await message.answer(
        "📍 Qaysi viloyatdagi ish e'lonlarini ko'rmoqchisiz? Tanlang:",
        reply_markup=region_kb("jobbrowse")
    )


@router.callback_query(JobBrowsing.choosing_type, F.data.startswith("jobbrowse_region_"))
async def job_browse_region(callback: CallbackQuery, state: FSMContext):
    region_key = callback.data.replace("jobbrowse_region_", "")
    await state.update_data(region_key=region_key)
    await callback.message.edit_text(
        f"📍 {REGIONS.get(region_key)} — qaysi tuman/shahar? Tanlang:",
        reply_markup=district_kb("jobbrowse", region_key)
    )
    await callback.answer()


@router.callback_query(JobBrowsing.choosing_type, F.data == "jobbrowse_back_regions")
async def job_browse_back_regions(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📍 Qaysi viloyatdagi ish e'lonlarini ko'rmoqchisiz? Tanlang:",
        reply_markup=region_kb("jobbrowse")
    )
    await callback.answer()


@router.callback_query(JobBrowsing.choosing_type, F.data.startswith("jobbrowse_district_"))
async def job_browse_district(callback: CallbackQuery, state: FSMContext):
    # format: jobbrowse_district_{region_key}_{index}
    payload = callback.data.replace("jobbrowse_district_", "")
    region_key, idx_str = payload.rsplit("_", 1)
    idx = int(idx_str)
    district_name = DISTRICTS.get(region_key, [])[idx]
    region_title = REGIONS.get(region_key, region_key)
    full_location = f"{region_title}, {district_name}"

    jobs = await db.get_active_jobs("ish_berish", region=full_location)

    if not jobs:
        await callback.message.edit_text(
            f"😔 Hozircha \"{full_location}\" hududida ish beruvchilardan e'lon yo'q.\n\n"
            "Boshqa tumanni tanlashingiz mumkin:",
            reply_markup=district_kb("jobbrowse", region_key)
        )
        await callback.answer()
        return

    await state.update_data(jobs=jobs, job_index=0)
    await state.set_state(JobBrowsing.browsing)
    await callback.answer()

    job = jobs[0]
    await callback.message.edit_text(
        _format_job_text(job),
        reply_markup=job_view_kb(job["job_id"], 0, len(jobs)),
        parse_mode="HTML"
    )


@router.callback_query(JobBrowsing.browsing, F.data.startswith("jobnav_"))
async def job_navigate(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.replace("jobnav_", ""))
    data = await state.get_data()
    jobs = data["jobs"]
    job = jobs[index]
    await state.update_data(job_index=index)

    await callback.message.edit_text(
        _format_job_text(job),
        reply_markup=job_view_kb(job["job_id"], index, len(jobs)),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("jobcontact_"))
async def job_view_contact(callback: CallbackQuery):
    job_id = int(callback.data.replace("jobcontact_", ""))
    job = await db.get_job(job_id)
    if not job:
        await callback.answer("⚠️ E'lon topilmadi.", show_alert=True)
        return
    await callback.message.answer(
        f"👤 Lichka: {job['contact_username']}\n"
        f"📞 Telefon: {job['contact_phone']}"
    )
    await callback.answer()

import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

TOKEN = "7853088639:AAH4geavCVFAqCJkbYJ0P-1xpwaiDYPq67I"
GROUP_ID = -1002428849357  # ID группы для голосования
ADMIN_IDS = [5700087640]  # ID админов, которые могут накладывать вето

bot = Bot(token=TOKEN)
dp = Dispatcher()

applications = {}
admin_override = False

class ApplicationForm(StatesGroup):
    nickname = State()
    device = State()
    server = State()
    redstone = State()
    pvp_pve = State()
    playtime = State()
    schedule = State()
    teammates = State()
    country = State()
    age = State()
    internet = State()

async def reset_attempts():
    while True:
        await asyncio.sleep(7 * 24 * 60 * 60)
        applications.clear()

@dp.message(Command("adminitbot"))
async def adminitbot_command(message: types.Message):
    global admin_override
    if message.from_user.id in ADMIN_IDS:
        admin_override = True
        await message.reply("Вы можете подавать заявки без ограничений на 10 минут!")
        await asyncio.sleep(600)
        admin_override = False

@dp.message(Command("inteam"))
async def start_application(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in applications and not admin_override:
        await message.reply("Вы уже подавали заявку на этой неделе! Попробуйте позже.")
        return
    
    await state.set_state(ApplicationForm.nickname)
    await message.reply("Введите ваш никнейм:")

@dp.message(ApplicationForm.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await state.set_state(ApplicationForm.device)
    await message.reply("ПК или Мб (комп/тел):")

@dp.message(ApplicationForm.device)
async def process_device(message: types.Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(ApplicationForm.server)
    await message.reply("На каком сервере играете:")

@dp.message(ApplicationForm.server)
async def process_server(message: types.Message, state: FSMContext):
    await state.update_data(server=message.text)
    if "меркурий" in message.text.lower() or "мерк" in message.text.lower():
        await state.set_state(ApplicationForm.redstone)
        await message.reply("Хорошо понимаете Редстоун (1-10):")
    else:
        await message.reply("Вы не приняты из-за сервера.")
        await state.clear()

@dp.message(ApplicationForm.redstone)
async def process_redstone(message: types.Message, state: FSMContext):
    await state.update_data(redstone=message.text)
    await state.set_state(ApplicationForm.pvp_pve)
    await message.reply("Пвп или Пве:")

@dp.message(ApplicationForm.pvp_pve)
async def process_pvp_pve(message: types.Message, state: FSMContext):
    await state.update_data(pvp_pve=message.text)
    await state.set_state(ApplicationForm.playtime)
    await message.reply("Сколько в день часов примерно играете:")

@dp.message(ApplicationForm.playtime)
async def process_playtime(message: types.Message, state: FSMContext):
    await state.update_data(playtime=message.text)
    await state.set_state(ApplicationForm.schedule)
    await message.reply("Со скольки у вас учеба/в какое время вы не можете играть:")

@dp.message(ApplicationForm.schedule)
async def process_schedule(message: types.Message, state: FSMContext):
    await state.update_data(schedule=message.text)
    await state.set_state(ApplicationForm.teammates)
    await message.reply("Есть ли у вас свои тимейты:")

@dp.message(ApplicationForm.teammates)
async def process_teammates(message: types.Message, state: FSMContext):
    await state.update_data(teammates=message.text)
    await state.set_state(ApplicationForm.country)
    await message.reply("В какой стране вы живёте:")

@dp.message(ApplicationForm.country)
async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(ApplicationForm.age)
    await message.reply("Сколько вам лет:")

@dp.message(ApplicationForm.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(ApplicationForm.internet)
    await message.reply("Какой у вас интернет (от 1 до 10):")

@dp.message(ApplicationForm.internet)
async def process_internet(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    application_text = "\n".join([f"{key}: {value}" for key, value in user_data.items()])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Взять в команду", callback_data=f"accept_{message.from_user.id}"),
         InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{message.from_user.id}")]
    ])
    await bot.send_message(GROUP_ID, f"Голосование за вступление:\n{application_text}", reply_markup=keyboard)
    await asyncio.sleep(86400)
    await bot.send_message(GROUP_ID, f"Голосование окончено. Решение по пользователю {message.from_user.full_name} необходимо принять.")
    await state.clear()

async def main():
    asyncio.create_task(reset_attempts())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

TOKEN = "7853088639:AAH4geavCVFAqCJkbYJ0P-1xpwaiDYPq67I"
GROUP_ID = -1002428849357  # ID группы для голосования
ADMIN_IDS = [5700087640]  # ID админов, которые могут накладывать вето

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

applications = {}
admin_override = False

async def reset_attempts():
    while True:
        await asyncio.sleep(7 * 24 * 60 * 60)  # Ждём неделю
        applications.clear()

@dp.message_handler(commands=['adminitbot'])
async def adminitbot_command(message: types.Message):
    global admin_override
    if message.from_user.id in ADMIN_IDS:
        admin_override = True
        await message.reply("Вы можете подавать заявки без ограничений на 10 минут!")
        await asyncio.sleep(600)  # 10 минут
        admin_override = False

@dp.message_handler(commands=['inteam'])
async def handle_application(message: types.Message):
    user_id = message.from_user.id
    if user_id in applications and not admin_override:
        await message.reply("Вы уже подавали заявку на этой неделе! Попробуйте позже.")
        return
    
    await message.reply("Заполните анкету следующим образом:\n"
                        "Никнейм: your_nikname\n"
                        "ПК или Мб: (комп/тел)\n"
                        "На каком сервере играете: (можно на русском)\n"
                        "Хорошо понимаете Редстоун:(1-10)\n"
                        "Пвп или Пве:(на русском)\n"
                        "Сколько в день часов примерно играете:(просто цифра)\n"
                        "Со скольки у вас учеба/в какое время вы не можете играть?:\n"
                        "Есть ли у вас свои тимейты: (нет / перечислите ники)\n"
                        "В какой стране вы живёте:(страна)\n"
                        "Сколько вам лет:\n"
                        "Какой у вас интернет: (от 1 до 10)")

    applications[user_id] = datetime.datetime.now()

@dp.message_handler(lambda message: message.text.startswith("Никнейм:"))
async def process_application(message: types.Message):
    user_id = message.from_user.id
    if user_id not in applications:
        return
    
    application_text = message.text
    if "меркурий" in application_text.lower() or "мерк" in application_text.lower():
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("✅ Взять в команду", callback_data=f"accept_{user_id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{user_id}")
        )
        
        vote_message = await bot.send_message(GROUP_ID, f"Голосование за вступление:\n{application_text}", reply_markup=keyboard)
        await asyncio.sleep(86400)  # 24 часа ожидания
        await bot.send_message(GROUP_ID, f"Голосование окончено. Решение по пользователю {message.from_user.full_name} необходимо принять.")
    else:
        await message.reply("Вы не приняты из-за сервера.")

@dp.callback_query_handler(lambda call: call.data.startswith("accept_"))
async def accept_application(call: types.CallbackQuery):
    user_id = int(call.data.split("_")[1])
    await bot.send_message(GROUP_ID, f"Пользователь {user_id} принят в команду!")

@dp.callback_query_handler(lambda call: call.data.startswith("reject_"))
async def reject_application(call: types.CallbackQuery):
    user_id = int(call.data.split("_")[1])
    await bot.send_message(GROUP_ID, f"Пользователь {user_id} не принят в команду!")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Команды бота:\n/help - помощь\n/inteam - подать заявку на вступление\n/adminitbot - снять ограничение на попытки (для админов)")

async def main():
    asyncio.create_task(reset_attempts())
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Вставь свой токен от BotFather
TOKEN = "7853088639:AAH4geavCVFAqCJkbYJ0P-1xpwaiDYPq67I"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я твой Telegram-бот 🤖\n\nНапиши /help, чтобы узнать, что я умею.")

# Команда /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("📌 **Команды бота:**\n"
                         "/start - Запустить бота\n"
                         "/help - Показать список команд\n"
                         "/inteam - Заполнить анкету для вступления в команду")

# Команда /inteam
@dp.message(Command("inteam"))
async def inteam_command(message: types.Message):
    await message.answer("✍ **Анкета для вступления в команду:**\n\n"
                         "🔹 Ваше имя в Minecraft?\n"
                         "🔹 Сервер, на котором играете?\n"
                         "🔹 Почему вы хотите играть с нами?")

# Эхо-бот (повторяет сообщения)
@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

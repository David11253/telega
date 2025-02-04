import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Вставь сюда свой токен от BotFather
TOKEN = "7853088639:AAH4geavCVFAqCJkbYJ0P-1xpwaiDYPq67I"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я твой Telegram-бот 🤖")

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

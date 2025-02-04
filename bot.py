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
    await message.answer("Привет! Я бот CCAinR 🤖\n\nНапиши /help, чтобы узнать, что я умею.")

# Команда /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("📌 **Команды бота:**\n"
                         "/start - Запустить бота\n"
                         "/help - Показать список команд\n"
                         "/inteam - Заполнить анкету для вступления в CCAinR")

# Команда /inteam
@dp.message(Command("inteam"))
async def inteam_command(message: types.Message):
    await message.answer(
        "📋 **Заполните анкету для вступления в CCAinR**\n"
        "*(Corporate Communist Alliance in Server)*\n"
        "———————————————\n\n"
        "Заполните анкету следующим образом:\n"
        "🔹 **Никнейм:** your_nikname\n"
        "🔹 **ПК или Мб:** (комп/тел)\n"
        "🔹 **На каком сервере играете:** (можно на русском)\n"
        "🔹 **Хорошо понимаете Редстоун:** (1-10)\n"
        "🔹 **Пвп или Пве:** (на русском)\n"
        "🔹 **Сколько в день часов примерно играете:** (просто цифра)\n"
        "🔹 **Со скольки у вас учеба/в какое время вы не можете играть?:** (по мск)\n"
        "🔹 **Есть ли у вас свои тимейты:** (нет/ (ник Тима), (если есть ещё Тим, перечислите через запятую))\n"
        "🔹 **В какой стране вы живёте:** (страна)\n"
        "🔹 **Сколько вам лет:**\n"
        "🔹 **Какой у вас интернет:** (от 1 до 10)\n\n"
        "📌 **Пример заполнения:**\n"
        "`Ratatu\n"
        "Комп\n"
        "Мерк\n"
        "4\n"
        "Не то и не это\n"
        "5 ч.\n"
        "С 8:30 до 13:00. С 18:30 до 20:00. С 23:00 до 7:00.\n"
        "Тима: bedbur, cat_3585, opovisee_game_703.\n"
        "Раша\n"
        "14\n"
        "8`"
    )

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

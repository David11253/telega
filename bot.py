import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Вставь сюда свой новый токен от BotFather
TOKEN = "7853088639:AAH4geavCVFAqCJkbYJ0P-1xpwaiDYPq67I"
GROUP_ID = -1002428849357  # ID группы, куда отправлять заявки

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Определяем состояния анкеты
class Form(StatesGroup):
    nickname = State()
    platform = State()
    server = State()
    redstone = State()
    pvp_pve = State()
    hours = State()
    study_time = State()
    teammates = State()
    country = State()
    age = State()
    internet = State()

# Хранение ID голосований
polls = {}

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Используй /help для списка команд.")

# Команда /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Команды:\n/help - Список команд\n/inteam - Подать заявку на вступление")

# Команда /inteam (начало анкеты)
@dp.message(Command("inteam"))
async def start_form(message: types.Message, state: FSMContext):
    await message.answer("✏ Введите ваш никнейм:")
    await state.set_state(Form.nickname)

@dp.message(Form.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer("Вы играете на ПК или мобильном? (ПК/Мб)")
    await state.set_state(Form.platform)

@dp.message(Form.platform)
async def process_platform(message: types.Message, state: FSMContext):
    await state.update_data(platform=message.text)
    await message.answer("На каком сервере играете?")
    await state.set_state(Form.server)

@dp.message(Form.server)
async def process_server(message: types.Message, state: FSMContext):
    await state.update_data(server=message.text)
    await message.answer("Как хорошо вы понимаете редстоун? (1-10)")
    await state.set_state(Form.redstone)

@dp.message(Form.redstone)
async def process_redstone(message: types.Message, state: FSMContext):
    await state.update_data(redstone=message.text)
    await message.answer("Вы предпочитаете ПВП или ПВЕ?")
    await state.set_state(Form.pvp_pve)

@dp.message(Form.pvp_pve)
async def process_pvp_pve(message: types.Message, state: FSMContext):
    await state.update_data(pvp_pve=message.text)
    await message.answer("Сколько часов в день вы играете? (Просто цифра)")
    await state.set_state(Form.hours)

@dp.message(Form.hours)
async def process_hours(message: types.Message, state: FSMContext):
    await state.update_data(hours=message.text)
    await message.answer("В какое время вы не можете играть? (Например, 8:00-13:00 по МСК)")
    await state.set_state(Form.study_time)

@dp.message(Form.study_time)
async def process_study_time(message: types.Message, state: FSMContext):
    await state.update_data(study_time=message.text)
    await message.answer("Есть ли у вас тиммейты? (Напишите ники через запятую или 'нет')")
    await state.set_state(Form.teammates)

@dp.message(Form.teammates)
async def process_teammates(message: types.Message, state: FSMContext):
    await state.update_data(teammates=message.text)
    await message.answer("В какой стране вы живёте?")
    await state.set_state(Form.country)

@dp.message(Form.country)
async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Оцените ваш интернет (от 1 до 10)")
    await state.set_state(Form.internet)

@dp.message(Form.internet)
async def process_internet(message: types.Message, state: FSMContext):
    data = await state.update_data(internet=message.text)

    if "мерк" in data["server"].lower() or "меркурий" in data["server"].lower():
        # Отправляем заявку в группу
        text = (
            "📝 Новая заявка на вступление!\n\n"
            f"Никнейм: {data['nickname']}\n"
            f"Платформа: {data['platform']}\n"
            f"Сервер: {data['server']}\n"
            f"Редстоун: {data['redstone']}/10\n"
            f"ПВП/ПВЕ: {data['pvp_pve']}\n"
            f"Часы в день: {data['hours']}\n"
            f"Время без игры: {data['study_time']}\n"
            f"Тиммейты: {data['teammates']}\n"
            f"Страна: {data['country']}\n"
            f"Возраст: {data['age']}\n"
            f"Интернет: {data['internet']}/10\n\n"
            "Принимаем в команду?"
        )

        poll_message = await bot.send_poll(
            chat_id=GROUP_ID,
            question="Принимаем в команду?",
            options=["✅ Да", "❌ Нет"],
            is_anonymous=False
        )

        polls[poll_message.poll.id] = {
            "message_id": poll_message.message_id,
            "user_data": data
        }

        asyncio.create_task(check_poll_result(poll_message.poll.id))

        await message.answer("Заявка отправлена на голосование! Ждите 24 часа.")
    else:
        await message.answer("Вы не приняты из-за сервера.")
    
    await state.clear()

# Проверка голосования через 24 часа
async def check_poll_result(poll_id):
    await asyncio.sleep(86400)  # Ждём 24 часа

    if poll_id in polls:
        poll_info = polls[poll_id]
        message_id = poll_info["message_id"]
        user_data = poll_info["user_data"]

        try:
            poll_results = await bot.stop_poll(GROUP_ID, message_id)

            yes_votes = poll_results.options[0].voter_count
            no_votes = poll_results.options[1].voter_count

            if yes_votes > no_votes:
                await bot.send_message(GROUP_ID, f"✅ {user_data['nickname']} принят в команду!")
            else:
                await bot.send_message(GROUP_ID, f"❌ {user_data['nickname']} не принят в команду.")
            
            del polls[poll_id]

        except Exception as e:
            print(f"Ошибка при получении результатов: {e}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

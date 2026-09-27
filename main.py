import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import g4f

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_ai_response(user_message: str) -> str:
    # 1. Автоматический выбор рабочего провайдера через g4f
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4o,
            messages=[{"role": "user", "content": user_message}],
        )
        if response and len(str(response)) > 0:
            return str(response)
    except Exception as e:
        print(f"Ошибка основного вызова g4f: {e}")

    # 2. Резервные провайдеры на случай сбоя
    backup_providers = [
        g4f.Provider.Blackbox,
        g4f.Provider.DDG,
        g4f.Provider.Pizzagpt,
    ]

    for provider in backup_providers:
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": user_message}],
                provider=provider
            )
            if response and len(str(response)) > 0:
                return str(response)
        except Exception as e:
            print(f"Ошибка резервного провайдера {provider}: {e}")
            continue

    return "К сожалению, все нейросети сейчас перегружены. Попробуй отправить запрос еще раз!"

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я MIRUS AI. Напиши мне любой вопрос, и я отвечу!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    ai_text = await get_ai_response(message.text)
    await message.answer(ai_text)

async def main():
    print("Бот MIRUS AI успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

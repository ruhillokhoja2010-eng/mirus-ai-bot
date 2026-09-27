import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import g4f

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Список проверенных провайдеров для поочерёдной проверки
PROVIDERS_TO_TRY = [
    g4f.Provider.Blackbox,
    g4f.Provider.DDG,
    g4f.Provider.Pizzagpt,
    g4f.Provider.Jaxx,
]

async def ask_g4f_with_fallback(user_message: str) -> str:
    # 1. Сначала пробуем автовыбор лучшего провайдера
    try:
        response = await asyncio.wait_for(
            g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4o,
                messages=[{"role": "user", "content": user_message}],
            ),
            timeout=8.0
        )
        if response and len(str(response).strip()) > 0:
            return str(response)
    except Exception as e:
        print(f"Основной автовыбор не сработал: {e}")

    # 2. Если автовыбор подвёл, перебираем резервных провайдеров по очереди
    for provider in PROVIDERS_TO_TRY:
        try:
            print(f"Пробуем резервный провайдер: {provider.__name__}")
            response = await asyncio.wait_for(
                g4f.ChatCompletion.create_async(
                    model=g4f.models.gpt_35_turbo,
                    messages=[{"role": "user", "content": user_message}],
                    provider=provider
                ),
                timeout=6.0
            )
            if response and len(str(response).strip()) > 0:
                return str(response)
        except Exception as e:
            print(f"Провайдер {provider.__name__} не ответил: {e}")
            continue

    # 3. Если вообще ни один провайдер не сработал
    return "⚠️ Извини, сейчас бесплатные нейросети перегружены. Попробуй отправить запрос еще раз через минуту!"

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я MIRUS AI. Напиши мне любой вопрос, и я отвечу!")

@dp.message()
async def handle_message(message: types.Message):
    # Показываем статус "печатает..." в Telegram
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Получаем ответ с перебором провайдеров
    ai_text = await ask_g4f_with_fallback(message.text)
    
    # Всегда отправляем ответ
    await message.answer(ai_text)

async def main():
    print("Бот MIRUS AI успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

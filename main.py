import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import g4f

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я MIRUS AI. Напиши мне любой вопрос, и я отвечу!")

@dp.message()
async def handle_message(message: types.Message):
    # Сразу показываем пользователю, что бот думает
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    response_text = ""
    
    # Пытаемся получить ответ от g4f с защитой от зависания (таймаут 15 секунд)
    try:
        response = await asyncio.wait_for(
            g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": message.text}],
            ),
            timeout=15.0
        )
        if response:
            response_text = str(response)
    except asyncio.TimeoutError:
        response_text = "⚠️ Нейросеть долго не отвечает (превышено время ожидания). Попробуй написать чуть позже."
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        response_text = "⚠️ Извини, сейчас возникла временная проблема с доступом к ИИ. Попробуй еще раз!"

    # Отправляем ответ в любом случае, чтобы бот не "молчал"
    await message.answer(response_text)

async def main():
    print("Бот MIRUS AI успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

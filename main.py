import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"
GEMINI_API_KEY = "AIzaSyDbN873OpjyKpqt_JInt2OZVfn1uv5LMXI"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Прямой URL для официального API Gemini
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

async def get_ai_response(user_message: str) -> str:
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(GEMINI_URL, json=payload, headers=headers, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Извлекаем текст ответа от Gemini
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    error_data = await resp.text()
                    print(f"Ошибка API (Код {resp.status}): {error_data}")
    except Exception as e:
        print(f"Ошибка сети/запроса: {e}")

    return "⚠️ Произошла ошибка при обработке запроса. Попробуй ещё раз!"

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я MIRUS AI. Чем могу помочь?")

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

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"
GEMINI_API_KEY = "AIzaSyDbN873OpjyKpqt_JInt2OZVfn1uv5LMXI"

# Настройка Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_ai_response(user_message: str) -> str:
    try:
        response = await asyncio.to_thread(
            model.generate_content,
            user_message
        )
        if response and response.text:
            return response.text
    except Exception as e:
        print(f"Ошибка Gemini API: {e}")
        
    return "⚠️ Произошла ошибка при обработке запроса. Попробуй еще раз!"

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

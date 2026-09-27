import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"
GEMINI_API_KEY = "AIzaSyDbN873OpjyKpqt_JInt2OZVfn1uv5LMXI"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализируем официальный клиент Google Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

async def get_ai_response(user_message: str) -> str:
    try:
        # Вызываем молниеносную модель Gemini 2.5 Flash
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=user_message,
        )
        if response and response.text:
            return response.text
    except Exception as e:
        print(f"Ошибка при запросе к Gemini: {e}")
        
    return "⚠️ Произошла ошибка при обращении к нейросети. Попробуй еще раз!"

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я MIRUS AI на базе Google Gemini. Задай мне любой вопрос!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    ai_text = await get_ai_response(message.text)
    await message.answer(ai_text)

async def main():
    print("Бот MIRUS AI (Gemini) успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

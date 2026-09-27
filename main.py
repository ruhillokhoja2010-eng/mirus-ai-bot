import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import g4f

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_ai_response(user_text: str) -> str:
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4o,
            messages=[
                {
                    "role": "system",
                    "content": "Ты — MIRUS AI, умный и дружелюбный ассистент."
                },
                {"role": "user", "content": user_text}
            ]
        )
        if response:
            return str(response)
        return "Сервер нейросети временно не ответил. Попробуй еще раз!"
    except Exception as e:
        return f"Произошла ошибка: {e}"

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    welcome_text = (
        "Приветствую! Я MIRUS AI ⚡\n\n"
        "💡 **Чем я могу помочь:**\n"
        "• Отвечу на любые вопросы\n"
        "• Помогу с учебой и кодом\n"
        "• Напишу или переведу текст\n\n"
        "Просто напиши мне свой вопрос ниже!"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    ai_response = await asyncio.to_thread(get_ai_response, message.text)
    
    if len(ai_response) > 4000:
        for i in range(0, len(ai_response), 4000):
            await message.answer(ai_response[i:i+4000])
    else:
        await message.answer(ai_response)

async def main():
    print("Бот MIRUS AI успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")

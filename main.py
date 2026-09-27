import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
import g4f

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"

# Юзернейм твоего аккаунта и Telegram-канала
MY_USERNAME = "ruhillokhoja"
MY_CHANNEL = "mirus_ai"  # Укажи юзернейм своего канала без @

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =====================================================================
# 📚 БАЗА ЗНАНИЙ (ОБУЧЕНИЕ БОТА)
# Добавляй сюда новые ответы в формате: "слово": "ответ",
# =====================================================================
KNOWLEDGE_BASE = {
    "версия": "🚀 Текущая версия MIRUS AI — 2.0!",
}

def check_custom_knowledge(user_text: str) -> str | None:
    msg = user_text.strip().lower()
    for word, answer in KNOWLEDGE_BASE.items():
        if word in msg:
            return answer
    return None

def get_local_response(text: str) -> str | None:
    msg = text.strip().lower()

    # 1. Проверяем обученную базу знаний
    custom_ans = check_custom_knowledge(text)
    if custom_ans:
        return custom_ans

    # 2. Что ты умеешь / Возможности 🤖
    if any(q in msg for q in ["что ты умеешь", "что умеешь", "что ты умееш", "что умееш", "твои функции", "возможности"]):
        return (
            "🤖 **Вот что я умею:**\n\n"
            "1. 🔢 **Решать примеры и задачи:** Складываю, умножаю, делю, вычисляю скобки и решаю математические выражения (например: `125*8` или `(50+15)/5`).\n"
            "2. 💬 **Общаться и отвечать на вопросы:** Распознаю приветствия, благодарности и вежливо общаюсь с эмодзи.\n"
            "3. 🧠 **Понимать умные темы:** Помогаю отвечать на вопросы, объясняю термины и поддерживаю диалог.\n"
            "4. 📚 **Учиться новому:** Знаю ответы из своей базы знаний, а если чего-то не знаю — подскажу, как отправить отзыв.\n"
            "5. 📝 **Принимать отзывы:** Принимаю ваши предложения и замечания через команду `/feedback`.\n\n"
            "💡 *Просто напиши мне любой вопрос или математический пример!*"
        )

    # 3. Приветствия 👋
    if any(word in msg for word in ["привет", "салом", "hello", "hi", "здравствуй", "добрый день", "добрый вечер", "доброе утро", "салом алейкум"]):
        return "Привет! 👋 Я MIRUS AI. Очень рад тебя видеть! Чем могу помочь сегодня? 😊"

    # 4. Вежливость и прощания 🙏
    if any(word in msg for word in ["спасибо", "рахмат", "благодарю", "thanks", "thx"]):
        return "Всегда пожалуйста! 😉 Рад был помочь! Если будут ещё вопросы — обращайся! ✨"

    if any(word in msg for word in ["пока", "до свидания", "бай", "goodbye", "до встречи"]):
        return "До свидания! 👋 Хорошего дня и отличного настроения! ✨"

    if any(word in msg for word in ["как дела", "как ты", "как жизнь", "чихели"]):
        return "У меня всё отлично, спасибо! 🚀 Готов решать любые задачи! А как у тебя дела? 😊"

    # 5. Кто ты / Что за бот 🤖
    if any(q in msg for q in ["кто ты", "кто такой"]):
        return "Я MIRUS AI — твой виртуальный умный помощник! 🤖 Умею отвечать на вопросы, решать математику и помогать с текстом!"

    # 6. Математика 🔢
    clean_math = re.sub(r'[^0-9\+\-\*\/\(\)\.\,\s]', '', msg).strip()
    if clean_math and re.search(r'\d', clean_math) and re.search(r'[\+\-\*\/]', clean_math):
        if re.match(r'^[0-9\+\-\*\/\(\)\.\,\s]+$', msg):
            try:
                expr = clean_math.replace(',', '.')
                result = eval(expr, {"__builtins__": None}, {})
                return f"🔢 Результат: {result} ✅"
            except Exception:
                pass

    return None

# =====================================================================
# 💌 КРАСИВОЕ СООБЩЕНИЕ ДЛЯ ОТЗЫВОВ И СВЯЗИ
# =====================================================================
@dp.message(Command("feedback"))
async def feedback_cmd(message: types.Message):
    text = (
        "✨ **Оставить отзыв или предложение** ✨\n\n"
        "Огромное спасибо за ваш отзыв! 🙏\n"
        "Мы очень ценим ваше мнение и обязательно будем исправлять все ошибки, чтобы делать бота лучше и умнее с каждым днём. 🚀\n\n"
        "📬 **Написать нам напрямую:**\n"
        f"• В личные сообщения: @{MY_USERNAME}\n"
        f"• В наш Telegram-канал: @{MY_CHANNEL}\n\n"
        "Будем рады любым вашим пожеланиям и идеям! 💙"
    )
    await message.answer(text, parse_mode="Markdown")

# Вызов внешней нейросети g4f
async def get_ai_response(user_message: str) -> str:
    local_ans = get_local_response(user_message)
    if local_ans:
        return local_ans

    try:
        response = await asyncio.wait_for(
            g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": user_message}],
                provider=g4f.Provider.DDG
            ),
            timeout=10.0
        )
        if response and len(str(response).strip()) > 0:
            return f"🤖 {str(response)}"
    except Exception:
        pass

    try:
        response = await asyncio.wait_for(
            g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4o,
                messages=[{"role": "user", "content": user_message}],
                provider=g4f.Provider.Blackbox
            ),
            timeout=10.0
        )
        if response and len(str(response).strip()) > 0:
            return f"🤖 {str(response)}"
    except Exception:
        pass

    return (
        "💡 Я пока не знаю ответа на этот вопрос.\n\n"
        f"Спасибо за ваш вопрос! Вы можете написать свой отзыв или замечание в личку (@{MY_USERNAME}) или в канал (@{MY_CHANNEL}) — мы обязательно исправим ошибки и научим бота новому! 🙏✨"
    )

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! 👋 Я MIRUS AI. Задай мне вопрос или отправь /feedback, чтобы оставить отзыв! 😊✨")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    ai_text = await get_ai_response(message.text)
    await message.answer(ai_text, parse_mode="Markdown")

async def main():
    print("Бот MIRUS AI успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

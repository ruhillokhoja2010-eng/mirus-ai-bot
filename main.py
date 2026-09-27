import asyncio
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import g4f

BOT_TOKEN = "8644786361:AAEwDgQxcDUJ5i2E2M-E6ChiocPHeT3pUi8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Локальная база ответов и авто-вычисления
def get_local_response(text: str) -> str | None:
    msg = text.strip().lower()

    # 1. Приветствие
    if msg in ["привет", "салом", "hello", "hi", "здравствуй", "добрый день", "добрый вечер"]:
        return "Привет! Я MIRUS AI. Чем могу помочь?"

    # 2. Что ты умеешь / Возможности
    if any(q in msg for q in ["что ты умеешь", "что умеешь", "что ты умееш", "что умееш", "твои функции", "возможности"]):
        return (
            "🤖 **Вот что я умею:**\n\n"
            "1. **Отвечать на вопросы:** Расскажу факты, объясню сложные темы и термины.\n"
            "2. **Решать математику:** Отправляй мне любые примеры (например: `125*8`, `(50+15)/5`).\n"
            "3. **Программировать:** Помогаю писать и искать ошибки в коде на Python, HTML, CSS, JavaScript и других языках.\n"
            "4. **Работать с текстом:** Пишу посты, статьи, делаю переводы и исправления ошибок.\n"
            "5. **Точная дата и время:** Назову текущий день, число и точное время.\n\n"
            "Задай мне любой вопрос!"
        )

    # 3. Кто ты / Кто создал
    if any(q in msg for q in ["кто ты", "кто такой", "что за бот"]):
        return "Я MIRUS AI — твой виртуальный помощник. Я умею отвечать на вопросы, решать задачи, помогать с кодом и текстами!"

    if any(q in msg for q in ["кто тебя создал", "кто твой создатель", "кто твой автор", "кто тебя сделал", "кто создатель"]):
        return "Меня создал и разработал Ruhillokhoja!"

    # 4. Дата и время
    if any(q in msg for q in ["какой сегодня день", "какая дата", "число сегодня", "сегодняшнее число", "какой день"]):
        now = datetime.now()
        days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        day_name = days[now.weekday()]
        return f"Сегодня {now.strftime('%d.%m.%Y')} г., {day_name}."

    if any(q in msg for q in ["сколько время", "который час", "время сейчас", "точное время"]):
        now = datetime.now()
        return f"Текущее время: {now.strftime('%H:%M')}."

    # 5. Автоматическое решение математических примеров (например: 2+2, 100/4*2, (15+5)/2)
    clean_math = re.sub(r'[^0-9\+\-\*\/\(\)\.\,\s]', '', msg).strip()
    if clean_math and re.search(r'\d', clean_math) and re.search(r'[\+\-\*\/]', clean_math):
        if re.match(r'^[0-9\+\-\*\/\(\)\.\,\s]+$', msg):
            try:
                expr = clean_math.replace(',', '.')
                result = eval(expr, {"__builtins__": None}, {})
                return f"🔢 Результат: {result}"
            except Exception:
                pass

    return None

# Генерация ответа через внешнюю нейросеть
async def get_ai_response(user_message: str) -> str:
    # Шаг 1: Проверяем локальные ответы
    local_ans = get_local_response(user_message)
    if local_ans:
        return local_ans

    # Шаг 2: Попытка через DuckDuckGo
    try:
        response = await asyncio.wait_for(
            g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": user_message}],
                provider=g4f.Provider.DDG
            ),
            timeout=12.0
        )
        if response and len(str(response).strip()) > 0:
            return str(response)
    except Exception as e:
        print(f"Ошибка DDG: {e}")

    # Шаг 3: Попытка через Blackbox
    try:
        response = await asyncio.wait_for(
            g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_4o,
                messages=[{"role": "user", "content": user_message}],
                provider=g4f.Provider.Blackbox
            ),
            timeout=12.0
        )
        if response and len(str(response).strip()) > 0:
            return str(response)
    except Exception as e:
        print(f"Ошибка Blackbox: {e}")

    # Запасной ответ, если внешняя сеть недоступна
    return (
        "💡 Внешняя нейросеть сейчас временно перегружена.\n\n"
        "Но я могу прямо сейчас:\n"
        "• Решить математический пример (отправь например `25*8`)\n"
        "• Назвать текущую дату и время\n"
        "• Рассказать, кто меня создал и что я умею!"
    )

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я MIRUS AI. Задай мне вопрос, спроси что я умею или отправь математический пример!")

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

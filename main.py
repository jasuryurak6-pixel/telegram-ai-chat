import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from google import genai

# Kalitlaringizni shu yerga kiriting
BOT_TOKEN = "8948827233:AAGsqPrqPaATw_2wq7YhxWV8Kbssj8Nm2mw"
GEMINI_API_KEY = "GEMINI_API_KALITINGIZNI_YOZING"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
Siz foydalanuvchining shaxsiy sun'iy intellekt yordamchisisiz.
Egangiz hozirda tarmoqda emas yoki band.
Vazifangiz:
1. Kelgan xabarga muloyim, qisqa va aniq javob berish.
2. Egangizning o'rnida yordamchi sifatida yozayotganingizni bildirish.
3. Foydalanuvchi qaysi tilda yozsa, shu tilda javob qaytarish.
4. Javoblaringiz 2-3 ta ixcham jumlalardan oshmasin.
"""

@dp.business_message()
async def handle_business_message(message: types.Message):
    if not message.text:
        return
        
    # Agar xabarni o'zingiz yozgan bo'lsangiz, bot aralashmaydi
    if message.from_user.id == message.chat.id:
        return

    try:
        await bot.send_chat_action(
            chat_id=message.chat.id, 
            action="typing", 
            business_connection_id=message.business_connection_id
        )

        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "temperature": 0.7,
            }
        )

        await message.answer(
            text=response.text,
            business_connection_id=message.business_connection_id
        )

    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

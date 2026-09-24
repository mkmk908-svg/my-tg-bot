import subprocess
import sys

# Хитрый трюк: сам код устанавливает библиотеку aiogram прямо при запуске
try:
    import aiogram
except ImportError:
    print("Библиотека aiogram не найдена. Устанавливаю...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiogram==3.13.1"])
    import aiogram

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8943567222:AAEVUVR5QDY-DWhlP9erjQiJ4jjzSR28mD8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Бот готов.\nВведите команду /sud")

@dp.message(Command("sud"))
async def send_sud_photo(message: types.Message):
    photo_path = "sud_document.jpg" 
    
    # Кнопка для звонка (замени номер на свой, если нужно)
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Сделать звонок и выяснить", url="tel:+79991112233")]
    ])
    
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo, 
            caption="⚠️ **Внимание!**\nКакой-то уебок обиделся и подал в суд!",
            reply_markup=inline_kb,
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "⚠️ **Внимание!**\nКакой-то уебок обиделся и подал в суд!\n\n*(Картинка 'sud_document.jpg' не найдена в репозитории на GitHub)*",
            reply_markup=inline_kb,
            parse_mode="Markdown"
        )

@dp.message()
async def echo_message(message: types.Message):
    await message.answer(message.text)

async def main():
    print("Бот успешно запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")

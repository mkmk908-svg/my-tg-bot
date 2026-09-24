import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

# Токен успешно добавлен!
API_TOKEN = "8943567222:AAEVUVR5QDY-DWhlP9erjQiJ4jjzSR28mD8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Бот заряжен и готов.\n"
        f"Введите команду /sud, чтобы отправить уведомление."
    )

# Обработчик команды /sud
@dp.message(Command("sud"))
async def send_sud_photo(message: types.Message):
    # Картинку нужно назвать именно так и положить в папку с ботом
    photo_path = "sud_document.jpg" 
    
    # Создаем кнопку для звонка (вместо ТЕЛЕФОН вставьте реальный номер, например +79991112233)
    # Важно: префикс tel: обязателен, чтобы Telegram понял, что это звонок
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Сделать звонок и выяснить", url="tel:+79991112233")]
    ])
    
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        
        # Отправляем ОДНО сообщение: фото, ваш текст и кнопку ниже
        await message.answer_photo(
            photo=photo, 
            caption="⚠️ **Внимание!**\nКакой-то уебок обиделся и подал в суд!",
            reply_markup=inline_kb,
            parse_mode="Markdown"
        )
    else:
        # Если картинку забыли положить, бот просто отправит текст с кнопкой
        await message.answer(
            "⚠️ **Внимание!**\nКакой-то уебок обиделся и подал в суд!\n\n*(Ошибка: файл 'sud_document.jpg' не найден в папке)*",
            reply_markup=inline_kb,
            parse_mode="Markdown"
        )

# Эхо-эффект для остальных сообщений
@dp.message()
async def echo_message(message: types.Message):
    await message.answer(message.text)

async def main():
    print("Бот запущен на вашем токене...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")

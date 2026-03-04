import asyncio
import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command
from bot_instance import bot
from tasks import generate_review

# Настройка логирования
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет! Я бот-генератор отзывов.\n"
        "Просто отправь мне название товара, и я создам правдоподобный отзыв на него.\n"
        "Генерация может занять несколько секунд, нужно подождать."
    )


@dp.message()
async def handle_product(message: types.Message):
    product_name = message.text.strip()
    if not product_name:
        await message.answer("Пожалуйста, напиши название товара.")
        return

    await message.answer("⏳ Отзыв генерируется, подождите немного...")
    # Отправляем задачу в Celery
    generate_review.delay(product_name, message.from_user.id)
    logging.info(
        f"Задача поставлена для товара: {product_name}, user_id: {message.from_user.id}"
    )


async def main():
    logging.info("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")

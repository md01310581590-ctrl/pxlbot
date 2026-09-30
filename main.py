import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, ADMIN_ID
from handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "="*60)
        print("❌ ОШИБКА: Вы не указали BOT_TOKEN в файле .env!")
        print("1. Откройте файл .env в папке pxlbot_studio_bot на Рабочем столе")
        print("2. Вставьте токен, полученный от @BotFather в Telegram")
        print("="*60 + "\n")
        sys.exit(1)

    bot = DefaultBotProperties(parse_mode=ParseMode.HTML)
    aiogram_bot = Bot(token=BOT_TOKEN, default=bot)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    print("\n" + "="*60)
    print("👾 PXLBOT STUDIOS BOT ЗАПУЩЕН И ГОТОВ К РАБОТЕ!")
    print(f"Администратор (ID для заявок): {ADMIN_ID}")
    print("Нажмите Ctrl + C для остановки бота")
    print("="*60 + "\n")

    await aiogram_bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(aiogram_bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nБот остановлен пользователем.")

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database import init_db
from handlers import admin, cart, checkout, menu, payment, start


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(cart.router)
    dp.include_router(checkout.router)
    dp.include_router(payment.router)
    dp.include_router(admin.router)
    return dp


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await init_db()

    if config.bot_token == "YOUR_BOT_TOKEN":
        print("Укажите реальный BOT_TOKEN в .env и запустите: python bot.py")
        return

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = build_dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

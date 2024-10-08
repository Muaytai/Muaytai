import asyncio

from aiogram import Bot, Dispatcher
from gimini_bot.app.database.models import async_main
from config import TOKEN
from gimini_bot.app.handlers import router


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


async def on_startup(dispatcher):
    await async_main()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
